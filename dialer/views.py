from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.timezone import now
from calendar import month_name
from collections import defaultdict
from datetime import timedelta, date
from customer.models import ScamComplaint, User


def get_complaint_percent_by_category():
    total = ScamComplaint.objects.count()
    if total == 0:
        return {}

    data = (
        ScamComplaint.objects
        .values('category__name')
        .annotate(count=Count('id'))
    )

    return {
        entry['category__name']: round((entry['count'] / total) * 100, 2)
        for entry in data
    }


def get_monthly_complaints_data():
    today = now().date().replace(day=1)
    monthly_total = {}
    monthly_by_category = defaultdict(lambda: [0] * 6)

    months = []
    for i in range(5, -1, -1):  # last 6 months
        month_date = today - timedelta(days=30 * i)
        month_label = month_name[month_date.month]
        months.append(month_label)

        complaints = (
            ScamComplaint.objects
            .filter(created_at__year=month_date.year, created_at__month=month_date.month)
            .values('category__name')
            .annotate(count=Count('id'))
        )

        total = sum(entry['count'] for entry in complaints)
        monthly_total[month_label] = total

        for entry in complaints:
            monthly_by_category[entry['category__name']][5 - i] = entry['count']

    return monthly_total, monthly_by_category, months


@login_required(login_url='login_admin')
def dashboard(request):
    total_users = User.objects.count()
    total_complaints = ScamComplaint.objects.count()
    resolved_count = ScamComplaint.objects.filter(is_resolved=True).count()
    pending_count = ScamComplaint.objects.filter(status='pending').count()
    in_review_count = ScamComplaint.objects.filter(status='in_review').count()
    marked_safe_count = ScamComplaint.objects.filter(status='mark_as_safe').count()
    marked_scam_count = ScamComplaint.objects.filter(status='mark_as_scam').count()

    category_percent = get_complaint_percent_by_category()
    monthly_total_data, monthly_by_category_data, months = get_monthly_complaints_data()

    context = {
        'total_users': total_users,
        'total_complaints': total_complaints,
        'resolved_count': resolved_count,
        'pending_count': pending_count,
        'in_review_count': in_review_count,
        'marked_safe_count': marked_safe_count,
        'marked_scam_count': marked_scam_count,

        'category_percent': category_percent,
        'months': months,
        'complaint_counts': list(monthly_total_data.values()),
        'monthly_complaint_data': dict(monthly_by_category_data),
    }

    return render(request, 'adminDashboard.html', context)


