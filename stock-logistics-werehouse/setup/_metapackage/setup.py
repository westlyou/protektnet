import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-stock-logistics-warehouse",
    description="Meta package for oca-stock-logistics-warehouse Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-account_move_line_product',
        'odoo11-addon-account_move_line_stock_info',
        'odoo11-addon-packaging_uom',
        'odoo11-addon-procurement_auto_create_group',
        'odoo11-addon-stock_account_internal_move',
        'odoo11-addon-stock_available',
        'odoo11-addon-stock_available_global',
        'odoo11-addon-stock_available_unreserved',
        'odoo11-addon-stock_cycle_count',
        'odoo11-addon-stock_demand_estimate',
        'odoo11-addon-stock_inventory_chatter',
        'odoo11-addon-stock_inventory_discrepancy',
        'odoo11-addon-stock_inventory_exclude_sublocation',
        'odoo11-addon-stock_inventory_lockdown',
        'odoo11-addon-stock_inventory_preparation_filter',
        'odoo11-addon-stock_inventory_verification_request',
        'odoo11-addon-stock_mts_mto_rule',
        'odoo11-addon-stock_orderpoint_generator',
        'odoo11-addon-stock_orderpoint_manual_procurement',
        'odoo11-addon-stock_orderpoint_manual_procurement_uom',
        'odoo11-addon-stock_orderpoint_move_link',
        'odoo11-addon-stock_orderpoint_purchase_link',
        'odoo11-addon-stock_orderpoint_uom',
        'odoo11-addon-stock_picking_procure_method',
        'odoo11-addon-stock_production_lot_expiry_state',
        'odoo11-addon-stock_putaway_method',
        'odoo11-addon-stock_putaway_product',
        'odoo11-addon-stock_putaway_same_location',
        'odoo11-addon-stock_quant_manual_assign',
        'odoo11-addon-stock_removal_location_by_priority',
        'odoo11-addon-stock_request',
        'odoo11-addon-stock_request_analytic',
        'odoo11-addon-stock_request_kanban',
        'odoo11-addon-stock_request_purchase',
        'odoo11-addon-stock_warehouse_calendar',
        'odoo11-addon-stock_warehouse_orderpoint_stock_info',
        'odoo11-addon-stock_warehouse_orderpoint_stock_info_unreserved',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
