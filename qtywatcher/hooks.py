app_name = "qtywatcher"
app_title = "qtywatcher"
app_publisher = "mhmed rjb"
app_description = "in andusetry there is some items like(cheese) sell by Kg but this QTY is not fixed ,it is lose waight by dayes so we need another QTY to track stock "
app_email = "m222ragab@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/qtywatcher/css/qtywatcher.css"
# app_include_js = "/assets/qtywatcher/js/qtywatcher.js"
# include js, css files in header of web template
# web_include_css = "/assets/qtywatcher/css/qtywatcher.css"
# web_include_js = "/assets/qtywatcher/js/qtywatcher.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "qtywatcher/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Sales Invoice": ["public/js/common_invoices.js", "public/js/Sales_Invoice.js"],
    "Purchase Invoice": ["public/js/common_invoices.js", "public/js/Purchase_Invoice.js"],
    "Stock Entry": ["public/js/common_invoices.js", "public/js/Stock_Entry.js"],
    "Stock Reconciliation": ["public/js/common_invoices.js", "public/js/Stock_Reconciliation.js"]
};
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

app_include_js = [
    "/assets/qtywatcher/js/custom_pos_item_details.js"
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "qtywatcher.utils.jinja_methods",
# 	"filters": "qtywatcher.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "qtywatcher.install.before_install"
# after_install = "qtywatcher.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "qtywatcher.uninstall.before_uninstall"
# after_uninstall = "qtywatcher.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "qtywatcher.utils.before_app_install"
# after_app_install = "qtywatcher.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "qtywatcher.utils.before_app_uninstall"
# after_app_uninstall = "qtywatcher.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "qtywatcher.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes
override_doctype_class = {
	"Stock Ledger Entry": "qtywatcher.overrides.stock_ledger_entry.CustomStockLedgerEntry",
    "POS Invoice Merge Log": "qtywatcher.overrides.pos_invoice_merge_log.CustomPOSInvoiceMergeLog",
    }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Sales Invoice": {
        "validate": "qtywatcher.utility.validate_nosquantity"
    },
    "Purchase Invoice": {
        "validate": "qtywatcher.utility.validate_nosquantity"
    },
    "Stock Entry": {
        "validate": "qtywatcher.utility.validate_nosquantity"
    },
    "Stock Reconciliation": {
        "validate":"qtywatcher.utility.validate_nosquantity"
    },
    "POS Invoice": {
        "validate": "qtywatcher.utility.validate_nosquantity"
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"qtywatcher.tasks.all"
# 	],
# 	"daily": [
# 		"qtywatcher.tasks.daily"
# 	],
# 	"hourly": [
# 		"qtywatcher.tasks.hourly"
# 	],
# 	"weekly": [
# 		"qtywatcher.tasks.weekly"
# 	],
# 	"monthly": [
# 		"qtywatcher.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "qtywatcher.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "qtywatcher.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "qtywatcher.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["qtywatcher.utils.before_request"]
# after_request = ["qtywatcher.utils.after_request"]

# Job Events
# ----------
# before_job = ["qtywatcher.utils.before_job"]
# after_job = ["qtywatcher.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"qtywatcher.auth.validate"
# ]

#add all custom fields to item
# fixtures = ["Custom Field"]
