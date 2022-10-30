# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import content_disposition, request
import io

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from pytz import timezone
import xlsxwriter

from odoo.tools.misc import get_lang


class AccountFinancialExcelReportController(http.Controller):

    def _compute_account_balance(self, accounts):
        """ compute the balance, debit and credit for the provided accounts
        """
        mapping = {
            'balance': "COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance",
            'debit': "COALESCE(SUM(debit), 0) as debit",
            'credit': "COALESCE(SUM(credit), 0) as credit",
        }

        res = {}
        for account in accounts:
            res[account.id] = dict.fromkeys(mapping, 0.0)
        if accounts:
            tables, where_clause, where_params = request.env['account.move.line']._query_get()
            tables = tables.replace('"', '') if tables else "account_move_line"
            wheres = [""]
            if where_clause.strip():
                wheres.append(where_clause.strip())
            filters = " AND ".join(wheres)
            request = "SELECT account_id as id, " + ', '.join(mapping.values()) + \
                      " FROM " + tables + \
                      " WHERE account_id IN %s " \
                      + filters + \
                      " GROUP BY account_id"
            params = (tuple(accounts._ids),) + tuple(where_params)
            request.env.cr.execute(request, params)
            for row in request.env.cr.dictfetchall():
                res[row['id']] = row
        return res

    def _compute_report_balance(self, reports):
        '''returns a dictionary with key=the ID of a record and value=the credit, debit and balance amount
           computed for this record. If the record is of type :
               'accounts' : it's the sum of the linked accounts
               'account_type' : it's the sum of leaf accoutns with such an account_type
               'account_report' : it's the amount of the related report
               'sum' : it's the sum of the children of this record (aka a 'view' record)'''
        res = {}
        fields = ['credit', 'debit', 'balance']
        for report in reports:
            if report.id in res:
                continue
            res[report.id] = dict((fn, 0.0) for fn in fields)
            if report.type == 'accounts':
                # it's the sum of the linked accounts
                res[report.id]['account'] = self._compute_account_balance(report.account_ids)
                for value in res[report.id]['account'].values():
                    for field in fields:
                        res[report.id][field] += value.get(field)
            elif report.type == 'account_type':
                # it's the sum the leaf accounts with such an account type
                accounts = request.env['account.account'].search([('user_type_id', 'in', report.account_type_ids.ids)])
                res[report.id]['account'] = self._compute_account_balance(accounts)
                for value in res[report.id]['account'].values():
                    for field in fields:
                        res[report.id][field] += value.get(field)
            elif report.type == 'account_report' and report.account_report_id:
                # it's the amount of the linked report
                res2 = self._compute_report_balance(report.account_report_id)
                for key, value in res2.items():
                    for field in fields:
                        res[report.id][field] += value[field]
            elif report.type == 'sum':
                # it's the sum of the children of this account.report
                res2 = self._compute_report_balance(report.children_ids)
                for key, value in res2.items():
                    for field in fields:
                        res[report.id][field] += value[field]
        return res

    def get_account_lines(self, data):
        print(data)
        lines = []
        account_report = request.env['account.financial.report'].search([('id', '=', data['account_report_id'][0])])
        child_reports = account_report._get_children_by_order()
        res = request.env.with_context(data.get('used_context'))._compute_report_balance(child_reports)
        if data['enable_filter']:
            comparison_res = request.env.with_context(data.get('comparison_context'))._compute_report_balance(
                child_reports)
            for report_id, value in comparison_res.items():
                res[report_id]['comp_bal'] = value['balance']
                report_acc = res[report_id].get('account')
                if report_acc:
                    for account_id, val in comparison_res[report_id].get('account').items():
                        report_acc[account_id]['comp_bal'] = val['balance']
        for report in child_reports:
            vals = {
                'name': report.name,
                'balance': res[report.id]['balance'] * float(report.sign),
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type or False,  # used to underline the financial report balances
            }
            if data['debit_credit']:
                vals['debit'] = res[report.id]['debit']
                vals['credit'] = res[report.id]['credit']

            if data['enable_filter']:
                vals['balance_cmp'] = res[report.id]['comp_bal'] * float(report.sign)

            lines.append(vals)
            if report.display_detail == 'no_detail':
                # the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if res[report.id].get('account'):
                sub_lines = []
                for account_id, value in res[report.id]['account'].items():
                    # if there are accounts to display, we add them to the lines with a level equals to their level in
                    # the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    # financial reports for Assets, liabilities...)
                    flag = False
                    account = request.env['account.account'].browse(account_id)
                    vals = {
                        'name': account.code + ' ' + account.name,
                        'balance': value['balance'] * float(report.sign) or 0.0,
                        'type': 'account',
                        'level': report.display_detail == 'detail_with_hierarchy' and 4,
                        'account_type': account.internal_type,
                    }
                    if data['debit_credit']:
                        vals['debit'] = value['debit']
                        vals['credit'] = value['credit']
                        if not account.company_id.currency_id.is_zero(
                                vals['debit']) or not account.company_id.currency_id.is_zero(vals['credit']):
                            flag = True
                    if not account.company_id.currency_id.is_zero(vals['balance']):
                        flag = True
                    if data['enable_filter']:
                        vals['balance_cmp'] = value['comp_bal'] * float(report.sign)
                        if not account.company_id.currency_id.is_zero(vals['balance_cmp']):
                            flag = True
                    if flag:
                        sub_lines.append(vals)
                lines += sorted(sub_lines, key=lambda sub_line: sub_line['name'])
        return lines

    @http.route([
        '/accounting_excel_reports/excel_report/<model("accounting.report"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_account_financial_excel_report(self, wizard=None, **args):
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
                ('Content-Disposition', content_disposition('Financial Report in Excel Format' + '.xlsx'))
            ]
        )

        # buat object workbook dari library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # buat style untuk mengatur jenis font, ukuran font, border dan alligment
        title_style = workbook.add_format({'font_name': 'Times', 'font_size': 20, 'bold': True, 'align': 'left'})
        title_style2 = workbook.add_format({'font_name': 'Times', 'font_size': 12, 'bold': True, 'align': 'left'})
        header_style = workbook.add_format(
            {'font_name': 'Times', 'bold': True, 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'center'})
        text_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'left'})

        text_style_number = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})

        text_style_number.set_num_format('"Rp" #,##0')
        text_style_persen = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})

        text_style_persen.set_num_format('0"%"')
        number_style = workbook.add_format(
            {'font_name': 'Times', 'left': 1, 'bottom': 1, 'right': 1, 'top': 1, 'align': 'right'})

        # loop user / sales person yang dipilih
        # buat worksheet / tab per user
        sheet = workbook.add_worksheet('Report Sales')
        # set orientation jadi landscape
        sheet.set_portrait()
        # set ukuran kertas, 9 artinya kertas A4
        sheet.set_paper(9)
        # set margin kertas dalam satuan inchi
        sheet.set_margins(0.5, 0.5, 0.5, 0.5)
        header3 = '&LPage &P of &N' + '&C'+wizard.company_id.name + '&R '+str(datetime.now())
        footer3 = '&LCurrent date: &D' + '&RCurrent time: &T'

        sheet.set_header(header3)
        sheet.set_footer(footer3)
        # set lebar kolom
        sheet.set_column('A:A', 5)
        sheet.set_column('B:N', 15)
        date_from=False
        if wizard.date_from:
            date_from = datetime.strftime(wizard.date_from, "%Y-%m-%d")
        date_to=False
        if wizard.date_to:
            date_to = datetime.strftime(wizard.date_to, "%Y-%m-%d")
        date_from_cmp=False
        if wizard.date_from_cmp:
            date_from_cmp = datetime.strftime(wizard.date_from_cmp, "%Y-%m-%d")
        date_to_cmp=False
        if wizard.date_to_cmp:
            date_to_cmp = datetime.strftime(wizard.date_to_cmp, "%Y-%m-%d")
        data = {'id': wizard.id,
                'date_from':  date_from,
                'date_to': date_to,
                'journal_ids': wizard.journal_ids or [],
                'target_move': wizard.target_move,
                'company_id': [wizard.company_id.id,wizard.company_id.name],
                'used_context': {
                    'journal_ids': wizard.journal_ids or False,
                    'state': wizard.target_move,
                    'date_from': date_from,
                    'date_to': date_to,
                    'strict_range': True if wizard.date_from else False,
                    'company_id': wizard.company_id.id,
                    'lang': get_lang(request.env).code
                },
                'date_from_cmp': date_from_cmp,
                'debit_credit': wizard.debit_credit,
                'date_to_cmp':date_to_cmp,
                'filter_cmp': wizard.filter_cmp,
                'account_report_id': [wizard.account_report_id.id, wizard.account_report_id.name],
                'enable_filter': wizard.enable_filter,
                'label_filter': wizard.label_filter,
                'comparison_context': {
                    'journal_ids': wizard.journal_ids or False,
                    'state': wizard.target_move,
                    'date_from': date_from_cmp,
                    'date_to': date_to_cmp,
                    'strict_range': True if wizard.date_from else False,
                }
            }
        # data = {'id': 6, 'date_from': False, 'date_to': False, 'journal_ids': [], 'target_move': 'posted',
        #         'company_id': [1, 'PT. Inti Teknologi Informasi'],
        #         'used_context': {'journal_ids': False, 'state': 'posted', 'date_from': False, 'date_to': False,
        #                          'strict_range': False, 'company_id': 1, 'lang': 'en_US'}, 'date_f rom_cmp': False,'debit_credit': False, 'date_to_cmp': False, 'filter_cmp': 'filter_no',
        #         'account_report_id': [26, 'Balance Sheet'], 'enable_filter': False, 'label_filter': False,
        #                              'comparison_context': {'journal_ids': False, 'state': 'posted'}}

        # data['ids'] = request.env.context.get('active_ids', [])
        # data['model'] = request.env.context.get('active_model', 'ir.ui.menu')
        # data['form'] = request.env['accounting.report'].read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0]
        # used_context = request.env['accounting.report']._build_contexts(data)
        # data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
        # print(data)
        # print("=========================")

        report_lines = request.env['report.accounting_pdf_reports.report_financial'].get_account_lines(data)

        # print(report_lines)
        # print("=========================")
        row=1
        sheet.write(row, 0, wizard.account_report_id.name, title_style)
        row+=1
        sheet.write(row, 0, "Target Move", title_style2)
        if date_from:
            sheet.write(row, 1,'Date from : '+ str(date_from), title_style2)
        row+=1
        if wizard.target_move == "posted":
            targetmove="All Posted Entries"
        else:
            targetmove='All Entries'
        sheet.write(row, 0,targetmove, title_style2)
        if date_to:
            sheet.write(row, 1,'Date to : '+ str(date_to), title_style2)
        row+=1
        sheet.write(row, 0, "Name", header_style)
        sheet.write(row, 1, "Balance", header_style)
        if wizard.enable_filter:
            sheet.write(row, 2, wizard.label_filter, header_style)
        row+=1
        row+=1

        sheet.set_column(0,0, 60)
        sheet.set_column(1,1, 15)
        sheet.set_column(2,2, 15)
        for lines in report_lines:
            level=''
            for l in range(int(lines['level'])):
                level+=' '
            sheet.write(row, 0, level+lines['name'], text_style)
            sheet.write(row, 1, lines['balance'], text_style_number)
            if wizard.enable_filter:
                sheet.write(row, 2, lines['balance_cmp'], text_style_number)
            row+=1


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response
