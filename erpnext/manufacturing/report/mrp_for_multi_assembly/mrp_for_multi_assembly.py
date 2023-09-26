import frappe

def get_data(filters=None):
    if not filters:
        frappe.throw("Please select at least one filter option.")

    # Rest of the code that retrieves and processes the data
    # ...
    # Your code logic goes here
    # ...

    # Return the processed data
    return processed_data
