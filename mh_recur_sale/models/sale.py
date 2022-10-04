from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    recur = fields.Boolean('Recur', copy=True)
    period_recur = fields.Selection([('harian', 'Harian'), ('mingguan', 'Mingguan'),  ('bulanan', 'Bulanan'),
                                     ('tahunan', 'Tahunan')], copy=True,)
    next_date = fields.Date('Next Date Purchase Order')



    def button_confirm(self):
        res = super(SaleOrder, self).button_confirm()
        # self.copy()
        if self.recur:
            if self.period_recur == 'harian':

                self.next_date = self.date_order+ relativedelta(days=1)
            elif self.period_recur == 'mingguan':

                self.next_date = self.date_order+ relativedelta(days=7)
            elif self.period_recur == 'bulanan':

                self.next_date = self.date_order+ relativedelta(months=1)
            elif self.period_recur == 'tahunan':

                self.next_date = self.date_order+ relativedelta(years=1)
        return


    @api.model
    def _create_sale_recur(self):
        today=date.today()
        # print(today)
        po_ids = self.env['sale.order'].search([('next_date','=',today),('state','not in',('draft','cancel'))])

        for po in po_ids:
            next_po=po.copy({'next_date':False})


