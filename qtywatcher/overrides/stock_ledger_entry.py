import frappe
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
class CustomStockLedgerEntry(StockLedgerEntry):
    def before_insert(self):
        try:
            self.last_record = frappe.get_last_doc("Stock Ledger Entry", {"warehouse": self.warehouse, "item_code": self.item_code})
        except:
            self.last_record = None    

    
    def after_insert(self):
        childtable= frappe.get_last_doc(self.voucher_type).as_dict(no_nulls=True, convert_dates_to_str=False)['items'][0]['doctype']

        custom_nosquantity = frappe.get_doc(childtable,self.voucher_detail_no).get("custom_nosquantity")

 
        if self.actual_qty<0:
            custom_nosquantity = - abs(custom_nosquantity)
        else :
            custom_nosquantity = abs(custom_nosquantity)

        # handel if there is no value in custom_nosquantity

        if self.last_record:
            if self.voucher_type == "Stock Reconciliation":
                custom_nosquantity_after_transaction = custom_nosquantity
                custom_nosquantity = 0
            else:
                custom_nosquantity_after_transaction = self.last_record.custom_nosquantity_after_transaction + custom_nosquantity
        else:
            custom_nosquantity_after_transaction = custom_nosquantity

        

        self.db_set('custom_nosquantity_after_transaction', custom_nosquantity_after_transaction)
        self.db_set('custom_nosquantity', custom_nosquantity)
        

    

