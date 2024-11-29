import frappe
from erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log import POSInvoiceMergeLog
from frappe import _
from frappe.model.mapper import map_child_doc, map_doc
from frappe.utils import cint, flt
from erpnext.accounts.doctype.pos_profile.pos_profile import required_accounting_dimensions

class CustomPOSInvoiceMergeLog(POSInvoiceMergeLog):
    
    
	def merge_pos_invoice_into(self, invoice, data):
		items, payments, taxes = [], [], []

		loyalty_amount_sum, loyalty_points_sum = 0, 0

		rounding_adjustment, base_rounding_adjustment = 0, 0
		rounded_total, base_rounded_total = 0, 0

		loyalty_amount_sum, loyalty_points_sum, idx = 0, 0, 1

		for doc in data:
			map_doc(doc, invoice, table_map={"doctype": invoice.doctype})

			if doc.redeem_loyalty_points:
				invoice.loyalty_redemption_account = doc.loyalty_redemption_account
				invoice.loyalty_redemption_cost_center = doc.loyalty_redemption_cost_center
				loyalty_points_sum += doc.loyalty_points
				loyalty_amount_sum += doc.loyalty_amount

			for item in doc.get("items"):
				found = False
				for i in items:
					if (
						i.item_code == item.item_code
						and not i.serial_and_batch_bundle
						and not i.serial_no
						and not i.batch_no
						and i.uom == item.uom
						and i.net_rate == item.net_rate
						and i.warehouse == item.warehouse
					):
						found = True
						i.qty = i.qty + item.qty
						i.custom_nosquantity=i.custom_nosquantity+item.custom_nosquantity
						i.amount = i.amount + item.net_amount
						i.net_amount = i.amount
						i.base_amount = i.base_amount + item.base_net_amount
						i.base_net_amount = i.base_amount

				if not found:
					item.rate = item.net_rate
					item.amount = item.net_amount
					item.base_amount = item.base_net_amount
					item.price_list_rate = 0
					si_item = map_child_doc(item, invoice, {"doctype": "Sales Invoice Item"})
					if item.serial_and_batch_bundle:
						si_item.serial_and_batch_bundle = item.serial_and_batch_bundle
					items.append(si_item)

			for tax in doc.get("taxes"):
				found = False
				for t in taxes:
					if t.account_head == tax.account_head and t.cost_center == tax.cost_center:
						t.tax_amount = flt(t.tax_amount) + flt(tax.tax_amount_after_discount_amount)
						t.base_tax_amount = flt(t.base_tax_amount) + flt(
							tax.base_tax_amount_after_discount_amount
						)
						update_item_wise_tax_detail(t, tax)
						found = True
				if not found:
					tax.charge_type = "Actual"
					tax.idx = idx
					idx += 1
					tax.included_in_print_rate = 0
					tax.tax_amount = tax.tax_amount_after_discount_amount
					tax.base_tax_amount = tax.base_tax_amount_after_discount_amount
					tax.item_wise_tax_detail = tax.item_wise_tax_detail
					taxes.append(tax)

			for payment in doc.get("payments"):
				found = False
				for pay in payments:
					if pay.account == payment.account and pay.mode_of_payment == payment.mode_of_payment:
						pay.amount = flt(pay.amount) + flt(payment.amount)
						pay.base_amount = flt(pay.base_amount) + flt(payment.base_amount)
						found = True
				if not found:
					payments.append(payment)

			rounding_adjustment += doc.rounding_adjustment
			rounded_total += doc.rounded_total
			base_rounding_adjustment += doc.base_rounding_adjustment
			base_rounded_total += doc.base_rounded_total

		if loyalty_points_sum:
			invoice.redeem_loyalty_points = 1
			invoice.loyalty_points = loyalty_points_sum
			invoice.loyalty_amount = loyalty_amount_sum

		invoice.set("items", items)
		invoice.set("payments", payments)
		invoice.set("taxes", taxes)
		invoice.set("rounding_adjustment", rounding_adjustment)
		invoice.set("base_rounding_adjustment", base_rounding_adjustment)
		invoice.set("rounded_total", rounded_total)
		invoice.set("base_rounded_total", base_rounded_total)
		invoice.additional_discount_percentage = 0
		invoice.discount_amount = 0.0
		invoice.taxes_and_charges = None
		invoice.ignore_pricing_rule = 1
		invoice.customer = self.customer
		invoice.disable_rounded_total = cint(
			frappe.db.get_value("POS Profile", invoice.pos_profile, "disable_rounded_total")
		)
		accounting_dimensions = required_accounting_dimensions()
		dimension_values = frappe.db.get_value(
			"POS Profile", {"name": invoice.pos_profile}, accounting_dimensions, as_dict=1
		)
		for dimension in accounting_dimensions:
			dimension_value = dimension_values.get(dimension)

			if not dimension_value:
				frappe.throw(
					_("Please set Accounting Dimension {} in {}").format(
						frappe.bold(frappe.unscrub(dimension)),
						frappe.get_desk_link("POS Profile", invoice.pos_profile),
					)
				)

			invoice.set(dimension, dimension_value)

		if self.merge_invoices_based_on == "Customer Group":
			invoice.flags.ignore_pos_profile = True
			invoice.pos_profile = ""

		return invoice

