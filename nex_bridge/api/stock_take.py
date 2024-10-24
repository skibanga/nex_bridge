import frappe


@frappe.whitelist()
def get_user_warehouses_and_companies():
    # Ensure the user is authenticated
    user_email = frappe.session.user
    if not user_email or user_email == "Guest":
        frappe.response["message"] = "User must be logged in to access this resource."
        return

    warehouses = frappe.db.get_list("Warehouse", fields=["name"], limit=1000)

    if not warehouses:
        frappe.response["message"] = "No warehouses found."
        return

    companies = frappe.db.get_list("Company", fields=["name"], limit=1000)

    if not companies:
        frappe.response["message"] = "No companies found."
        return

    warehouse_names = [wh.get("name") for wh in warehouses]
    company_names = [comp.get("name") for comp in companies]

    frappe.response["message"] = {
        "warehouses": warehouse_names,
        "companies": company_names,
        "user_id": user_email,
    }
