from odoo import fields, models, api

from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import time

class record_document(models.Model):
    _name = 'record.document'


    name = fields.Char('Record No. ', required=True,  default="/",readonly=True, states={'draft': [('readonly', False)]})

    nama_record = fields.Char('Title', readonly=True, states={'draft':[('readonly', False)]})
    tanggal = fields.Date('Create Date', readonly=True,default=lambda *a: time.strftime('%Y-%m-%d'), required=True,
                          states={'draft': [('readonly', False)]})
    pembuat = fields.Many2one('res.users', 'Created By', required=True, default=lambda self: self.env.user,
                              readonly=True)

    jenis = fields.Many2one('document.page', 'Type Record', required=True, domain=[('type', '!=', 'category')],readonly=True, states={'draft':[('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('uploaded', 'Uploaded'),
                              ('obsolete', 'Obsolete'),
                              ('cancel', 'Cancelled')], required=True, string='Status state', default="draft",
                             track_visibility='always')

    attach_record = fields.Many2many(comodel_name='ir.attachment', relation='attachment_record', string="Add Attachment",
                                  readonly=True, states={'draft': [('readonly', False)]})

    dept =  fields.Many2one('hr.department', 'Department',required=True,domain=[('parent_id', '=', False)], readonly=True, states={'draft':[('readonly', False)]})

    def set_date(self,obj_date):
        if obj_date:
            date_utc = datetime.strptime(str(obj_date), '%Y-%m-%d')
            date = date_utc.strftime('%d-%m-%Y')
            return date
    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('record.no.seq')

        record_ids=self.env['document.page'].search([('id','=', vals.get('jenis'))])
        tgl=vals.get('tanggal')
        vals['nama_record'] = record_ids[0].name+" "+self.set_date(tgl)

        opl_id = super(record_document, self).create(vals)
        return opl_id

    # @api.multi
    def write(self, vals):
        tgl = vals.get('tanggal')
        jenis =vals.get('jenis')
        if tgl and jenis:
            record_ids = self.env['document.page'].search([('id', '=', jenis)])
            vals['nama_record'] = record_ids[0].name+" "+self.set_date(tgl)

        if tgl:
            vals['nama_record'] = self.jenis.name + " " + self.set_date(tgl)
        if jenis:
            record_ids = self.env['document.page'].search([('id', '=', jenis)])
            vals['nama_record'] = record_ids[0].name+" "+self.set_date(self.tanggal)

        return super(record_document, self).write(vals)

    # @api.multi
    def upload(self):
        if self.env.uid == self.pembuat.id:
            return self.write({
                'state': 'uploaded'
            })
        else:
            raise osv.except_osv(_('Invalid Action!'),
                                 _("can't upload! You are not from the %s department" % (self.dept.name)))


    # @api.multi
    def reupload(self):
        if self.env.user.dept_id.id == self.dept.id:
            return self.write({
                'state': 'draft'
            })
        else:
            raise osv.except_osv(_('Invalid Action!'),
                                 _("can't re-upload! You are not from the %s department" % (self.dept.name)))

    # @api.multi
    def remove_record(self):
        # print "rremove"
        record_ids=self.env['record.document'].search([('state','=','uploaded')], order="tanggal asc")
        for record in record_ids:

            tglrecord=datetime.strptime(str(record.tanggal),  '%Y-%m-%d')
            tglsrkng=date.today()
            difference_in_years = relativedelta(tglsrkng, tglrecord).years
            # print difference_in_years
            if record.jenis.masasimpan:
                masadurasi = record.jenis.masasimpan.durasi
                # print masadurasi
                if difference_in_years >=masadurasi:
                    for attach in record.attach_record:
                        attachment_ir = self.env['ir.attachment']
                        bin_value = attach.datas.decode('base64')
                        fname, full_path = attachment_ir._get_path(bin_value, attach.checksum)
                        # print full_path
                        attach.unlink()
                    record.unlink()

    # @api.multi
    def download_doc(self):

        depthead = self.env.ref('mgmtsystem.group_mgmtsystem_dept_head')
        mr = self.env.ref('mgmtsystem.group_mgmtsystem_qmr')
        list_grup = [x.id for x in self.env.user.groups_id]
        if mr.id in list_grup:
            for attach in self.attach_record:
                return {
                    'type': 'ir.actions.act_url',
                    'url': '/web/content/%s?download=True' % (attach.id),
                    'target': "new"
                }
        if depthead.id in list_grup:
            if self.env.user.dept_id.id == self.dept.id:
                for attach in self.attach_record:
                    return {
                        'type': 'ir.actions.act_url',
                        'url': '/web/content/%s?download=True' % (attach.id),
                        'target': "new"
                    }
            else:
                raise osv.except_osv(_('Invalid Action!'), _('You are not from the %s department' % (self.dept.name)))
        else:

            raise osv.except_osv(_('Invalid Action!'), _('You are not dept head'))

