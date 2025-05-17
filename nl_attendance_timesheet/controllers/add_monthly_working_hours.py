import frappe
from frappe import _

@frappe.whitelist()
def add_monthly_working_hours(payroll_entry):
    salary_slips = frappe.db.get_all(
        "Salary Slip", filters={"payroll_entry": payroll_entry, "docstatus": 0}
    )

    for entry in salary_slips:
        salary_slip = frappe.get_doc("Salary Slip", entry.get("name"))

        payment_days = salary_slip.payment_days or 0
        monthly_hours = float(payment_days) * 8

        salary_slip.monthly_working_hours = monthly_hours

        # Optional: Log to console (visible in logs for debugging)
        frappe.logger().info(
            f"Updated Salary Slip: {salary_slip.name}, Monthly Hours: {monthly_hours}"
        )

        salary_slip.save(ignore_permissions=True)

    frappe.db.commit()
    return _("Monthly working hours updated successfully.")