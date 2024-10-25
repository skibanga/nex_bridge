import frappe


@frappe.whitelist()
def get_warehouses_grouped_by_company():
    # Ensure the user is authenticated
    user_email = frappe.session.user
    if not user_email or user_email == "Guest":
        frappe.response["message"] = "User must be logged in to access this resource."
        return

    warehouses = frappe.db.get_list("Warehouse", fields=["name", "company"], limit=1000)

    if not warehouses:
        frappe.response["message"] = "No warehouses found."
        return

    companies = frappe.db.get_list("Company", fields=["name"], limit=1000)

    if not companies:
        frappe.response["message"] = "No companies found."
        return

    company_warehouse_map = {}
    for wh in warehouses:
        company = wh.get("company")
        warehouse_name = wh.get("name")
        if company not in company_warehouse_map:
            company_warehouse_map[company] = []
        company_warehouse_map[company].append(warehouse_name)

    frappe.response["message"] = {
        "warehouses_by_company": company_warehouse_map,
        "companies": [comp.get("name") for comp in companies],
    }


@frappe.whitelist()
def get_user_assigned_items():
    user_email = frappe.session.user
    if not user_email or user_email == "Guest":
        frappe.response["message"] = "User must be logged in to access this resource."
        return

    stock_taker_records = frappe.db.get_list(
        "CSF TZ Stock Taker",
        filters={"stock_taker": user_email},
        fields=["name", "stock_taker"],
        limit=1000,
    )

    if not stock_taker_records:
        frappe.response["message"] = "No assigned items found for this user."
        return

    assigned_items = []
    for record in stock_taker_records:
        items = frappe.get_all(
            "CSF TZ Stock Taker Item",
            filters={"parent": record["name"]},
            fields=["name", "item"],
        )
        assigned_items.extend(items)

    frappe.response["message"] = {"assigned_items": assigned_items}
