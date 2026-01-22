// Copyright (c) 2025, K. Ronoh and contributors
// For license information, please see license.txt

frappe.query_reports["ESG Activity Log"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1
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
			"fieldname": "source_type",
			"label": __("Source Type"),
			"fieldtype": "Select",
			"options": "\nSales Invoice\nPurchase Invoice\nDelivery Note\nStock Entry\nWork Order\nProduction Plan"
		},
		{
			"fieldname": "activity_type",
			"label": __("Activity Type"),
			"fieldtype": "Select",
			"options": "\nCarbon Footprint\nSupplier Carbon Footprint\nManufacturing Carbon Impact\nDelivery Carbon Impact\nMaterial Receipt Carbon Impact\nMaterial Issue Carbon Impact"
		},
		{
			"fieldname": "performance",
			"label": __("Performance"),
			"fieldtype": "Select",
			"options": "\nGreen\nRed"
		},
		{
			"fieldname": "include_initiatives",
			"label": __("Include Initiatives"),
			"fieldtype": "Check",
			"default": 1
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		if (!data) return default_formatter(value, row, column, data);
		
		if (column.fieldname === "performance") {
			if (!value) return "";
			const color = value === "Green" ? "#28a745" : "#dc3545";
			return `<span style="color: ${color}; font-weight: bold;">●</span> ${value}`;
		}
		
		if (column.fieldname === "impact_value") {
			if (!value) return "";
			if (data.entry_type === 'Initiative') {
				return frappe.format(value, {fieldtype: 'Currency'});
			}
			// Format number with 2 decimal places
			const formatted = frappe.format(value, {fieldtype: 'Float', precision: 2});
			return `${formatted} kg CO₂e`;
		}
		
		if (column.fieldname === "activity_type") {
			if (!value) return "";
			const status = data.status ? data.status.toLowerCase() : 'default';
			if (data.entry_type === 'Initiative') {
				return `<span class="indicator-pill ${status}">${value}</span>`;
			}
			return value;
		}
		
		if (column.fieldname === "source_name") {
			if (!value) return "";
			const doctype = (data.source_type || '').toLowerCase().replace(/ /g, '-');
			return `<a href="/app/${doctype}/${value}">${value}</a>`;
		}
		
		if (column.fieldname === "party" && value) {
			if (!data.party_type) return value;
			const doctype = (data.party_type || '').toLowerCase().replace(/ /g, '-');
			return `<a href="/app/${doctype}/${value}">${value}</a>`;
		}
		
		return default_formatter(value, row, column, data);
	}
};
