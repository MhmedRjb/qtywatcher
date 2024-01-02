// Copyright (c) 2024, mhmed rjb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["test"] = {
	"filters": [
		{fieldname:"company", fieldtype:"Link", options:"Company",default:frappe.defaults.get_user_default("Company"),reqd:1},
		{fieldname:"from_date", fieldtype:"Date", label:"From Date",default:frappe.defaults.get_user_default("year_start_date")},
		{fieldname:"to_date", fieldtype:"Date", label:"To Date",default:frappe.defaults.get_user_default("year_end_date")},
		{fieldname:"item", fieldtype:"Link", options:"Item",label:"Item"},
		{fieldname:"warehouse", fieldtype:"Link", options:"Warehouse",label:"Warehouse"},
		{fieldname:"item_group", fieldtype:"Link", options:"Item Group",label:"Item Group"},
		{fieldname:"item_code", fieldtype:"Link", options:"Item",label:"Item"},
		
	]
};
