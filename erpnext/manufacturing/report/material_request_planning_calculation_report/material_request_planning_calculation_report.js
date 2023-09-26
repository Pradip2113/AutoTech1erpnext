frappe.query_reports["Material Request Planning Calculation Report"] = {
    "filters": [
        
        {
            label: __("Sales Orders"),
            fieldname: "sales_order",
            fieldtype: "MultiSelectList",
            get_data: function(txt) {
                return frappe.db.get_link_options('Sales Order', txt);
            }
        },  
        
    ]
};