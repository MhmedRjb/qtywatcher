import frappe
from erpnext.accounts.doctype.pos_invoice import POSInvoice
class CustomPOSInvoice(POSInvoice):
    def before_submit(self):
        super().before_submit()
        self.update_custom_nosquantity()
    def before_save(self):
        super().before_save()
        self.update_custom_nosquantity()
    def update_custom_nosquantity(self):
        for item in self.items:
            custom_dual_quantity = frappe.db.get_value("Item", item.item_code, "custom_dual_quantity")
            if custom_dual_quantity == 0:
                item.custom_nosquantity = item.qty
            else:
                item.custom_nosquantity = 55