import codecs
import itertools
import mimetypes
import textwrap
from dataclasses import dataclass

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from tablib import Dataset

from commcare_connect.opportunity.models import (
    Opportunity,
    OpportunityAccess,
    Payment,
    UserVisit,
    VisitValidationStatus,
)
from commcare_connect.opportunity.tasks import send_payment_notification
from commcare_connect.utils.itertools import batched

VISIT_ID_COL = "visit id"
STATUS_COL = "status"
USERNAME_COL = "username"
AMOUNT_COL = "payment amount"
REASON_COL = "rejected reason"
REQUIRED_COLS = [VISIT_ID_COL, STATUS_COL]


class ImportException(Exception):
    def __init__(self, message, rows=None):
        self.message = message
        self.rows = rows


@dataclass
class VisitImportStatus:
    seen_visits: set[str]
    missing_visits: set[str]

    def __len__(self):
        return len(self.seen_visits)

    def get_missing_message(self):
        joined = ", ".join(self.missing_visits)
        missing = textwrap.wrap(joined, width=115, break_long_words=False, break_on_hyphens=False)
        return f"<br>{len(self.missing_visits)} visits were not found:<br>{'<br>'.join(missing)}"


@dataclass
class PaymentImportStatus:
    seen_users: set[str]
    missing_users: set[str]

    def __len__(self):
        return len(self.seen_users)

    def get_missing_message(self):
        joined = ", ".join(self.missing_visits)
        missing = textwrap.wrap(joined, width=115, break_long_words=False, break_on_hyphens=False)
        return f"<br>{len(self.missing_users)} usernames were not found:<br>{'<br>'.join(missing)}"


def bulk_update_visit_status(opportunity: Opportunity, file: UploadedFile) -> VisitImportStatus:
    file_format = None
    if file.content_type:
        file_format = mimetypes.guess_extension(file.content_type)
        if file_format:
            file_format = file_format[1:]
    if not file_format:
        file_format = file.name.split(".")[-1].lower()
    if file_format not in ("csv", "xlsx"):
        raise ImportException(f"Invalid file format. Only 'CSV' and 'XLSX' are supported. Got {file_format}")
    imported_data = get_imported_dataset(file, file_format)
    return _bulk_update_visit_status(opportunity, imported_data)


def _bulk_update_visit_status(opportunity: Opportunity, dataset: Dataset):
    status_by_visit_id, reasons_by_visit_id = get_status_by_visit_id(dataset)
    visit_ids = list(status_by_visit_id)
    missing_visits = set()
    seen_visits = set()
    with transaction.atomic():
        for visit_batch in batched(visit_ids, 100):
            to_update = []
            visits = UserVisit.objects.filter(xform_id__in=visit_batch, opportunity=opportunity)
            for visit in visits:
                seen_visits.add(visit.xform_id)
                status = status_by_visit_id[visit.xform_id]
                if visit.status != status:
                    visit.status = status
                    reason = reasons_by_visit_id.get(visit.xform_id)
                    if visit.status == VisitValidationStatus.rejected and reason:
                        visit.reason = reason
                    to_update.append(visit)

            UserVisit.objects.bulk_update(to_update, fields=["status"])
            missing_visits |= set(visit_batch) - seen_visits
            update_payment_accrued(opportunity, users={visit.user_id for visit in visits})

    return VisitImportStatus(seen_visits, missing_visits)


def update_payment_accrued(opportunity: Opportunity, users):
    payment_units = opportunity.paymentunit_set.all()
    for user in users:
        user_visits = UserVisit.objects.filter(
            opportunity=opportunity, user=user, status=VisitValidationStatus.approved
        ).order_by("entity_id")
        access = OpportunityAccess.objects.get(user=user, opportunity=opportunity)
        payment_accrued = 0
        for payment_unit in payment_units:
            payment_unit_deliver_units = {deliver_unit.id for deliver_unit in payment_unit.deliver_units.all()}
            for entity_id, visits in itertools.groupby(user_visits, key=lambda x: x.entity_id):
                deliver_units = {v.deliver_unit.id for v in visits}
                if payment_unit_deliver_units.issubset(deliver_units):
                    payment_accrued += payment_unit.amount
        access.payment_accrued = payment_accrued
        access.save()


def get_status_by_visit_id(dataset) -> dict[int, VisitValidationStatus]:
    headers = [header.lower() for header in dataset.headers or []]
    if not headers:
        raise ImportException("The uploaded file did not contain any headers")

    visit_col_index = _get_header_index(headers, VISIT_ID_COL)
    status_col_index = _get_header_index(headers, STATUS_COL)
    reason_col_index = _get_header_index(headers, REASON_COL)
    status_by_visit_id = {}
    reason_by_visit_id = {}
    invalid_rows = []
    for row in dataset:
        row = list(row)
        visit_id = str(row[visit_col_index])
        status_raw = row[status_col_index].lower().replace(" ", "_")
        try:
            status_by_visit_id[visit_id] = VisitValidationStatus[status_raw]
        except KeyError:
            invalid_rows.append((row, f"status must be one of {VisitValidationStatus.values}"))
        if status_raw == VisitValidationStatus.rejected:
            reason_by_visit_id[visit_id] = str(row[reason_col_index])

    if invalid_rows:
        raise ImportException(f"{len(invalid_rows)} have errors", invalid_rows)
    return status_by_visit_id, reason_by_visit_id


def get_imported_dataset(file, file_format):
    if file_format == "csv":
        file = codecs.iterdecode(file, "utf-8")
    imported_data = Dataset().load(file, format=file_format)
    return imported_data


def _get_header_index(headers: list[str], col_name: str) -> int:
    try:
        return headers.index(col_name)
    except ValueError:
        raise ImportException(f"Missing required column(s): '{col_name}'")


def bulk_update_payment_status(opportunity: Opportunity, file: UploadedFile) -> PaymentImportStatus:
    file_format = None
    if file.content_type:
        file_format = mimetypes.guess_extension(file.content_type)
        if file_format:
            file_format = file_format[1:]
    if not file_format:
        file_format = file.name.split(".")[-1].lower()
    if file_format not in ("csv", "xlsx"):
        raise ImportException(f"Invalid file format. Only 'CSV' and 'XLSX' are supported. Got {file_format}")
    imported_data = get_imported_dataset(file, file_format)
    return _bulk_update_payments(opportunity, imported_data)


def _bulk_update_payments(opportunity: Opportunity, imported_data: Dataset) -> PaymentImportStatus:
    headers = [header.lower() for header in imported_data.headers or []]
    if not headers:
        raise ImportException("The uploaded file did not contain any headers")

    username_col_index = _get_header_index(headers, USERNAME_COL)
    amount_col_index = _get_header_index(headers, AMOUNT_COL)
    invalid_rows = []
    payments = {}
    for row in imported_data:
        row = list(row)
        username = str(row[username_col_index])
        amount_raw = row[amount_col_index]
        if amount_raw:
            if not username:
                invalid_rows.append((row, "username required"))
            try:
                amount = int(amount_raw)
            except ValueError:
                invalid_rows.append((row, "amount must be an integer"))
            payments[username] = amount

    if invalid_rows:
        raise ImportException(f"{len(invalid_rows)} have errors", invalid_rows)

    seen_users = set()
    payment_ids = []
    with transaction.atomic():
        usernames = list(payments)
        users = OpportunityAccess.objects.filter(user__username__in=usernames, opportunity=opportunity).select_related(
            "user"
        )
        for access in users:
            username = access.user.username
            amount = payments[username]
            payment = Payment.objects.create(opportunity_access=access, amount=amount)
            seen_users.add(username)
            payment_ids.append(payment.pk)
    missing_users = set(usernames) - seen_users
    send_payment_notification.delay(opportunity.id, payment_ids)
    return PaymentImportStatus(seen_users, missing_users)
