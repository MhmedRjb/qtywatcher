# Copyright (c) 2024, mhmed rjb and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder.functions import CombineDatetime
from frappe.utils import cint, flt
from frappe import _

def build_columns():
    return [
        _("Item") + ":Link/Item:100",
        _("Warehouse") + ":Link/Warehouse:120",
        _("Stock Balance") + ":Float:120",
        _("Stock Balance sec qty") + ":Float:120",
    ]

def build_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += f" AND posting_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND posting_date <= '{filters['to_date']}'"
    if filters.get("item"):
        conditions += f" AND item_code = '{filters['item']}'"
    if filters.get("warehouse"):
        conditions += f" AND warehouse = '{filters['warehouse']}'"
    if filters.get("voucher_type"):
        conditions += f" AND voucher_type = '{filters['voucher_type']}'"
    return conditions

def execute(filters):
    columns = build_columns()
    conditions = build_conditions(filters)
    data = frappe.db.sql(f"""
        SELECT 
        s.Item,
        s.warehouse,
        s.stock_balance,
        s.stock_balanceNOS
        FROM 
        (
        SELECT 
        item_code as Item,
        DATE_FORMAT(CONCAT(posting_date, ' ', posting_time), '%Y-%m-%d %H:%i:%s') AS combined_date_time,
        warehouse,
        qty_after_transaction AS stock_balance,
        custom_nosquantity_after_transaction as stock_balanceNOS
        FROM 
        `tabStock Ledger Entry`
        WHERE 
        is_cancelled = 0 AND docstatus = 1 {conditions} 
        ) s
        JOIN 
        (
        SELECT 
        item_code,
        warehouse,
        MAX(DATE_FORMAT(CONCAT(posting_date, ' ', posting_time), '%Y-%m-%d %H:%i:%s')) AS max_date
        FROM 
        `tabStock Ledger Entry`
        WHERE 
        is_cancelled = 0 AND docstatus = 1 {conditions} 
        GROUP BY 
        item_code, warehouse
        ) m
        ON 
        s.Item = m.item_code AND s.warehouse = m.warehouse AND s.combined_date_time = m.max_date
    """)
    return columns, data
