// Copyright (c) 2025, K. Ronoh and contributors
// For license information, please see license.txt

frappe.query_reports["ESG Analysis"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1
		},
		{
			"fieldname": "metric",
			"label": __("ESG Metric"),
			"fieldtype": "Select",
			"options": "\nCarbon Footprint\nSupplier Carbon Footprint\nManufacturing Carbon Impact\nMaterial Receipt Carbon Impact\nMaterial Issue Carbon Impact\nMaterial Transfer Carbon Impact\nDelivery Carbon Impact\nProduction Planning Carbon Impact",
			"width": "120"
		},
		{
			"fieldname": "source_doctype",
			"label": __("Source Document Type"),
			"fieldtype": "Select",
			"options": "\nSales Invoice\nPurchase Invoice\nWork Order\nStock Entry\nProduction Plan\nDelivery Note",
			"width": "120"
		},
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Select",
			"options": "\nCustomer\nSupplier\nWarehouse\nItem\nProduction Plan",
			"width": "100"
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"depends_on": "party_type",
			"width": "100"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "performance",
			"label": __("Performance"),
			"fieldtype": "Select",
			"options": "\nGreen\nRed",
			"width": "100"
		},
		{
			"fieldname": "verification_status",
			"label": __("Verification Status"),
			"fieldtype": "Select",
			"options": "\nPending\nVerified",
			"width": "100"
		},
		{
			"fieldname": "data_source",
			"label": __("Data Source"),
			"fieldtype": "Select",
			"options": "\nSystem Generated",
			"default": "System Generated",
			"width": "100"
		},
		{
			"fieldname": "group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": "\nMetric\nCompany\nMonth\nQuarter\nYear\nPerformance\nSource Document\nParty Type",
			"default": "Metric",
			"width": "100"
		}
	],

	"formatter": function(value, row, column, data, default_formatter) {
		// Format performance indicators with colors
		if (column.fieldname === "performance") {
			if (value === "Green") {
				return `<span style="color: #28a745; font-weight: bold;">● ${value}</span>`;
			} else if (value === "Red") {
				return `<span style="color: #dc3545; font-weight: bold;">● ${value}</span>`;
			}
		}

		// Format variance percentage with colors
		if (column.fieldname === "variance_percent") {
			if (value && !isNaN(value)) {
				let color = value > 0 ? "#dc3545" : "#28a745";
				return `<span style="color: ${color}; font-weight: bold;">${default_formatter(value, row, column, data)}%</span>`;
			}
			return default_formatter(value, row, column, data);
		}

		// Format verification status
		if (column.fieldname === "verification_status") {
			let color = "#6c757d";
			if (value === "Verified") color = "#28a745";
			else if (value === "Rejected") color = "#dc3545";
			else if (value === "Pending") color = "#ffc107";
			
			return `<span style="color: ${color};">${value || "Not Set"}</span>`;
		}

		// Format currency and numbers
		if (column.fieldname === "measured_value" || column.fieldname === "target_value" || column.fieldname === "variance") {
			if (value && !isNaN(value)) {
				return parseFloat(value).toLocaleString('en-US', {
					minimumFractionDigits: 2,
					maximumFractionDigits: 2
				});
			}
		}

		return default_formatter(value, row, column, data);
	},

	"get_datatable_options": function(options) {
		return Object.assign(options, {
			checkboxColumn: true,
			events: {
				onCheckRow: function(data) {
					// Handle row selection for bulk operations
					console.log("Selected rows:", data);
				}
			}
		});
	},

	"onload": function(report) {
		// Add custom buttons
		report.page.add_inner_button(__("Export to Excel"), function() {
			frappe.tools.downloadify(report.data, null, report.report_name);
		});

		report.page.add_inner_button(__("Send Email Report"), function() {
			frappe.prompt([
				{
					fieldname: "recipients",
					label: __("Recipients"),
					fieldtype: "Data",
					reqd: 1,
					description: __("Comma separated email addresses")
				},
				{
					fieldname: "subject",
					label: __("Subject"),
					fieldtype: "Data",
					default: __("ESG Analysis Report - {0}", [frappe.datetime.get_today()])
				},
				{
					fieldname: "message",
					label: __("Message"),
					fieldtype: "Text Editor",
					default: __("Please find the ESG Analysis Report attached.")
				}
			], function(values) {
				frappe.call({
					method: "frappe.core.doctype.communication.email.make",
					args: {
						recipients: values.recipients,
						subject: values.subject,
						content: values.message,
						attachments: [{
							fname: report.report_name + ".xlsx",
							fcontent: frappe.tools.get_csv_data(report.data, report.columns)
						}]
					},
					callback: function(r) {
						if (!r.exc) {
							frappe.show_alert(__("Email sent successfully"));
						}
					}
				});
			}, __("Send Email"), __("Send"));
		});

		// Add dashboard button
		report.page.add_inner_button(__("View Dashboard"), function() {
			frappe.set_route("query-report", "ESG Dashboard");
		});
	}
};