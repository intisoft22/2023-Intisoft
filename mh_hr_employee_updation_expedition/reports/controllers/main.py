# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import io

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from pytz import timezone
import xlsxwriter


def set_date(obj_date):
    if obj_date:
        date_utc = datetime.strptime(str(obj_date), '%Y-%m-%d %H:%M:%S')
        date_utc = timezone('Asia/Jakarta').localize(date_utc)
        tz = timezone('UTC')
        date_tz = date_utc
        date = date_tz.strftime('%d %b %Y')
        return date


def set_date2(obj_date):
    date_utc = datetime.strptime(str(obj_date), '%Y-%m-%d %H:%M:%S')
    date_tz = date_utc
    date = date_tz.strftime('%d %B %Y')
    return date


def set_date2a(obj_date):
    date_utc = datetime.strptime(str(obj_date), '%Y-%m-%d %H:%M:%S.%f')
    date_tz = date_utc
    date = date_tz.strftime('%d %B %Y')
    return date


def set_date3(obj_date):
    bln_array = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober',
                 'November', 'Desember']
    date_utc = datetime.strptime(str(obj_date), '%Y-%m-%d')
    date_utc = timezone('UTC').localize(date_utc)
    date_tz = date_utc.astimezone(timezone('Asia/Jakarta'))
    bln = int(date_tz.strftime('%m'))
    date = date_tz.strftime('%d/%m/%Y')
    return date


def month2name(month):
    return [0, 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'][month]


def lengthmonth(year, month):
    if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
        return 29
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]


class EmployeeExcelReportController(http.Controller):
    @http.route([
        '/employee/excel_report/<model("employee.report.wizard"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_employee_excel_report(self, wizard=None, **args):
        # wizard ini adalah model yang dikirim dengan method get_excel_report
        # pada model ng.sale.wizard
        # berisi data sales person, tanggal mulai dan tanggal akhir

        # buat response dengan header berupa file excel
        # agar browser segera mendownload response
        # header Content-Disposition ini adalah nama file
        # isi sesuai kebutuhan

        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Database M081 Krian Jaya Sentosa Template' + '.xlsx'))
            ]
        )

        # buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # buat style untuk mengatur jenis font, ukuran font, border dan alligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 13, 'bold': True, 'align': 'center'})
        header_style_top = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center', })
        header_style_top.set_text_wrap()
        header_style_top.set_bg_color('#92d050')
        header_style_top.set_align('center')
        header_style_top.set_align('vcenter')
        header_style_top.set_font_size(10)
        header_style_top_os = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center', })
        header_style_top_os.set_text_wrap()
        header_style_top_os.set_bg_color('#ffff00')
        header_style_top_os.set_align('center')
        header_style_top_os.set_align('vcenter')
        header_style_top_os.set_font_size(10)
        header_style = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center'})
        header_style.set_text_wrap()
        header_style.set_bg_color('#44546a')
        header_style.set_font_color('#ffffff')
        header_style.set_align('center')
        header_style.set_align('vcenter')
        header_style.set_font_size(10)
        header_style_os = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center'})
        header_style_os.set_text_wrap()
        header_style_os.set_bg_color('#92d050')
        header_style_os.set_align('center')
        header_style_os.set_align('vcenter')
        header_style_os.set_font_size(10)

        text_style = workbook.add_format(
            {'font_name': 'Cambria', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center','num_format': 'dd-mm-yyyy'})
        text_style.set_text_wrap()
        text_style.set_align('center')
        text_style.set_align('vcenter')
        text_style.set_font_size(10)
        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet = workbook.add_worksheet('Reguler')

        # set orientation jadi landscape
        sheet.set_landscape()
        # set ukuran kertas, 9 artinya kertas A4
        sheet.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)

        sheet.set_column(0, 0, 2.14)
        sheet.set_column(1, 1, 4.29)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 15)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 15)
        sheet.set_column(8, 8, 15)
        sheet.set_column(9, 9, 15)
        sheet.set_column(10, 10, 15)
        sheet.set_column(11, 11, 15)
        sheet.set_column(12, 12, 15)
        sheet.set_column(13, 13, 15)
        sheet.set_column(14, 14, 15)
        sheet.set_column(15, 15, 15)
        sheet.set_column(16, 16, 15)
        sheet.set_column(17, 17, 15)
        sheet.set_column(18, 18, 15)
        sheet.set_column(19, 19, 15)
        sheet.set_column(20, 20, 15)
        sheet.set_column(21, 21, 15)
        sheet.set_column(22, 22, 15)
        sheet.set_column(23, 23, 15)
        sheet.set_column(24, 24, 15)
        sheet.set_column(25, 25, 15)
        sheet.set_column(26, 26, 15)
        sheet.set_column(27, 27, 15)
        sheet.set_column(28, 28, 15)
        sheet.set_column(29, 29, 15)
        sheet.set_column(30, 30, 15)
        sheet.set_column(31, 31, 15)
        sheet.set_column(32, 32, 15)
        sheet.set_column(33, 33, 15)
        sheet.set_column(34, 34, 15)
        sheet.set_column(35, 35, 15)
        sheet.set_column(36, 36, 15)
        sheet.set_column(37, 37, 15)
        sheet.set_column(38, 38, 15)
        sheet.set_column(39, 39, 15)
        sheet.set_column(40, 40, 15)
        sheet.set_column(41, 41, 15)
        sheet.set_column(42, 42, 15)
        sheet.set_column(43, 43, 15)
        sheet.set_column(44, 44, 15)
        sheet.set_column(45, 45, 15)
        sheet.set_column(46, 46, 15)
        sheet.set_column(47, 47, 15)
        sheet.set_column(48, 48, 15)
        sheet.set_column(49, 49, 15)
        sheet.set_column(50, 50, 15)
        sheet.set_column(51, 51, 15)
        sheet.set_column(52, 52, 15)
        sheet.set_column(53, 53, 15)
        sheet.set_column(54, 54, 15)
        sheet.set_column(55, 55, 15)
        sheet.set_column(56, 56, 15)
        sheet.set_column(57, 57, 15)
        sheet.set_column(58, 58, 15)
        sheet.set_column(59, 59, 15)
        sheet.freeze_panes(4, 0)
        sheet.merge_range(0, 1, 1, 6, 'Reguler', header_style_top)
        sheet.merge_range(2, 1, 3, 1, 'No', header_style)
        sheet.merge_range(2, 2, 3, 2, 'NIK KNA', header_style)
        sheet.merge_range(2, 3, 3, 3, 'NIK PT Baru', header_style)
        sheet.merge_range(2, 4, 3, 4, 'Nama Mitra', header_style)
        sheet.merge_range(2, 5, 3, 5, 'ERM', header_style)
        sheet.merge_range(2, 6, 3, 6, 'RM Area di KNA', header_style)
        sheet.merge_range(2, 7, 3, 7, 'Kode DP', header_style)
        sheet.merge_range(2, 8, 3, 8, 'Tanggal Join KNA', header_style)
        sheet.merge_range(2, 9, 3, 9, 'Tanggal Join Mitra', header_style)
        sheet.merge_range(2, 10, 3, 10, 'Tanggal Resign', header_style)
        sheet.merge_range(2, 11, 3, 11, 'Divisi', header_style)
        sheet.merge_range(2, 12, 3, 12, 'Department', header_style)
        sheet.merge_range(2, 13, 3, 13, 'Jabatan', header_style)
        sheet.merge_range(2, 14, 3, 14, 'Status Karyawan', header_style)
        sheet.merge_range(2, 15, 3, 15, 'Legalitas Karyawan di KNA', header_style)
        sheet.merge_range(2, 16, 3, 16, 'Nama Karyawan', header_style)
        sheet.merge_range(2, 17, 3, 17, 'TTD SURAT PERNYATAAN', header_style)
        sheet.merge_range(2, 18, 3, 18, 'NAMA PT', header_style)
        sheet.merge_range(2, 19, 2, 24, 'History karyawan', header_style)
        sheet.write(3, 19, 'Tanggal Efektif.', header_style)
        sheet.write(3, 20, 'Status PMD', header_style)
        sheet.write(3, 21, 'Kode DP sebelumnya', header_style)
        sheet.write(3, 22, 'Divisi', header_style)
        sheet.write(3, 23, 'Department', header_style)
        sheet.write(3, 24, 'Jabatan Sebelumnya', header_style)
        sheet.merge_range(2, 25, 2, 28, 'Surat Peringatan', header_style)
        sheet.write(3, 25, 'Surat Teguran', header_style)
        sheet.write(3, 26, 'Tgl SP 1', header_style)
        sheet.write(3, 27, 'Tgl SP 2', header_style)
        sheet.write(3, 28, 'Tgl SP 3', header_style)
        sheet.merge_range(2, 29, 2, 47, 'Data Pribadi', header_style)
        sheet.write(3, 29, 'Jenis Kelamin', header_style)
        sheet.write(3, 30, 'Warga Negara', header_style)
        sheet.write(3, 31, 'Jenis ID', header_style)
        sheet.write(3, 32, 'No.ID', header_style)
        sheet.write(3, 33, 'No.KK', header_style)
        sheet.write(3, 34, 'No.NPWP', header_style)
        sheet.write(3, 35, 'Status Pajak', header_style)
        sheet.write(3, 36, 'Bank', header_style)
        sheet.write(3, 37, 'No.Rekening', header_style)
        sheet.write(3, 38, 'Tempat Lahir', header_style)
        sheet.write(3, 39, 'Tanggal Lahir', header_style)
        sheet.write(3, 40, 'Alamat Sesuai NPWP', header_style)
        sheet.write(3, 41, 'Alamat Domisili', header_style)
        sheet.write(3, 42, 'Agama', header_style)
        sheet.write(3, 43, 'Pendidikan', header_style)
        sheet.write(3, 44, 'Nama Instansi Pendidkan', header_style)
        sheet.write(3, 45, 'Status Pernikahan', header_style)
        sheet.write(3, 46, 'No HP', header_style)
        sheet.write(3, 47, 'Email', header_style)
        sheet.merge_range(2, 48, 2, 53, 'Emergency Contact', header_style)
        sheet.write(3, 48, 'Nama', header_style)
        sheet.write(3, 49, 'Hubungan', header_style)
        sheet.write(3, 50, 'No. Telp', header_style)
        sheet.write(3, 51, 'Alamat', header_style)
        sheet.write(3, 52, 'Nama Ayah', header_style)
        sheet.write(3, 53, 'Nama Ibu', header_style)
        sheet.merge_range(2, 54, 2, 61, 'DATA KELUARGA', header_style)
        sheet.write(3, 54, 'Nama Suami/Istri', header_style)
        sheet.write(3, 55, 'Tanggal Lahir', header_style)
        sheet.write(3, 56, 'Anak 1', header_style)
        sheet.write(3, 57, 'Tanggal Lahir', header_style)
        sheet.write(3, 58, 'Anak 2', header_style)
        sheet.write(3, 59, 'Tanggal Lahir', header_style)
        sheet.write(3, 60, 'Anak 3', header_style)
        sheet.write(3, 61, 'Tanggal Lahir', header_style)

        sheet.write(4, 1, '', header_style)
        sheet.write(4, 2, '', header_style)
        sheet.write(4, 3, '', header_style)
        sheet.write(4, 4, '', header_style)
        sheet.write(4, 5, '', header_style)
        sheet.write(4, 6, '', header_style)
        sheet.write(4, 7, '', header_style)
        sheet.write(4, 8, '', header_style)
        sheet.write(4, 9, '', header_style)
        sheet.write(4, 10, '', header_style)
        sheet.write(4, 11, '', header_style)
        sheet.write(4, 12, '', header_style)
        sheet.write(4, 13, '', header_style)
        sheet.write(4, 14, '', header_style)
        sheet.write(4, 15, '', header_style)
        sheet.write(4, 16, '', header_style)
        sheet.write(4, 17, '', header_style)
        sheet.write(4, 18, '', header_style)
        sheet.write(4, 19, '', header_style)
        sheet.write(4, 20, '', header_style)
        sheet.write(4, 21, '', header_style)
        sheet.write(4, 22, '', header_style)
        sheet.write(4, 23, '', header_style)
        sheet.write(4, 24, '', header_style)
        sheet.write(4, 25, '', header_style)
        sheet.write(4, 26, '', header_style)
        sheet.write(4, 27, '', header_style)
        sheet.write(4, 28, '', header_style)
        sheet.write(4, 29, '', header_style)
        sheet.write(4, 30, '', header_style)
        sheet.write(4, 31, '', header_style)
        sheet.write(4, 32, '', header_style)
        sheet.write(4, 33, '', header_style)
        sheet.write(4, 34, '', header_style)
        sheet.write(4, 35, '', header_style)
        sheet.write(4, 36, '', header_style)
        sheet.write(4, 37, '', header_style)
        sheet.write(4, 38, '', header_style)
        sheet.write(4, 39, '', header_style)
        sheet.write(4, 40, '', header_style)
        sheet.write(4, 41, '', header_style)
        sheet.write(4, 42, '', header_style)
        sheet.write(4, 43, '', header_style)
        sheet.write(4, 44, '', header_style)
        sheet.write(4, 45, '', header_style)
        sheet.write(4, 46, '', header_style)
        sheet.write(4, 47, '', header_style)
        sheet.write(4, 48, '', header_style)
        sheet.write(4, 49, '', header_style)
        sheet.write(4, 50, '', header_style)
        sheet.write(4, 51, '', header_style)
        sheet.write(4, 52, '', header_style)
        sheet.write(4, 53, '', header_style)
        sheet.write(4, 54, '', header_style)
        sheet.write(4, 55, '', header_style)
        sheet.write(4, 56, '', header_style)
        sheet.write(4, 57, '', header_style)
        sheet.write(4, 58, '', header_style)
        sheet.write(4, 59, '', header_style)
        sheet.write(4, 60, '', header_style)
        sheet.write(4, 61, '', header_style)
        sheet.autofilter(4, 1, 4, 61)

        domain_1 = [('vendor_id', '=', False), ('job_id.name', 'not ilike', 'Kurir')]
        employee_1 = request.env['hr.employee'].search(domain_1, order='name ASC')
        no1 = 1
        baris = 5

        for emp1 in employee_1:
            if emp1.resign_date:
                text_style.set_bg_color('#ff0000')
            sheet.write(baris, 1, no1, text_style)
            sheet.write(baris, 2, emp1.nik_kna or '', text_style)
            sheet.write(baris, 3, emp1.nik or '', text_style)
            sheet.write(baris, 4, emp1.company_id.company_registry or '', text_style)
            rm = ''
            erm = ''
            dbarray=[]
            rmarray=[]
            ermarray=[]
            if emp1.dp_id:
                for d in emp1.dp_id:
                    if d.name not in dbarray:
                        dbarray.append(d.name)
                    if d.rm_id.name not in rmarray:
                        rmarray.append(d.rm_id.name)
                        if d.rm_id.erm_id.name not in ermarray:
                            ermarray.append(d.rm_id.erm_id.name )
            dp=','.join(dbarray)
            rm=','.join(rmarray)
            erm=','.join(ermarray)
            sheet.write(baris, 5, erm, text_style)
            sheet.write(baris, 6, rm, text_style)
            sheet.write(baris, 7, dp, text_style)
            sheet.write(baris, 8, emp1.joining_kna_date or '', text_style)
            sheet.write(baris, 9, emp1.joining_date or '', text_style)
            sheet.write(baris, 10, emp1.resign_date or '', text_style)
            sheet.write(baris, 11, emp1.divisi or '', text_style)
            sheet.write(baris, 12, emp1.department_id.name or '', text_style)
            sheet.write(baris, 13, emp1.job_id.name or '', text_style)
            sheet.write(baris, 14, emp1.status or '', text_style)
            sheet.write(baris, 15, emp1.contract_type.name or '', text_style)
            sheet.write(baris, 16, emp1.name, text_style)
            centang_letter = ''
            if emp1.letter_sign:
                centang_letter = 'V'
            sheet.write(baris, 17, centang_letter, text_style)
            sheet.write(baris, 18, emp1.company_id.name or '', text_style)
            sheet.write(baris, 19, '', text_style)
            sheet.write(baris, 20, '', text_style)
            sheet.write(baris, 21, '', text_style)
            sheet.write(baris, 22, '', text_style)
            sheet.write(baris, 23, '', text_style)
            sheet.write(baris, 24, '', text_style)
            sheet.write(baris, 25, '', text_style)
            sheet.write(baris, 26, '', text_style)
            sheet.write(baris, 27, '', text_style)
            sheet.write(baris, 28, '', text_style)
            sheet.write(baris, 29, emp1.gender or '', text_style)
            sheet.write(baris, 30, emp1.country_id.name or '', text_style)
            identification = ''
            if emp1.identification_id:
                identification = 'KTP'
            sheet.write(baris, 31, identification or '', text_style)
            sheet.write(baris, 32, emp1.identification_id or '', text_style)
            sheet.write(baris, 33, emp1.kk_no or '', text_style)
            sheet.write(baris, 34, emp1.npwp_no or '', text_style)
            sheet.write(baris, 35, emp1.npwp_state or '', text_style)
            sheet.write(baris, 36, emp1.bank_account_id.bank_id.name or '', text_style)
            sheet.write(baris, 37, emp1.bank_account_id.acc_number or '', text_style)
            sheet.write(baris, 38, emp1.place_of_birth or '', text_style)
            sheet.write(baris, 39, emp1.birthday or '', text_style)
            sheet.write(baris, 40, emp1.npwp_address or '', text_style)
            sheet.write(baris, 41, emp1.address_home_id.street or '', text_style)
            sheet.write(baris, 42, emp1.religion or '', text_style)
            sheet.write(baris, 43, emp1.certificate or '', text_style)
            sheet.write(baris, 44, emp1.study_field or '', text_style)
            sheet.write(baris, 45, emp1.marital or '', text_style)
            sheet.write(baris, 46, emp1.work_phone or '', text_style)
            sheet.write(baris, 47, emp1.work_email or '', text_style)
            sheet.write(baris, 48, emp1.emergency_contact or '', text_style)
            sheet.write(baris, 49, emp1.emergency_relation or '', text_style)
            sheet.write(baris, 50, emp1.emergency_phone or '', text_style)
            sheet.write(baris, 51, emp1.emergency_address or '', text_style)

            pasangan_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship')
            ayah_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_father')
            ibu_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_mother')
            anak1_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_child_1')
            anak2_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_child_2')
            anak3_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_child_3')
            ayah=''
            ibu=''
            pasangan=''
            anak1=''
            anak2=''
            anak3=''
            pasangantgl=''
            anak1tgl=''
            anak2tgl=''
            anak3tgl=''
            for fam in emp1.fam_ids:
                if fam.relation_id.id == ayah_id:
                    ayah=fam.member_name
                if fam.relation_id.id == ibu_id:
                    ibu=fam.member_name
                if fam.relation_id.id == pasangan_id:
                    pasangan=fam.member_name
                    pasangantgl=fam.birth_date
                if fam.relation_id.id == anak1_id:
                    anak1=fam.member_name
                    anak1tgl=fam.birth_date
                if fam.relation_id.id == anak2_id:
                    anak2=fam.member_name
                    anak2tgl=fam.birth_date
                if fam.relation_id.id == anak3_id:
                    anak3=fam.member_name
                    anak3tgl=fam.birth_date

            sheet.write(baris, 52, ayah, text_style)
            sheet.write(baris, 53, ibu, text_style)
            sheet.write(baris, 54, pasangan, text_style)
            sheet.write(baris, 55, pasangantgl, text_style)
            sheet.write(baris, 56, anak1, text_style)
            sheet.write(baris, 57, anak1tgl, text_style)
            sheet.write(baris, 58, anak2, text_style)
            sheet.write(baris, 59, anak2tgl, text_style)
            sheet.write(baris, 60, anak3, text_style)
            sheet.write(baris, 61, anak3tgl, text_style)
            no1 += 1
            baris += 1
        # ganti sheet

        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet2 = workbook.add_worksheet('Kurir')
        # set orientation jadi landscape
        sheet2.set_landscape()
        # set ukuran kertas, 9 artinya kertas A4
        sheet2.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet2.set_margins(0.5, 0.5, 0.5, 0.5)

        sheet2.set_column(0, 0, 2.14)
        sheet2.set_column(1, 1, 4.29)
        sheet2.set_column(2, 2, 15)
        sheet2.set_column(3, 3, 15)
        sheet2.set_column(4, 4, 15)
        sheet2.set_column(5, 5, 15)
        sheet2.set_column(6, 6, 15)
        sheet2.set_column(7, 7, 15)
        sheet2.set_column(8, 8, 15)
        sheet2.set_column(9, 9, 15)
        sheet2.set_column(10, 10, 15)
        sheet2.set_column(11, 11, 15)
        sheet2.set_column(12, 12, 15)
        sheet2.set_column(13, 13, 15)
        sheet2.set_column(14, 14, 15)
        sheet2.set_column(15, 15, 15)
        sheet2.set_column(16, 16, 15)
        sheet2.set_column(17, 17, 15)
        sheet2.set_column(18, 18, 15)
        sheet2.set_column(19, 19, 15)
        sheet2.set_column(20, 20, 15)
        sheet2.set_column(21, 21, 15)
        sheet2.set_column(22, 22, 15)
        sheet2.set_column(23, 23, 15)
        sheet2.set_column(24, 24, 15)
        sheet2.set_column(25, 25, 15)
        sheet2.set_column(26, 26, 15)
        sheet2.set_column(27, 27, 15)
        sheet2.set_column(28, 28, 15)
        sheet2.set_column(29, 29, 15)
        sheet2.set_column(30, 30, 15)
        sheet2.set_column(31, 31, 15)
        sheet2.set_column(32, 32, 15)
        sheet2.set_column(33, 33, 15)
        sheet2.set_column(34, 34, 15)
        sheet2.set_column(35, 35, 15)
        sheet2.set_column(36, 36, 15)
        sheet2.set_column(37, 37, 15)
        sheet2.set_column(38, 38, 15)
        sheet2.set_column(39, 39, 15)
        sheet2.set_column(40, 40, 15)
        sheet2.set_column(41, 41, 15)
        sheet2.set_column(42, 42, 15)
        sheet2.set_column(43, 43, 15)
        sheet2.set_column(44, 44, 15)
        sheet2.set_column(45, 45, 15)
        sheet2.set_column(46, 46, 15)
        sheet2.set_column(47, 47, 15)
        sheet2.set_column(48, 48, 15)
        sheet2.set_column(49, 49, 15)
        sheet2.set_column(50, 50, 15)
        sheet2.set_column(51, 51, 15)
        sheet2.set_column(52, 52, 15)
        sheet2.set_column(53, 53, 15)
        sheet2.set_column(54, 54, 15)
        sheet2.set_column(55, 55, 15)
        sheet2.set_column(56, 56, 15)
        sheet2.set_column(57, 57, 15)
        sheet2.set_column(58, 58, 15)
        sheet2.set_column(59, 59, 15)
        sheet2.freeze_panes(4, 0)
        sheet2.merge_range(0, 1, 1, 6, 'KURIR', header_style_top)
        sheet2.merge_range(2, 1, 3, 1, 'No', header_style)
        sheet2.merge_range(2, 2, 3, 2, 'NIK Kurir KNA', header_style)
        sheet2.merge_range(2, 3, 3, 3, 'NIK Kurir PT Baru', header_style)
        sheet2.merge_range(2, 4, 3, 4, 'Nama Mitra', header_style)
        sheet2.merge_range(2, 5, 3, 5, 'ERM', header_style)
        sheet2.merge_range(2, 6, 3, 6, 'RM Area di KNA', header_style)
        sheet2.merge_range(2, 7, 3, 7, 'Kode DP', header_style)
        sheet2.merge_range(2, 8, 3, 8, 'Tanggal Join KNA', header_style)
        sheet2.merge_range(2, 9, 3, 9, 'Tanggal Join Mitra', header_style)
        sheet2.merge_range(2, 10, 3, 10, 'Tanggal Resign', header_style)
        sheet2.merge_range(2, 11, 3, 11, 'Divisi', header_style)
        sheet2.merge_range(2, 12, 3, 12, 'Departmen', header_style)
        sheet2.merge_range(2, 13, 3, 13, 'Jabatan', header_style)
        sheet2.merge_range(2, 14, 3, 14, 'Status Karyawan', header_style)
        sheet2.merge_range(2, 15, 3, 15, 'Nama Karyawan', header_style)
        sheet2.merge_range(2, 16, 3, 16, 'NAMA PT', header_style)
        sheet2.merge_range(2, 17, 2, 18, 'Mutasi Kurir', header_style)
        sheet2.write(3, 17, 'Tanggal Efektif.', header_style)
        sheet2.write(3, 18, 'Kode DP sebelumnya', header_style)
        sheet2.merge_range(2, 19, 2, 38, 'Data Pribadi', header_style)

        sheet2.write(3, 19, 'Jenis Kelamin', header_style)
        sheet2.write(3, 20, 'Warga Negara', header_style)
        sheet2.write(3, 21, 'Jenis ID', header_style)
        sheet2.write(3, 22, 'No.ID', header_style)
        sheet2.write(3, 23, 'No.KK', header_style)
        sheet2.write(3, 24, 'No.NPWP', header_style)
        sheet2.write(3, 25, 'No.SIM', header_style)
        sheet2.write(3, 26, 'Status Pajak', header_style)
        sheet2.write(3, 27, 'Bank', header_style)
        sheet2.write(3, 28, 'No.Rekening', header_style)
        sheet2.write(3, 29, 'Tempat Lahir', header_style)
        sheet2.write(3, 30, 'Tanggal Lahir', header_style)
        sheet2.write(3, 31, 'Alamat Sesuai NPWP', header_style)
        sheet2.write(3, 32, 'Alamat Domisili', header_style)
        sheet2.write(3, 33, 'Agama', header_style)
        sheet2.write(3, 34, 'Pendidikan', header_style)
        sheet2.write(3, 35, 'Nama Instansi Pendidkan', header_style)
        sheet2.write(3, 36, 'Status Pernikahan', header_style)
        sheet2.write(3, 37, 'No HP', header_style)
        sheet2.write(3, 38, 'Email', header_style)
        sheet2.merge_range(2, 39, 2, 44, 'Emergency Contact', header_style)
        sheet2.write(3, 39, 'Nama', header_style)
        sheet2.write(3, 40, 'Hubungan', header_style)
        sheet2.write(3, 41, 'No. Telp', header_style)
        sheet2.write(3, 42, 'Alamat', header_style)
        sheet2.write(3, 43, 'Nama Ayah', header_style)
        sheet2.write(3, 44, 'Nama Ibu', header_style)
        sheet2.merge_range(2, 45, 2, 52, 'DATA KELUARGA', header_style)
        sheet2.write(3, 45, 'Nama Suami/Istri', header_style)
        sheet2.write(3, 46, 'Tanggal Lahir', header_style)
        sheet2.write(3, 47, 'Anak 1', header_style)
        sheet2.write(3, 48, 'Tanggal Lahir', header_style)
        sheet2.write(3, 49, 'Anak 2', header_style)
        sheet2.write(3, 50, 'Tanggal Lahir', header_style)
        sheet2.write(3, 51, 'Anak 3', header_style)
        sheet2.write(3, 52, 'Tanggal Lahir', header_style)

        sheet2.write(4, 1, '', header_style)
        sheet2.write(4, 2, '', header_style)
        sheet2.write(4, 3, '', header_style)
        sheet2.write(4, 4, '', header_style)
        sheet2.write(4, 5, '', header_style)
        sheet2.write(4, 6, '', header_style)
        sheet2.write(4, 7, '', header_style)
        sheet2.write(4, 8, '', header_style)
        sheet2.write(4, 9, '', header_style)
        sheet2.write(4, 10, '', header_style)
        sheet2.write(4, 11, '', header_style)
        sheet2.write(4, 12, '', header_style)
        sheet2.write(4, 13, '', header_style)
        sheet2.write(4, 14, '', header_style)
        sheet2.write(4, 15, '', header_style)
        sheet2.write(4, 16, '', header_style)
        sheet2.write(4, 17, '', header_style)
        sheet2.write(4, 18, '', header_style)
        sheet2.write(4, 19, '', header_style)
        sheet2.write(4, 20, '', header_style)
        sheet2.write(4, 21, '', header_style)
        sheet2.write(4, 22, '', header_style)
        sheet2.write(4, 23, '', header_style)
        sheet2.write(4, 24, '', header_style)
        sheet2.write(4, 25, '', header_style)
        sheet2.write(4, 26, '', header_style)
        sheet2.write(4, 27, '', header_style)
        sheet2.write(4, 28, '', header_style)
        sheet2.write(4, 29, '', header_style)
        sheet2.write(4, 30, '', header_style)
        sheet2.write(4, 31, '', header_style)
        sheet2.write(4, 32, '', header_style)
        sheet2.write(4, 33, '', header_style)
        sheet2.write(4, 34, '', header_style)
        sheet2.write(4, 35, '', header_style)
        sheet2.write(4, 36, '', header_style)
        sheet2.write(4, 37, '', header_style)
        sheet2.write(4, 38, '', header_style)
        sheet2.write(4, 39, '', header_style)
        sheet2.write(4, 40, '', header_style)
        sheet2.write(4, 41, '', header_style)
        sheet2.write(4, 42, '', header_style)
        sheet2.write(4, 43, '', header_style)
        sheet2.write(4, 44, '', header_style)
        sheet2.write(4, 45, '', header_style)
        sheet2.write(4, 46, '', header_style)
        sheet2.write(4, 47, '', header_style)
        sheet2.write(4, 48, '', header_style)
        sheet2.write(4, 49, '', header_style)
        sheet2.write(4, 50, '', header_style)
        sheet2.autofilter(4, 1, 4, 59)
        domain_2 = [('vendor_id', '=', False), ('job_id.name', 'ilike', 'Kurir')]
        employee_2 = request.env['hr.employee'].search(domain_2, order='name ASC')
        no2 = 1
        baris2 = 5

        for emp2 in employee_2:
            if emp2.resign_date:
                text_style.set_bg_color('#ff0000')
            sheet2.write(baris2, 1, no2, text_style)
            sheet2.write(baris2, 2, emp2.nik_kna or '', text_style)
            sheet2.write(baris2, 3, emp2.nik or '', text_style)
            sheet2.write(baris2, 4, emp2.company_id.company_registry or '', text_style)
            rm = ''
            db = ''
            erm = ''
            if emp2.dp_id:
                dp = emp2.dp_id.name
                if emp2.dp_id.rm_id:
                    rm = emp2.dp_id.rm_id.name
                    if emp2.dp_id.rm_id.erm_id:
                        erm = emp2.dp_id.rm_id.erm_id.name

            sheet2.write(baris2, 5, erm, text_style)
            sheet2.write(baris2, 6, rm, text_style)
            sheet2.write(baris2, 7, dp, text_style)
            sheet2.write(baris2, 8, emp2.joining_kna_date or '', text_style)
            sheet2.write(baris2, 9, emp2.joining_date or '', text_style)
            sheet2.write(baris2, 10, emp2.resign_date or '', text_style)
            sheet2.write(baris2, 11, emp2.divisi or '', text_style)
            sheet2.write(baris2, 12, emp2.department_id.name or '', text_style)
            sheet2.write(baris2, 13, emp2.job_id.name or '', text_style)
            sheet2.write(baris2, 14, emp2.status or '', text_style)
            sheet2.write(baris2, 15, emp2.name, text_style)
            sheet2.write(baris2, 16, emp2.company_id.name or '', text_style)
            sheet2.write(baris2, 17, '', text_style)
            sheet2.write(baris2, 18, '', text_style)
            sheet2.write(baris2, 19, emp2.gender or '', text_style)
            sheet2.write(baris2, 20, emp2.country_id.name or '', text_style)
            identification = ''
            if emp2.identification_id:
                identification = 'KTP'
            sheet2.write(baris2, 21, identification or '', text_style)
            sheet2.write(baris2, 22, emp2.identification_id or '', text_style)
            sheet2.write(baris2, 23, emp2.kk_no or '', text_style)
            sheet2.write(baris2, 24, emp2.npwp_no or '', text_style)
            sheet2.write(baris2, 25, emp2.npwp_no or '', text_style)
            sheet2.write(baris2, 26, emp2.npwp_state or '', text_style)
            sheet2.write(baris2, 27, emp2.bank_account_id.bank_id.name or '', text_style)
            sheet2.write(baris2, 28, emp2.bank_account_id.acc_number or '', text_style)
            sheet2.write(baris2, 29, emp2.place_of_birth or '', text_style)
            sheet2.write(baris2, 30, emp2.birthday or '', text_style)
            sheet2.write(baris2, 31, emp2.npwp_address or '', text_style)
            sheet2.write(baris2, 32, emp2.address_home_id.street or '', text_style)
            sheet2.write(baris2, 33, emp2.religion or '', text_style)
            sheet2.write(baris2, 34, emp2.certificate or '', text_style)
            sheet2.write(baris2, 35, emp2.study_field or '', text_style)
            sheet2.write(baris2, 36, emp2.marital or '', text_style)
            sheet2.write(baris2, 37, emp2.work_phone or '', text_style)
            sheet2.write(baris2, 38, emp2.work_email or '', text_style)
            sheet2.write(baris2, 39, emp2.emergency_contact or '', text_style)
            sheet2.write(baris2, 40, emp2.emergency_relation or '', text_style)
            sheet2.write(baris2, 41, emp2.emergency_phone or '', text_style)
            sheet2.write(baris2, 42, emp2.emergency_address or '', text_style)

            pasangan_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship')
            ayah_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_father')
            ibu_id = request.env['ir.model.data'].xmlid_to_res_id('hr_employee_updation.employee_relationship_mother')
            anak1_id = request.env['ir.model.data'].xmlid_to_res_id(
                'hr_employee_updation.employee_relationship_child_1')
            anak2_id = request.env['ir.model.data'].xmlid_to_res_id(
                'hr_employee_updation.employee_relationship_child_2')
            anak3_id = request.env['ir.model.data'].xmlid_to_res_id(
                'hr_employee_updation.employee_relationship_child_3')
            ayah = ''
            ibu = ''
            pasangan = ''
            anak1 = ''
            anak2 = ''
            anak3 = ''
            pasangantgl = ''
            anak1tgl = ''
            anak2tgl = ''
            anak3tgl = ''
            for fam in emp2.fam_ids:
                if fam.relation_id.id == ayah_id:
                    ayah = fam.member_name
                if fam.relation_id.id == ibu_id:
                    ibu = fam.member_name
                if fam.relation_id.id == pasangan_id:
                    pasangan = fam.member_name
                    pasangantgl = fam.birth_date
                if fam.relation_id.id == anak1_id:
                    anak1 = fam.member_name
                    anak1tgl = fam.birth_date
                if fam.relation_id.id == anak2_id:
                    anak2 = fam.member_name
                    anak2tgl = fam.birth_date
                if fam.relation_id.id == anak3_id:
                    anak3 = fam.member_name
                    anak3tgl = fam.birth_date

            sheet2.write(baris2, 43, ayah, text_style)
            sheet2.write(baris2, 44, ibu, text_style)
            sheet2.write(baris2, 45, pasangan, text_style)
            sheet2.write(baris2, 46, pasangantgl, text_style)
            sheet2.write(baris2, 47, anak1, text_style)
            sheet2.write(baris2, 48, anak1tgl, text_style)
            sheet2.write(baris2, 49, anak2, text_style)
            sheet2.write(baris2, 50, anak2tgl, text_style)
            sheet2.write(baris2, 51, anak3, text_style)
            sheet2.write(baris2, 52, anak3tgl, text_style)
            no2 += 1
            baris2 += 1
        # sheet3

        # ganti sheet

        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet3 = workbook.add_worksheet('Reguler OS')
        # set orientation jadi landscape
        sheet3.set_landscape()
        # set ukuran kertas, 9 artinya kertas A4
        sheet3.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet3.set_margins(0.5, 0.5, 0.5, 0.5)

        sheet3.set_column(0, 0, 2.14)
        sheet3.set_column(1, 1, 4.29)
        sheet3.set_column(2, 2, 15)
        sheet3.set_column(3, 3, 15)
        sheet3.set_column(4, 4, 15)
        sheet3.set_column(5, 5, 15)
        sheet3.set_column(6, 6, 15)
        sheet3.set_column(7, 7, 15)
        sheet3.set_column(8, 8, 15)
        sheet3.set_column(9, 9, 15)
        sheet3.set_column(10, 10, 15)
        sheet3.set_column(11, 11, 15)
        sheet3.set_column(12, 12, 15)
        sheet3.set_column(13, 13, 15)
        sheet3.set_column(14, 14, 15)
        sheet3.set_column(15, 15, 15)
        sheet3.set_column(16, 16, 15)
        sheet3.set_column(17, 17, 15)
        sheet3.set_column(18, 18, 15)
        sheet3.set_column(19, 19, 15)
        sheet3.set_column(20, 20, 15)
        sheet3.set_column(21, 21, 15)
        sheet3.set_column(22, 22, 15)
        sheet3.set_column(23, 23, 15)
        sheet3.set_column(24, 24, 15)
        sheet3.set_column(25, 25, 15)
        sheet3.set_column(26, 26, 15)
        sheet3.set_column(27, 27, 15)
        sheet3.set_column(28, 28, 15)
        sheet3.set_column(29, 29, 15)
        sheet3.set_column(30, 30, 15)
        sheet3.set_column(31, 31, 15)
        sheet3.set_column(32, 32, 15)
        sheet3.set_column(33, 33, 15)
        sheet3.set_column(34, 34, 15)
        sheet3.set_column(35, 35, 15)
        sheet3.set_column(36, 36, 15)
        sheet3.set_column(37, 37, 15)
        sheet3.set_column(38, 38, 15)
        sheet3.set_column(39, 39, 15)
        sheet3.set_column(40, 40, 15)
        sheet3.set_column(41, 41, 15)
        sheet3.set_column(42, 42, 15)
        sheet3.set_column(43, 43, 15)
        sheet3.set_column(44, 44, 15)
        sheet3.set_column(45, 45, 15)
        sheet3.set_column(46, 46, 15)
        sheet3.set_column(47, 47, 15)
        sheet3.set_column(48, 48, 15)
        sheet3.set_column(49, 49, 15)
        sheet3.set_column(50, 50, 15)
        sheet3.set_column(51, 51, 15)
        sheet3.set_column(52, 52, 15)
        sheet3.set_column(53, 53, 15)
        sheet3.set_column(54, 54, 15)
        sheet3.set_column(55, 55, 15)
        sheet3.set_column(56, 56, 15)
        sheet3.set_column(57, 57, 15)
        sheet3.set_column(58, 58, 15)
        sheet3.set_column(59, 59, 15)
        sheet3.freeze_panes(4, 0)
        sheet3.merge_range(0, 1, 1, 6, 'Reguler OS', header_style_top_os)
        sheet3.merge_range(2, 1, 3, 1, 'No', header_style_os)
        sheet3.merge_range(2, 2, 3, 2, 'NIK KNA', header_style_os)
        sheet3.merge_range(2, 3, 3, 3, 'NIK PT Baru', header_style_os)
        sheet3.merge_range(2, 4, 3, 4, 'Nama Mitra', header_style_os)
        sheet3.merge_range(2, 5, 3, 5, 'Vendor', header_style_os)
        sheet3.merge_range(2, 6, 3, 6, 'ERM', header_style_os)
        sheet3.merge_range(2, 7, 3, 7, 'RM Area', header_style_os)
        sheet3.merge_range(2, 8, 3, 8, 'Kode DP', header_style_os)
        sheet3.merge_range(2, 9, 3, 9, 'Tanggal Join', header_style_os)
        sheet3.merge_range(2, 10, 3, 10, 'Tanggal Join Mitra', header_style_os)
        sheet3.merge_range(2, 11, 3, 11, 'Tanggal Resign', header_style_os)
        sheet3.merge_range(2, 12, 3, 12, 'Divisi', header_style_os)
        sheet3.merge_range(2, 13, 3, 13, 'Departmenen', header_style_os)
        sheet3.merge_range(2, 14, 3, 14, 'Jabatan', header_style_os)
        sheet3.merge_range(2, 15, 3, 15, 'Status Karyawan', header_style_os)
        sheet3.merge_range(2, 16, 3, 16, 'Legalitas Karyawan', header_style_os)
        sheet3.merge_range(2, 17, 3, 17, 'Nama Karyawan (Sesuai KTP)', header_style_os)
        sheet3.merge_range(2, 18, 3, 18, 'Nama PT', header_style)
        sheet3.merge_range(2, 19, 3, 19, 'Janis ID', header_style_os)
        sheet3.merge_range(2, 20, 3, 20, 'No.ID', header_style_os)
        sheet3.merge_range(2, 21, 3, 21, 'Alamat Sesuai KTP', header_style_os)
        sheet3.merge_range(2, 22, 3, 22, 'No. HP Karyawan', header_style_os)
        sheet3.merge_range(2, 23, 3, 23, 'Email Karyawan', header_style_os)

        sheet3.write(4, 1, '', header_style_os)
        sheet3.write(4, 2, '', header_style_os)
        sheet3.write(4, 3, '', header_style_os)
        sheet3.write(4, 4, '', header_style_os)
        sheet3.write(4, 5, '', header_style_os)
        sheet3.write(4, 6, '', header_style_os)
        sheet3.write(4, 7, '', header_style_os)
        sheet3.write(4, 8, '', header_style_os)
        sheet3.write(4, 9, '', header_style_os)
        sheet3.write(4, 10, '', header_style_os)
        sheet3.write(4, 11, '', header_style_os)
        sheet3.write(4, 12, '', header_style_os)
        sheet3.write(4, 13, '', header_style_os)
        sheet3.write(4, 14, '', header_style_os)
        sheet3.write(4, 15, '', header_style_os)
        sheet3.write(4, 16, '', header_style_os)
        sheet3.write(4, 17, '', header_style_os)
        sheet3.write(4, 18, '', header_style)
        sheet3.write(4, 19, '', header_style_os)
        sheet3.write(4, 20, '', header_style_os)
        sheet3.write(4, 21, '', header_style_os)
        sheet3.write(4, 22, '', header_style_os)
        sheet3.write(4, 23, '', header_style_os)
        sheet3.autofilter(4, 1, 4, 23)
        domain_3 = [('vendor_id', '!=', False), ('job_id.name', 'not ilike', 'Kurir')]
        employee_3 = request.env['hr.employee'].search(domain_3, order='name ASC')
        no3 = 1
        baris3 = 5

        for emp3 in employee_3:
            if emp3.resign_date:
                text_style.set_bg_color('#ff0000')
            sheet3.write(baris3, 1, no3, text_style)
            sheet3.write(baris3, 2, emp3.nik_kna or '', text_style)
            sheet3.write(baris3, 3, emp3.nik or '', text_style)
            sheet3.write(baris3, 4, emp3.company_id.company_registry or '', text_style)
            sheet3.write(baris3, 5, emp3.vendor_id.name or '', text_style)
            rm = ''
            db = ''
            erm = ''
            if emp3.dp_id:
                dp = emp3.dp_id.name
                if emp3.dp_id.rm_id:
                    rm = emp3.dp_id.rm_id.name
                    if emp3.dp_id.rm_id.erm_id:
                        erm = emp3.dp_id.rm_id.erm_id.name

            sheet3.write(baris3, 6, erm, text_style)
            sheet3.write(baris3, 7, rm, text_style)
            sheet3.write(baris3, 8, dp, text_style)
            sheet3.write(baris3, 9, emp3.joining_kna_date or '', text_style)
            sheet3.write(baris3, 10, emp3.joining_date or '', text_style)
            sheet3.write(baris3, 11, emp3.resign_date or '', text_style)
            sheet3.write(baris3, 12, emp3.divisi or '', text_style)
            sheet3.write(baris3, 13, emp3.department_id.name or '', text_style)
            sheet3.write(baris3, 14, emp3.job_id.name or '', text_style)
            sheet3.write(baris3, 15, emp3.status or '', text_style)
            sheet3.write(baris3, 16, emp3.contract_type.name or '', text_style)
            sheet3.write(baris3, 17, emp3.name, text_style)
            sheet3.write(baris3, 18, emp3.company_id.name or '', text_style)
            identification = ''
            if emp3.identification_id:
                identification = 'KTP'
            sheet3.write(baris3, 19, identification or '', text_style)
            sheet3.write(baris3, 20, emp3.identification_id or '', text_style)
            sheet3.write(baris3, 21, emp3.address_home_id.street or '', text_style)
            sheet3.write(baris3, 22, emp3.work_phone or '', text_style)
            sheet3.write(baris3, 23, emp3.work_email or '', text_style)

            no3 += 1
            baris3 += 1
        # sheet4
        # ganti sheet

        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet4 = workbook.add_worksheet('Kurir OS')
        # set orientation jadi landscape
        sheet4.set_landscape()
        # set ukuran kertas, 9 artinya kertas A4
        sheet4.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet4.set_margins(0.5, 0.5, 0.5, 0.5)

        sheet4.set_column(0, 0, 2.14)
        sheet4.set_column(1, 1, 4.29)
        sheet4.set_column(2, 2, 15)
        sheet4.set_column(3, 3, 15)
        sheet4.set_column(4, 4, 15)
        sheet4.set_column(5, 5, 15)
        sheet4.set_column(6, 6, 15)
        sheet4.set_column(7, 7, 15)
        sheet4.set_column(8, 8, 15)
        sheet4.set_column(9, 9, 15)
        sheet4.set_column(10, 10, 15)
        sheet4.set_column(11, 11, 15)
        sheet4.set_column(12, 12, 15)
        sheet4.set_column(13, 13, 15)
        sheet4.set_column(14, 14, 15)
        sheet4.set_column(15, 15, 15)
        sheet4.set_column(16, 16, 15)
        sheet4.set_column(17, 17, 15)
        sheet4.set_column(18, 18, 15)
        sheet4.set_column(19, 19, 15)
        sheet4.set_column(20, 20, 15)
        sheet4.set_column(21, 21, 15)
        sheet4.set_column(22, 22, 15)
        sheet4.set_column(23, 23, 15)
        sheet4.set_column(24, 24, 15)
        sheet4.set_column(25, 25, 15)
        sheet4.set_column(26, 26, 15)
        sheet4.set_column(27, 27, 15)
        sheet4.set_column(28, 28, 15)
        sheet4.set_column(29, 29, 15)
        sheet4.set_column(30, 30, 15)
        sheet4.set_column(31, 31, 15)
        sheet4.set_column(32, 32, 15)
        sheet4.set_column(33, 33, 15)
        sheet4.set_column(34, 34, 15)
        sheet4.set_column(35, 35, 15)
        sheet4.set_column(36, 36, 15)
        sheet4.set_column(37, 37, 15)
        sheet4.set_column(38, 38, 15)
        sheet4.set_column(39, 39, 15)
        sheet4.set_column(40, 40, 15)
        sheet4.set_column(41, 41, 15)
        sheet4.set_column(42, 42, 15)
        sheet4.set_column(43, 43, 15)
        sheet4.set_column(44, 44, 15)
        sheet4.set_column(45, 45, 15)
        sheet4.set_column(46, 46, 15)
        sheet4.set_column(47, 47, 15)
        sheet4.set_column(48, 48, 15)
        sheet4.set_column(49, 49, 15)
        sheet4.set_column(50, 50, 15)
        sheet4.set_column(51, 51, 15)
        sheet4.set_column(52, 52, 15)
        sheet4.set_column(53, 53, 15)
        sheet4.set_column(54, 54, 15)
        sheet4.set_column(55, 55, 15)
        sheet4.set_column(56, 56, 15)
        sheet4.set_column(57, 57, 15)
        sheet4.set_column(58, 58, 15)
        sheet4.set_column(59, 59, 15)
        sheet4.freeze_panes(4, 0)
        sheet4.merge_range(0, 1, 1, 6, 'Kurir OS', header_style_top_os)
        sheet4.merge_range(2, 1, 3, 1, 'No', header_style_os)
        sheet4.merge_range(2, 2, 3, 2, 'NIK KNA', header_style_os)
        sheet4.merge_range(2, 3, 3, 3, 'NIK PT Baru', header_style_os)
        sheet4.merge_range(2, 4, 3, 4, 'Kode Mitra', header_style_os)
        sheet4.merge_range(2, 5, 3, 5, 'Vendor', header_style_os)
        sheet4.merge_range(2, 6, 3, 6, 'ERM', header_style_os)
        sheet4.merge_range(2, 7, 3, 7, 'RM Area', header_style_os)
        sheet4.merge_range(2, 8, 3, 8, 'Kode DP', header_style_os)
        sheet4.merge_range(2, 9, 3, 9, 'Tanggal Join', header_style_os)
        sheet4.merge_range(2, 10, 3, 10, 'Tanggal Join Mitra', header_style_os)
        sheet4.merge_range(2, 11, 3, 11, 'Tanggal Resign', header_style_os)
        sheet4.merge_range(2, 12, 3, 12, 'Divisi', header_style_os)
        sheet4.merge_range(2, 13, 3, 13, 'Departmenen', header_style_os)
        sheet4.merge_range(2, 14, 3, 14, 'Jabatan', header_style_os)
        sheet4.merge_range(2, 15, 3, 15, 'Status Karyawan', header_style_os)
        sheet4.merge_range(2, 16, 3, 16, 'Legalitas Karyawan', header_style_os)
        sheet4.merge_range(2, 17, 3, 17, 'Nama Karyawan (Sesuai KTP)', header_style_os)
        sheet4.merge_range(2, 18, 3, 18, 'Nama PT', header_style)
        sheet4.merge_range(2, 19, 3, 19, 'Janis ID', header_style_os)
        sheet4.merge_range(2, 20, 3, 20, 'No.ID', header_style_os)
        sheet4.merge_range(2, 21, 3, 21, 'Alamat Sesuai KTP', header_style_os)
        sheet4.merge_range(2, 22, 3, 22, 'No. HP Karyawan', header_style_os)
        sheet4.merge_range(2, 23, 3, 23, 'Email Karyawan', header_style_os)

        sheet4.write(4, 1, '', header_style_os)
        sheet4.write(4, 2, '', header_style_os)
        sheet4.write(4, 3, '', header_style_os)
        sheet4.write(4, 4, '', header_style_os)
        sheet4.write(4, 5, '', header_style_os)
        sheet4.write(4, 6, '', header_style_os)
        sheet4.write(4, 7, '', header_style_os)
        sheet4.write(4, 8, '', header_style_os)
        sheet4.write(4, 9, '', header_style_os)
        sheet4.write(4, 10, '', header_style_os)
        sheet4.write(4, 11, '', header_style_os)
        sheet4.write(4, 12, '', header_style_os)
        sheet4.write(4, 13, '', header_style_os)
        sheet4.write(4, 14, '', header_style_os)
        sheet4.write(4, 15, '', header_style_os)
        sheet4.write(4, 16, '', header_style_os)
        sheet4.write(4, 17, '', header_style_os)
        sheet4.write(4, 18, '', header_style)
        sheet4.write(4, 19, '', header_style_os)
        sheet4.write(4, 20, '', header_style_os)
        sheet4.write(4, 21, '', header_style_os)
        sheet4.write(4, 22, '', header_style_os)
        sheet4.write(4, 23, '', header_style_os)
        sheet4.autofilter(4, 1, 4, 23)

        domain_4 = [('vendor_id', '!=', False), ('job_id.name', 'ilike', 'Kurir')]
        employee_4 = request.env['hr.employee'].search(domain_4, order='name ASC')
        no4 = 1
        baris4 = 5

        for emp4 in employee_4:
            if emp4.resign_date:
                text_style.set_bg_color('#ff0000')
            sheet4.write(baris4, 1, no4, text_style)
            sheet4.write(baris4, 2, emp4.nik_kna or '', text_style)
            sheet4.write(baris4, 3, emp4.nik or '', text_style)
            sheet4.write(baris4, 4, emp4.company_id.company_registry or '', text_style)
            sheet4.write(baris4, 5, emp4.vendor_id.name or '', text_style)
            rm = ''
            db = ''
            erm = ''
            if emp4.dp_id:
                dp = emp4.dp_id.name
                if emp4.dp_id.rm_id:
                    rm = emp4.dp_id.rm_id.name
                    if emp4.dp_id.rm_id.erm_id:
                        erm = emp4.dp_id.rm_id.erm_id.name

            sheet4.write(baris4, 6, erm, text_style)
            sheet4.write(baris4, 7, rm, text_style)
            sheet4.write(baris4, 8, dp, text_style)
            sheet4.write(baris4, 9, emp4.joining_kna_date or '', text_style)
            sheet4.write(baris4, 10, emp4.joining_date or '', text_style)
            sheet4.write(baris4, 11, emp4.resign_date or '', text_style)
            sheet4.write(baris4, 12, emp4.divisi or '', text_style)
            sheet4.write(baris4, 13, emp4.department_id.name or '', text_style)
            sheet4.write(baris4, 14, emp4.job_id.name or '', text_style)
            sheet4.write(baris4, 15, emp4.status or '', text_style)
            sheet4.write(baris4, 16, emp4.contract_type.name or '', text_style)
            sheet4.write(baris4, 17, emp4.name, text_style)
            sheet4.write(baris4, 18, emp4.company_id.name or '', text_style)
            identification = ''
            if emp4.identification_id:
                identification = 'KTP'
            sheet4.write(baris4, 19, identification or '', text_style)
            sheet4.write(baris4, 20, emp4.identification_id or '', text_style)
            sheet4.write(baris4, 21, emp4.address_home_id.street or '', text_style)
            sheet4.write(baris4, 22, emp4.work_phone or '', text_style)
            sheet4.write(baris4, 23, emp4.work_email or '', text_style)

            no4 += 1
            baris4 += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response
