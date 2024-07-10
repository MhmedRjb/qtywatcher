# test_custom_stock_ledger.py

from erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry import StockLedgerEntry
from qtywatcher.overrides.stock_ledger_entry import CustomStockLedgerEntry
from frappe.tests.utils import FrappeTestCase, change_settings
import frappe

class TestDriver(FrappeTestCase):
    def test_set(self):
        sle = frappe.get_doc({
            "doctype": "Stock Ledger Entry",
            "warehouse": "testwarehouse - E",
            "item_code": "ABC123",
            "custom_nosquantity": 10,
            "voucher_type": "Stock Entry",
            "posting_date": "2024-07-10",
            "voucher_no": "MAT-STE-2024-00002",
            "actual_qty": 10,
        }).insert()

        self.assertEqual(sle.custom_nosquantity_after_transaction, 10)

        
        

