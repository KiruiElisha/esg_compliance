# Copyright (c) 2025, K. Ronoh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate, add_months, get_first_day, get_last_day
from datetime import datetime, timedelta
import json

def execute(filters=None):
	"""
	Execute ESG Analysis Report
	
	Returns comprehensive analysis of ESG metrics including:
	- Performance tracking
	- Variance analysis
	- Target comparison
	- Trend analysis
	- Verification status
	"""
	if not filters:
		filters = {}
	
	# Validate required filters
	validate_filters(filters)
	
	# Get columns based on filters
	columns = get_columns(filters)
	
	# Get data
	data = get_data(filters)
	
	# Process data for grouping and calculations
	if filters.get("group_by"):
		data = process_grouped_data(data, filters)
	
	# Add summary row if needed
	if data and filters.get("show_summary"):
		summary_row = get_summary_row(data, filters)
		data.append(summary_row)
	
	return columns, data

def validate_filters(filters):
	"""Validate required filters and set defaults"""
	if not filters.get("from_date"):
		filters["from_date"] = add_months(getdate(), -12)
	
	if not filters.get("to_date"):
		filters["to_date"] = getdate()
	
	if getdate(filters.get("from_date")) > getdate(filters.get("to_date")):
		frappe.throw(_("From Date cannot be greater than To Date"))

def get_columns(filters):
	"""Define report columns based on filters"""
	columns = [
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
			"width": 120
		},
		{
			"fieldname": "metric",
			"label": _("ESG Metric"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "source_doctype",
			"label": _("Source Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "source_document",
			"label": _("Source Document"),
			"fieldtype": "Dynamic Link",
			"options": "source_doctype",
			"width": 120
		},
		{
			"fieldname": "entry_date",
			"label": _("Entry Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "reporting_period",
			"label": _("Period"),
			"fieldtype": "Data",
			"width": 90
		},
		{
			"fieldname": "measured_value",
			"label": _("Measured Value"),
			"fieldtype": "Float",
			"width": 110,
			"precision": 2
		},
		{
			"fieldname": "unit",
			"label": _("Unit"),
			"fieldtype": "Data",
			"width": 80
		}
	]
	
	# Add target comparison columns if requested
	if filters.get("include_targets"):
		columns.extend([
			{
				"fieldname": "target_value",
				"label": _("Target Value"),
				"fieldtype": "Float",
				"width": 110,
				"precision": 2
			},
			{
				"fieldname": "variance",
				"label": _("Variance"),
				"fieldtype": "Float",
				"width": 100,
				"precision": 2
			},
			{
				"fieldname": "variance_percent",
				"label": _("Variance %"),
				"fieldtype": "Percent",
				"width": 90,
				"precision": 1
			}
		])
	
	# Add performance and verification columns
	columns.extend([
		{
			"fieldname": "performance",
			"label": _("Performance"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "data_source",
			"label": _("Data Source"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "verification_status",
			"label": _("Verification"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "verified_by",
			"label": _("Verified By"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120
		}
	])
	
	# Add grouping column if grouped
	if filters.get("group_by") and filters.get("group_by") != "None":
		group_column = {
			"fieldname": "group_field",
			"label": _(f"Group ({filters.get('group_by')})"),
			"fieldtype": "Data",
			"width": 150
		}
		columns.insert(0, group_column)
	
	return columns

def get_data(filters):
    """Fetch ESG metric entry data based on filters"""
    conditions = get_conditions(filters)
    
    query = f"""
        SELECT 
            eme.name,
            eme.metric,
            eme.company,
            eme.entry_date,
            eme.reporting_period,
            eme.period_from,
            eme.period_to,
            eme.value,
            eme.measured_value,
            eme.target_value,
            eme.unit,
            eme.variance,
            eme.variance_ as variance_percent,
            eme.performance,
            eme.data_source,
            eme.verification_status,
            eme.verified_by,
            eme.verification_date,
            eme.remarks,
            eme.source_doctype,
            eme.source_document,
            eme.party_type,
            eme.party,
            em.metric_name,
            em.category,
            em.unit as metric_unit,
            em.description as metric_description,
            c.company_name
        FROM 
            `tabESG Metric Entry` eme
        LEFT JOIN 
            `tabESG Metric` em ON eme.metric = em.name
        LEFT JOIN 
            `tabCompany` c ON eme.company = c.name
        WHERE 
            {conditions}
        ORDER BY 
            eme.entry_date DESC, eme.metric, eme.company
    """
    
    data = frappe.db.sql(query, filters, as_dict=True)
    return data

def get_conditions(filters):
	"""Build WHERE conditions based on filters"""
	conditions = []
	
	if filters.get("company"):
		conditions.append("eme.company = %(company)s")
	
	if filters.get("metric"):
		conditions.append("eme.metric = %(metric)s")
		
	if filters.get("source_doctype"):
		conditions.append("eme.source_doctype = %(source_doctype)s")
		
	if filters.get("party_type"):
		conditions.append("eme.party_type = %(party_type)s")
		
	if filters.get("party"):
		conditions.append("eme.party = %(party)s")
	
	if filters.get("from_date"):
		conditions.append("eme.entry_date >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("eme.entry_date <= %(to_date)s")
	
	if filters.get("performance"):
		conditions.append("eme.performance = %(performance)s")
	
	if filters.get("verification_status"):
		conditions.append("eme.verification_status = %(verification_status)s")
	
	if filters.get("data_source"):
		conditions.append("eme.data_source = %(data_source)s")
	
	return " AND ".join(conditions) if conditions else "1=1"

def process_row(row, filters):
	"""Process individual row data"""
	processed = {}
	
	# Essential fields
	processed["metric"] = row.get("metric")
	processed["company"] = row.get("company")
	processed["entry_date"] = formatdate(row.get("entry_date"))
	processed["measured_value"] = flt(row.get("measured_value"))
	processed["target_value"] = flt(row.get("target_value"))
	processed["unit"] = row.get("unit") or "kg"
	processed["performance"] = row.get("performance")
	processed["verification_status"] = row.get("verification_status")
	
	# Party information - ensure these are included
	processed["party_type"] = row.get("party_type")
	processed["party"] = row.get("party")
	
	# Source document details
	processed["source_doctype"] = row.get("source_doctype")
	processed["source_document"] = row.get("source_document")
	
	# Calculate variance
	if processed["measured_value"] and processed["target_value"]:
		processed["variance"] = processed["measured_value"] - processed["target_value"]
		if processed["target_value"]:
			processed["variance_percent"] = (processed["variance"] / processed["target_value"]) * 100
	
	# Add grouping field if needed
	if filters.get("group_by"):
		processed["group_field"] = get_group_field_value(row, filters.get("group_by"))
	
	return processed

def get_group_field_value(row, group_by):
    """Get the value for grouping field"""
    if group_by == "Metric":
        return row.get("metric") or "Not Specified"
    elif group_by == "Company":
        return row.get("company") or "Not Specified"
    elif group_by == "Source Document":
        source_type = row.get("source_doctype", "")
        source_doc = row.get("source_document", "")
        if source_type and source_doc:
            return f"{source_type}: {source_doc}"
        return "Not Specified"
    elif group_by == "Party Type":
        party_type = row.get("party_type", "")
        party = row.get("party", "")
        if party_type and party:
            return f"{party_type}: {party}"
        return "Not Specified"
    elif group_by == "Month":
        if row.get("entry_date"):
            return formatdate(row.get("entry_date"), "MMM yyyy")
        return "Not Specified"
    elif group_by == "Quarter":
        if row.get("entry_date"):
            date = getdate(row.get("entry_date"))
            quarter = ((date.month - 1) // 3) + 1
            return f"Q{quarter} {date.year}"
        return "Not Specified"
    elif group_by == "Year":
        if row.get("entry_date"):
            return str(getdate(row.get("entry_date")).year)
        return "Not Specified"
    elif group_by == "Performance":
        return row.get("performance") or "Not Specified"
    
    return row.get(group_by) or "Not Specified"

def process_grouped_data(data, filters):
    """Process data for grouping and add subtotals"""
    if not filters.get("group_by") or not data:
        return data
    
    grouped_data = {}
    
    # Group data
    for row in data:
        group_key = get_group_field_value(row, filters.get("group_by"))
        if group_key not in grouped_data:
            grouped_data[group_key] = []
        grouped_data[group_key].append(row)
    
    # Sort group keys for better presentation
    sorted_keys = sorted(grouped_data.keys())
    if "Not Specified" in sorted_keys:
        sorted_keys.remove("Not Specified")
        sorted_keys.append("Not Specified")
    
    # Flatten with group headers and subtotals
    processed_data = []
    for group_key in sorted_keys:
        group_rows = grouped_data[group_key]
        
        # Add group header
        header_row = {
            "group_field": f"<b>{group_key}</b>",
            "metric": "",
            "party_type": "",
            "party": "",
            "measured_value": "",
            "target_value": "",
            "variance": "",
            "variance_percent": "",
            "performance": "",
            "verification_status": "",
            "is_group": 1
        }
        processed_data.append(header_row)
        
        # Add group data
        total_measured = 0
        total_target = 0
        count = 0
        
        for row in group_rows:
            row["group_field"] = "    " + (row.get("group_field") or "")  # Indent entries
            processed_data.append(row)
            if row.get("measured_value"):
                total_measured += flt(row.get("measured_value"))
            if row.get("target_value"):
                total_target += flt(row.get("target_value"))
            count += 1
        
        # Add subtotal row
        if count > 1:  # Only add subtotal if there's more than one entry
            subtotal_row = {
                "group_field": f"<i>Subtotal ({count} entries)</i>",
                "metric": "",
                "party_type": "",
                "party": "",
                "measured_value": total_measured,
                "target_value": total_target,
                "variance": total_measured - total_target if total_target else "",
                "variance_percent": ((total_measured - total_target) / total_target * 100) if total_target else "",
                "performance": "",
                "verification_status": "",
                "is_subtotal": 1
            }
            processed_data.append(subtotal_row)
            
            # Add separator
            processed_data.append({})
    
    return processed_data

def get_summary_row(data, filters):
	"""Generate summary row with totals"""
	if not data:
		return {}
	
	total_entries = len([d for d in data if d.get("name")])
	total_measured = sum(flt(d.get("measured_value", 0)) for d in data if d.get("measured_value"))
	total_target = sum(flt(d.get("target_value", 0)) for d in data if d.get("target_value"))
	
	# Count performance status
	green_count = len([d for d in data if d.get("performance") == "Green"])
	yellow_count = len([d for d in data if d.get("performance") == "Yellow"])
	red_count = len([d for d in data if d.get("performance") == "Red"])
	
	# Count verification status
	verified_count = len([d for d in data if d.get("verification_status") == "Verified"])
	pending_count = len([d for d in data if d.get("verification_status") == "Pending"])
	
	summary = {
		"metric": f"<b>SUMMARY ({total_entries} entries)</b>",
		"company": "",
		"measured_value": total_measured,
		"target_value": total_target,
		"variance": total_measured - total_target if total_target else 0,
		"variance_percent": ((total_measured - total_target) / total_target * 100) if total_target else 0,
		"performance": f"G:{green_count} Y:{yellow_count} R:{red_count}",
		"verification_status": f"V:{verified_count} P:{pending_count}",
		"remarks": "Summary row with aggregated totals"
	}
	
	return summary

@frappe.whitelist()
def get_chart_data(filters=None):
	"""Get data for charts and dashboard"""
	if isinstance(filters, str):
		filters = json.loads(filters)
	
	# Get basic data
	data = get_data(filters or {})
	
	# Performance distribution
	performance_data = {}
	for row in data:
		perf = row.get("performance", "Not Set")
		performance_data[perf] = performance_data.get(perf, 0) + 1
	
	# Monthly trend
	monthly_data = {}
	for row in data:
		if row.get("entry_date"):
			month_key = formatdate(row.get("entry_date"), "MMM yyyy")
			if month_key not in monthly_data:
				monthly_data[month_key] = {"count": 0, "total_value": 0}
			monthly_data[month_key]["count"] += 1
			monthly_data[month_key]["total_value"] += flt(row.get("measured_value", 0))
	
	return {
		"performance_distribution": performance_data,
		"monthly_trends": monthly_data,
		"total_entries": len(data),
		"verification_stats": {
			"verified": len([d for d in data if d.get("verification_status") == "Verified"]),
			"pending": len([d for d in data if d.get("verification_status") == "Pending"]),
			"rejected": len([d for d in data if d.get("verification_status") == "Rejected"])
		}
	}