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
    stock_balance_nos_condition = "AND sb.stock_balance != 0" if filters.get("not_exulde_zero") else ""
    data = frappe.db.sql(f"""
        SELECT 
            sb.Item,
            sb.warehouse,
            sb.stock_balance,
            sn.stock_balanceNOS
        FROM 
        (
            SELECT 
                item_code as Item,
                DATE_FORMAT(CONCAT(posting_date, ' ', posting_time), '%Y-%m-%d %H:%i:%s') AS combined_date_time,
                warehouse,
                qty_after_transaction AS stock_balance
            FROM 
                `tabStock Ledger Entry`
            WHERE 
                1=1 {conditions}
        ) sb
        JOIN 
        (
            SELECT 
                item_code as Item,
                DATE_FORMAT(creation, '%Y-%m-%d %H:%i:%s') AS combined_date_time,
                warehouse,
                custom_nosquantity_after_transaction as stock_balanceNOS
            FROM 
                `tabStock Ledger Entry`
            WHERE 
                1=1 {conditions}
        ) sn
        ON 
            sb.Item = sn.Item AND sb.warehouse = sn.warehouse
        JOIN 
        (
            SELECT 
                item_code,
                warehouse,
                MAX(DATE_FORMAT(CONCAT(posting_date, ' ', posting_time), '%Y-%m-%d %H:%i:%s')) AS max_posting_date,
                MAX(DATE_FORMAT(creation, '%Y-%m-%d %H:%i:%s')) AS max_creation_date
            FROM 
                `tabStock Ledger Entry`
            WHERE 
                1=1 {conditions}
            GROUP BY 
                item_code, warehouse
        ) m
        ON 
            sb.Item = m.item_code AND sb.warehouse = m.warehouse 
            AND sb.combined_date_time = m.max_posting_date
            AND sn.combined_date_time = m.max_creation_date
            WHERE
            1=1 {stock_balance_nos_condition}

    """)
    return columns, data