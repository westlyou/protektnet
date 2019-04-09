# Copyright 2019, Grupo Censere
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _push_apply(self):
        # TDE CLEANME:
        # I am quite sure I already saw this code somewhere ... in routing ??
        Push = self.env['stock.location.path']
        for move in self:
            # if the move is already chained, there is no
            # need to check push rules
            if move.move_dest_ids:
                continue
            # if the move is a returned move, we don't want to check push
            # rules, as returning a returned move is the only decent way
            # to receive goods without triggering the push rules again
            # (which would duplicate chained operations)
            domain = [('location_from_id', '=', move.location_dest_id.id)]
            # priority goes to the route defined on the product
            # and product category
            routes = (move.product_id.route_ids |
                      move.product_id.categ_id.total_route_ids)
            rules = Push.search(domain + [('route_id', 'in', routes.ids)],
                                order='route_sequence, sequence', limit=1)
            if not rules:
                # TDE FIXME/ should those really be in a if / elif ??
                # then we search on the warehouse if a rule can apply
                if move.sale_line_id.route_id:
                    rules = Push.search(
                        domain +
                        [('route_id', 'in', move.sale_line_id.route_id.ids)],
                        order='route_sequence, sequence', limit=1)
                elif move.warehouse_id:
                    rules = Push.search(
                        domain +
                        [('route_id', 'in', move.warehouse_id.route_ids.ids)],
                        order='route_sequence, sequence', limit=1)
                elif move.picking_id.picking_type_id.warehouse_id:
                    rules = Push.search(
                        domain +
                        [('route_id', 'in', move.picking_id.picking_type_id.
                            warehouse_id.route_ids.ids)],
                        order='route_sequence, sequence', limit=1)

            # Make sure it is not returning the return
            if rules and (not move.origin_returned_move_id or
                          move.origin_returned_move_id.location_dest_id.id !=
                          rules.location_dest_id.id):
                rules._apply(move)
