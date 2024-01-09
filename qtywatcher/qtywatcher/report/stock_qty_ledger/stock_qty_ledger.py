# Copyright (c) 2024, mhmed rjb and contributors
# For license information, please see license.txt

import frappe


from frappe import _

def execute(filters=None):
    columns = [
        _("Item") + ":Link/Item:120",
        _("Posting Date") + "::120",
        _("In Qty") + ":Float:100",
        _("In Qty NOS") + ":Float:100",
        _("Out Qty") + ":Float:100",
        _("Out Qty NOS") + ":Float:100",
        _("Warehouse") + ":Link/Warehouse:120",
        _("Voucher Type") + "::120",
        _("Voucher No") + "::120",
        _("Batch No") + "::120",
        _("Stock Balance") + ":Float:120",
        _("Stock Balance NOS") + ":Float:120"
    ]

    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND posting_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        print(filters.get("to_date"))
        print(f" AND posting_date <= '{filters['to_date']}'")
        conditions += f" AND posting_date <= '{filters['to_date']}'"
    if filters.get("item"):
        conditions += f" AND item_code = '{filters['item']}'"
    if filters.get("warehouse"):
        conditions += f" AND warehouse = '{filters['warehouse']}'"
    if filters.get("voucher_type"):
        conditions += f" AND voucher_type = '{filters['voucher_type']}'"

    data = frappe.db.sql(f"""
        SELECT 
            item_code as Item,
            posting_date,
            COALESCE(CASE WHEN actual_qty > 0 THEN actual_qty ELSE 0 END, 0) AS in_qty,
            COALESCE(CASE WHEN actual_qty > 0 THEN custom_nosquantity ELSE 0 END, 0) AS in_qtyNOS,
            COALESCE(CASE WHEN actual_qty < 0 THEN -actual_qty ELSE 0 END, 0) AS out_qty,
            COALESCE(CASE WHEN actual_qty < 0 THEN -custom_nosquantity ELSE 0 END, 0) AS out_qtyNOS,
            warehouse,
            voucher_type,
            voucher_no,
            batch_no,
            qty_after_transaction AS stock_balance,
            custom_nosquantity_after_transaction as stock_balanceNOS
        FROM 
            `tabStock Ledger Entry`
        WHERE 
            is_cancelled = 0 AND docstatus = 1  {conditions} 
        GROUP BY 
            voucher_detail_no, Item, warehouse, voucher_type, voucher_no, batch_no,posting_date
    """)

    return columns, data
