from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    platform_id = fields.Many2one('platform.sale', 'Platform')

    def find_parent_categ(self, idcateg, platform, disc):
        # print(idcateg.name)
        finddiscout = self.env['platform.sale.disc'].search([('platform_id', '=', platform.id),
                                                             ('categ_id', '=', idcateg.id)])
        # print(finddiscout)
        # print("==============")
        if finddiscout:
            discnom = finddiscout[0].disc
            disc.append(discnom)
            # print(disc)
            return disc
        else:
            if idcateg.parent_id:
                self.find_parent_categ(idcateg.parent_id, platform, disc)
            else:
                return disc

    @api.onchange('platform_id')
    def onchange_platform(self):
        if self.platform_id:
            if self.order_line:
                for line in self.order_line:
                    if self.platform_id.type == 'product':
                        finddiscout = self.env['platform.sale.disc'].search([('platform_id', '=', self.platform_id.id),
                                                                             ('product_id', '=', line.product_id.id)])
                        if finddiscout:
                            line.discount = finddiscout[0].disc
                        else:

                            line.discount = 0
                    else:
                        disc=[]
                        self.find_parent_categ(line.product_id.categ_id, self.platform_id,disc)
                        if disc:

                            line.discount = disc[0]
                        else:
                            line.discount = 0

        else:
            if self.order_line:
                for line in self.order_line:
                    line.discount = 0


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def find_parent_categ(self, idcateg, platform, disc):
        # print(idcateg.name)
        finddiscout = self.env['platform.sale.disc'].search([('platform_id', '=', platform.id),
                                                             ('categ_id', '=', idcateg.id)])
        # print(finddiscout)
        # print("==============")
        if finddiscout:
            discnom = finddiscout[0].disc
            disc.append(discnom)
            # print(disc)
            return disc
        else:
            if idcateg.parent_id:
                self.find_parent_categ(idcateg.parent_id, platform, disc)
            else:
                return disc

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            if self.order_id.platform_id:
                if self.order_id.platform_id.type == 'product':
                    finddiscout = self.env['platform.sale.disc'].search(
                        [('platform_id', '=', self.order_id.platform_id.id),
                         ('product_id', '=', self.product_id.id)])

                    if finddiscout:
                        self.discount = finddiscout[0].disc
                    else:

                        self.discount = 0
                else:
                    disc=[]
                    self.find_parent_categ(self.product_id.categ_id, self.order_id.platform_id,disc)

                    if disc:

                        self.discount = disc[0]
                    else:
                        self.discount=0
        return res
