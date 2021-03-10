from odoo import models, fields

# This piece of code was shared by @filoquin at github:
# https://github.com/filoquin/filoquin.github.io/blob/main/deliveryinovice.md

class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_ids = fields.Many2many(
        'stock.picking',
        string='Pickings',
        compute='compute_picking_ids',
        search="search_picking_ids"
    )

    def compute_picking_ids(self):
        for move in self:
            sale_order_ids = self.env['sale.order'].search(
                [('invoice_ids', '=', move.id)])
            move.picking_ids = [(6, 0, sale_order_ids.picking_ids.ids)]

    def search_picking_ids(self, operator, value):
        invoice_ids = self.env['sale.order'].search(['picking_ids', operator, value]).mapped('invoice_ids')
        return [('id', 'in', invoice_ids.ids)]