
from odoo import api, fields, models, _


class SaleConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    so_state = fields.Selection(
        [
            ('draft', 'RFQ'),
            ('sent', 'RFQ Sent'),
            ('to approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
        ],
        string="Default PO State",
        help="Created Purchase Order will be put to selected state.",
        default='draft',
        required=True,
    )
    so_draft_allow_convert_po = fields.Boolean(
        "Allow convert Quotation",
        default=True,
        help="If checked Quotation state will have `Convert to Purchase Order` button.",
    )
    so_sent_allow_convert_po = fields.Boolean(
        "Allow convert Quotation Sent",
        default=True,
        help="If checked Quotation Sent state will have `Convert to Purchase Order` button.",
    )
    so_sale_allow_convert_po = fields.Boolean(
        "Allow convert Sales Order",
        default=True,
        help="If checked Sales Order state will have `Convert to Purchase Order` button.",
    )

    def get_values(self):
        res = super(SaleConfiguration, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        so_state = params.get_param('so_convert_po.so_state')
        so_draft_allow_convert_po = params.get_param('so_convert_po.so_draft_allow_convert_po')
        so_sent_allow_convert_po = params.get_param('so_convert_po.so_sent_allow_convert_po')
        so_sale_allow_convert_po = params.get_param('so_convert_po.so_sale_allow_convert_po')
        res.update(
            so_state=so_state,
            so_draft_allow_convert_po=so_draft_allow_convert_po,
            so_sent_allow_convert_po=so_sent_allow_convert_po,
            so_sale_allow_convert_po=so_sale_allow_convert_po,
        )
        return res

    def set_values(self):
        super(SaleConfiguration, self).set_values()
        config = self.env['ir.config_parameter'].sudo().set_param
        config('so_convert_po.so_state', self.so_state)
        config('so_convert_po.so_draft_allow_convert_po', self.so_draft_allow_convert_po)
        config('so_convert_po.so_sent_allow_convert_po', self.so_sent_allow_convert_po)
        config('so_convert_po.so_sale_allow_convert_po', self.so_sale_allow_convert_po)
