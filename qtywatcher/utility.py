import frappe
def validate_nosquantity(doc, method):
	for item in doc.items:
		dual_qty = frappe.db.get_value("Item", item.item_code, "custom_dual_quantity")
		
		if not dual_qty:
			item.custom_nosquantity = item.qty
			continue
		
  
		if not item.custom_nosquantity:
			frappe.throw("Please enter the nosquantity")
	
  
		if item.custom_nosquantity <item.qty:
			frappe.throw("The quantity of item {} is bigger than qty".format(item.item_code))




