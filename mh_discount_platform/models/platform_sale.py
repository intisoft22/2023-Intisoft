from odoo import fields, models, api


class PlatformSale(models.Model):
    _name = 'platform.sale'
    _description = 'Platform for Sale'

    name = fields.Char(required=True)
    disc_ids = fields.One2many('platform.sale.disc','platform_id', 'Discount by Product')
    disc_categ_ids = fields.One2many('platform.sale.disc','platform_id', 'Discount by Category')
    type = fields.Selection([('category','Product Category'),('product', 'Product')],' Type by',required=True)

    @api.onchange('type')
    def onchange_type(self):
        self.disc_ids=False
        self.disc_categ_ids=False

class PlatformSaleDiskon(models.Model):
    _name = 'platform.sale.disc'
    _description = 'Platform for Sale'

    platform_id = fields.Many2one('platform.sale', 'Platform')
    categ_id = fields.Many2one('product.category', 'Category')
    product_id = fields.Many2one('product.product', 'Product')
    disc = fields.Float('Discount')
