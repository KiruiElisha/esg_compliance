import frappe
from frappe.utils import getdate, nowtime, add_days

def create_esg_metric_entry(doc, method):
    if not doc.custom_total_carbon_emissions_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_total_carbon_emissions_kg_co2e
    variance = target_value - measured
    
    # Calculate performance based on variance
    performance = "Red" if variance < 0 else "Green"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": "Carbon Footprint",
        "company": doc.company,
        "reporting_period": doc.posting_date,
        "period_from": doc.posting_date,
        "period_to": doc.posting_date,
        "value": measured,
        "source_doctype": "Sales Invoice",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(target_value),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Customer",
        "party": doc.customer,
        "remarks": f"Carbon emissions from Sales Invoice {doc.name}",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()

def delete_esg_metric_entry(doc, method):
    # Find and delete linked ESG entries
    esg_entries = frappe.get_all("ESG Metric Entry",
        filters={
            "source_doctype": "Sales Invoice",
            "source_document": doc.name
        }
    )
    
    for entry in esg_entries:
        frappe.delete_doc("ESG Metric Entry", entry.name, ignore_permissions=True)
    
    frappe.db.commit()

def create_purchase_esg_metric_entry(doc, method):
    if not doc.custom_total_carbon_emissions_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_total_carbon_emissions_kg_co2e
    variance = target_value - measured
    
    # Calculate performance based on variance and certification
    performance = "Green" if doc.custom_supplier_is_carbon_certified else "Red"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": "Supplier Carbon Footprint",
        "company": doc.company,
        "reporting_period": doc.posting_date,
        "period_from": doc.posting_date,
        "period_to": doc.posting_date,
        "value": measured,
        "source_doctype": "Purchase Invoice",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(target_value),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Verified" if doc.custom_supplier_is_carbon_certified else "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Supplier",
        "party": doc.supplier,
        "remarks": f"Carbon emissions from Purchase Invoice {doc.name}",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()

def create_stock_esg_metric_entry(doc, method):
    if not doc.custom_total_carbon_impact_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_total_carbon_impact_kg_co2e
    variance = target_value - measured
    
    # Calculate performance based on variance and stock entry type
    performance = "Green" if doc.purpose == "Material Receipt" else "Red"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": f"{doc.purpose} Carbon Impact",
        "company": doc.company,
        "reporting_period": doc.posting_date,
        "period_from": doc.posting_date,
        "period_to": doc.posting_date,
        "value": measured,
        "source_doctype": "Stock Entry",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(target_value),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Warehouse",
        "party": doc.to_warehouse or doc.from_warehouse,
        "remarks": f"Carbon impact from {doc.purpose} {doc.name}",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()

def create_workorder_esg_metric_entry(doc, method):
    if not doc.custom_total_work_order_emissions_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_total_work_order_emissions_kg_co2e
    variance = target_value - measured
    
    # Calculate total manufacturing impact
    total_impact = (doc.custom_raw_material_emissions_kg_co2e or 0) + (doc.custom_manufacturing_process_emissions_kg_co2e or 0)
    
    # Calculate performance based on total impact vs target
    performance = "Red" if total_impact > target_value else "Green"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": "Manufacturing Carbon Impact",
        "company": doc.company,
        "reporting_period": doc.planned_start_date,
        "period_from": doc.planned_start_date,
        "period_to": doc.planned_start_date,
        "value": measured,
        "source_doctype": "Work Order",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(target_value),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Item",
        "party": doc.production_item,
        "remarks": f"Manufacturing emissions for {doc.item_name} (WO: {doc.name})",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()

def create_production_plan_esg_metric_entry(doc, method):
    if not doc.custom_estimated_carbon_emissions_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_estimated_carbon_emissions_kg_co2e
    reduction_target = doc.custom_carbon_reduction_target_ or 0
    adjusted_target = target_value * (1 - (reduction_target / 100))
    variance = adjusted_target - measured
    
    # Calculate performance based on meeting reduction target
    performance = "Green" if measured <= adjusted_target else "Red"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": "Production Planning Carbon Impact",
        "company": doc.company,
        "reporting_period": doc.posting_date,
        "period_from": doc.posting_date,
        "period_to": doc.posting_date,
        "value": measured,
        "source_doctype": "Production Plan",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(adjusted_target),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Production Plan",
        "party": doc.name,
        "remarks": f"Estimated carbon emissions for Production Plan {doc.name} (Target reduction: {reduction_target}%)",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()

def create_delivery_esg_metric_entry(doc, method):
    if not doc.custom_total_delivery_emissions_kg_co2e:
        return
        
    # Get company target value from ESG settings or default
    target_value = frappe.db.get_value('Company', doc.company, 
        'custom_baseline_emissions_tonnes_co2e') or 5000
    
    measured = doc.custom_total_delivery_emissions_kg_co2e
    product_emissions = doc.custom_product_carbon_emissions_kg_co2e or 0
    transport_emissions = doc.custom_transport_carbon_emissions_kg_co2e or 0
    variance = target_value - measured
    
    # Calculate performance based on transport vs product emissions
    performance = "Green" if transport_emissions < (product_emissions * 0.1) else "Red"
    
    esg_entry = frappe.get_doc({
        "doctype": "ESG Metric Entry",
        "metric": "Delivery Carbon Impact",
        "company": doc.company,
        "reporting_period": doc.posting_date,
        "period_from": doc.posting_date,
        "period_to": doc.posting_date,
        "value": measured,
        "source_doctype": "Delivery Note",
        "source_document": doc.name,
        "entry_date": getdate(),
        "measured_value": str(measured),
        "target_value": str(target_value),
        "unit": "kg",
        "variance": variance,
        "variance_": str(variance),
        "performance": performance,
        "data_source": "System Generated",
        "verification_status": "Pending",
        "verification_date": add_days(getdate(), 7),
        "party_type": "Customer",
        "party": doc.customer,
        "remarks": f"Delivery emissions for {doc.customer_name} (Product: {product_emissions}kg, Transport: {transport_emissions}kg)",
        "supporting_documents": [{
            "document_type": "Evidence",
            "document_name": doc.name,
            "idx": 1
        }]
    })
    
    esg_entry.insert(ignore_permissions=True)
    frappe.db.commit()
