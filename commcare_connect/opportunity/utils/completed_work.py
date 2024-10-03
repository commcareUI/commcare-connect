from commcare_connect.opportunity.models import (
    CompletedWork,
    CompletedWorkStatus,
    Payment,
    VisitReviewStatus,
    VisitValidationStatus,
)


def update_status(completed_works, opportunity_access, compute_payment=True):
    """
    Updates the status of completed works and optionally calculates & update total payment_accrued.
    """
    payment_accrued = 0
    for completed_work in completed_works:
        if completed_work.completed_count < 1:
            continue

        if opportunity_access.opportunity.auto_approve_payments:
            visits = completed_work.uservisit_set.values_list("status", "reason", "review_status")
            if any(status == VisitValidationStatus.rejected for status, *_ in visits):
                completed_work.status = CompletedWorkStatus.rejected
                completed_work.reason = "\n".join(reason for _, reason, _ in visits if reason)
            elif all(status == VisitValidationStatus.approved for status, *_ in visits):
                completed_work.status = CompletedWorkStatus.approved

            if (
                opportunity_access.opportunity.managed
                and not all(review_status == VisitReviewStatus.agree for *_, review_status in visits)
                and completed_work.status == CompletedWorkStatus.approved
            ):
                completed_work.status = CompletedWorkStatus.pending

            completed_work.save()

        if compute_payment:
            approved_count = completed_work.approved_count
            if approved_count > 0 and completed_work.status == CompletedWorkStatus.approved:
                payment_accrued += approved_count * completed_work.payment_unit.amount

    if compute_payment:
        opportunity_access.payment_accrued = payment_accrued
        opportunity_access.save()


def update_work_payment_date(payment: Payment):
    completed_works = CompletedWork.objects.filter(opportunity_access=payment.opportunity_access)
    paid = payment.amount
    works_to_update = []

    for current_work in completed_works:
        if paid > current_work.payment_accrued:
            works_to_update.append(current_work.id)

    if works_to_update:
        CompletedWork.objects.filter(id__in=works_to_update).update(payment_date=payment.date_paid)
