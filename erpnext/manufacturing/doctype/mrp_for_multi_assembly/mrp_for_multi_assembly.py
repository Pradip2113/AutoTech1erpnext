# Copyright (c) 2023, Vivek.kumbhar@erpdata.in 
# For license information, please see license.txt


# -----------------------------------------

# ******************************* if any permission error comes *************************************8

# there is change in standerd doctype

# /home/erp/bench01-test/apps/frappe/frappe/model/db_query.py

# following method only change
# 	def execute(
# 		self,
# 		fields=None,
# 		filters=None,
# 		or_filters=None,
# 		docstatus=None,
# 		group_by=None,
# 		order_by=DefaultOrderBy,
# 		limit_start=False,
# 		limit_page_length=None,
# 		as_list=False,
# 		with_childnames=False,
# 		debug=False,
# 		ignore_permissions=False,
# 		user=None,
# 		with_comment_count=False,
# 		join="left join",
# 		distinct=False,
# 		start=None,
# 		page_length=None,
# 		limit=None,
# 		ignore_ifnull=False,
# 		save_user_settings=False,
# 		save_user_settings_fields=False,
# 		update=None,
# 		add_total_row=None,
# 		user_settings=None,
# 		reference_doctype=None,
# 		run=True,
# 		strict=True,
# 		pluck=None,
# 		ignore_ddl=False,
# 		*,
# 		parent_doctype=None,
# 	) -> list:

# 		if (
# 			not ignore_permissions
# 			and not frappe.has_permission(self.doctype, "select", user=user, parent_doctype=parent_doctype)
# 			and not frappe.has_permission(self.doctype, "read", user=user, parent_doctype=parent_doctype)
# 		):	

			
# 			if self.doctype =='Child MRP for Multi Assembly':
# 				pass
# 			else:
# 				frappe.flags.error_message = _("Insufficient Permission for {0}").format(
# 					frappe.bold(self.doctype)
# 				)
# 				raise frappe.PermissionError(self.doctype)

# 		# filters and fields swappable
# 		# its hard to remember what comes first
# 		if isinstance(fields, dict) or (
# 			fields and isinstance(fields, list) and isinstance(fields[0], list)
# 		):
# 			# if fields is given as dict/list of list, its probably filters
# 			filters, fields = fields, filters

# 		elif fields and isinstance(filters, list) and len(filters) > 1 and isinstance(filters[0], str):
# 			# if `filters` is a list of strings, its probably fields
# 			filters, fields = fields, filters

# 		if fields:
# 			self.fields = fields
# 		else:
# 			self.fields = [f"`tab{self.doctype}`.`{pluck or 'name'}`"]

# 		if start:
# 			limit_start = start
# 		if page_length:
# 			limit_page_length = page_length
# 		if limit:
# 			limit_page_length = limit

# 		self.filters = filters or []
# 		self.or_filters = or_filters or []
# 		self.docstatus = docstatus or []
# 		self.group_by = group_by
# 		self.order_by = order_by
# 		self.limit_start = cint(limit_start)
# 		self.limit_page_length = cint(limit_page_length) if limit_page_length else None
# 		self.with_childnames = with_childnames
# 		self.debug = debug
# 		self.join = join
# 		self.distinct = distinct
# 		self.as_list = as_list
# 		self.ignore_ifnull = ignore_ifnull
# 		self.flags.ignore_permissions = ignore_permissions
# 		self.user = user or frappe.session.user
# 		self.update = update
# 		self.user_settings_fields = copy.deepcopy(self.fields)
# 		self.run = run
# 		self.strict = strict
# 		self.ignore_ddl = ignore_ddl

# 		# for contextual user permission check
# 		# to determine which user permission is applicable on link field of specific doctype
# 		self.reference_doctype = reference_doctype or self.doctype

# 		if user_settings:
# 			self.user_settings = json.loads(user_settings)

# 		if is_virtual_doctype(self.doctype):
# 			from frappe.model.base_document import get_controller

# 			controller = get_controller(self.doctype)
# 			self.parse_args()
# 			kwargs = {
# 				"as_list": as_list,
# 				"with_comment_count": with_comment_count,
# 				"save_user_settings": save_user_settings,
# 				"save_user_settings_fields": save_user_settings_fields,
# 				"pluck": pluck,
# 				"parent_doctype": parent_doctype,
# 			} | self.__dict__
# 			return controller.get_list(kwargs)

# 		self.columns = self.get_table_columns()

# 		# no table & ignore_ddl, return
# 		if not self.columns:
# 			return []

# 		result = self.build_and_run()

# 		if with_comment_count and not as_list and self.doctype:
# 			self.add_comment_count(result)

# 		if save_user_settings:
# 			self.save_user_settings_fields = save_user_settings_fields
# 			self.update_user_settings()

# 		if pluck:
# 			return [d[pluck] for d in result]

# 		return result
# -----------------------------------------







import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
# from frappe.utils.xlsxutils import make_xlsx
# from frappe.utils.csvutils import get_csv

class MRPforMultiAssembly(Document):
	@frappe.whitelist()
	def get_report(self):
		if self.sales_order and (not self.production_plan):
			
			sales_order_data_list = [d.sales_order for d in self.sales_order]
			sales_order_parent_list = set()
			
			sales_order_items = doc=frappe.get_all('Sales Order Item',filters={"parent": ['in',sales_order_data_list], "docstatus": 1},fields=['item_code','qty'])
			total_items = {}
			for item in sales_order_items:
				item_code = item['item_code']
				qty = item['qty']
				if item_code in total_items:
					total_items[item_code]+= qty
				else:
					total_items[item_code] = qty 

			items_with_qty = [{'item_code': item_code, 'qty': qty} for item_code, qty in total_items.items()]
			
			for sys in items_with_qty:


				total_material_to_request=0
				total_materialrequestedqty =0
				total_materialorderedqty =0
				total_materialreceivedqty=0
				totalalloted_qty =0


				for xox in sales_order_data_list:
					material_request_plan_item =frappe.get_all("Material Request Item",filters={"sales_order": xox ,"docstatus": 1, 'item_code' : sys['item_code']},fields=['qty'])
					if 	material_request_plan_item:
						for sp in material_request_plan_item:
							total_material_to_request += sp.qty

					material_request_item = frappe.get_all("Material Request Item",filters={"sales_order": xox ,"docstatus": 1, 'item_code' : sys['item_code']},fields=['qty','parent'])
					if 	material_request_item:
						for sk in material_request_item:
							total_materialrequestedqty += sk.qty

							purchase_order_item = frappe.get_all("Purchase Order Item",filters={"material_request": sk.parent ,"docstatus": 1, 'item_code' : sys['item_code']},fields=['qty'])
							if 	purchase_order_item:
								for pk in purchase_order_item:
									total_materialorderedqty += pk.qty
									# frappe.msgprint("mr"+str(sk.parent))


							purchase_receipt_item = frappe.get_all("Purchase Receipt Item",filters={"material_request": sk.parent ,"docstatus": 1, 'item_code' : sys['item_code']},fields=['qty','parent'])
							if 	purchase_receipt_item:
								for rc in purchase_receipt_item:
									total_materialreceivedqty += rc.qty

									get_stock_entry_child_table = frappe.get_all("Stock Entry Detail",filters={"reference_purchase_receipt": rc.parent ,"docstatus": 1,'item_code': sys['item_code'],"t_warehouse": "Virtual Allocation for Trading - APL"},fields=['qty'] )
									if get_stock_entry_child_table:
										for gc in get_stock_entry_child_table:
											totalalloted_qty += gc.qty



					# purchase_order_item_po = frappe.get_all("Purchase Order Item",filters={"sales_order": xox ,"docstatus": 1, 'item_code' : sys['item_code'],"material_request":""},fields=['qty','parent'])
					# if 	purchase_order_item_po:
					# 	for pk_po in purchase_order_item_po:
					# 		total_materialorderedqty += pk_po.qty
					# 		# frappe.msgprint("po"+str(pk.qty))

					# 	purchase_receipt_item_po = frappe.get_all("Purchase Receipt Item",filters={"purchase_order": pk_po.parent ,"docstatus": 1, 'item_code' : sys['item_code']},fields=['qty'])
					# 	if 	purchase_receipt_item_po:
					# 		for rc_po in purchase_receipt_item_po:
					# 			total_materialreceivedqty += rc_po.qty

				rbomqty = sys['qty']
				aqty = (frappe.get_all('Bin', filters={'item_code': sys['item_code'], 'warehouse': 'Stores - APL'}, fields=['SUM(actual_qty) as qty']))[0]['qty']
				self.append("table", {
					"itemcode": sys['item_code'],
					"itemname": frappe.get_value("Item",sys['item_code'],'item_name'),
					"requiredbomqty" :rbomqty if  rbomqty > 0 else 0,
					"actualqty": aqty if  aqty > 0 else 0,
					"alloted_qty":totalalloted_qty if totalalloted_qty > 0 else  0,
					"virtual_warehouse": get_link_to_form('Warehouse',"Virtual Allocation for Trading - APL") , #"Virtual Allocation for Trading - APL", 
					"material_to_request" : ((rbomqty -aqty)-total_materialrequestedqty) if  ((rbomqty -aqty)-total_materialrequestedqty) > 0 else 0,
					"materialrequestedqty" : total_materialrequestedqty if  total_materialrequestedqty > 0 else 0,
					"materialorderedqty" : total_materialorderedqty if  total_materialorderedqty > 0 else 0,
					"materialreceivedqty" : total_materialreceivedqty if  total_materialreceivedqty > 0 else 0 ,
					"material_ordered_but_pending_to_receive_qty": (total_materialorderedqty - total_materialreceivedqty) if  (total_materialorderedqty - total_materialreceivedqty) > 0 else 0 ,
					"material_to_order" :  ((rbomqty -aqty) - total_materialorderedqty )  if  ((rbomqty -aqty) - total_materialorderedqty ) > 0 else 0# total_material_to_request - total_materialorderedqty if total_material_to_request else total_material_to_request
				})
				
			

		if self.production_plan and (not self.sales_order) :
			

			doc=frappe.get_all('Production Plan Sales Order',filters={"parent": self.production_plan, "docstatus": 1},fields=['sales_order'])
			for d in doc:
				self.append('sales_order', {
					'sales_order': d.sales_order
				})

			all_bom_in_production_plane = frappe.get_all('Production Plan Item',filters={"parent": self.production_plan, "docstatus": 1},fields=['bom_no'])
			list_bom_in_production_plane = sorted(set(item['bom_no'] for item in all_bom_in_production_plane))
			all_bom_exploded_items_filter =  {'parent': ['in',list_bom_in_production_plane] ,"docstatus": 1}

			
			self.report_when_production_plan(all_bom_exploded_items_filter)

		if (not self.production_plan) and (not self.sales_order):
			
			
			all_bom_exploded_items_filter = { "docstatus": 1}

			self.report_when_production_plan(all_bom_exploded_items_filter)

	@frappe.whitelist()
	def report_when_production_plan(self,all_bom_exploded_items_filter):
		variable_for_names_in_sales_order_parent_list=None
		all_bom_exploded_items =frappe.get_all('BOM Explosion Item',filters= all_bom_exploded_items_filter,fields=['item_code','parent'])  
		total_items = {}
		for item in all_bom_exploded_items:
			item_code = item['item_code']
			parent = item['parent']
			if item_code in total_items:
				total_items[item_code]['parent'].append(parent)
			else:
				total_items[item_code] = {'parent': [parent] }

		bom_exploded_items = [{'item_code': item_code, 'parent': values['parent']} for item_code, values in total_items.items()]
		bom_exploded_items_sorted = sorted(bom_exploded_items, key=lambda x: x['item_code'])



		for row in bom_exploded_items_sorted:

			xoxoxo = frappe.get_all("Production Plan Item", filters={"bom_no": ["in", row['parent']]}, fields=['parent'])
			filtered_plans =[]
			for plan in xoxoxo:
				filtered_plans.append(plan.parent)
			gogogog = frappe.get_all("Production Plan", filters={"name": ["in", filtered_plans],'status' : ["in", ["Submitted", "Material Requested", "In Process"]]}, fields=['name'])

			variable_for_names_in_gogogog = ','.join(set(item['name'] for item in gogogog))
			variable_for_names_of_production_plane = variable_for_names_in_sales_order_parent_list if variable_for_names_in_sales_order_parent_list else variable_for_names_in_gogogog
			production_plane_names = self.production_plan if self.production_plan else variable_for_names_of_production_plane

			unique_valuex = set(frappe.get_value("Production Plan", x.parent, "for_warehouse") for x in xoxoxo if frappe.get_value("Production Plan", x.parent, "for_warehouse") is not None)
			if production_plane_names:
				stock_qty=0
				work_order_list=[]
				total_alloted_qty=0
				total_material_to_request=0
				total_materialrequestedqty =0
				total_materialorderedqty =0
				total_materialreceivedqty=0
				production_plane_list = production_plane_names.split(',')
				for pj in  production_plane_list:

					bom_for_each_pp = frappe.get_all("Production Plan Item", filters={"parent": pj}, fields=['bom_no','planned_qty'] )
					for vd in bom_for_each_pp:
						items_req_qty = frappe.get_all("BOM Explosion Item", filters={"parent": vd.bom_no , 'item_code': row['item_code']  }, fields=['stock_qty'] )
						for vk in items_req_qty:
							stock_qty += round((vk.stock_qty * vd.planned_qty),2)

					work_order_doc_list = frappe.get_all("Work Order", filters={"production_plan": pj}, fields=['source_warehouse','name'] )
					unique_warehouses = set()
					for am in work_order_doc_list:
						item_work_order_made_ahe_ka_nahi = frappe.get_all("Work Order Item", filters={"parent": am.name ,"item_code" : row['item_code']}, fields=['source_warehouse','name'] )
						if item_work_order_made_ahe_ka_nahi:

							if am.source_warehouse:
								unique_warehouses.add(am.source_warehouse)
								stock_entry_doctype=frappe.get_all("Stock Entry",filters={"work_order": am.name ,"docstatus": 1},fields=['name'])
								for jp in stock_entry_doctype:
									get_stock_entry_child_table = frappe.get_all("Stock Entry Detail",filters={"parent": jp.name ,"docstatus": 1,'t_warehouse': am.source_warehouse ,'item_code': row['item_code']},fields=['qty'] )
									if get_stock_entry_child_table:
										for gc in get_stock_entry_child_table:
											total_alloted_qty += gc.qty

								
					work_order_list.extend(list(unique_warehouses))

					material_request_plan_item =frappe.get_all("Material Request Plan Item",filters={"parent": pj ,"docstatus": 1, 'item_code' : row['item_code']},fields=['quantity'])
					if 	material_request_plan_item:
						for sp in material_request_plan_item:
							total_material_to_request += sp.quantity

					material_request_item = frappe.get_all("Material Request Item",filters={"production_plan": pj ,"docstatus": 1, 'item_code' : row['item_code']},fields=['qty','parent'])
					if 	material_request_item:
						for sk in material_request_item:
							total_materialrequestedqty += sk.qty

							purchase_order_item = frappe.get_all("Purchase Order Item",filters={"material_request": sk.parent ,"docstatus": 1, 'item_code' : row['item_code']},fields=['qty'])
							if 	purchase_order_item:
								for pk in purchase_order_item:
									total_materialorderedqty += pk.qty


							purchase_receipt_item = frappe.get_all("Purchase Receipt Item",filters={"material_request": sk.parent ,"docstatus": 1, 'item_code' : row['item_code']},fields=['qty'])
							if 	purchase_receipt_item:
								for rc in purchase_receipt_item:
									total_materialreceivedqty += rc.qty


						
                    
				self.append("table", {
					"itemcode": row['item_code'],
					"itemname": frappe.get_value("Item",row['item_code'],'item_name'),
					"requiredbomqty" : stock_qty,
					"actualqty": (frappe.get_all('Bin', filters={'item_code': row['item_code'], 'warehouse': 'Stores - APL'}, fields=['SUM(actual_qty) as qty']))[0]['qty'],
					"productionplan": production_plane_names,
					"prodplanwarehouse":  frappe.get_value("Production Plan", self.production_plan, "for_warehouse") if self.production_plan else   ", ".join(f"'{item}'" for item in unique_valuex),
					"virtual_warehouse": ', '.join(work_order_list),
					"alloted_qty": total_alloted_qty,
					"material_to_request" : total_material_to_request -total_materialrequestedqty,
					"materialrequestedqty" : total_materialrequestedqty,
					"materialorderedqty" : total_materialorderedqty,
					"materialreceivedqty" : total_materialreceivedqty ,
					"material_ordered_but_pending_to_receive_qty": total_materialorderedqty - total_materialreceivedqty ,
					"material_to_order" : total_material_to_request - total_materialorderedqty
				})

		self.save()


	# @frappe.whitelist()
	# def export_report(self):
	# 	data = frappe.get_all('Child MRP for Multi Assembly', filters={'parent': docname})
	# 	headers = ["Sales Order", "Production Plan", ...]  # Add actual field names
	# 	rows = [[row.get('sales_order'), row.get('production_plan'), ...] for row in data]

	# 	# Create the Excel file
	# 	xlsx_file = make_xlsx({docname: {'data': rows, 'sheet_name': 'Sheet 1', 'doctype': doctype}}, "exported_data.xlsx")

	# 	return xlsx_file
	

	# @frappe.whitelist()
	# def export_report(parent_name):
	# 	# Fetch the data for the child table
	# 	data = frappe.get_all("Child MRP for Multi Assembly", filters={"parent": "MRP for Multi Assembly"},
	# 						fields=["productionplan", "prodplanwarehouse", "itemname"])  # Replace with your field names

	# 	# Convert the data to a CSV string
	# 	csv_data = get_csv(data)

	# 	return csv_data
