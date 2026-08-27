# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AcademicBillingWizard(models.TransientModel):
    _name = 'academic.billing.wizard'
    _description = 'Batch SPP & UKT Billing Generator'

    billing_type = fields.Selection([
        ('spp_monthly', 'SPP Bulanan (Sekolah / Pesantren)'),
        ('ukt_semester', 'UKT Semesteran (Universitas / Institut)'),
        ('building_fee', 'Uang Gedung / DPP / Uang Pangkal'),
    ], string="Jenis Tagihan", default='spp_monthly', required=True)

    academic_year_id = fields.Many2one('academic.year', string="Tahun Akademik", required=True)
    month_name = fields.Selection([
        ('01', 'Januari'), ('02', 'Februari'), ('03', 'Maret'), ('04', 'April'),
        ('05', 'Mei'), ('06', 'Juni'), ('07', 'Juli'), ('08', 'Agustus'),
        ('09', 'September'), ('10', 'Oktober'), ('11', 'November'), ('12', 'Desember')
    ], string="Bulan Tagihan SPP", default='08')

    program_id = fields.Many2one('academic.program', string="Program Studi / Kelas (Opsional, Kosongkan untuk Semua)")

    def action_generate_batch_invoices(self):
        self.ensure_one()
        Student = self.env['academic.student']
        Invoice = self.env['account.move']
        
        domain = [('academic_status', '=', 'active')]
        if self.program_id:
            domain.append(('program_id', '=', self.program_id.id))
        
        students = Student.search(domain)
        if not students:
            raise UserError(_("Tidak ada peserta didik aktif yang ditemukan untuk kriteria ini."))

        created_invoices = Invoice
        for st in students:
            if self.billing_type == 'spp_monthly':
                amount = st.spp_monthly_amount or 750000.0
                desc = f"SPP Bulanan {dict(self._fields['month_name'].selection).get(self.month_name)} - {st.name} ({st.nisn or st.nis or 'Siswa'})"
            elif self.billing_type == 'ukt_semester':
                tier_prices = {
                    'ukt_1': 500000.0, 'ukt_2': 1000000.0, 'ukt_3': 2500000.0, 'ukt_4': 4000000.0,
                    'ukt_5': 6000000.0, 'ukt_6': 8000000.0, 'ukt_7': 10000000.0, 'ukt_8': 12500000.0,
                }
                amount = tier_prices.get(st.ukt_tier, 3000000.0)
                desc = f"UKT {self.academic_year_id.name} - {st.name} ({st.nim or 'Mhs'})"
            else:
                amount = 2500000.0
                desc = f"Uang Pangkal / DPP - {st.name}"

            inv = Invoice.create({
                'move_type': 'out_invoice',
                'partner_id': st.partner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'name': desc,
                    'quantity': 1.0,
                    'price_unit': amount,
                })]
            })
            created_invoices += inv

        return {
            'name': _('Draf Tagihan Pendidikan Dibuat'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created_invoices.ids)],
        }
