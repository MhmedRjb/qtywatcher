// Copyright (c) 2024, mhmed rjb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["stock qty ledger"] = {
	"filters": [
		{fieldname:"item", fieldtype:"Link", options:"Item", label:__("Item")},
		{fieldname:"item_group", fieldtype:"Link", options:"Item Group", label:__("Item Group")},
		{fieldname:"warehouse", fieldtype:"Link", options:"Warehouse", label:__("Warehouse")},
		{fieldname:"from_date", fieldtype:"Date", label:__("From Date")},
		{fieldname:"to_date", fieldtype:"Date", label:__("To Date")},
		{fieldname:"voucher_type", fieldtype:"Select", options:"Stock Entry\nDelivery Note\nPurchase Receipt\nPurchase Invoice\nSales Invoice\nSales Order\nPurchase Order", label:__("Voucher Type")}
		
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
	
		if (column.fieldname == "out_qty" && data && data.out_qty < 0) {
			value = "<span style='color:red'>" + value + "</span>";
		} else if (column.fieldname == "in_qty" && data && data.in_qty > 0) {
			value = "<span style='color:green'>" + value + "</span>";
		} else if (column.fieldname == "out_sec_qty" && data && data.out_sec_qty < 0) {
			value = "<span style='color:red'>" + value + "</span>";
		} else if (column.fieldname == "in_sec_qty" && data && data.in_sec_qty > 0) {
			value = "<span style='color:green'>" + value + "</span>";
		}
	
		return value;
	}
	
};
