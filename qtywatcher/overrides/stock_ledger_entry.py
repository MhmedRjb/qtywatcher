import frappe
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
class CustomStockLedgerEntry(StockLedgerEntry):
    # set custome field (nosquantity) equal to 5 
    def after_insert(self):
        self.db_set('custom_nosquantity', 12)
        print("after insert")
        print(self.voucher_no)
        print(self.vocher_Detail_no)
        #print custom_nosquantity from stocke entry 




