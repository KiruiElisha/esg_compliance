# Copyright (c) 2025, K. Ronoh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, formatdate, flt

def execute(filters=None):
    """Main report execution"""
    if not filters:
        filters = frappe._dict({})
    
    validate_filters(filters)
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    summary = get_report_summary(data)
    
    report_config = {
        "print_format": "ESG Log Format",
        "no_breadcrumbs": 1,
        "add_total_row": 0,
        "initial_depth": 0,
        "skip_total_row": 1
    }
    
    return columns, data, "ESG Activity Log", chart, summary, report_config

def validate_filters(filters):
    """Ensure required filters are present"""
    if not filters.get("company"):
        frappe.throw(_("Please select a Company"))
    if not filters.get("from_date"):
        filters.from_date = frappe.datetime.add_months(frappe.datetime.get_today(), -1)
    if not filters.get("to_date"):
        filters.to_date = frappe.datetime.get_today()

def get_columns():
    return [
        {
            "fieldname": "entry_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 95
        },
        {
            "fieldname": "activity_type",
            "label": _("Activity Type"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "source_type",
            "label": _("Source Type"),
            "fieldtype": "Link",
            "options": "DocType",
            "width": 130
        },
        {
            "fieldname": "source_name",
            "label": _("Source Document"),
            "fieldtype": "Dynamic Link",
            "options": "source_type",
            "width": 130
        },
        {
            "fieldname": "party_type",
            "label": _("Party Type"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "party",
            "label": _("Party"),
            "fieldtype": "Dynamic Link",
            "options": "party_type",
            "width": 150
        },
        {
            "fieldname": "impact_value",
            "label": _("Carbon Impact"),
            "fieldtype": "Float",
            "width": 120,
            "precision": 2
        },
        {
            "fieldname": "performance",
            "label": _("Performance"),
            "fieldtype": "Data",
            "width": 100
        },
        {
            "fieldname": "verification",
            "label": _("Verification"),
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_conditions(filters):
    conditions = ["1=1"]
    
    if filters.get("company"):
        conditions.append("company = %(company)s")
    
    if filters.get("from_date"):
        conditions.append("entry_date >= %(from_date)s")
    
    if filters.get("to_date"):
        conditions.append("entry_date <= %(to_date)s")
        
    if filters.get("source_type"):
        conditions.append("source_doctype = %(source_type)s")
        
    if filters.get("activity_type"):
        conditions.append("metric = %(activity_type)s")
        
    if filters.get("performance"):
        conditions.append("performance = %(performance)s")
    
    return " AND ".join(conditions)

def get_chart_data(data):
    metrics = {}
    performance = {"Green": 0, "Red": 0}
    
    # Process metrics
    for d in data:
        metric_type = d.get("activity_type", "Other").replace("Initiative: ", "")
        impact = flt(d.get("impact_value", 0))
        perf = d.get("performance", "")
        
        if metric_type not in metrics:
            metrics[metric_type] = 0
        metrics[metric_type] += impact
        
        if perf in performance:
            performance[perf] += 1
    
    chart = {
        "data": {
            "labels": list(metrics.keys()),
            "datasets": [
                {
                    "name": "Carbon Impact (kg CO₂e)",
                    "values": [flt(v, 2) for v in metrics.values()]
                }
            ]
        },
        "type": "bar",
        "colors": ["#28a745"],
        "barOptions": {
            "spaceRatio": 0.2
        }
    }
    
    # Add performance donut chart
    if performance["Green"] + performance["Red"] > 0:
        chart["performance_chart"] = {
            "data": {
                "labels": ["Green Performance", "Red Performance"],
                "datasets": [{
                    "values": [performance["Green"], performance["Red"]]
                }]
            },
            "type": "donut",
            "colors": ["#28a745", "#dc3545"]
        }
    
    return chart

def get_report_summary(data):
    total_impact = sum(flt(d.get("impact_value", 0)) for d in data)
    total_entries = len(data)
    green_count = len([d for d in data if d.get("performance") == "Green"])
    red_count = len([d for d in data if d.get("performance") == "Red"])
    verified_count = len([d for d in data if d.get("verification") == "Verified"])
    
    return [
        {
            "value": flt(total_impact, 2),
            "label": "Total Carbon Impact (kg CO₂e)",
            "datatype": "Float",
            "indicator": "blue"
        },
        {
            "value": total_entries,
            "label": "Total Entries",
            "datatype": "Int",
            "indicator": "gray"
        },
        {
            "value": green_count,
            "label": "Green Performance",
            "datatype": "Int",
            "indicator": "green"
        },
        {
            "value": red_count,
            "label": "Red Performance",
            "datatype": "Int",
            "indicator": "red"
        },
        {
            "value": verified_count,
            "label": "Verified Entries",
            "datatype": "Int",
            "indicator": "blue"
        },
        {
            "value": f"{(green_count/total_entries*100) if total_entries else 0:.1f}%",
            "label": "Performance Score",
            "datatype": "Percentage",
            "indicator": "green" if green_count > red_count else "red"
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    # Get ESG Metric Entries
    metric_entries = get_metric_entries(conditions, filters)
    
    # Get Initiative Entries if enabled
    initiative_entries = []
    if filters.get("include_initiatives"):
        initiative_entries = get_initiative_entries(filters)
    
    # Combine and sort all activities
    data = metric_entries + initiative_entries
    data.sort(key=lambda x: x.get('entry_date'), reverse=True)
    
    return data

def get_metric_entries(conditions, filters):
    query = """
        SELECT 
            entry_date,
            metric as activity_type,
            source_doctype as source_type,
            source_document as source_name,
            party_type,
            party,
            CAST(measured_value AS DECIMAL(18,2)) as impact_value,
            performance,
            verification_status as verification,
            'ESG Metric' as entry_type,
            CAST(value AS DECIMAL(18,2)) as value,
            CAST(target_value AS DECIMAL(18,2)) as target,
            verification_status,
            data_source,
            company
        FROM `tabESG Metric Entry`
        WHERE {conditions}
    """.format(conditions=conditions)
    
    data = frappe.db.sql(query, filters, as_dict=1)
    
    processed_data = []
    for row in data:
        processed = {
            "entry_date": formatdate(row.entry_date),
            "activity_type": row.activity_type.replace("Carbon Impact", "").strip() if row.activity_type else "",
            "source_type": row.source_type,
            "source_name": row.source_name,
            "party_type": row.party_type,
            "party": row.party,
            "impact_value": flt(row.impact_value, 2),
            "performance": row.performance,
            "verification": row.verification_status,
            "company": row.company,
            "entry_type": "ESG Metric"
        }
        processed_data.append(processed)
    
    return processed_data

def get_initiative_entries(filters):
    conditions = []
    if filters.get("company"):
        conditions.append("company = %(company)s")
    if filters.get("from_date"):
        conditions.append("creation >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("creation <= %(to_date)s")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = """
        SELECT 
            creation as entry_date,
            initiative_name,
            CONCAT('Initiative: ', initiative_name) as activity_type,
            'ESG Initiative' as source_type,
            name as source_name,
            'Employee' as party_type,
            responsible_person as party,
            CAST(budget AS DECIMAL(18,2)) as impact_value,
            status,
            priority,
            CAST(progress_ AS DECIMAL(18,2)) as progress,
            related_policy,
            company
        FROM `tabESG Initiative`
        WHERE {where_clause}
    """.format(where_clause=where_clause)
    
    data = frappe.db.sql(query, filters, as_dict=1)
    
    processed_data = []
    for row in data:
        processed = {
            "entry_date": formatdate(row.entry_date),
            "activity_type": f"Initiative: {row.initiative_name}",
            "source_type": "ESG Initiative",
            "source_name": row.source_name,
            "party_type": "Employee",
            "party": row.party,
            "impact_value": flt(row.impact_value, 2),
            "performance": get_initiative_performance(row),
            "verification": "Verified" if row.status == "Completed" else "In Progress",
            "status": row.status,
            "company": row.company,
            "entry_type": "Initiative"
        }
        processed_data.append(processed)
    
    return processed_data

def get_initiative_performance(initiative):
    """Determine initiative performance based on progress and status"""
    if initiative.status == "Completed":
        return "Green"
    elif initiative.status == "Ongoing":
        if initiative.progress >= 50:
            return "Green"
        else:
            return "Red"
    elif initiative.priority == "High" and initiative.status == "Pending":
        return "Red"
    return "Red"
