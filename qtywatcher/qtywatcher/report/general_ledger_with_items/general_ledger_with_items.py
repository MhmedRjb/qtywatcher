# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from collections import OrderedDict

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate
def build_conditions(filters):
    conditions = ""
    party_list = filters.get("party")
    
    if party_list:
        if isinstance(party_list, list):
            party_list_str = "','".join(party_list)
            conditions += f" AND gle.party IN ('{party_list_str}')"
        else:
            conditions += f" AND gle.party = '{party_list}'"
    # from data to date
    conditions += f" AND gle.posting_date >= '{filters.get('from_date')}'"
    conditions += f" AND gle.posting_date <= '{filters.get('to_date')}'"

    return conditions


def execute(filters):
    columns , data = [], []
    columns = get_columns()
    conditions = build_conditions(filters)
    data = frappe.db.sql(f"""SELECT
    gle.creation,
        CASE
        WHEN item.stock_qty < 0 AND gle.voucher_type = 'Purchase Invoice' THEN 'مرتد شراء'
        WHEN item.stock_qty < 0 AND gle.voucher_type = 'Sales Invoice' THEN 'مرتجع مبيعات'
        ELSE gle.voucher_type
    END AS transaction_type,
    gle.voucher_type,
    gle.voucher_no,
    item.item_name,
    item.rate,
    item.stock_qty,
    COALESCE(item.amount, (gle.debit - gle.credit)) AS amount,                            

    gle.debit,
    gle.credit,
    @balance_running := @balance_running + COALESCE(item.amount, (gle.debit - gle.credit)) AS running_balance
FROM
    `tabGL Entry` AS gle
LEFT JOIN
    (
        SELECT
            parent,
            rate,
            amount,
            stock_qty,
            item_name,
            docstatus
        FROM
            `tabPurchase Invoice Item`
        WHERE
            docstatus = 1

        UNION ALL

        SELECT
            parent,
            rate,
            amount,
            stock_qty,
            item_name,
            docstatus
        FROM
            `tabSales Invoice Item`
        WHERE
            docstatus = 1
    ) AS item ON gle.voucher_no = item.parent
JOIN
    (SELECT @balance_running := 0) AS init
WHERE
    gle.docstatus = 1
     {conditions}
    AND gle.party != gle.against
    AND gle.is_cancelled = 0
ORDER BY
    gle.is_opening DESC,
    gle.creation;
    """)
    print (data)

    return columns, data




def get_columns(filters=None):
    columns = [
                {
            "label": _("Creation"),
            "fieldname": "creation",
            "fieldtype": "Date",
            "width": 120,
        },
                {
            "label": _("transaction_type"),
            "fieldname": "transaction_type",
            "fieldtype": "Data",
            "width": 120,
        },
                {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 120,
            "hidden": 1,
        },        

        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
            "width": 120,
        },
                {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 120,
        },

        
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "float",
            "width": 120,
        },
        {
            "label": _("Stock Qty"),
            "fieldname": "stock_qty",
            "fieldtype": "float",
            "width": 120,
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "float",
            "width": 120,
        },


        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "float",
            "width": 120,
        },
        {
            "label": _("Credit"),
            "fieldname": "credit",
            "fieldtype": "float",
            "width": 120,
        },
        

        {
            "label": _("Running Balance"),
            "fieldname": "running_balance",
            "fieldtype": "float",
            "width": 120,
        },
    ]
    return columns


