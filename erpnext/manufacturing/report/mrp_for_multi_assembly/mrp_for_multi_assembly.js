frappe.query_reports["MRP for Multi Assembly"] = {
    "filters": [
        {
            label: __("Sales Orders"),
            fieldname: "sales_order",
            fieldtype: "MultiSelectList",
            reqd: 1, // Add this line to make the selection mandatory
            get_data: function(txt) {
                return frappe.db.get_link_options('Sales Order', txt);
            }
        },
        {
            label: __("Production Plann"),
            fieldname: "production_plan",
            fieldtype: "MultiSelectList",
            reqd: 1, // Add this line to make the selection mandatory
            get_data: function(txt) {
                return frappe.db.get_link_options('Production Plan', txt);
            }
        }
    ]
};
