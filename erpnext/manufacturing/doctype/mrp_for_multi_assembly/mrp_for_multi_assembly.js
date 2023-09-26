// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt


frappe.ui.form.on('MRP for Multi Assembly', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('MRP for Multi Assembly', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('MRP for Multi Assembly', {
	
	show_report: function(frm) {

        frm.clear_table("table");
        frm.refresh_field('table');

        if (frm.doc.sales_order && frm.doc.sales_order.length > 0 && frm.doc.production_plan && frm.doc.production_plan.length > 0) {
            frm.clear_table("sales_order");
            frm.refresh_field('sales_order');
        }


		frm.call({
			method: 'get_report',//function name defined in python
			doc: frm.doc, //current document
		});

	}

});



frappe.ui.form.on("MRP for Multi Assembly", {
    refresh: function(frm) {
        frm.fields_dict['sales_order'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ["Sales Order", "docstatus", '=', 1]
                ]
            };
        };
    }
});

frappe.ui.form.on("MRP for Multi Assembly", {
    refresh: function(frm) {
            frm.set_query("production_plan", function() { // Replace with the name of the link field
                return {
                    filters: [
                        ["Production Plan", "status", 'in', ["Submitted", "Material Requested", "In Process"]] // Replace with your actual filter criteria
                    ]
                };
            });
        }
    });



    // frappe.ui.form.on('MRP for Multi Assembly', {

    //     export_report(frm) {
    //         frappe.require("data_import_tools.bundle.js", () => {
    //             frm.data_exporter = new frappe.data_import.DataExporter(
    //                 'Child MRP for Multi Assembly', //frm.doc.reference_doctype,
    //                 "Insert New Records"// frm.doc.import_type"
    //             );
    //         });
    //     },
    
    // });
    

    frappe.ui.form.on('MRP for Multi Assembly', {
        export_report(frm) {
            frappe.run_serially([
                () => {
                    // Temporarily bypass permissions
                    frm.bypass_doctype_permissions = true;
                },
                () => {
                    // Your export logic here
                    frappe.require("data_import_tools.bundle.js", () => {
                        frm.data_exporter = new frappe.data_import.DataExporter(
                            'Child MRP for Multi Assembly',
                            "Insert New Records"
                        );
                    });
                },
                () => {
                    // Reset bypass permissions flag after export
                    frm.bypass_doctype_permissions = false;
                }
            ]);
        },
    });
    








// frappe.ui.form.on('MRP for Multi Assembly', {
//     refresh: function(frm) {
//         frappe.call({
//             method: "erpnext.manufacturing.doctype.mrp_for_multi_assembly.mrp_for_multi_assembly.get_sales_order_list",   // "erpnext.manufacturing.doctype.MRP_for_Multi_Assembly.MRP_for_Multi_Assembly.get_sales_order_list"
//             args: {
//                 production_plan: frm.doc.production_plan
//             },
//             doc: frm.doc, // Pass the form data /home/erp/bench01-test/apps/erpnext/erpnext/manufacturing/doctype/mrp_for_multi_assembly/mrp_for_multi_assembly.js
//             callback: function(response) {
//                 if (response.message) {
//                     console.log("Response:", response.message);
//                 } else {
//                     console.log("Error:", response.exc);
//                 }
//             }
//         });
//     }
// });





// frappe.ui.form.on('MRP for Multi Assembly', {
//     production_plan: function(frm) {

//         frappe.call({ 
//             method: 'frappe.get_list',
//             args: {
//                 doctype: 'Production Plan Sales Order',
//                 filters: {'parent': frm.doc.production_plan , "docstatus": 1},
//                 fieldname: 'sales_order'
//             },
//             callback: function(response) {
//                 var options = (response.message);
//                 frappe.msgprint(JSON.stringify(options));
//             }
//         });
//     } 
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     production_plan: function(frm) {

//         frappe.call({ 
//             method: 'custom_get_all',
//             args: {
//                 doctype: 'Production Plan Sales Order',
//                 filters: {'parent': frm.doc.production_plan , "docstatus": 1},
//                 fieldname: 'sales_order'
//             },
//             callback: function(response) {
//                 var options = (response.message);
//                 frappe.msgprint(JSON.stringify(options));
//             }
//         });
//     }
// });



// frappe.ui.form.on('MRP for Multi Assembly', {
	
// 	production_plan: function(frm) {


// 		frm.call({
// 			method: 'get_sales_order_list',//function name defined in python
// 			doc: frm.doc, //current document
// 		});

// 	}

// });

// frappe.ui.form.on('MRP for Multi Assembly', {
	
// 	production_plan: function(frm) {
// 		var sales_order_list = frm.doc.sales_order_list
//         frm.fields_dict['sales_order'].get_query = function(doc, cdt, cdn) {
			
//             return {
//                 filters: [
//                     ["Sales Order", "docstatus", '=', 1]
//                 ]
//             };
//         };
//     }

// });



// frappe.ui.form.on('MRP for Multi Assembly', {
//     production_plan: function(frm) {

//         frappe.call({ 
//             method: 'frappe.client.get_all',
//             args: {
//                 doctype: 'Production Plan Sales Order',
//                 filters: {'parent': frm.doc.production_plan , "docstatus": 1},
//                 fieldname: 'sales_order'
//             },
//             callback: function(response) {
//                 var options = (response.message.sales_order);
// 				frappe.msgprint(str(options))
 
//             }
//         });
//     }
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     production_plan: function(frm) {
//         // frappe.msgprint("Hello World"); // You can print a string directly
//         frappe.call({
//             method: 'frappe.client.get_value',
//             args: {
//                 doctype: 'Production Plan Sales Order',
//                 filters: {"parent": frm.production_plan, "docstatus": 1},
//                 fieldname: 'sales_order'
//             },
//             callback: function(response) {
//                 var options = eval(response.message.list_of_items);
// 				frappe.msgprint(str(options))
//                 // frm.set_df_property('address', 'options', options);
//             }
//         });
//     }
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     refresh: function(frm) {
// 		frappe.call({
// 			method: "get_sales_order_list",
// 			doc: frm.doc, 
// 			callback: function(response) {

// 				if (response.message) {
// 					console.log("Response:", response.message);
// 				} else {
// 					console.log("Error:", response.exc);
// 				}
// 			}
// 		});
//     }
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     production_plan: function(frm) {
//         frappe.call({
//             method: "get_sales_order_list",
//             args: {
//                 doc: frm.doc  // Pass frm.doc as an argument
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     console.log("Response:", response.message);
//                 } else {
//                     console.log("Error:", response.exc);
//                 }
//             }
//         });
//     }
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     refresh: function(frm) {
//         frappe.call({
//             method: "get_sales_order_list",
//             doc: frm.doc,
//             callback: function(response) {
//                 if (!response.exc) {
//                     // Handle the response here
//                     if (response.message) {
//                         console.log("Sales Orders:", response.message);
//                     } else {
//                         console.log("No Sales Orders found.");
//                     }
//                 } else {
//                     console.error("Error:", response.exc);
//                 }
//             }
//         });
//     }
// });


// frappe.ui.form.on('MRP for Multi Assembly', {
//     refresh: function(frm) {
//         frappe.call({
//             method: 'get_sales_order_list', // Change this path to match your app and module structure  "erpnext.manufacturing.doctype.MRP_for_Multi_Assembly.MRP_for_Multi_Assembly.get_sales_order_list"
//             // args: {
//             //     doc: frm.doc.production_plan
//             // },
//             callback: function(response) {
//                 if (!response.exc) {
//                     // Handle the response here
//                     if (response.message) {
//                         console.log("Sales Orders:", response.message);
//                     } else {
//                         console.log("No Sales Orders found.");
//                     }
//                 } else {
//                     console.error("Error:", response.exc);
//                 }
//             }
//         });
//     }
// });

// frappe.ui.form.on('MRP for Multi Assembly', {
//     refresh: function(frm) {
//         frappe.call({
//             method: "frappe.client.get_sales_order_list", // Corrected method name
//             args: {
//                 production_plan: frm.doc.production_plan // Pass production_plan as an argument
//             },
//             callback: function(response) {
//                 if (response.message) {
//                     console.log("Response:", response.message);
//                 } else {
//                     console.log("Error:", response.exc);
//                 }
//             }
//         });
//     }
// });

// method: 'get_report',//function name defined in python
// 			doc: frm.doc,
