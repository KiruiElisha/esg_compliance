# Complete ESG Compliance Module - Integrated with ERPNext Core

import frappe
from frappe.utils import today, now, add_months, add_days

# Create the custom module if it doesn't exist
if not frappe.db.exists('Module Def', 'ESG Compliance'):
    module_doc = frappe.get_doc({
        'doctype': 'Module Def',
        'module_name': 'ESG Compliance',
        'app_name': 'erpnext'
    })
    module_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("✓ Created ESG Compliance module")

# Enhanced DocType definitions with deep ERPNext integration
esg_doctypes = [
    {
        "doctype": "DocType",
        "name": "ESG Policy",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "ESG-POL-.YYYY.-.#####",
        "title_field": "policy_name",
        "fields": [
            {"fieldname": "policy_name", "label": "Policy Name", "fieldtype": "Data", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "description", "label": "Description", "fieldtype": "Text Editor", "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "effective_date", "label": "Effective Date", "fieldtype": "Date", "reqd": 1, "idx": 5},
            {"fieldname": "expiry_date", "label": "Expiry Date", "fieldtype": "Date", "idx": 6},
            {"fieldname": "policy_owner", "label": "Policy Owner", "fieldtype": "Link", "options": "Employee", "reqd": 1, "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Departments & Approval", "idx": 8},
            {"fieldname": "applicable_departments", "label": "Applicable Departments", "fieldtype": "Table", "options": "ESG Policy Department", "idx": 9},
            {"fieldname": "column_break_2", "fieldtype": "Column Break", "idx": 10},
            {"fieldname": "approved_by", "label": "Approved By", "fieldtype": "Link", "options": "Employee", "idx": 11},
            {"fieldname": "approval_date", "label": "Approval Date", "fieldtype": "Date", "idx": 12},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Documents", "idx": 13},
            {"fieldname": "document", "label": "Policy Document", "fieldtype": "Attach", "idx": 14},
            {"fieldname": "additional_documents", "label": "Additional Documents", "fieldtype": "Table", "options": "ESG Document", "idx": 15},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Review & Compliance", "idx": 16},
            {"fieldname": "review_frequency", "label": "Review Frequency", "fieldtype": "Select", "options": "Monthly\nQuarterly\nHalf Yearly\nAnnually", "default": "Annually", "idx": 17},
            {"fieldname": "next_review_date", "label": "Next Review Date", "fieldtype": "Date", "idx": 18},
            {"fieldname": "compliance_checklist", "label": "Compliance Checklist", "fieldtype": "Table", "options": "ESG Compliance Checklist", "idx": 19}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "idx": 2},
            {"role": "HR Manager", "read": 1, "write": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Policy Department",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "department", "label": "Department", "fieldtype": "Link", "options": "Department", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "mandatory", "label": "Mandatory", "fieldtype": "Check", "in_list_view": 1, "idx": 2},
            {"fieldname": "training_required", "label": "Training Required", "fieldtype": "Check", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Document",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "document_name", "label": "Document Name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "document_type", "label": "Type", "fieldtype": "Select", "options": "Certificate\nReport\nGuideline\nEvidence\nOther", "in_list_view": 1, "idx": 2},
            {"fieldname": "attachment", "label": "Attachment", "fieldtype": "Attach", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Compliance Checklist",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "requirement", "label": "Requirement", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Pending\nCompliant\nNon-Compliant\nPartially Compliant", "default": "Pending", "in_list_view": 1, "idx": 2},
            {"fieldname": "responsible", "label": "Responsible", "fieldtype": "Link", "options": "Employee", "in_list_view": 1, "idx": 3},
            {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "in_list_view": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Initiative",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "ESG-INI-.YYYY.-.#####",
        "title_field": "initiative_name",
        "fields": [
            {"fieldname": "initiative_name", "label": "Initiative Name", "fieldtype": "Data", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "related_policy", "label": "Related Policy", "fieldtype": "Link", "options": "ESG Policy", "reqd": 1, "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "esg_category", "label": "ESG Category", "fieldtype": "Select", "options": "Environmental\nSocial\nGovernance", "reqd": 1, "idx": 5},
            {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "Low\nMedium\nHigh\nCritical", "default": "Medium", "idx": 6},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Planned\nOngoing\nCompleted\nCancelled\nOn Hold", "default": "Planned", "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Timeline & Resources", "idx": 8},
            {"fieldname": "start_date", "label": "Start Date", "fieldtype": "Date", "reqd": 1, "idx": 9},
            {"fieldname": "end_date", "label": "End Date", "fieldtype": "Date", "reqd": 1, "idx": 10},
            {"fieldname": "project", "label": "Linked Project", "fieldtype": "Link", "options": "Project", "idx": 11},
            {"fieldname": "column_break_2", "fieldtype": "Column Break", "idx": 12},
            {"fieldname": "budget", "label": "Budget", "fieldtype": "Currency", "options": "Company:company:default_currency", "idx": 13},
            {"fieldname": "actual_cost", "label": "Actual Cost", "fieldtype": "Currency", "options": "Company:company:default_currency", "read_only": 1, "idx": 14},
            {"fieldname": "cost_center", "label": "Cost Center", "fieldtype": "Link", "options": "Cost Center", "idx": 15},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Team & Responsibility", "idx": 16},
            {"fieldname": "responsible_person", "label": "Project Lead", "fieldtype": "Link", "options": "Employee", "reqd": 1, "idx": 17},
            {"fieldname": "initiative_team", "label": "Initiative Team", "fieldtype": "Table", "options": "ESG Initiative Team", "idx": 18},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Description & Goals", "idx": 19},
            {"fieldname": "description", "label": "Description", "fieldtype": "Text Editor", "idx": 20},
            {"fieldname": "objectives", "label": "Objectives & KPIs", "fieldtype": "Table", "options": "ESG Initiative Objective", "idx": 21},
            {"fieldname": "section_break_4", "fieldtype": "Section Break", "label": "Progress Tracking", "idx": 22},
            {"fieldname": "progress_percentage", "label": "Progress %", "fieldtype": "Percent", "read_only": 1, "idx": 23},
            {"fieldname": "milestones", "label": "Milestones", "fieldtype": "Table", "options": "ESG Initiative Milestone", "idx": 24}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "idx": 2},
            {"role": "Project Manager", "read": 1, "write": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Initiative Team",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "fetch_from": "employee.employee_name", "read_only": 1, "in_list_view": 1, "idx": 2},
            {"fieldname": "role", "label": "Role", "fieldtype": "Data", "in_list_view": 1, "idx": 3},
            {"fieldname": "allocation_percentage", "label": "Allocation %", "fieldtype": "Percent", "in_list_view": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Initiative Objective",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "objective", "label": "Objective", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "kpi", "label": "KPI", "fieldtype": "Link", "options": "ESG Metric", "in_list_view": 1, "idx": 2},
            {"fieldname": "target_value", "label": "Target Value", "fieldtype": "Float", "in_list_view": 1, "idx": 3},
            {"fieldname": "achieved_value", "label": "Achieved Value", "fieldtype": "Float", "in_list_view": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Initiative Milestone",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "milestone", "label": "Milestone", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "target_date", "label": "Target Date", "fieldtype": "Date", "reqd": 1, "in_list_view": 1, "idx": 2},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Pending\nIn Progress\nCompleted\nDelayed", "default": "Pending", "in_list_view": 1, "idx": 3},
            {"fieldname": "completion_date", "label": "Completion Date", "fieldtype": "Date", "in_list_view": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Metric",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 0,
        "track_changes": 1,
        "autoname": "ESG-MET-.YYYY.-.#####",
        "title_field": "metric_name",
        "fields": [
            {"fieldname": "metric_name", "label": "Metric Name", "fieldtype": "Data", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "category", "label": "ESG Category", "fieldtype": "Select", "options": "Environmental\nSocial\nGovernance", "reqd": 1, "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "sub_category", "label": "Sub Category", "fieldtype": "Select", "options": "", "depends_on": "category", "idx": 5},
            {"fieldname": "metric_code", "label": "Metric Code", "fieldtype": "Data", "unique": 1, "idx": 6},
            {"fieldname": "is_active", "label": "Active", "fieldtype": "Check", "default": 1, "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Measurement Details", "idx": 8},
            {"fieldname": "description", "label": "Description", "fieldtype": "Small Text", "idx": 9},
            {"fieldname": "unit", "label": "Unit of Measurement", "fieldtype": "Link", "options": "UOM", "reqd": 1, "idx": 10},
            {"fieldname": "data_type", "label": "Data Type", "fieldtype": "Select", "options": "Quantitative\nQualitative\nPercentage\nRatio", "default": "Quantitative", "idx": 11},
            {"fieldname": "column_break_2", "fieldtype": "Column Break", "idx": 12},
            {"fieldname": "frequency", "label": "Reporting Frequency", "fieldtype": "Select", "options": "Daily\nWeekly\nMonthly\nQuarterly\nHalf Yearly\nAnnually", "default": "Monthly", "reqd": 1, "idx": 13},
            {"fieldname": "collection_method", "label": "Collection Method", "fieldtype": "Select", "options": "Manual Entry\nAutomatic from System\nIntegration\nCalculated", "default": "Manual Entry", "idx": 14},
            {"fieldname": "responsible_role", "label": "Responsible Role", "fieldtype": "Link", "options": "Role", "idx": 15},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Targets & Benchmarks", "idx": 16},
            {"fieldname": "target_value", "label": "Target Value", "fieldtype": "Float", "idx": 17},
            {"fieldname": "benchmark_value", "label": "Industry Benchmark", "fieldtype": "Float", "idx": 18},
            {"fieldname": "improvement_target", "label": "Improvement Target %", "fieldtype": "Percent", "idx": 19},
            {"fieldname": "column_break_3", "fieldtype": "Column Break", "idx": 20},
            {"fieldname": "threshold_red", "label": "Red Threshold", "fieldtype": "Float", "idx": 21},
            {"fieldname": "threshold_yellow", "label": "Yellow Threshold", "fieldtype": "Float", "idx": 22},
            {"fieldname": "threshold_green", "label": "Green Threshold", "fieldtype": "Float", "idx": 23},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Integration Settings", "idx": 24},
            {"fieldname": "auto_calculation_formula", "label": "Auto Calculation Formula", "fieldtype": "Code", "idx": 25},
            {"fieldname": "linked_doctypes", "label": "Linked DocTypes", "fieldtype": "Table", "options": "ESG Metric Integration", "idx": 26}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "idx": 2},
            {"role": "Data Entry Operator", "read": 1, "write": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Metric Integration",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "source_doctype", "label": "Source DocType", "fieldtype": "Select", "options": "Purchase Invoice\nSales Invoice\nStock Entry\nDelivery Note\nPurchase Receipt\nPayroll Entry\nAttendance\nEmployee\nCustomer\nSupplier", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "source_field", "label": "Source Field", "fieldtype": "Data", "in_list_view": 1, "idx": 2},
            {"fieldname": "calculation_method", "label": "Calculation", "fieldtype": "Select", "options": "Sum\nAverage\nCount\nMax\nMin\nCustom Formula", "default": "Sum", "in_list_view": 1, "idx": 3},
            {"fieldname": "filter_conditions", "label": "Filter Conditions", "fieldtype": "Code", "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Metric Entry",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "ESG-ENT-.YYYY.-.#####",
        "fields": [
            {"fieldname": "metric", "label": "ESG Metric", "fieldtype": "Link", "options": "ESG Metric", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "entry_date", "label": "Entry Date", "fieldtype": "Date", "reqd": 1, "default": "Today", "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "reporting_period", "label": "Reporting Period", "fieldtype": "Select", "options": "Daily\nWeekly\nMonthly\nQuarterly\nAnnually", "reqd": 1, "idx": 5},
            {"fieldname": "period_from", "label": "Period From", "fieldtype": "Date", "reqd": 1, "idx": 6},
            {"fieldname": "period_to", "label": "Period To", "fieldtype": "Date", "reqd": 1, "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Measurement Data", "idx": 8},
            {"fieldname": "value", "label": "Measured Value", "fieldtype": "Float", "reqd": 1, "idx": 9},
            {"fieldname": "unit", "label": "Unit", "fieldtype": "Link", "options": "UOM", "fetch_from": "metric.unit", "read_only": 1, "idx": 10},
            {"fieldname": "target_value", "label": "Target Value", "fieldtype": "Float", "fetch_from": "metric.target_value", "read_only": 1, "idx": 11},
            {"fieldname": "column_break_2", "fieldtype": "Column Break", "idx": 12},
            {"fieldname": "variance", "label": "Variance", "fieldtype": "Float", "read_only": 1, "idx": 13},
            {"fieldname": "variance_percentage", "label": "Variance %", "fieldtype": "Percent", "read_only": 1, "idx": 14},
            {"fieldname": "performance_indicator", "label": "Performance", "fieldtype": "Select", "options": "Green\nYellow\nRed", "read_only": 1, "idx": 15},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Data Source & Validation", "idx": 16},
            {"fieldname": "data_source", "label": "Data Source", "fieldtype": "Select", "options": "Manual Entry\nSystem Generated\nImported\nCalculated", "default": "Manual Entry", "idx": 17},
            {"fieldname": "source_doctype", "label": "Source DocType", "fieldtype": "Select", "options": "\nPurchase Invoice\nSales Invoice\nStock Entry\nDelivery Note\nPurchase Receipt\nPayroll Entry", "idx": 18},
            {"fieldname": "source_document", "label": "Source Document", "fieldtype": "Dynamic Link", "options": "source_doctype", "idx": 19},
            {"fieldname": "column_break_3", "fieldtype": "Column Break", "idx": 20},
            {"fieldname": "verified_by", "label": "Verified By", "fieldtype": "Link", "options": "Employee", "idx": 21},
            {"fieldname": "verification_date", "label": "Verification Date", "fieldtype": "Date", "idx": 22},
            {"fieldname": "verification_status", "label": "Verification Status", "fieldtype": "Select", "options": "Pending\nVerified\nRejected", "default": "Pending", "idx": 23},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Comments & Attachments", "idx": 24},
            {"fieldname": "remarks", "label": "Remarks", "fieldtype": "Text", "idx": 25},
            {"fieldname": "attachments", "label": "Supporting Documents", "fieldtype": "Table", "options": "ESG Document", "idx": 26}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "idx": 2},
            {"role": "Data Entry Operator", "read": 1, "write": 1, "create": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Compliance Report",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "ESG-RPT-.YYYY.-.#####",
        "title_field": "report_name",
        "fields": [
            {"fieldname": "report_name", "label": "Report Name", "fieldtype": "Data", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "report_type", "label": "Report Type", "fieldtype": "Select", "options": "Monthly\nQuarterly\nHalf Yearly\nAnnual\nCustom\nRegulatory", "default": "Quarterly", "reqd": 1, "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "reporting_period_from", "label": "Reporting Period From", "fieldtype": "Date", "reqd": 1, "idx": 5},
            {"fieldname": "reporting_period_to", "label": "Reporting Period To", "fieldtype": "Date", "reqd": 1, "idx": 6},
            {"fieldname": "generated_on", "label": "Generated On", "fieldtype": "Datetime", "default": "now", "read_only": 1, "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Report Configuration", "idx": 8},
            {"fieldname": "esg_categories", "label": "ESG Categories", "fieldtype": "Table", "options": "ESG Report Category", "idx": 9},
            {"fieldname": "include_charts", "label": "Include Charts", "fieldtype": "Check", "default": 1, "idx": 10},
            {"fieldname": "include_benchmarks", "label": "Include Benchmarks", "fieldtype": "Check", "default": 1, "idx": 11},
            {"fieldname": "column_break_2", "fieldtype": "Column Break", "idx": 12},
            {"fieldname": "template", "label": "Report Template", "fieldtype": "Link", "options": "ESG Report Template", "idx": 13},
            {"fieldname": "stakeholders", "label": "Target Stakeholders", "fieldtype": "Table", "options": "ESG Report Stakeholder", "idx": 14},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Executive Summary", "idx": 15},
            {"fieldname": "summary", "label": "Executive Summary", "fieldtype": "Text Editor", "idx": 16},
            {"fieldname": "key_highlights", "label": "Key Highlights", "fieldtype": "Table", "options": "ESG Report Highlight", "idx": 17},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Performance Analysis", "idx": 18},
            {"fieldname": "performance_summary", "label": "Performance Summary", "fieldtype": "HTML", "read_only": 1, "idx": 19},
            {"fieldname": "metric_analysis", "label": "Detailed Metric Analysis", "fieldtype": "Table", "options": "ESG Report Metric", "idx": 20},
            {"fieldname": "section_break_4", "fieldtype": "Section Break", "label": "Compliance & Risks", "idx": 21},
            {"fieldname": "compliance_status", "label": "Overall Compliance Status", "fieldtype": "Select", "options": "Fully Compliant\nMostly Compliant\nPartially Compliant\nNon-Compliant", "read_only": 1, "idx": 22},
            {"fieldname": "risk_assessment", "label": "Risk Assessment", "fieldtype": "Table", "options": "ESG Risk Assessment", "idx": 23},
            {"fieldname": "section_break_5", "fieldtype": "Section Break", "label": "Actions & Recommendations", "idx": 24},
            {"fieldname": "action_items", "label": "Action Items", "fieldtype": "Table", "options": "ESG Action Item", "idx": 25},
            {"fieldname": "recommendations", "label": "Recommendations", "fieldtype": "Text Editor", "idx": 26},
            {"fieldname": "section_break_6", "fieldtype": "Section Break", "label": "Attachments & Approval", "idx": 27},
            {"fieldname": "attached_documents", "label": "Supporting Documents", "fieldtype": "Table", "options": "ESG Document", "idx": 28},
            {"fieldname": "column_break_3", "fieldtype": "Column Break", "idx": 29},
            {"fieldname": "prepared_by", "label": "Prepared By", "fieldtype": "Link", "options": "Employee", "reqd": 1, "idx": 30},
            # Continue from where the document left off - Complete ESG Compliance Report and remaining components

            {"fieldname": "reviewed_by", "label": "Reviewed By", "fieldtype": "Link", "options": "Employee", "idx": 31},
            {"fieldname": "approved_by", "label": "Approved By", "fieldtype": "Link", "options": "Employee", "idx": 32},
            {"fieldname": "approval_date", "label": "Approval Date", "fieldtype": "Date", "idx": 33}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "idx": 2},
            {"role": "Accounts Manager", "read": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    # Additional child tables for ESG Compliance Report
    {
        "doctype": "DocType",
        "name": "ESG Report Category",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "category", "label": "ESG Category", "fieldtype": "Select", "options": "Environmental\nSocial\nGovernance", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "include", "label": "Include in Report", "fieldtype": "Check", "default": 1, "in_list_view": 1, "idx": 2},
            {"fieldname": "weight", "label": "Weight %", "fieldtype": "Percent", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Report Stakeholder",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "stakeholder_type", "label": "Stakeholder Type", "fieldtype": "Select", "options": "Investors\nRegulators\nCustomers\nEmployees\nCommunity\nSuppliers\nBoard of Directors", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "contact_person", "label": "Contact Person", "fieldtype": "Link", "options": "Contact", "in_list_view": 1, "idx": 2},
            {"fieldname": "email", "label": "Email", "fieldtype": "Data", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Report Highlight",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "highlight", "label": "Key Highlight", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "category", "label": "Category", "fieldtype": "Select", "options": "Achievement\nImprovement\nRisk\nOpportunity\nChallenge", "in_list_view": 1, "idx": 2},
            {"fieldname": "impact", "label": "Impact Level", "fieldtype": "Select", "options": "High\nMedium\nLow", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Report Metric",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "metric", "label": "ESG Metric", "fieldtype": "Link", "options": "ESG Metric", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "current_value", "label": "Current Value", "fieldtype": "Float", "in_list_view": 1, "idx": 2},
            {"fieldname": "target_value", "label": "Target", "fieldtype": "Float", "in_list_view": 1, "idx": 3},
            {"fieldname": "previous_value", "label": "Previous Period", "fieldtype": "Float", "in_list_view": 1, "idx": 4},
            {"fieldname": "trend", "label": "Trend", "fieldtype": "Select", "options": "Improving\nStable\nDeclining", "in_list_view": 1, "idx": 5},
            {"fieldname": "analysis", "label": "Analysis", "fieldtype": "Text", "idx": 6}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Risk Assessment",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "risk_area", "label": "Risk Area", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "risk_level", "label": "Risk Level", "fieldtype": "Select", "options": "Low\nMedium\nHigh\nCritical", "in_list_view": 1, "idx": 2},
            {"fieldname": "probability", "label": "Probability", "fieldtype": "Select", "options": "Low\nMedium\nHigh", "in_list_view": 1, "idx": 3},
            {"fieldname": "impact", "label": "Impact", "fieldtype": "Select", "options": "Low\nMedium\nHigh", "in_list_view": 1, "idx": 4},
            {"fieldname": "mitigation_plan", "label": "Mitigation Plan", "fieldtype": "Text", "idx": 5}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Action Item",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "action", "label": "Action Item", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "priority", "label": "Priority", "fieldtype": "Select", "options": "Low\nMedium\nHigh\nUrgent", "in_list_view": 1, "idx": 2},
            {"fieldname": "responsible", "label": "Responsible", "fieldtype": "Link", "options": "Employee", "in_list_view": 1, "idx": 3},
            {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "in_list_view": 1, "idx": 4},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Open\nIn Progress\nCompleted\nOverdue", "default": "Open", "in_list_view": 1, "idx": 5}
        ]
    },
    # ESG Audit DocType
    {
        "doctype": "DocType",
        "name": "ESG Audit",
        "module": "ESG Compliance",
        "custom": 1,
        "is_submittable": 1,
        "track_changes": 1,
        "autoname": "ESG-AUD-.YYYY.-.#####",
        "title_field": "audit_name",
        "fields": [
            {"fieldname": "audit_name", "label": "Audit Name", "fieldtype": "Data", "reqd": 1, "idx": 1},
            {"fieldname": "company", "label": "Company", "fieldtype": "Link", "options": "Company", "reqd": 1, "idx": 2},
            {"fieldname": "audit_type", "label": "Audit Type", "fieldtype": "Select", "options": "Internal\nExternal\nCertification\nRegulatory", "reqd": 1, "idx": 3},
            {"fieldname": "column_break_1", "fieldtype": "Column Break", "idx": 4},
            {"fieldname": "audit_date", "label": "Audit Date", "fieldtype": "Date", "reqd": 1, "idx": 5},
            {"fieldname": "audit_status", "label": "Status", "fieldtype": "Select", "options": "Planned\nOngoing\nCompleted\nReporting", "default": "Planned", "idx": 6},
            {"fieldname": "auditor", "label": "Lead Auditor", "fieldtype": "Link", "options": "Employee", "reqd": 1, "idx": 7},
            {"fieldname": "section_break_1", "fieldtype": "Section Break", "label": "Audit Scope", "idx": 8},
            {"fieldname": "audit_scope", "label": "Audit Scope", "fieldtype": "Text Editor", "idx": 9},
            {"fieldname": "policies_reviewed", "label": "Policies Under Review", "fieldtype": "Table", "options": "ESG Audit Policy", "idx": 10},
            {"fieldname": "metrics_reviewed", "label": "Metrics Under Review", "fieldtype": "Table", "options": "ESG Audit Metric", "idx": 11},
            {"fieldname": "section_break_2", "fieldtype": "Section Break", "label": "Audit Team", "idx": 12},
            {"fieldname": "audit_team", "label": "Audit Team", "fieldtype": "Table", "options": "ESG Audit Team", "idx": 13},
            {"fieldname": "external_auditor", "label": "External Auditor", "fieldtype": "Data", "idx": 14},
            {"fieldname": "section_break_3", "fieldtype": "Section Break", "label": "Findings & Observations", "idx": 15},
            {"fieldname": "overall_rating", "label": "Overall Rating", "fieldtype": "Select", "options": "Excellent\nGood\nSatisfactory\nNeeds Improvement\nPoor", "idx": 16},
            {"fieldname": "findings", "label": "Audit Findings", "fieldtype": "Table", "options": "ESG Audit Finding", "idx": 17},
            {"fieldname": "recommendations", "label": "Recommendations", "fieldtype": "Text Editor", "idx": 18},
            {"fieldname": "section_break_4", "fieldtype": "Section Break", "label": "Action Plan", "idx": 19},
            {"fieldname": "corrective_actions", "label": "Corrective Actions", "fieldtype": "Table", "options": "ESG Corrective Action", "idx": 20},
            {"fieldname": "next_audit_date", "label": "Next Audit Date", "fieldtype": "Date", "idx": 21}
        ],
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1, "submit": 1, "cancel": 1, "idx": 1},
            {"role": "ESG Manager", "read": 1, "write": 1, "create": 1, "submit": 1, "idx": 2},
            {"role": "Auditor", "read": 1, "write": 1, "create": 1, "idx": 3},
            {"role": "Employee", "read": 1, "idx": 4}
        ]
    },
    # Child tables for ESG Audit
    {
        "doctype": "DocType",
        "name": "ESG Audit Policy",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "policy", "label": "ESG Policy", "fieldtype": "Link", "options": "ESG Policy", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "compliance_status", "label": "Compliance Status", "fieldtype": "Select", "options": "Compliant\nPartially Compliant\nNon-Compliant\nNot Applicable", "in_list_view": 1, "idx": 2},
            {"fieldname": "score", "label": "Score", "fieldtype": "Percent", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Audit Metric",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "metric", "label": "ESG Metric", "fieldtype": "Link", "options": "ESG Metric", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "data_accuracy", "label": "Data Accuracy", "fieldtype": "Select", "options": "Accurate\nMinor Issues\nMajor Issues\nInaccurate", "in_list_view": 1, "idx": 2},
            {"fieldname": "completeness", "label": "Data Completeness", "fieldtype": "Percent", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Audit Team",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "team_member", "label": "Team Member", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "role", "label": "Audit Role", "fieldtype": "Select", "options": "Lead Auditor\nAuditor\nObserver\nSubject Matter Expert", "in_list_view": 1, "idx": 2},
            {"fieldname": "specialization", "label": "Specialization", "fieldtype": "Select", "options": "Environmental\nSocial\nGovernance\nData Analytics\nCompliance", "in_list_view": 1, "idx": 3}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Audit Finding",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "finding_type", "label": "Finding Type", "fieldtype": "Select", "options": "Non-Conformity\nObservation\nOpportunity for Improvement\nPositive Finding", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "category", "label": "ESG Category", "fieldtype": "Select", "options": "Environmental\nSocial\nGovernance", "in_list_view": 1, "idx": 2},
            {"fieldname": "severity", "label": "Severity", "fieldtype": "Select", "options": "Critical\nHigh\nMedium\nLow", "in_list_view": 1, "idx": 3},
            {"fieldname": "description", "label": "Finding Description", "fieldtype": "Text", "reqd": 1, "idx": 4},
            {"fieldname": "evidence", "label": "Evidence", "fieldtype": "Text", "idx": 5},
            {"fieldname": "root_cause", "label": "Root Cause", "fieldtype": "Text", "idx": 6}
        ]
    },
    {
        "doctype": "DocType",
        "name": "ESG Corrective Action",
        "module": "ESG Compliance",
        "custom": 1,
        "istable": 1,
        "fields": [
            {"fieldname": "action_description", "label": "Corrective Action", "fieldtype": "Text", "reqd": 1, "in_list_view": 1, "idx": 1},
            {"fieldname": "responsible_person", "label": "Responsible Person", "fieldtype": "Link", "options": "Employee", "reqd": 1, "in_list_view": 1, "idx": 2},
            {"fieldname": "due_date", "label": "Due Date", "fieldtype": "Date", "reqd": 1, "in_list_view": 1, "idx": 3},
            {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Open\nIn Progress\nCompleted\nOverdue", "default": "Open", "in_list_view": 1, "idx": 4},
            {"fieldname": "completion_date", "label": "Completion Date", "fieldtype": "Date", "idx": 5}
        ]
    },
    
]

print("Creating ESG DocTypes...")
for doctype_data in esg_doctypes:
    try:
        if not frappe.db.exists('DocType', doctype_data['name']):
            doc = frappe.get_doc(doctype_data)
            doc.insert(ignore_permissions=True)
            print(f"✓ Created DocType: {doctype_data['name']}")
        else:
            print(f"◦ DocType {doctype_data['name']} already exists")
    except Exception as e:
        print(f"✗ Error creating {doctype_data['name']}: {str(e)}")

frappe.db.commit()

# Create custom roles for ESG module
esg_roles = [
    {
        "doctype": "Role",
        "role_name": "ESG Manager",
        "is_custom": 1
    },
    {
        "doctype": "Role", 
        "role_name": "ESG Auditor",
        "is_custom": 1
    },
    {
        "doctype": "Role",
        "role_name": "ESG Data Analyst",
        "is_custom": 1
    }
]

print("\nCreating ESG Roles...")
for role_data in esg_roles:
    try:
        if not frappe.db.exists('Role', role_data['role_name']):
            role_doc = frappe.get_doc(role_data)
            role_doc.insert(ignore_permissions=True)
            print(f"✓ Created Role: {role_data['role_name']}")
        else:
            print(f"◦ Role {role_data['role_name']} already exists")
    except Exception as e:
        print(f"✗ Error creating role {role_data['role_name']}: {str(e)}")

frappe.db.commit()

# Create sample ESG metrics with integration to ERPNext modules
sample_metrics = [
    {
        "doctype": "ESG Metric",
        "metric_name": "Total Energy Consumption",
        "metric_code": "ENV_001",
        "category": "Environmental",
        "sub_category": "Energy",
        "unit": "kWh",
        "frequency": "Monthly",
        "description": "Total energy consumption across all facilities",
        "collection_method": "Integration",
        "target_value": 10000,
        "threshold_green": 8000,
        "threshold_yellow": 9500,
        "threshold_red": 12000,
        "company": frappe.defaults.get_global_default("company")
    },
    {
        "doctype": "ESG Metric",
        "metric_name": "Carbon Footprint",
        "metric_code": "ENV_002", 
        "category": "Environmental",
        "sub_category": "Emissions",
        "unit": "Kg",
        "frequency": "Monthly",
        "description": "Direct and indirect carbon emissions",
        "collection_method": "Calculated",
        "target_value": 5000,
        "threshold_green": 4000,
        "threshold_yellow": 4500,
        "threshold_red": 6000,
        "company": frappe.defaults.get_global_default("company")
    },
    {
        "doctype": "ESG Metric",
        "metric_name": "Employee Satisfaction Score",
        "metric_code": "SOC_001",
        "category": "Social", 
        "sub_category": "Employee Wellbeing",
        "unit": "Score",
        "frequency": "Quarterly",
        "description": "Employee satisfaction survey results",
        "collection_method": "Manual Entry",
        "target_value": 85,
        "threshold_green": 80,
        "threshold_yellow": 70,
        "threshold_red": 60,
        "company": frappe.defaults.get_global_default("company")
    },
    {
        "doctype": "ESG Metric",
        "metric_name": "Training Hours per Employee",
        "metric_code": "SOC_002",
        "category": "Social",
        "sub_category": "Training & Development", 
        "unit": "Hours",
        "frequency": "Monthly",
        "description": "Average training hours per employee",
        "collection_method": "Integration",
        "target_value": 40,
        "threshold_green": 35,
        "threshold_yellow": 25,
        "threshold_red": 15,
        "company": frappe.defaults.get_global_default("company")
    },
    {
        "doctype": "ESG Metric",
        "metric_name": "Board Independence Ratio",
        "metric_code": "GOV_001",
        "category": "Governance",
        "sub_category": "Board Composition",
        "unit": "Percent",
        "frequency": "Annually",
        "description": "Percentage of independent directors on board",
        "collection_method": "Manual Entry", 
        "target_value": 60,
        "threshold_green": 50,
        "threshold_yellow": 40,
        "threshold_red": 30,
        "company": frappe.defaults.get_global_default("company")
    }
]

print("\nCreating Sample ESG Metrics...")
for metric_data in sample_metrics:
    try:
        if not frappe.db.exists('ESG Metric', {'metric_code': metric_data['metric_code']}):
            metric_doc = frappe.get_doc(metric_data)
            metric_doc.insert(ignore_permissions=True)
            print(f"✓ Created Metric: {metric_data['metric_name']}")
        else:
            print(f"◦ Metric {metric_data['metric_name']} already exists")
    except Exception as e:
        print(f"✗ Error creating metric {metric_data['metric_name']}: {str(e)}")

frappe.db.commit()

# Create workspace for ESG module
esg_workspace = {
    "doctype": "Workspace",
    "name": "ESG Compliance",
    "title": "ESG Compliance",
    "module": "ESG Compliance",
    "icon": "leaf",
    "color": "#28a745",
    "is_standard": 0,
    "public": 1,
    "content": '''[
        {
            "type": "shortcut",
            "data": {
                "type": "DocType",
                "label": "ESG Policy",
                "name": "ESG Policy",
                "color": "#ff9800"
            }
        },
        {
            "type": "shortcut", 
            "data": {
                "type": "DocType",
                "label": "ESG Initiative",
                "name": "ESG Initiative", 
                "color": "#2196f3"
            }
        },
        {
            "type": "shortcut",
            "data": {
                "type": "DocType",
                "label": "ESG Metric",
                "name": "ESG Metric",
                "color": "#4caf50"
            }
        },
        {
            "type": "shortcut",
            "data": {
                "type": "DocType", 
                "label": "ESG Metric Entry",
                "name": "ESG Metric Entry",
                "color": "#9c27b0"
            }
        },
        {
            "type": "shortcut",
            "data": {
                "type": "DocType",
                "label": "ESG Compliance Report", 
                "name": "ESG Compliance Report",
                "color": "#607d8b"
            }
        },
        {
            "type": "shortcut",
            "data": {
                "type": "DocType",
                "label": "ESG Audit",
                "name": "ESG Audit",
                "color": "#795548"
            }
        }
    ]'''
}

try:
    if not frappe.db.exists('Workspace', 'ESG Compliance'):
        workspace_doc = frappe.get_doc(esg_workspace)
        workspace_doc.insert(ignore_permissions=True)
        print("✓ Created ESG Compliance Workspace")
    else:
        print("◦ ESG Compliance Workspace already exists")
except Exception as e:
    print(f"✗ Error creating workspace: {str(e)}")

frappe.db.commit()

# Add workflow states for key doctypes
workflow_states = [
    {
        "doctype": "Workflow State",
        "workflow_state_name": "Draft",
        "style": "Info"
    },
    {
        "doctype": "Workflow State", 
        "workflow_state_name": "Under Review",
        "style": "Warning"
    },
    {
        "doctype": "Workflow State",
        "workflow_state_name": "Approved", 
        "style": "Success"
    },
    {
        "doctype": "Workflow State",
        "workflow_state_name": "Rejected",
        "style": "Danger"
    }
]

print("\nCreating Workflow States...")
for state_data in workflow_states:
    try:
        if not frappe.db.exists('Workflow State', state_data['workflow_state_name']):
            state_doc = frappe.get_doc(state_data)
            state_doc.insert(ignore_permissions=True)
            print(f"✓ Created Workflow State: {state_data['workflow_state_name']}")
        else:
            print(f"◦ Workflow State {state_data['workflow_state_name']} already exists")
    except Exception as e:
        print(f"✗ Error creating workflow state {state_data['workflow_state_name']}: {str(e)}")

frappe.db.commit()

# Create workflow for ESG Policy
esg_policy_workflow = {
    "doctype": "Workflow",
    "workflow_name": "ESG Policy Approval",
    "document_type": "ESG Policy",
    "workflow_state_field": "workflow_state",
    "is_active": 1,
    "states": [
        {
            "state": "Draft",
            "doc_status": "0",
            "allow_edit": "All"
        },
        {
            "state": "Under Review",
            "doc_status": "0",
            "allow_edit": "ESG Manager"
        },
        {
            "state": "Approved",
            "doc_status": "1",
            "allow_edit": "System Manager"
        },
        {
            "state": "Rejected",
            "doc_status": "2",
            "allow_edit": "System Manager"
        }
    ],
    "transitions": [
        {
            "state": "Draft",
            "action": "Submit for Review",
            "next_state": "Under Review",
            "allowed": "System Manager,ESG Manager",
            "allow_self_approval": 1
        },
        {
            "state": "Under Review",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "System Manager",
            "allow_self_approval": 0
        },
        {
            "state": "Under Review",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "System Manager",
            "allow_self_approval": 0
        },
        {
            "state": "Rejected",
            "action": "Reopen",
            "next_state": "Draft",
            "allowed": "System Manager,ESG Manager",
            "allow_self_approval": 1
        }
    ]
}

print("\nCreating ESG Policy Workflow...")
try:
    if not frappe.db.exists('Workflow', 'ESG Policy Approval'):
        workflow_doc = frappe.get_doc(esg_policy_workflow)
        workflow_doc.insert(ignore_permissions=True)
        print("✓ Created ESG Policy Approval Workflow")
    else:
        print("◦ ESG Policy Approval Workflow already exists")
except Exception as e:
    print(f"✗ Error creating workflow: {str(e)}")

frappe.db.commit()

# Create workflow for ESG Metric Entry
esg_metric_workflow = {
    "doctype": "Workflow",
    "workflow_name": "ESG Metric Verification",
    "document_type": "ESG Metric Entry",
    "workflow_state_field": "verification_status",
    "is_active": 1,
    "states": [
        {
            "state": "Pending",
            "doc_status": "0",
            "allow_edit": "All"
        },
        {
            "state": "Verified",
            "doc_status": "1",
            "allow_edit": "System Manager"
        },
        {
            "state": "Rejected",
            "doc_status": "2",
            "allow_edit": "System Manager"
        }
    ],
    "transitions": [
        {
            "state": "Pending",
            "action": "Verify",
            "next_state": "Verified",
            "allowed": "ESG Manager,ESG Data Analyst",
            "allow_self_approval": 0
        },
        {
            "state": "Pending",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "ESG Manager,ESG Data Analyst",
            "allow_self_approval": 0
        },
        {
            "state": "Rejected",
            "action": "Reopen",
            "next_state": "Pending",
            "allowed": "System Manager,ESG Manager",
            "allow_self_approval": 1
        }
    ]
}

print("\nCreating ESG Metric Entry Workflow...")
try:
    if not frappe.db.exists('Workflow', 'ESG Metric Verification'):
        workflow_doc = frappe.get_doc(esg_metric_workflow)
        workflow_doc.insert(ignore_permissions=True)
        print("✓ Created ESG Metric Verification Workflow")
    else:
        print("◦ ESG Metric Verification Workflow already exists")
except Exception as e:
    print(f"✗ Error creating workflow: {str(e)}")

frappe.db.commit()

# Create dashboard charts for ESG metrics
print("\nCreating Sample Dashboard Charts...")
try:
    if not frappe.db.exists("Dashboard", "ESG Metrics"):
        dashboard = frappe.get_doc({
            "doctype": "Dashboard",
            "dashboard_name": "ESG Metrics",
            "is_standard": 1,
            "charts": [
                {
                    "chart_name": "Energy Consumption Trend",
                    "chart_type": "Line",
                    "doctype": "Dashboard Chart",
                    "filters_json": "{}",
                    "is_custom": 1,
                    "is_public": 1,
                    "owner": "Administrator",
                    "source": "ESG Metric Entry",
                    "time_interval": "Monthly",
                    "timeseries": 1,
                    "type": "Line"
                },
                {
                    "chart_name": "Carbon Footprint Analysis",
                    "chart_type": "Bar",
                    "doctype": "Dashboard Chart",
                    "filters_json": "{}",
                    "is_custom": 1,
                    "is_public": 1,
                    "owner": "Administrator",
                    "source": "ESG Metric Entry",
                    "time_interval": "Monthly",
                    "timeseries": 1,
                    "type": "Bar"
                }
            ]
        })
        dashboard.insert(ignore_permissions=True)
        print("✓ Created ESG Metrics Dashboard")
    else:
        print("◦ ESG Metrics Dashboard already exists")
except Exception as e:
    print(f"✗ Error creating dashboard: {str(e)}")

frappe.db.commit()

print("\nESG Compliance Module Setup Complete!")
print("You can now access the ESG Compliance module from the workspace.")