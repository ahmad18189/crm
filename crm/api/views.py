import frappe
from pypika import Criterion


@frappe.whitelist()
def get_views(doctype=None):
	# Prebuilt CRM SPA (Pinia store setup) sometimes posts `doctype` as a dict.
	if not isinstance(doctype, str):
		doctype = ""

	View = frappe.qb.DocType("CRM View Settings")
	query = (
		frappe.qb.from_(View)
		.select("*")
		.where(Criterion.any([View.user == "", View.user == frappe.session.user]))
	)
	if doctype:
		query = query.where(View.dt == doctype)
	views = query.run(as_dict=True)
	return views
