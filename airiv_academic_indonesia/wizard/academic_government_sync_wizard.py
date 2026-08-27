# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AcademicGovernmentSyncWizard(models.TransientModel):
    _name = 'academic.government.sync.wizard'
    _description = 'Universal Government Integration Sync Wizard'

    target_portal = fields.Selection([
        ('pddikti_feeder', 'PDDikti Neo Feeder (KRS, KHS & AKM Semester)'),
        ('dapodik_k12', 'Dapodik Kemendikbud (Peserta Didik & Rombel K-12)'),
        ('emis_kemenag', 'EMIS 4.0 Kemenag (Santri & Madrasah BOSP)'),
        ('pin_sivil_batch', 'Batch Penerbitan PIN & SIVIL Ijazah Nasional'),
    ], string="Portal Sasaran Integrasi", default='pddikti_feeder', required=True)

    academic_year_id = fields.Many2one('academic.year', string="Tahun Akademik", required=True)
    summary_report = fields.Text(string="Hasil Laporan Sinkronisasi", readonly=True)

    def action_execute_batch_government_sync(self):
        self.ensure_one()
        gov_cfg = self.env['academic.government.config'].get_active_config()
        Student = self.env['academic.student']
        Krs = self.env['academic.krs']
        
        sync_count = 0
        if self.target_portal == 'pddikti_feeder':
            krs_records = Krs.search([('academic_year_id', '=', self.academic_year_id.id), ('state', '=', 'graded')])
            for k in krs_records:
                k.action_sync_krs_to_pddikti()
                sync_count += 1
            msg = f"Berhasil menyinkronkan {sync_count} record KRS/AKM ke PDDikti Neo Feeder (Mode: {gov_cfg.execution_mode.upper()})."

        elif self.target_portal == 'dapodik_k12':
            students = Student.search([('student_type', '=', 'school'), ('academic_status', '=', 'active')])
            for st in students:
                st.action_sync_to_government_portal()
                sync_count += 1
            msg = f"Berhasil memvalidasi {sync_count} siswa K-12 ke Dapodik Local WebService."

        elif self.target_portal == 'emis_kemenag':
            students = Student.search([('student_type', '=', 'pesantren'), ('academic_status', '=', 'active')])
            for st in students:
                st.action_sync_to_government_portal()
                sync_count += 1
            msg = f"Berhasil menyinkronkan {sync_count} santri ke EMIS 4.0 Kemenag."

        else:
            students = Student.search([('student_type', '=', 'university'), ('academic_status', '=', 'active')])
            for st in students:
                st.action_issue_national_diploma_pin()
                sync_count += 1
            msg = f"Berhasil menerbitkan {sync_count} PIN Ijazah Nasional & Tautan Verifikasi SIVIL."

        self.summary_report = msg
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'academic.government.sync.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
