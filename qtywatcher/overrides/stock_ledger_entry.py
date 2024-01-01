import frappe
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
class CustomStockLedgerEntry(StockLedgerEntry):

    def after_insert(self):
        # get last doc of voucher type
        StockLedgerEntryVoucher_type = frappe.get_last_doc(self.voucher_type)
        #check sign of Qty Change
        positive_qty_change = self.actual_qty/abs(self.actual_qty)

        dictData=StockLedgerEntryVoucher_type.as_dict(no_nulls=True, convert_dates_to_str=False)

        childTableName=dictData['items'][0]['doctype']

        ItemsTable = frappe.get_doc(childTableName, self.voucher_detail_no)
        nosquantity=(ItemsTable.custom_nosquantity)*positive_qty_change

        self.db_set('custom_nosquantity', nosquantity)

        print("After insert:")
        print(f"Voucher No: {self.voucher_no}")
        print(f"Voucher Detail No: {self.voucher_detail_no}")
