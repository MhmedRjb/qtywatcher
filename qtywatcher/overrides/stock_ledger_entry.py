import frappe
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
class CustomStockLedgerEntry(StockLedgerEntry):
    # def before_insert(self):
    #     pass
    #     # get actual qty from stock ledger entry have same voucher type and 
    #     # #warehouse and item code and batch no and serial no
    #     # lastrelatedstockledgerentry = frappe.db.sql("""select sle.actual_qty from `tabStock Ledger Entry` sle
    #     # where sle.voucher_type = %s and sle.warehouse = %s and sle.item_code = %s and sle.batch_no = %s and sle.serial_no = %s
    #     # order by sle.creation desc limit 1""", (self.voucher_type, self.warehouse, self.item_code, self.batch_no, self.serial_no), as_dict=True)
    #     # if lastrelatedstockledgerentry:
    #     #     self.db_set('custom_actual_qty', lastrelatedstockledgerentry[0].actual_qty)
    #     # else:
    #     #     self.db_set('custom_actual_qty', 0)
    #     self.db_set('custom_nosquantity_after_transaction', 125)
    # def before_insert(self):

    def after_insert(self):
        
        if self.actual_qty == 0:
            return self.db_set('custom_nosquantity', 0)
        else:
            StockLedgerEntryVoucher_type = frappe.get_last_doc(self.voucher_type)

            qty_sign  = self.actual_qty/abs(self.actual_qty)

            dictData=StockLedgerEntryVoucher_type.as_dict(no_nulls=True, convert_dates_to_str=False)

            childTableName=dictData['items'][0]['doctype']

            ItemsTable = frappe.get_doc(childTableName, self.voucher_detail_no)

            try:
                nosquantity=abs(ItemsTable.custom_nosquantity)*qty_sign 
            except AttributeError:
                nosquantity = 0.1
            self.db_set('custom_nosquantity', nosquantity)


