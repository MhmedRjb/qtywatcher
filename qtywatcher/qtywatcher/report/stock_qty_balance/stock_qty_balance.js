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
		{fieldname:"voucher_type", fieldtype:"Select", options:"Stock Entry\nDelivery Note\nPurchase Receipt\nPurchase Invoice\nSales Invoice\nSales Order\nPurchase Order", label:__("Voucher Type")},
		{fieldname:"simple_view", fieldtype:"Check", label:__("simple_view")}

	]	
};
