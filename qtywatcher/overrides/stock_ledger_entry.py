import frappe
from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
class CustomStockLedgerEntry(StockLedgerEntry):


        
    def after_insert(self):
        lastrelatedstockledgerentry = frappe.db.sql("""SELECT sle.custom_nosquantity_after_transaction 
                                                        FROM `tabStock Ledger Entry` sle
                                                        WHERE sle.voucher_type = %s 
                                                        AND sle.warehouse = %s 
                                                        AND sle.item_code = %s 
                                                        AND sle.batch_no = %s 
                                                        AND sle.serial_no = %s
                                                        ORDER BY sle.creation DESC 
                                                        LIMIT 1 OFFSET 1;
                                                                        """,
        (self.voucher_type, self.warehouse, self.item_code, self.batch_no, self.serial_no), as_dict=True)

        StockLedgerEntryVoucher_type = frappe.get_last_doc(self.voucher_type)
        try:
            qty_sign  = self.actual_qty/abs(self.actual_qty)
        except ZeroDivisionError:
            qty_sign = 1


        dictData=StockLedgerEntryVoucher_type.as_dict(no_nulls=True, convert_dates_to_str=False)

        childTableName=dictData['items'][0]['doctype']

        ItemsTable = frappe.get_doc(childTableName, self.voucher_detail_no)

        try:
            nosquantity=abs(ItemsTable.custom_nosquantity)*qty_sign 
        except AttributeError:
            nosquantity = 0.1

        # if self.actual_qty == 0:
        #     return self.db_set('custom_nosquantity', 0)
        # else:
        self.db_set('custom_nosquantity', nosquantity)
        try:
            self.db_set('custom_nosquantity_after_transaction', lastrelatedstockledgerentry[0].custom_nosquantity_after_transaction + nosquantity)
        except IndexError:
            self.db_set('custom_nosquantity_after_transaction',  nosquantity)


        # self.db_set('custom_nosquantity_after_transaction',lastrelatedstockledgerentry[0].custom_nosquantity_after_transaction+nosquantity)
            


