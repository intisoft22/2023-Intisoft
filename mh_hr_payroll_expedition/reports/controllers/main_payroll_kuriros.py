# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import io

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from pytz import timezone
import xlsxwriter

import calendar


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
    return [0, 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'][month]


def lengthmonth(year, month):
    if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
        return 29
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]


class EmployeeExcelReportController(http.Controller):
    @http.route([
        '/payroll/kurir_excel_report/<model("payroll.kuriros.report.wizard"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_payroll_kuriros_excel_report(self, wizard=None, **args):
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
                ('Content-Disposition', content_disposition('Lap Gaji Kurir '+ month2name(int(wizard.bulan))+' '+str(wizard.tahun) + '.xlsx'))
            ]
        )

        # buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # buat style untuk mengatur jenis font, ukuran font, border dan alligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 13, 'bold': True, 'align': 'center'})
        header_style_1 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center', })
        header_style_1.set_text_wrap()
        header_style_1.set_bg_color('#ffc000')
        header_style_1.set_align('center')
        header_style_1.set_align('vcenter')
        header_style_1.set_font_size(10)
        header_style_2 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center', })
        header_style_2.set_text_wrap()
        header_style_2.set_bg_color('#ffff00')
        header_style_2.set_align('center')
        header_style_2.set_align('vcenter')
        header_style_2.set_font_size(10)
        header_style_3 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center'})
        header_style_3.set_text_wrap()
        header_style_3.set_bg_color('#92d050')
        header_style_3.set_align('center')
        header_style_3.set_align('vcenter')
        header_style_3.set_font_size(10)
        header_style_4 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center'})
        header_style_4.set_text_wrap()
        header_style_4.set_bg_color('#00b0f0')
        header_style_4.set_align('center')
        header_style_4.set_align('vcenter')
        header_style_4.set_font_size(10)
        header_style_5 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center'})
        header_style_5.set_text_wrap()
        header_style_5.set_bg_color('#b7dde8')
        header_style_5.set_align('center')
        header_style_5.set_align('vcenter')
        header_style_5.set_font_size(10)
        header_style_6 = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center','num_format': '_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)'})
        header_style_6.set_text_wrap()
        header_style_6.set_bg_color('#ff66cc')
        header_style_6.set_align('right')
        header_style_6.set_align('vcenter')
        header_style_6.set_font_size(10)
        header_style_6a = workbook.add_format(
            {'font_name': 'Cambria', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'valign': 'center','num_format': '_([$Rp-421]* #,##0_);_([$Rp-421]* (#,##0);_([$Rp-421]* "-"_);_(@_)'})
        header_style_6a.set_text_wrap()
        header_style_6a.set_bg_color('#ff66cc')
        header_style_6a.set_align('right')
        header_style_6a.set_align('vcenter')
        header_style_6a.set_font_size(10)

        text_style = workbook.add_format(
            {'font_name': 'Cambria', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'num_format': 'dd-mm-yyyy'})
        text_style.set_text_wrap()
        text_style.set_align('center')
        text_style.set_align('vcenter')
        text_style.set_font_size(10)
        text_style2 = workbook.add_format(
            {'font_name': 'Cambria', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'num_format': '_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)'})
        text_style2.set_text_wrap()
        text_style2.set_align('right')
        text_style2.set_align('vcenter')
        text_style2.set_font_size(10)
        text_style3 = workbook.add_format(
            {'font_name': 'Cambria', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center',
             'num_format': '_([$Rp-421]* #,##0_);_([$Rp-421]* (#,##0);_([$Rp-421]* "-"_);_(@_)'})
        text_style3.set_text_wrap()
        text_style3.set_align('right')
        text_style3.set_align('vcenter')
        text_style3.set_font_size(10)
        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet = workbook.add_worksheet('Lap Gaji Kurir '+ month2name(int(wizard.bulan))+' '+str(wizard.tahun))

        # set orientation jadi landscape
        sheet.set_landscape()
        # set ukuran kertas, 9 artinya kertas A4
        sheet.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 27)
        sheet.set_column(2, 2, 21)
        sheet.set_column(3, 3, 13)
        sheet.set_column(4, 4, 13)
        sheet.set_column(5, 5, 33)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 19)
        sheet.set_column(8, 8, 13)
        sheet.set_column(9, 9, 13)
        sheet.set_column(10, 10, 16)
        sheet.set_column(11, 11, 16)
        sheet.set_column(12, 12, 18)
        sheet.set_column(13, 13, 18)
        sheet.set_column(14, 14, 18)
        sheet.set_column(15, 15, 18)
        sheet.set_column(16, 16, 18)
        sheet.set_column(17, 17, 18)
        sheet.set_column(18, 18, 18)
        sheet.set_column(19, 19, 18)
        sheet.set_column(20, 20, 18)
        sheet.set_column(21, 21, 18)
        sheet.set_column(22, 22, 18)
        sheet.set_column(23, 23, 18)
        sheet.set_column(24, 24, 18)
        sheet.set_column(25, 25, 18)
        sheet.set_column(26, 26, 18)
        sheet.set_column(27, 27, 19)
        sheet.set_column(28, 28, 18)
        sheet.set_column(29, 29, 20)
        sheet.set_column(30, 30, 21)
        sheet.set_column(31, 31, 21)
        sheet.set_column(32, 32, 21)
        sheet.set_column(33, 33, 21)
        sheet.set_column(34, 34, 21)
        sheet.set_column(35, 35, 21)
        sheet.set_column(36, 36, 21)
        sheet.set_column(37, 37, 21)
        sheet.set_column(38, 38, 15)
        sheet.set_column(39, 39, 15)
        sheet.freeze_panes(5, 0)

        sheet.set_row(4, 51)
        sheet.write(4, 0, 'No', header_style_1)
        sheet.write(4, 1, 'Nama Perusahaan Mitra', header_style_1)
        sheet.write(4, 2, 'Status Karyawan', header_style_1)
        sheet.write(4, 3, 'Tanggal Join', header_style_1)
        sheet.write(4, 4, 'Kode DP', header_style_1)
        sheet.write(4, 5, 'Nama', header_style_1)
        sheet.write(4, 6, 'NIK Karyawan', header_style_1)
        sheet.write(4, 7, 'Departemen', header_style_1)
        sheet.write(4, 8, 'Jabatan', header_style_1)
        sheet.write(4, 9, 'Tanggal Resign', header_style_1)
        sheet.write(4, 10, 'Nama OS', header_style_1)
        sheet.write(4, 11, 'ERM', header_style_1)
        sheet.write(4, 12, 'RM', header_style_1)
        sheet.write(4, 13, 'PP_CASH - INTERCITY', header_style_2)
        sheet.write(4, 14, 'PP_CASH - OUTCITY', header_style_2)
        sheet.write(4, 15, 'PP_PM - TOTAL', header_style_2)
        sheet.write(4, 16, 'CC_CASH - TOTAL', header_style_2)
        sheet.write(4, 17, 'TOTAL PENDAPATAN PICKUP', header_style_3)
        sheet.write(4, 18, 'PP_CASH - INTERCITY', header_style_2)
        sheet.write(4, 19, 'PP_CASH - OUTCITY', header_style_2)
        sheet.write(4, 20, 'PP_PM - TOTAL', header_style_2)
        sheet.write(4, 21, 'CC_CASH - TOTAL', header_style_2)
        sheet.write(4, 22, 'TOTAL INSENTIF PICKUP', header_style_3)
        sheet.write(4, 23, 'DELIV - INTERCITY', header_style_2)
        sheet.write(4, 24, 'DELIV - OUTCITY', header_style_2)
        sheet.write(4, 25, 'Total Delivery', header_style_3)
        sheet.write(4, 26, 'RATE DELIV', header_style_3)
        sheet.write(4, 27, 'GAJI KURIR', header_style_2)
        sheet.write(4, 28, 'DENDA', header_style_2)
        sheet.write(4, 29, 'REWARD SUBSIDI BBM', header_style_4)
        sheet.write(4, 30, 'TOTAL GAJI KURIR', header_style_5)
        sheet.write(4, 31, 'RATE FEE', header_style_5)
        sheet.write(4, 32, 'Management Fee Rp 100/paket', header_style_5)
        sheet.write(4, 33, 'PPN 11%', header_style_5)
        sheet.write(4, 34, 'Total Gaji Yang dikeluarkan oleh perusahaan yang seharusnya', header_style_5)
        sheet.write(4, 35, 'RUMUS', header_style_5)
        sheet.write(4, 36, 'Ket Denda', header_style_5)
        sheet.write(4, 37, 'QTY TITIP TTD', header_style_2)

        sheet.write(5, 0, '', header_style_1)
        sheet.write(5, 1, '', header_style_1)
        sheet.write(5, 2, '', header_style_1)
        sheet.write(5, 3, '', header_style_1)
        sheet.write(5, 4, '', header_style_1)
        sheet.write(5, 5, '', header_style_1)
        sheet.write(5, 6, '', header_style_1)
        sheet.write(5, 7, '', header_style_1)
        sheet.write(5, 8, '', header_style_1)
        sheet.write(5, 9, '', header_style_1)
        sheet.write(5, 10, '', header_style_1)
        sheet.write(5, 11, '', header_style_1)
        sheet.write(5, 12, '', header_style_1)
        sheet.write(5, 13, '', header_style_2)
        sheet.write(5, 14, '', header_style_2)
        sheet.write(5, 15, '', header_style_2)
        sheet.write(5, 16, '', header_style_2)
        sheet.write(5, 17, '', header_style_3)
        sheet.write(5, 18, '', header_style_2)
        sheet.write(5, 19, '', header_style_2)
        sheet.write(5, 20, '', header_style_2)
        sheet.write(5, 21, '', header_style_2)
        sheet.write(5, 22, '', header_style_3)
        sheet.write(5, 23, '', header_style_2)
        sheet.write(5, 24, '', header_style_2)
        sheet.write(5, 25, '', header_style_3)
        sheet.write(5, 26, '', header_style_3)
        sheet.write(5, 27, '', header_style_2)
        sheet.write(5, 28, '', header_style_2)
        sheet.write(5, 29, '', header_style_4)
        sheet.write(5, 30, '', header_style_5)
        sheet.write(5, 31, '', header_style_5)
        sheet.write(5, 32, '', header_style_5)
        sheet.write(5, 33, '', header_style_5)
        sheet.write(5, 34, '', header_style_5)
        sheet.write(5, 35, '', header_style_5)
        sheet.write(5, 36, '', header_style_5)
        sheet.write(5, 37, '', header_style_2)

        sheet.autofilter(5, 1, 5, 37)
        year = wizard.tahun
        month = wizard.bulan
        _dateFromx = str(year) + '-' + str(month) + '-01'
        _dateTox = '%s-%s-%s' % (str(year), str(month), str(calendar.monthrange(int(year), int(month))[1]))
        if int(month) == 1:
            _dateFromx = str(int(year) - 1) + '-' + str(12) + '-01'
            _dateTox = '%s-%s-%s' % (str(int(year) - 1), str(12), str(calendar.monthrange(int(year) - 1, 12)[1]))
        else:
            _dateFromx = str(year) + '-' + str(int(month) - 1) + '-01'
            _dateTox = '%s-%s-%s' % (
                str(year), str(int(month) - 1), str(calendar.monthrange(int(year), int(month) - 1)[1]))
        if int(month) > 9:
            dateFromx = str(year) + '-' + str(month) + '-01'
            dateTox = '%s-%s-%s' % (str(year), str(month), str(calendar.monthrange(int(year), int(month))[1]))
        else:
            dateFromx = str(year) + '-0' + str(month) + '-01'
            dateTox = '%s-0%s-%s' % (str(year), str(month), str(calendar.monthrange(int(year), int(month))[1]))
        # print dateFromx
        # print dateTox
        dateFrom = datetime.strptime(dateFromx, '%Y-%m-%d')
        dateTo = datetime.strptime(dateTox, '%Y-%m-%d')

        dateAwal = dateFrom.strftime('%Y-%m-%d')
        dateAkhir = dateTo.strftime('%Y-%m-%d')

        domain_1_2 = [('date_to', '>=', dateAwal), ('date_to', '<=', dateAkhir), ]
        domain_1 = domain_1_2 + [('employee_id.vendor_id', '!=', False), ('employee_id.job_id.name', 'ilike', 'Kurir')]
        # print(domain_1)
        listIds = request.env['hr.payslip'].search(domain_1, order='employee_id ASC')
        no1 = 1
        baris = 6
        gt1 = 0
        gt2 = 0
        gt3 = 0
        gt4 = 0
        gt5 = 0
        gt6 = 0
        gt7 = 0
        gt8 = 0
        gt9 = 0
        gt10 = 0
        gt11 = 0
        gt12 = 0
        gt13 = 0
        gt14 = 0
        gt15 = 0
        gt16 = 0
        gt17 = 0
        gt18 = 0
        gt19 = 0
        gt20 = 0
        gt21 = 0
        gt22 = 0
        for payslip in listIds:
            # print(emp1.name)
            # print(emp1.resign_date)

            # print(text_style)
            sheet.write(baris, 0, str(no1), text_style)
            sheet.write(baris, 1, payslip.employee_id.company_id.name or '', text_style)
            if payslip.employee_id.status == 'Mitra Aktif':
                status = 'AKTIF'
            else:
                status = 'TIDAK AKTIF'
            emp1 = payslip.employee_id
            sheet.write(baris, 2, status or '', text_style)
            sheet.write(baris, 3, emp1.joining_date or '', text_style)
            rm = ''
            erm = ''
            dbarray = []
            rmarray = []
            ermarray = []
            if payslip.employee_id.dp_id:
                for d in payslip.employee_id.dp_id:
                    if d.name not in dbarray:
                        dbarray.append(d.name)
                    if d.rm_id.name not in rmarray:
                        rmarray.append(d.rm_id.name)
                        if d.rm_id.erm_id.name not in ermarray:
                            ermarray.append(d.rm_id.erm_id.name)
            dp = ','.join(dbarray)
            rm = ','.join(rmarray)
            erm = ','.join(ermarray)
            sheet.write(baris, 4, dp, text_style)
            sheet.write(baris, 5, emp1.name, text_style)
            sheet.write(baris, 6, emp1.nik, text_style)
            sheet.write(baris, 7, emp1.department_id.name or '', text_style)
            sheet.write(baris, 8, emp1.job_id.name or '', text_style)
            sheet.write(baris, 9, emp1.resign_date or '', text_style)
            sheet.write(baris, 10, emp1.vendor_id.name or '', text_style)
            sheet.write(baris, 11, erm, text_style)
            sheet.write(baris, 12, rm, text_style)
            nilai1 = 0
            nilai2 = 0
            nilai3 = 0
            nilai4 = 0
            nilai5 = 0
            nilai6 = 0
            nilai7 = 0
            nilai8 = 0
            nilai9 = 0
            nilai10 = 0
            nilai11 = 0
            nilai12 = 0
            nilai13 = 0
            nilai14 = 0
            nilai15 = 0
            nilai16 = 0
            nilai17 = 0
            nilai18 = 0
            nilai19 = 0
            nilai20 = 0
            nilai21 = 0
            nilai22 = 0

            for py in payslip.line_ids:
                if py.code == 'PPCO':
                    nilai1 += py.total
                    gt1 += py.total
                if py.code == 'PPCI':
                    nilai2 += py.total
                    gt2 += py.total
                if py.code == 'PPPM':
                    nilai3 += py.total
                    gt3 += py.total
                if py.code == 'CCC':
                    nilai4 += py.total
                    gt4 += py.total
                if py.code == 'TOTBASIC':
                    nilai5 += py.total
                    gt5 += py.total
                if py.code == 'IPPCO':
                    nilai6 += py.total
                    gt6 += py.total
                if py.code == 'IPPCI':
                    nilai7 += py.total
                    gt7 += py.total
                if py.code == 'IPPPM':
                    nilai8 += py.total
                    gt8 += py.total
                if py.code == 'ICCC':
                    nilai9 += py.total
                    gt9 += py.total
                if py.code == 'TOTINS':
                    nilai10 += py.total
                    gt10 += py.total
                if py.code == 'DIC':
                    nilai11 += py.total
                    gt11 += py.total
                if py.code == 'DOC':
                    nilai12 += py.total
                    gt12 += py.total
                if py.code == 'TOTDELIV':
                    nilai13 += py.total
                    gt13 += py.total
                if py.code == 'TOTGROSS':
                    nilai14 += py.total
                    gt14 += py.total
                if py.code == 'DENDA':
                    nilai15 += py.total
                    gt15 += py.total
                if py.code == 'REWARDK':
                    nilai16 += py.total
                    gt16 += py.total
                if py.code == 'TOTALEMP':
                    nilai17 += py.total
                    gt17 += py.total
                if py.code == 'FEEMNGK':
                    nilai18 += py.total
                    gt18 += py.total
                if py.code == 'TAX':
                    nilai19 += py.total
                    gt19 += py.total
                if py.code == 'TOTAL':
                    nilai20 += py.total
                    gt20 += py.total

            sheet.write(baris, 13, nilai1, text_style2)
            sheet.write(baris, 14, nilai2, text_style2)
            sheet.write(baris, 15, nilai3, text_style2)
            sheet.write(baris, 16, nilai4, text_style2)
            sheet.write(baris, 17, nilai5, text_style2)
            sheet.write(baris, 18, nilai6, text_style2)
            sheet.write(baris, 19, nilai7, text_style2)
            sheet.write(baris, 20, nilai8, text_style2)
            sheet.write(baris, 21, nilai9, text_style2)
            sheet.write(baris, 22, nilai10, text_style2)
            sheet.write(baris, 23, nilai11, text_style2)
            sheet.write(baris, 24, nilai12, text_style2)
            sheet.write(baris, 25, nilai13, text_style2)
            sheet.write(baris, 26, payslip.contract_id.rate_deliv, text_style2)
            sheet.write(baris, 27, nilai14, text_style3)
            sheet.write(baris, 28, nilai15, text_style3)
            sheet.write(baris, 29, nilai16, text_style3)
            sheet.write(baris, 30, nilai17, text_style3)
            sheet.write(baris, 31, payslip.contract_id.rate_fee, text_style2)
            sheet.write(baris, 32, nilai18, text_style3)
            sheet.write(baris, 33, nilai19, text_style3)
            sheet.write(baris, 34, nilai20, text_style3)
            sheet.write(baris, 35, nilai20, text_style3)
            sheet.write(baris, 36, '', text_style)
            sheet.write(baris, 37, '', text_style)

            no1 += 1
            baris += 1
        sheet.merge_range(baris, 0, baris, 12, 'GRAND TOTAL', header_style_6)
        sheet.write(baris, 13, gt1, header_style_6)
        sheet.write(baris, 14, gt2, header_style_6)
        sheet.write(baris, 15, gt3, header_style_6)
        sheet.write(baris, 16, gt4, header_style_6)
        sheet.write(baris, 17, gt5, header_style_6a)
        sheet.write(baris, 18, gt6, header_style_6)
        sheet.write(baris, 19, gt7, header_style_6)
        sheet.write(baris, 20, gt8, header_style_6)
        sheet.write(baris, 21, gt9, header_style_6)
        sheet.write(baris, 22, gt10, header_style_6a)
        sheet.write(baris, 23, gt11, header_style_6)
        sheet.write(baris, 24, gt12, header_style_6)
        sheet.write(baris, 25, gt13, header_style_6)
        sheet.write(baris, 26, '', header_style_6)
        sheet.write(baris, 27, gt14, header_style_6a)
        sheet.write(baris, 28, gt15, header_style_6a)
        sheet.write(baris, 29, gt16, header_style_6a)
        sheet.write(baris, 30, gt17, header_style_6a)
        sheet.write(baris, 31, '', header_style_6)
        sheet.write(baris, 32, gt18, header_style_6a)
        sheet.write(baris, 33, gt19, header_style_6a)
        sheet.write(baris, 34, gt20, header_style_6a)
        sheet.write(baris, 35, gt20, header_style_6a)
        sheet.write(baris, 36, '', header_style_6)
        sheet.write(baris, 37, '', header_style_6)
        sheet.set_row(baris, 51)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response
