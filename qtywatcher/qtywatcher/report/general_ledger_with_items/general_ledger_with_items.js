frappe.query_reports["General Ledger with items"] = {
	"filters": [{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "Link",
			options: "Account",
			reqd: 1
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Autocomplete",
			options: Object.keys(frappe.boot.party_account_types),
			on_change: function () {
				frappe.query_report.set_filter_value("party", "");
			}
		},
		{
			fieldname: "party",
			label: __("Party"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value("party_type");
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
		}
		
			]
};
