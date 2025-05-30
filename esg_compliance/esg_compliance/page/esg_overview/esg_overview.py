import frappe
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def get_metrics_trend(filters=None):
    try:
        if isinstance(filters, str):
            filters = frappe.parse_json(filters)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        # Get initiatives with proper category mapping
        initiatives = frappe.get_all('ESG Initiative',
            filters={
                'company': filters.get('company'),
                'docstatus': 0,
                'status': ['not in', ['Completed', 'Cancelled']]
            },
            fields=['name', 'related_policy', 'start_date', 'end_date']
        )

        # Generate monthly labels
        labels = []
        current = start_date
        while current <= end_date:
            labels.append(current.strftime('%b %Y'))
            current += timedelta(days=30)

        # Calculate progress for each category
        categories = {
            'Environmental': {'color': '#4ade80', 'data': []},
            'Social': {'color': '#60a5fa', 'data': []},
            'Governance': {'color': '#a78bfa', 'data': []}
        }

        # Calculate monthly progress
        for month_start in range(0, 180, 30):
            month_date = end_date - timedelta(days=month_start)
            period_start = month_date - timedelta(days=30)

            for category in categories:
                # Filter initiatives by policy type
                category_initiatives = [
                    i for i in initiatives 
                    if (i.related_policy and (
                        (category == 'Environmental' and any(term in i.related_policy.lower() for term in ['environmental', 'carbon', 'energy'])) or
                        (category == 'Social' and any(term in i.related_policy.lower() for term in ['social', 'employee', 'community'])) or
                        (category == 'Governance' and any(term in i.related_policy.lower() for term in ['governance', 'compliance', 'policy']))
                    ))
                ]

                if category_initiatives:
                    # Calculate average progress
                    progress = sum(
                        min(100, max(0, (
                            frappe.utils.date_diff(month_date, i.start_date) / 
                            max(1, frappe.utils.date_diff(i.end_date, i.start_date))
                        ) * 100))
                        for i in category_initiatives
                    ) / len(category_initiatives)
                else:
                    progress = 0

                categories[category]['data'].insert(0, round(progress, 2))

        return {
            'labels': labels,
            'datasets': [
                {
                    'label': category,
                    'data': data['data'],
                    'color': data['color']
                }
                for category, data in categories.items()
            ]
        }

    except Exception as e:
        error_msg = str(e)[:130] if len(str(e)) > 130 else str(e)
        frappe.log_error(message=f"ESG Overview: {error_msg}", title="ESG Metrics Error")
        return {
            'labels': [],
            'datasets': []
        }
