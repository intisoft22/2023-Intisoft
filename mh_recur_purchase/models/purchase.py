from odoo import fields, models, api
from datetime import date
from dateutil.relativedelta import relativedelta


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
        'to approve': [('readonly', True)],
    }

    recur = fields.Boolean('Recur', copy=True, states=READONLY_STATES, )
    period_recur = fields.Selection([('harian', 'Harian'), ('mingguan', 'Mingguan'), ('bulanan', 'Bulanan'), ('tahunan',
                                                                                                              'Tahunan')],
                                    copy=True, states=READONLY_STATES, )
    next_date = fields.Date('Next Date Purchase Order', states=READONLY_STATES, )

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        # self.copy()
        if self.recur:
            if self.period_recur == 'harian':

                self.next_date = self.date_order + relativedelta(days=1)
            elif self.period_recur == 'mingguan':

                self.next_date = self.date_order + relativedelta(days=7)
            elif self.period_recur == 'bulanan':

                self.next_date = self.date_order + relativedelta(months=1)
            elif self.period_recur == 'tahunan':

                self.next_date = self.date_order + relativedelta(years=1)
        return

    @api.model
    def _create_po_recur(self):
        today = date.today()
        # print(today)
        po_ids = self.env['purchase.order'].search(
            [('next_date', '=', today), ('state', 'not in', ('draft', 'cancel'))])

        for po in po_ids:
            next_po = po.copy({'next_date': False})

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):

        if 'date_order:year' in groupby or 'date_order:month' in groupby or 'date_order:quarter' in groupby or 'date_order:month' in groupby or 'date_order:week' in groupby or 'date_order:day' in groupby:
            orderby = 'date_order DESC' + (orderby and (',' + orderby) or '')
        return super(PurchaseOrder, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                     orderby=orderby, lazy=lazy)
