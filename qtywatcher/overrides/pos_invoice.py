#make a ovveride on pos_invoice.py
import frappe
from erpnext.accounts.doctype.pos_invoice.pos_invoice import POSInvoice
from qtywatcher.utility import validate_nosquantity
class CustomPOSInvoice(POSInvoice):
    
    def validate(self):
        super().validate()
        validate_nosquantity(self)


            