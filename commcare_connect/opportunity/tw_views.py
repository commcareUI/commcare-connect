from django.http import HttpResponse
from django.shortcuts import render

from .tw_tables import OpportunitiesListTable, VisitsTable, WorkerFlaggedTable, WorkerPaymentsTable


def home(request, org_slug=None, opp_id=None):
    # Static data for the cards
    rows = [
        {"name": "Data Points 1", "value": "45"},
        {"name": "Data Points 1", "value": "45"},
        {"name": "Data Points 2", "value": "45"},
        {"name": "Data Points 3", "value": "45"},
        {"name": "Data Points 4", "value": "45"},
        {"name": "Data Points 5", "value": "45"},
        {"name": "Data Points 6", "value": "45"},
        {"name": "Data Points 7", "value": "45"},
        {"name": "Data Points 8", "value": "45"},
    ]
    timeline = [
        {"title": "Event Title", "desc": "Additional Supporting Message with the Event", "date": "24 Feb, 2024"},
        {"title": "Event Title", "desc": "Additional Supporting Message with the Event", "date": "24 Feb, 2024"},
        {"title": "Event Title", "desc": "Additional Supporting Message with the Event", "date": "24 Feb, 2024"},
    ]
    flags = [
        {"title": "Location", "desc": "Minimum distance between deliveries.", "value": "2.5m"},
        {"title": "Form Duration", "desc": "Minimum time between deliveries.", "value": "10min"},
        {"title": "Photos", "desc": "Added media for proof"},
        {"title": "GPS location", "desc": "GPS location of the site is present"},
    ]
    return render(
        request,
        "tailwind/pages/home.html",
        {"rows": rows, "timeline": timeline, "flags": flags, "header_title": "Worker"},
    )


def about(request, org_slug=None, opp_id=None):
    return render(request, "tailwind/pages/about.html")


def worker(request, org_slug=None, opp_id=None):
    data = [
        {"name": "Flagged", "count": "45", "url": "/tables"},
        {"name": "PM Review", "count": "45", "url": "/tables"},
        {"name": "Revalidate", "count": "45", "url": "/tables"},
        {"name": "Approved", "count": "45", "url": "/tabls"},
        {"name": "Rejected", "count": "45", "url": "/tables"},
        {"name": "All", "count": "45", "url": "/tables"},
    ]

    return render(request, "tailwind/pages/worker.html", {"header_title": "Worker", "tabs": data})


def opportunities(request, org_slug=None, opp_id=None):
    data = [
        {"name": "Learn App", "count": "2", "icon": "fa-book-open-cover"},
        {"name": "Delivery App", "count": "2", "icon": "fa-clipboard-check"},
        {"name": "Payments Units", "count": "2", "icon": "fa-hand-holding-dollar"},
    ]
    totalinfo = [
        {
            "name": "Delivery Type",
            "count": "Early Childhood Development",
            "icon": "fa-file-check",
            "color": "",
        },
        {
            "name": "Start Date",
            "count": "21-Dec-2024",
            "icon": "fa-calendar-range",
            "color": "",
        },
        {
            "name": "End Date",
            "count": "21-Dec-2024",
            "icon": "fa-arrow-right",
            "color": "",
        },
        {
            "name": "Total Workers",
            "count": "248",
            "icon": "fa-users",
            "color": "brand-mango",
        },
        {
            "name": "Total Service Deliveries",
            "count": "350",
            "icon": "fa-gears",
            "color": "",
        },
        {
            "name": "Worker Budget",
            "count": "₹250,000",
            "icon": "fa-money-bill",
            "color": "",
        },
    ]
    opList = [
        {
            "opName": "Workers",
            "opLabel": "Active Yesterday",
            "opValue": "10",
            "ops": [
                {"icon": "fa-user-group", "name": "Workers", "status": "Invited", "value": "25"},
                {"icon": "fa-user-check", "name": "Workers", "status": "Yet to Accept Invitation", "value": "12"},
                {
                    "icon": "fa-clipboard-list",
                    "name": "Workers",
                    "status": "Inactive last 3 days",
                    "value": "7",
                    "type": "2",
                },
            ],
        },
        {
            "opName": "Deliveries",
            "opLabel": "Last Delivery",
            "opValue": "10 Feb, 2025 | 14:67",
            "ops": [
                {
                    "icon": "fa-clipboard-list-check",
                    "name": "Deliveries",
                    "status": "Total",
                    "value": "248",
                    "incr": "6",
                },
                {
                    "icon": "fa-clipboard-list-check",
                    "name": "Deliveries",
                    "status": "Awaiting Flag Review",
                    "value": "32",
                },
            ],
        },
        {
            "opName": "Worker Payments",
            "opLabel": "Last Payment ",
            "opValue": "10 Feb, 2025 | 14:67",
            "ops": [
                {
                    "icon": "fa-hand-holding-dollar",
                    "name": "Payments",
                    "status": "Earned",
                    "value": "₹25,000",
                    "incr": "6",
                },
                {"icon": "fa-light", "name": "Payments", "status": "Due", "value": "₹1,200"},
            ],
        },
    ]
    return render(
        request,
        "tailwind/pages/opportunities.html",
        {"data": data, "totalinfo": totalinfo, "opList": opList, "header_title": "Opportunities"},
    )


def flagged_workers(request, org_slug=None, opp_id=None):
    # Sample dynamic data (replace with your actual data source later)
    data = [
        {
            "index": 1,
            "time": "14:56",
            "entityName": "Violla Maeya",
            "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"],
        },
        {"index": 2, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {
            "index": 3,
            "time": "14:58",
            "entityName": "Jane Smith",
            "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"],
        },
        {"index": 4, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 5, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {
            "index": 11,
            "time": "14:56",
            "entityName": "Violla Maeya",
            "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"],
        },
        {"index": 12, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {
            "index": 13,
            "time": "14:58",
            "entityName": "Jane Smith",
            "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"],
        },
        {"index": 14, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 15, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {
            "index": 21,
            "time": "14:56",
            "entityName": "Violla Maeya",
            "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"],
        },
        {"index": 22, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {
            "index": 23,
            "time": "14:58",
            "entityName": "Jane Smith",
            "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"],
        },
        {"index": 24, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 25, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {
            "index": 31,
            "time": "14:56",
            "entityName": "Violla Maeya",
            "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"],
        },
        {"index": 32, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {
            "index": 33,
            "time": "14:58",
            "entityName": "Jane Smith",
            "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"],
        },
        {"index": 34, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 35, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
    ]
    table = WorkerFlaggedTable(data)
    return render(request, "tailwind/components/tables/worker_flagged_table.html", {"table": table})


def opportunity_visits(request, org_slug=None, opp_id=None):
    data = [
        {
            "index": 1,
            "user_id": "AB12CD34EF56",
            "name": "John Doe",
            "max_visit": 120,
            "used_visits": 89,
            "end_date": "2025-07-12",
        },
        {
            "index": 2,
            "user_id": "XY98GH76IJ54",
            "name": "Alice Smith",
            "max_visit": 150,
            "used_visits": 45,
            "end_date": "2025-09-30",
        },
        {
            "index": 3,
            "user_id": "MN45KL89OP12",
            "name": "Bob Johnson",
            "max_visit": 100,
            "used_visits": 72,
            "end_date": "2026-02-15",
        },
        {
            "index": 4,
            "user_id": "QR23ST56UV78",
            "name": "Emma Wilson",
            "max_visit": 180,
            "used_visits": 160,
            "end_date": "2025-11-20",
        },
        {
            "index": 5,
            "user_id": "WX67YZ12AB34",
            "name": "Michael Brown",
            "max_visit": 90,
            "used_visits": 25,
            "end_date": "2026-05-10",
        },
        {
            "index": 6,
            "user_id": "KL34MN78OP56",
            "name": "Sophia Martinez",
            "max_visit": 130,
            "used_visits": 98,
            "end_date": "2025-08-21",
        },
        {
            "index": 7,
            "user_id": "UV12WX34YZ56",
            "name": "James Anderson",
            "max_visit": 170,
            "used_visits": 140,
            "end_date": "2026-04-05",
        },
        {
            "index": 8,
            "user_id": "CD78EF12GH34",
            "name": "Olivia Taylor",
            "max_visit": 200,
            "used_visits": 180,
            "end_date": "2025-12-25",
        },
        {
            "index": 9,
            "user_id": "IJ45KL67MN89",
            "name": "William Harris",
            "max_visit": 95,
            "used_visits": 50,
            "end_date": "2025-06-18",
        },
        {
            "index": 10,
            "user_id": "OP23QR45ST67",
            "name": "Charlotte White",
            "max_visit": 160,
            "used_visits": 130,
            "end_date": "2026-07-01",
        },
        {
            "index": 11,
            "user_id": "EF12GH34IJ56",
            "name": "Benjamin Lewis",
            "max_visit": 110,
            "used_visits": 85,
            "end_date": "2025-10-11",
        },
        {
            "index": 12,
            "user_id": "ST78UV12WX34",
            "name": "Mia Scott",
            "max_visit": 140,
            "used_visits": 95,
            "end_date": "2026-03-30",
        },
        {
            "index": 13,
            "user_id": "YZ45AB67CD89",
            "name": "Elijah Hall",
            "max_visit": 180,
            "used_visits": 170,
            "end_date": "2025-09-09",
        },
        {
            "index": 14,
            "user_id": "GH23IJ45KL67",
            "name": "Amelia Young",
            "max_visit": 125,
            "used_visits": 110,
            "end_date": "2026-01-25",
        },
        {
            "index": 15,
            "user_id": "MN78OP12QR34",
            "name": "Lucas King",
            "max_visit": 190,
            "used_visits": 150,
            "end_date": "2025-11-15",
        },
        {
            "index": 16,
            "user_id": "WX45YZ67AB89",
            "name": "Harper Wright",
            "max_visit": 105,
            "used_visits": 70,
            "end_date": "2026-06-20",
        },
        {
            "index": 17,
            "user_id": "CD12EF34GH56",
            "name": "Henry Green",
            "max_visit": 175,
            "used_visits": 160,
            "end_date": "2025-12-01",
        },
        {
            "index": 18,
            "user_id": "IJ78KL12MN34",
            "name": "Evelyn Adams",
            "max_visit": 115,
            "used_visits": 90,
            "end_date": "2026-05-17",
        },
        {
            "index": 19,
            "user_id": "OP45QR67ST89",
            "name": "Alexander Nelson",
            "max_visit": 145,
            "used_visits": 120,
            "end_date": "2025-08-05",
        },
        {
            "index": 20,
            "user_id": "UV23WX45YZ67",
            "name": "Isabella Carter",
            "max_visit": 135,
            "used_visits": 100,
            "end_date": "2026-02-22",
        },
    ]

    table = VisitsTable(data)
    return render(request, "tailwind/pages/opportunity_visits.html", {"table": table})


def opportunities_list_table_view(request):
    data = [
        {
            "index": 1,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 2,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 3,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 4,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 5,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 6,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 7,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 8,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 9,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 10,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 11,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 12,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 13,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 14,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 15,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 16,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 17,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 18,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 19,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 20,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
    ]

    table = OpportunitiesListTable(data)
    return render(request, "tailwind/components/tables/opportunities_list_table-backup.html", {"table": table})


def opportunities_list(request):
    headers = {
        "opportunities": [
            {"type": "radio", "name": "All"},
            {"type": "radio", "name": "Test"},
            {"type": "radio", "name": "Live"},
            {"type": "meta", "meta": {"sort": True}},
        ],
        "status": [
            {
                "type": "radio",
                "name": "All",
            },
            {
                "type": "radio",
                "name": "Inactive",
            },
            {
                "type": "radio",
                "name": "Active",
            },
            {
                "type": "radio",
                "name": "Ended",
            },
        ],
    }

    data = [
        {
            "index": 1,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 2,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 3,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 4,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 5,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 6,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 7,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 8,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 9,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 10,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 11,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 12,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 13,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 14,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 15,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 16,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 17,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 18,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 19,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
        {
            "index": 20,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {"count": 76, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "inactiveWorkers": {"count": 44, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "pendingApprovals": {"count": 56, "list": ["View Opportunity", "View Worker", "View Invoices"]},
            "paymentsDue": {"amount": "$123", "list": ["View Opportunity", "View Worker", "View Invoices"]},
        },
    ]

    return render(
        request,
        "tailwind/pages/opportunities_list.html",
        {"headers": headers, "data": data, "header_title": "Opportunities List"},
    )


def worker_payments(request):
    return render(request, "tailwind/pages/worker_payments.html")


def worker_payments_table(request):
    data = [
        {
            "index": 1,
            "worker": {"id": "UV23WX45YZ67", "name": "Isabella Carter"},
            "indicator": "orange-600",
            "lastActive": "9hr ago",
            "accrued": "₹ 4,780",
            "totalPaid": "₹ 4,780",
            "lastPaid": "12-Aug-2025",
            "confirmed": "₹ 4,780",
        },
        {
            "index": 2,
            "worker": {"id": "OP45QR67ST89", "name": "Alexander Nelson"},
            "indicator": "green-600",
            "lastActive": "9hr ago",
            "accrued": "₹ 4,780",
            "totalPaid": "₹ 4,780",
            "lastPaid": "12-Aug-2025",
            "confirmed": "₹ 4,780",
        },
        {
            "index": 3,
            "worker": {"id": "IJ78KL12MN34", "name": "Evelyn Adams"},
            "indicator": "red-600",
            "lastActive": "95 hr ago",
            "accrued": "₹ 4,780",
            "totalPaid": "₹ 4,780",
            "lastPaid": "12-Aug-2025",
            "confirmed": "₹ 4,780",
        },
        {
            "index": 4,
            "worker": {"id": "AB23CD45EF67", "name": "Liam Parker"},
            "lastActive": "3hr ago",
            "accrued": "₹ 5,000",
            "totalPaid": "₹ 5,000",
            "lastPaid": "13-Aug-2025",
            "confirmed": "₹ 5,000",
        },
        {
            "index": 5,
            "worker": {"id": "GH56IJ78KL90", "name": "Olivia Robinson"},
            "indicator": "yellow-600",
            "lastActive": "12hr ago",
            "accrued": "₹ 6,200",
            "totalPaid": "₹ 6,200",
            "lastPaid": "14-Aug-2025",
            "confirmed": "₹ 6,200",
        },
        {
            "index": 6,
            "worker": {"id": "MN23OP45QR67", "name": "Noah Martinez"},
            "indicator": "gray-600",
            "lastActive": "24hr ago",
            "accrued": "₹ 3,500",
            "totalPaid": "₹ 3,500",
            "lastPaid": "12-Aug-2025",
            "confirmed": "₹ 3,500",
        },
        {
            "index": 7,
            "worker": {"id": "ST89UV12WX34", "name": "Emma Wilson"},
            "lastActive": "48hr ago",
            "accrued": "₹ 4,000",
            "totalPaid": "₹ 4,000",
            "lastPaid": "15-Aug-2025",
            "confirmed": "₹ 4,000",
        },
        {
            "index": 8,
            "worker": {"id": "YZ12AB34CD56", "name": "James Smith"},
            "indicator": "red-600",
            "lastActive": "72hr ago",
            "accrued": "₹ 5,500",
            "totalPaid": "₹ 5,500",
            "lastPaid": "16-Aug-2025",
            "confirmed": "₹ 5,500",
        },
        {
            "index": 9,
            "worker": {"id": "EF78GH90IJ12", "name": "Sophia Johnson"},
            "indicator": "orange-600",
            "lastActive": "24hr ago",
            "accrued": "₹ 4,300",
            "totalPaid": "₹ 4,300",
            "lastPaid": "17-Aug-2025",
            "confirmed": "₹ 4,300",
        },
        {
            "index": 10,
            "worker": {"id": "KL34MN56OP78", "name": "Mason Taylor"},
            "indicator": "green-600",
            "lastActive": "96hr ago",
            "accrued": "₹ 5,000",
            "totalPaid": "₹ 5,000",
            "lastPaid": "18-Aug-2025",
            "confirmed": "₹ 5,000",
        },
        {
            "index": 11,
            "worker": {"id": "QR12ST34UV56", "name": "Amelia Brown"},
            "indicator": "yellow-600",
            "lastActive": "30hr ago",
            "accrued": "₹ 6,000",
            "totalPaid": "₹ 6,000",
            "lastPaid": "19-Aug-2025",
            "confirmed": "₹ 6,000",
        },
        {
            "index": 12,
            "worker": {"id": "WX78YZ90AB12", "name": "Lucas Harris"},
            "lastActive": "15hr ago",
            "accrued": "₹ 4,100",
            "totalPaid": "₹ 4,100",
            "lastPaid": "20-Aug-2025",
            "confirmed": "₹ 4,100",
        },
        {
            "index": 13,
            "worker": {"id": "CD56EF78GH90", "name": "Charlotte Garcia"},
            "lastActive": "8hr ago",
            "accrued": "₹ 5,500",
            "totalPaid": "₹ 5,500",
            "lastPaid": "21-Aug-2025",
            "confirmed": "₹ 5,500",
        },
        {
            "index": 14,
            "worker": {"id": "IJ34KL56MN78", "name": "Henry Lee"},
            "indicator": "red-600",
            "lastActive": "72hr ago",
            "accrued": "₹ 3,800",
            "totalPaid": "₹ 3,800",
            "lastPaid": "22-Aug-2025",
            "confirmed": "₹ 3,800",
        },
        {
            "index": 15,
            "worker": {"id": "OP90QR12ST34", "name": "Grace Scott"},
            "indicator": "gray-600",
            "lastActive": "60hr ago",
            "accrued": "₹ 6,200",
            "totalPaid": "₹ 6,200",
            "lastPaid": "23-Aug-2025",
            "confirmed": "₹ 6,200",
        },
        {
            "index": 16,
            "worker": {"id": "UV12WX34YZ56", "name": "David Martinez"},
            "indicator": "orange-600",
            "lastActive": "5hr ago",
            "accrued": "₹ 4,800",
            "totalPaid": "₹ 4,800",
            "lastPaid": "24-Aug-2025",
            "confirmed": "₹ 4,800",
        },
        {
            "index": 17,
            "worker": {"id": "AB34CD56EF78", "name": "Lily Robinson"},
            "indicator": "yellow-600",
            "lastActive": "28hr ago",
            "accrued": "₹ 5,200",
            "totalPaid": "₹ 5,200",
            "lastPaid": "25-Aug-2025",
            "confirmed": "₹ 5,200",
        },
        {
            "index": 18,
            "worker": {"id": "GH90IJ12KL34", "name": "Benjamin King"},
            "lastActive": "11hr ago",
            "accrued": "₹ 5,500",
            "totalPaid": "₹ 5,500",
            "lastPaid": "26-Aug-2025",
            "confirmed": "₹ 5,500",
        },
        {
            "index": 19,
            "worker": {"id": "MN23OP45QR67", "name": "Jack Wright"},
            "indicator": "green-600",
            "lastActive": "7hr ago",
            "accrued": "₹ 4,300",
            "totalPaid": "₹ 4,300",
            "lastPaid": "27-Aug-2025",
            "confirmed": "₹ 4,300",
        },
        {
            "index": 20,
            "worker": {"id": "ST89UV12WX34", "name": "Emily Johnson"},
            "lastActive": "55hr ago",
            "accrued": "₹ 6,000",
            "totalPaid": "₹ 6,000",
            "lastPaid": "28-Aug-2025",
            "confirmed": "₹ 6,000",
        },
    ]

    table = WorkerPaymentsTable(data)
    return render(request, "tailwind/components/tables/worker_payments_table.html", {"table": table})


def get_worker_last_payment(request):
    payments = [
        {"date": "12-Jul-2024", "amount": "₹4,780"},
        {"date": "15-Aug-2024", "amount": "₹5,230"},
        {"date": "20-Sep-2024", "amount": "₹4,950"},
        {"date": "25-Oct-2024", "amount": "₹6,100"},
    ]

    html = ""
    for payment in payments:
        html += f"""
            <div class="flex justify-between py-1 items-center">
                <p class="text-xs text-brand-deep-purple">{payment['date']}</p>
                <p class="text-sm text-slate-900">{payment['amount']}</p>
            </div>
        """

    return HttpResponse(html)


# views.py

'''
from django.shortcuts import render
from django.http import HttpResponse
from .tables import OpportunitiesListTable, WorkerFlaggedTable, WorkerPaymentsTable
from .tables import WorkerFlaggedTable,VisitsTable


def home(request):
    # Static data for the cards
    rows = [{'name': 'Data Points 1','value' : '45'}, {'name': 'Data Points 1','value' : '45'},{'name': 'Data Points 2','value' : '45'},{'name': 'Data Points 3','value' : '45'},{'name': 'Data Points 4','value' : '45'},{'name': 'Data Points 5','value' : '45'},{'name': 'Data Points 6','value' : '45'},{'name': 'Data Points 7','value' : '45'},{'name': 'Data Points 8','value' : '45'},]
    timeline = [{'title': 'Event Title','desc':'Additional Supporting Message with the Event','date' : '24 Feb, 2024'}, {'title': 'Event Title','desc':'Additional Supporting Message with the Event','date' : '24 Feb, 2024'},{'title': 'Event Title','desc':'Additional Supporting Message with the Event','date' : '24 Feb, 2024'}]
    flags = [{'title': 'Location','desc':'Minimum distance between deliveries.','value' : '2.5m'}, {'title': 'Form Duration','desc':'Minimum time between deliveries.','value' : '10min'},{'title': 'Photos','desc':'Added media for proof'},{'title': 'GPS location','desc':'GPS location of the site is present'}]
    return render(request, 'ccc_app/pages/home.html',  {'rows': rows,'timeline':timeline,'flags':flags,'header_title': 'Worker'})


def about(request):
    return render(request, 'ccc_app/pages/about.html')

def dashboard(request):
    data = {
        'programs': [
            {
                'name': 'Program Name',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor arcu ac ligula luctus venenatis. Aliquam rhonc msan. Aliquam rhonc msan.Aliquam rhonc msan.',
                'date': '06 May, 2024',
                'organization_name': 'Program Manager Organization Name',
                'status': 'invited',
                'delievery_type': 'Name of the delivery type',
                'start_date': '12-Jul-2024',
                'end_date': '12-Jul-2024',
            },
            {
                'name': 'Program Name',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor arcu ac ligula luctus venenatis. Aliquam rhonc msan. Aliquam rhonc msan.Aliquam rhonc msan.',
                'date': '06 May, 2024',
                'organization_name': 'Program Manager Organization Name',
                'status': 'applied',
                'delievery_type': 'Name of the delivery type',
                'start_date': '12-Jul-2024',
                'end_date': '12-Jul-2024',
            }
            ,
            {
                'name': 'Program Name',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor arcu ac ligula luctus venenatis. Aliquam rhonc msan. Aliquam rhonc msan.Aliquam rhonc msan.',
                'date': '06 May, 2024',
                'organization_name': 'Program Manager Organization Name',
                'status': 'accepted',
                'delievery_type': 'Name of the delivery type',
                'start_date': '12-Jul-2024',
                'end_date': '12-Jul-2024',
                'opportunities': [
                    {
                        'name': 'Oppurtunity Name',
                        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor arcu ac ligula luctus venenatis. Aliquam rhonc msan. Aliquam rhonc msan.Aliquam rhonc msan.',
                        'date': '06 May, 2024',
                        'organization_name': 'Program Manager Organization Name',
                        'status': 'invited',
                        'delievery_type': 'Name of the delivery type',
                        'start_date': '12-Jul-2024',
                        'end_date': '12-Jul-2024',
                        'labels':{
                            'name': 'Delieveries',
                            'count': '100/150',
                            'tags': [
                                {
                                    'name': 'Approved',
                                    'count': '70',
                                    'color': 'green-600'
                                },
                                {
                                    'name': 'Flagged',
                                    'count': '15',
                                    'color': 'sunset'
                                },
                                {
                                    'name': 'Rejected',
                                    'count': '70',
                                    'color': 'blue-light'
                                }
                            ]
                        }
                    },
                    {
                        'name': 'Oppurtunity Name',
                        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus tempor arcu ac ligula luctus venenatis. Aliquam rhonc msan. Aliquam rhonc msan.Aliquam rhonc msan.',
                        'date': '06 May, 2024',
                        'organization_name': 'Program Manager Organization Name',
                        'status': 'invited',
                        'delievery_type': 'Name of the delivery type',
                        'start_date': '12-Jul-2024',
                        'end_date': '12-Jul-2024',
                        'labels':{
                            'name': 'Workers',
                            'count': '256',
                            'tags': [
                                {
                                    'name': 'Learning',
                                    'count': '23',
                                    'color': 'mango'
                                },
                                {
                                    'name': 'Claimed Job',
                                    'count': '120',
                                    'color': 'indigo'
                                },
                                {
                                    'name': 'Assessed',
                                    'count': '124',
                                    'color': 'green-600'
                                }
                            ]
                        }
                    }
                ]
            }
        ],
        'recent_activities': [
            {
                'name': 'Visit Pending Review',
                'icon': 'clock-rotate-left',
                'rows': [
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                ]
            },
            {
                'name': 'Visit Pending Review',
                'icon': 'hand-holding-dollar',
                'rows': [
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                ]
            },
            {
                'name': 'Inactive Workers',
                'icon': 'user-slash',
                'rows': [
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                    {
                        'title': 'Opportunity Name',
                        'subtitle': 'Network Manager Organization Name',
                        'count': '11',
                    },
                ]
            },

        ]
    }

    return render(request, 'ccc_app/pages/dashboard.html', {'data': data, 'header_title': 'Dashboard'})

def worker(request):
    data =  [
                {
                    'name': 'Flagged',
                    'count': '45',
                    'url': '/tables'
                },
                {
                    'name': 'PM Review',
                    'count': '45',
                    'url': '/tables'
                    },
                {
                    'name': 'Revalidate',
                    'count': '45',
                    'url': '/tables'
                    },
                {
                    'name': 'Approved',
                    'count': '45',
                    'url': '/tabls'
                    },
                {
                    'name': 'Rejected',
                    'count': '45',
                    'url': '/tables'
                    },
                {
                    'name': 'All',
                    'count': '45',
                    'url': '/tables'
                    },
            ]


    return render(request, 'ccc_app/pages/worker.html',  {'header_title': 'Worker', 'tabs': data})

def opportunities(request):
    data = [
            {
                'name' : 'Learn App',
                'count' : '2',
                'icon' : 'fa-book-open-cover'
            },
             {
                'name' : 'Delivery App',
                'count' : '2',
                'icon' : 'fa-clipboard-check'
            },
             {
                'name' : 'Payments Units',
                'count' : '2',
                'icon' : 'fa-hand-holding-dollar'
            },
        ]
    totalinfo = [
            {
                'name' : 'Delivery Type',
                'count' : 'Early Childhood Development',
                'icon' : 'fa-file-check',
                'color': '',
            },
            {
                'name' : 'Start Date',
                'count' : '21-Dec-2024',
                'icon' : 'fa-calendar-range',
                'color' : '',
            },
            {
                'name' : 'End Date',
                'count' : '21-Dec-2024',
                'icon' : 'fa-arrow-right',
                'color' : '',
            },
             {
                'name' : 'Total Workers',
                'count' : '248',
                'icon' : 'fa-users',
                'color' : 'brand-mango',
            },
            {
                'name' : 'Total Service Deliveries',
                'count' : '350',
                'icon' : 'fa-gears',
                'color' : '',
            },
            {
                'name' : 'Worker Budget',
                'count' : '₹250,000',
                'icon' : 'fa-money-bill',
                'color' : '',
            },
        ]
    opList = [
           {
            'opName': 'Workers',
            'opLabel': 'Active Yesterday',
            'opValue': '10',
            'ops': [
                {
                    'icon': 'fa-user-group',
                    'name': 'Workers',
                    'status': 'Invited',
                    'value': '25'
                },
                {
                    'icon': 'fa-user-check',
                    'name': 'Workers',
                    'status': 'Yet to Accept Invitation',
                    'value': '12'
                },
                {
                    'icon': 'fa-clipboard-list',
                    'name': 'Workers',
                    'status': 'Inactive last 3 days',
                    'value': '7',
                    'type': '2'
                }
            ]
           },
           {
            'opName': 'Deliveries',
            'opLabel': 'Last Delivery',
            'opValue': '10 Feb, 2025 | 14:67',
            'ops': [
                {
                    'icon': 'fa-clipboard-list-check',
                    'name': 'Deliveries',
                    'status': 'Total',
                    'value': '248',
                    'incr': '6'
                },
                {
                    'icon': 'fa-clipboard-list-check',
                    'name': 'Deliveries',
                    'status': 'Awaiting Flag Review',
                    'value': '32',

                }

            ]
           },
           {
            'opName': 'Worker Payments',
            'opLabel': 'Last Payment ',
            'opValue': '10 Feb, 2025 | 14:67',
            'ops': [
                {
                    'icon': 'fa-hand-holding-dollar',
                    'name': 'Payments',
                    'status': 'Earned',
                    'value': '₹25,000',
                    'incr': '6'
                },
                {
                    'icon': 'fa-light',
                    'name': 'Payments',
                    'status': 'Due',
                    'value': '₹1,200'
                }
            ]
           }
    ]
    return render(request, 'ccc_app/pages/opportunities.html',  {'data':data,'totalinfo':totalinfo,'opList':opList,'header_title': 'Opportunities'})

def table_view(request):
    # Sample dynamic data (replace with your actual data source later)
    data = [
        {"index": 1, "time": "14:56", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"]},
        {"index": 2, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {"index": 3, "time": "14:58", "entityName": "Jane Smith", "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"]},
        {"index": 4, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 5, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {"index": 11, "time": "14:56", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"]},
        {"index": 12, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {"index": 13, "time": "14:58", "entityName": "Jane Smith", "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"]},
        {"index": 14, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 15, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {"index": 21, "time": "14:56", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"]},
        {"index": 22, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {"index": 23, "time": "14:58", "entityName": "Jane Smith", "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"]},
        {"index": 24, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 25, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},
        {"index": 31, "time": "14:56", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos", "Flag Name 1", "Flag Name 2", "Flag Name 3"]},
        {"index": 32, "time": "14:57", "entityName": "John Doe", "flags": ["Location", "Photos"]},
        {"index": 33, "time": "14:58", "entityName": "Jane Smith", "flags": ["Form Duration", "Flag Name 1", "Flag Name 2"]},
        {"index": 34, "time": "14:59", "entityName": "Alex Brown", "flags": []},
        {"index": 35, "time": "15:00", "entityName": "Violla Maeya", "flags": ["Location", "Form Duration", "Photos"]},

    ]
    table = WorkerFlaggedTable(data)
    return render(request, "ccc_app/components/tables/worker_flagged_table.html", {"table": table})


def opportunities_list_table_view(request):
    data = [
        {
            "index": 1,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 2,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 3,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 4,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 5,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 6,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 7,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 8,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 9,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 10,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 11,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 12,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 13,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 14,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 15,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 16,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 17,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 18,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 19,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 20,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        }
        ]


    table = OpportunitiesListTable(data)
    return render(request, "ccc_app/components/tables/opportunities_list_table-backup.html", {"table": table})

def opportunities_list(request):
    headers = {
        'opportunities': [
        {'type': 'radio', 'name': 'All'},
        {'type': 'radio', 'name': 'Test'},
        {'type': 'radio', 'name': 'Live'},
        {'type': 'meta', 'meta': {'sort': True}}
    ],
        'status' :[
        {
            'type': 'radio',
            'name': 'All',
        },
        {
            'type': 'radio',
            'name': 'Inactive',
        },
        {
            'type': 'radio',
            'name': 'Active',
        },
        {
            'type': 'radio',
            'name': 'Ended',
        }
    ]

    }

    data = [
        {
            "index": 1,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 2,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 3,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 4,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 5,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 6,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 7,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 8,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 9,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 10,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 11,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 12,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 13,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 14,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 15,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 16,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 17,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 18,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "inactive",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 19,
            "opportunity": "Opportunity Name",
            "entityType": "live",
            "entityStatus": "ended",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        },
        {
            "index": 20,
            "opportunity": "Opportunity Name",
            "entityType": "test",
            "entityStatus": "active",
            "program": "Program Name",
            "startDate": "12 Jul, 2025",
            "endDate": "12 Aug, 2025",
            "pendingInvites": {'count': 76, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "inactiveWorkers": {'count': 44, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "pendingApprovals": {'count': 56, 'list': ['View Opportunity', 'View Worker', 'View Invoices']},
            "paymentsDue": {'amount': '$123', 'list': ['View Opportunity', 'View Worker', 'View Invoices']}
        }
        ]





    return render(request, "ccc_app/pages/opportunities_list.html", {'headers':headers , 'data':data, 'header_title': 'Opportunities List'} )

def opportunity_visits(request):
    data = [
    {'index': 1, 'user_id': 'AB12CD34EF56', 'name': 'John Doe', 'max_visit': 120, 'used_visits': 89, 'end_date': '2025-07-12'},
    {'index': 2, 'user_id': 'XY98GH76IJ54', 'name': 'Alice Smith', 'max_visit': 150, 'used_visits': 45, 'end_date': '2025-09-30'},
    {'index': 3, 'user_id': 'MN45KL89OP12', 'name': 'Bob Johnson', 'max_visit': 100, 'used_visits': 72, 'end_date': '2026-02-15'},
    {'index': 4, 'user_id': 'QR23ST56UV78', 'name': 'Emma Wilson', 'max_visit': 180, 'used_visits': 160, 'end_date': '2025-11-20'},
    {'index': 5, 'user_id': 'WX67YZ12AB34', 'name': 'Michael Brown', 'max_visit': 90, 'used_visits': 25, 'end_date': '2026-05-10'},
    {'index': 6, 'user_id': 'KL34MN78OP56', 'name': 'Sophia Martinez', 'max_visit': 130, 'used_visits': 98, 'end_date': '2025-08-21'},
    {'index': 7, 'user_id': 'UV12WX34YZ56', 'name': 'James Anderson', 'max_visit': 170, 'used_visits': 140, 'end_date': '2026-04-05'},
    {'index': 8, 'user_id': 'CD78EF12GH34', 'name': 'Olivia Taylor', 'max_visit': 200, 'used_visits': 180, 'end_date': '2025-12-25'},
    {'index': 9, 'user_id': 'IJ45KL67MN89', 'name': 'William Harris', 'max_visit': 95, 'used_visits': 50, 'end_date': '2025-06-18'},
    {'index': 10, 'user_id': 'OP23QR45ST67', 'name': 'Charlotte White', 'max_visit': 160, 'used_visits': 130, 'end_date': '2026-07-01'},
    {'index': 11, 'user_id': 'EF12GH34IJ56', 'name': 'Benjamin Lewis', 'max_visit': 110, 'used_visits': 85, 'end_date': '2025-10-11'},
    {'index': 12, 'user_id': 'ST78UV12WX34', 'name': 'Mia Scott', 'max_visit': 140, 'used_visits': 95, 'end_date': '2026-03-30'},
    {'index': 13, 'user_id': 'YZ45AB67CD89', 'name': 'Elijah Hall', 'max_visit': 180, 'used_visits': 170, 'end_date': '2025-09-09'},
    {'index': 14, 'user_id': 'GH23IJ45KL67', 'name': 'Amelia Young', 'max_visit': 125, 'used_visits': 110, 'end_date': '2026-01-25'},
    {'index': 15, 'user_id': 'MN78OP12QR34', 'name': 'Lucas King', 'max_visit': 190, 'used_visits': 150, 'end_date': '2025-11-15'},
    {'index': 16, 'user_id': 'WX45YZ67AB89', 'name': 'Harper Wright', 'max_visit': 105, 'used_visits': 70, 'end_date': '2026-06-20'},
    {'index': 17, 'user_id': 'CD12EF34GH56', 'name': 'Henry Green', 'max_visit': 175, 'used_visits': 160, 'end_date': '2025-12-01'},
    {'index': 18, 'user_id': 'IJ78KL12MN34', 'name': 'Evelyn Adams', 'max_visit': 115, 'used_visits': 90, 'end_date': '2026-05-17'},
    {'index': 19, 'user_id': 'OP45QR67ST89', 'name': 'Alexander Nelson', 'max_visit': 145, 'used_visits': 120, 'end_date': '2025-08-05'},
    {'index': 20, 'user_id': 'UV23WX45YZ67', 'name': 'Isabella Carter', 'max_visit': 135, 'used_visits': 100, 'end_date': '2026-02-22'}
    ]

    table = VisitsTable(data)
    return render(request, 'ccc_app/pages/opportunity_visits.html', {'table': table})

def worker_payments(request):
    return render(request, 'ccc_app/pages/worker_payments.html')

def worker_payments_table(request):

    data = [
    {'index': 1, 'worker': {'id': 'UV23WX45YZ67', 'name': 'Isabella Carter'}, 'indicator': 'orange-600', 'lastActive': '9hr ago', 'accrued': '₹ 4,780', 'totalPaid': '₹ 4,780', 'lastPaid': '12-Aug-2025', 'confirmed': '₹ 4,780'},
    {'index': 2, 'worker': {'id': 'OP45QR67ST89', 'name': 'Alexander Nelson'}, 'indicator': 'green-600', 'lastActive': '9hr ago', 'accrued': '₹ 4,780', 'totalPaid': '₹ 4,780', 'lastPaid': '12-Aug-2025', 'confirmed': '₹ 4,780'},
    {'index': 3, 'worker': {'id': 'IJ78KL12MN34', 'name': 'Evelyn Adams'}, 'indicator': 'red-600', 'lastActive': '95 hr ago', 'accrued': '₹ 4,780', 'totalPaid': '₹ 4,780', 'lastPaid': '12-Aug-2025', 'confirmed': '₹ 4,780'},
    {'index': 4, 'worker': {'id': 'AB23CD45EF67', 'name': 'Liam Parker'},  'lastActive': '3hr ago', 'accrued': '₹ 5,000', 'totalPaid': '₹ 5,000', 'lastPaid': '13-Aug-2025', 'confirmed': '₹ 5,000'},
    {'index': 5, 'worker': {'id': 'GH56IJ78KL90', 'name': 'Olivia Robinson'}, 'indicator': 'yellow-600', 'lastActive': '12hr ago', 'accrued': '₹ 6,200', 'totalPaid': '₹ 6,200', 'lastPaid': '14-Aug-2025', 'confirmed': '₹ 6,200'},
    {'index': 6, 'worker': {'id': 'MN23OP45QR67', 'name': 'Noah Martinez'}, 'indicator': 'gray-600', 'lastActive': '24hr ago', 'accrued': '₹ 3,500', 'totalPaid': '₹ 3,500', 'lastPaid': '12-Aug-2025', 'confirmed': '₹ 3,500'},
    {'index': 7, 'worker': {'id': 'ST89UV12WX34', 'name': 'Emma Wilson'},  'lastActive': '48hr ago', 'accrued': '₹ 4,000', 'totalPaid': '₹ 4,000', 'lastPaid': '15-Aug-2025', 'confirmed': '₹ 4,000'},
    {'index': 8, 'worker': {'id': 'YZ12AB34CD56', 'name': 'James Smith'}, 'indicator': 'red-600', 'lastActive': '72hr ago', 'accrued': '₹ 5,500', 'totalPaid': '₹ 5,500', 'lastPaid': '16-Aug-2025', 'confirmed': '₹ 5,500'},
    {'index': 9, 'worker': {'id': 'EF78GH90IJ12', 'name': 'Sophia Johnson'}, 'indicator': 'orange-600', 'lastActive': '24hr ago', 'accrued': '₹ 4,300', 'totalPaid': '₹ 4,300', 'lastPaid': '17-Aug-2025', 'confirmed': '₹ 4,300'},
    {'index': 10, 'worker': {'id': 'KL34MN56OP78', 'name': 'Mason Taylor'}, 'indicator': 'green-600', 'lastActive': '96hr ago', 'accrued': '₹ 5,000', 'totalPaid': '₹ 5,000', 'lastPaid': '18-Aug-2025', 'confirmed': '₹ 5,000'},
    {'index': 11, 'worker': {'id': 'QR12ST34UV56', 'name': 'Amelia Brown'}, 'indicator': 'yellow-600', 'lastActive': '30hr ago', 'accrued': '₹ 6,000', 'totalPaid': '₹ 6,000', 'lastPaid': '19-Aug-2025', 'confirmed': '₹ 6,000'},
    {'index': 12, 'worker': {'id': 'WX78YZ90AB12', 'name': 'Lucas Harris'},  'lastActive': '15hr ago', 'accrued': '₹ 4,100', 'totalPaid': '₹ 4,100', 'lastPaid': '20-Aug-2025', 'confirmed': '₹ 4,100'},
    {'index': 13, 'worker': {'id': 'CD56EF78GH90', 'name': 'Charlotte Garcia'},  'lastActive': '8hr ago', 'accrued': '₹ 5,500', 'totalPaid': '₹ 5,500', 'lastPaid': '21-Aug-2025', 'confirmed': '₹ 5,500'},
    {'index': 14, 'worker': {'id': 'IJ34KL56MN78', 'name': 'Henry Lee'}, 'indicator': 'red-600', 'lastActive': '72hr ago', 'accrued': '₹ 3,800', 'totalPaid': '₹ 3,800', 'lastPaid': '22-Aug-2025', 'confirmed': '₹ 3,800'},
    {'index': 15, 'worker': {'id': 'OP90QR12ST34', 'name': 'Grace Scott'}, 'indicator': 'gray-600', 'lastActive': '60hr ago', 'accrued': '₹ 6,200', 'totalPaid': '₹ 6,200', 'lastPaid': '23-Aug-2025', 'confirmed': '₹ 6,200'},
    {'index': 16, 'worker': {'id': 'UV12WX34YZ56', 'name': 'David Martinez'}, 'indicator': 'orange-600', 'lastActive': '5hr ago', 'accrued': '₹ 4,800', 'totalPaid': '₹ 4,800', 'lastPaid': '24-Aug-2025', 'confirmed': '₹ 4,800'},
    {'index': 17, 'worker': {'id': 'AB34CD56EF78', 'name': 'Lily Robinson'}, 'indicator': 'yellow-600', 'lastActive': '28hr ago', 'accrued': '₹ 5,200', 'totalPaid': '₹ 5,200', 'lastPaid': '25-Aug-2025', 'confirmed': '₹ 5,200'},
    {'index': 18, 'worker': {'id': 'GH90IJ12KL34', 'name': 'Benjamin King'},  'lastActive': '11hr ago', 'accrued': '₹ 5,500', 'totalPaid': '₹ 5,500', 'lastPaid': '26-Aug-2025', 'confirmed': '₹ 5,500'},
    {'index': 19, 'worker': {'id': 'MN23OP45QR67', 'name': 'Jack Wright'}, 'indicator': 'green-600', 'lastActive': '7hr ago', 'accrued': '₹ 4,300', 'totalPaid': '₹ 4,300', 'lastPaid': '27-Aug-2025', 'confirmed': '₹ 4,300'},
    {'index': 20, 'worker': {'id': 'ST89UV12WX34', 'name': 'Emily Johnson'},  'lastActive': '55hr ago', 'accrued': '₹ 6,000', 'totalPaid': '₹ 6,000', 'lastPaid': '28-Aug-2025', 'confirmed': '₹ 6,000'},
]

    table = WorkerPaymentsTable(data)
    return render(request, 'ccc_app/components/tables/worker_payments_table.html', {'table': table})

def get_worker_last_payment(request):
    payments = [

        {"date": "12-Jul-2024", "amount": "₹4,780"},
        {"date": "15-Aug-2024", "amount": "₹5,230"},
        {"date": "20-Sep-2024", "amount": "₹4,950"},
        {"date": "25-Oct-2024", "amount": "₹6,100"}
    ]

    html = ""
    for payment in payments:
        html += f"""
            <div class="flex justify-between py-1 items-center">
                <p class="text-xs text-brand-deep-purple">{payment['date']}</p>
                <p class="text-sm text-slate-900">{payment['amount']}</p>
            </div>
        """

    return HttpResponse(html)

'''
