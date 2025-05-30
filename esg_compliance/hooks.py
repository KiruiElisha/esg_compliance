app_name = "esg_compliance"
app_title = "ESG Compliance"
app_publisher = "K. Ronoh"
app_description = "ESG plugin for erpnext"
app_email = "kronos@kronos.africa"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "esg_compliance",
# 		"logo": "/assets/esg_compliance/logo.png",
# 		"title": "ESG Compliance",
# 		"route": "/esg_compliance",
# 		"has_permission": "esg_compliance.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/esg_compliance/css/esg_compliance.css"
# app_include_js = "/assets/esg_compliance/js/esg_compliance.js"

# include js, css files in header of web template
# web_include_css = "/assets/esg_compliance/css/esg_compliance.css"
# web_include_js = "/assets/esg_compliance/js/esg_compliance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "esg_compliance/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "esg_compliance/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "esg_compliance.utils.jinja_methods",
# 	"filters": "esg_compliance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "esg_compliance.install.before_install"
# after_install = "esg_compliance.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "esg_compliance.uninstall.before_uninstall"
# after_uninstall = "esg_compliance.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "esg_compliance.utils.before_app_install"
# after_app_install = "esg_compliance.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "esg_compliance.utils.before_app_uninstall"
# after_app_uninstall = "esg_compliance.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "esg_compliance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "on_submit": "esg_compliance.api.create_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    },
    "Purchase Invoice": {
        "on_submit": "esg_compliance.api.create_purchase_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    },
    "Stock Entry": {
        "on_submit": "esg_compliance.api.create_stock_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    },
    "Work Order": {
        "on_submit": "esg_compliance.api.create_workorder_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    },
    "Production Plan": {
        "on_submit": "esg_compliance.api.create_production_plan_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    },
    "Delivery Note": {
        "on_submit": "esg_compliance.api.create_delivery_esg_metric_entry",
        "on_cancel": "esg_compliance.api.delete_esg_metric_entry"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"esg_compliance.tasks.all"
# 	],
# 	"daily": [
# 		"esg_compliance.tasks.daily"
# 	],
# 	"hourly": [
# 		"esg_compliance.tasks.hourly"
# 	],
# 	"weekly": [
# 		"esg_compliance.tasks.weekly"
# 	],
# 	"monthly": [
# 		"esg_compliance.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "esg_compliance.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "esg_compliance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "esg_compliance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["esg_compliance.utils.before_request"]
# after_request = ["esg_compliance.utils.after_request"]

# Job Events
# ----------
# before_job = ["esg_compliance.utils.before_job"]
# after_job = ["esg_compliance.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"esg_compliance.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# hooks.py (add to your custom app)

# Export Client Scripts and Custom Fields and Custom DocTypes relevant to ESG carbon calculations
fixtures = [
    {
        "dt": "Client Script",
        "filters": [
            ["name", "in", [
                # Existing scripts
                "Work Order Emissions Calculation",
                "Stock Entry Carbon Impact Calculation",
                # New script names
                "Item Carbon Management",
                "Work Order Carbon Tracking",
                "Production Plan Carbon Estimation",
                "Stock Entry Carbon Calculation",
                "Delivery Note Carbon Calculation",
                "Carbon Calculation",
                "Calculate ESG"
            ]]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["fieldname", "in", [
                # Company Multipliers & ESG Config
                "custom_subcontractor_multiplier",
                "custom_repack_multiplier",
                "custom_manufacture_multiplier",
                "custom_material_transfer_multiplier",
                "custom_material_receipt_multiplier",
                "custom_material_issue_multiplier",
                "custom_manufacturing_overhead_percentage",
                "custom_baseline_emissions_tonnes_co2e",
                "custom_baseline_year",
                "custom_annual_emission_reduction_target_",
                "custom_net_zero_target_year",
                "custom_carbon_emission_targets",
                # Customer Preferences
                "custom_carbon_offset_preference",
                "custom_requires_carbon_footprint_reporting",
                "custom_sustainability_focused_customer",
                # Supplier Profiles
                "custom_annual_carbon_emissions_tonnes_co2e",
                "custom_carbon_intensity_rating",
                "custom_certificate_expiry_date",
                "custom_carbon_certification_type",
                "custom_carbon_certified",
                # Work Order Emissions
                "custom_raw_material_emissions_kg_co2e",
                "custom_manufacturing_process_emissions_kg_co2e",
                "custom_total_work_order_emissions_kg_co2e",
                # Production Plan
                "custom_carbon_reduction_target_",
                "custom_estimated_carbon_emissions_kg_co2e",
                # Stock Entry Impacts
                "custom_carbon_impact_kg_co2e",
                "custom_total_carbon_impact_kg_co2e",
                # Purchase & Delivery
                "custom_carbon_emissions_kg_co2e",
                "custom_total_delivery_emissions_kg_co2e",
                "custom_transport_carbon_emissions_kg_co2e",
                # Purchase Invoice
                "custom_carbon_certificate_number",
                "custom_supplier_is_carbon_certified",
                "custom_total_carbon_emissions_kg_co2e",
                # Sales Invoice
                "custom_carbon_offset_cost",
                "custom_carbon_offset_required",
                "custom_total_carbon_emissions_kg_co2e",
                "custom_carbon_emissions_impact",
                # Item Master ESG
                "custom_emission_factor_last_updated",
                "custom_calculation_method",
                "custom_carbon_scope",
                "custom_emission_source",
                "custom_carbon_emission_factor_kg_co2e_per_unit"
            ]]
        ]
    },
    {
        "dt": "DocType",
        "filters": [
            ["module", "=", "ESG Compliance"]
        ]
    }
]
