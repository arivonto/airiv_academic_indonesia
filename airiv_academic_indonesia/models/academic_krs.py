# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicKrs(models.Model):
    _name = 'academic.krs'
    _description = 'Kartu Rencana Studi (KRS) & Nilai KHS'
    _order = 'academic_year_id desc, semester desc'

    name = fields.Char(string="Nomor Registrasi KRS", required=True, default=lambda self: _('New'))
    student_id = fields.Many2one('academic.student', string="Peserta Didik", required=True, ondelete='cascade')
    academic_year_id = fields.Many2one('academic.year', string="Tahun Akademik", required=True)
    semester = fields.Integer(string="Semester", default=1, required=True)
    
    line_ids = fields.One2many('academic.krs.line', 'krs_id', string="Daftar Mata Kuliah / Pelajaran")
    total_sks = fields.Integer(string="Total SKS Diambil", compute="_compute_krs_summary", store=True)
    gpa_semester = fields.Float(string="Indeks Prestasi Semester (IPS)", compute="_compute_krs_summary", store=True)
    
    state = fields.Selection([
        ('draft', 'Pengajuan (Draft)'),
        ('submitted', 'Diajukan ke Dosen Wali'),
        ('approved', 'Disetujui (KRS Aktif)'),
        ('graded', 'Nilai Lengkap (KHS / Rapor Terbit)'),
    ], string="Status KRS", default='draft', required=True)

    pddikti_sync_status = fields.Selection([
        ('draft', 'Belum Dilaporkan ke Dikti'),
        ('synced', 'Tervalidasi di PDDikti Feeder (AKM & Nilai)'),
    ], string="Status Pelaporan PDDikti", default='draft', readonly=True)
    
    pddikti_sync_log = fields.Char(string="Token Log Sinkronisasi Dikti", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = f"KRS-{fields.Date.today().strftime('%Y%m')}-{self.env['ir.sequence'].next_by_code('academic.krs') or '0001'}"
        return super(AcademicKrs, self).create(vals_list)

    @api.depends('line_ids.credits', 'line_ids.grade_point', 'line_ids.state')
    def _compute_krs_summary(self):
        for rec in self:
            tot_sks = sum(rec.line_ids.mapped('credits'))
            rec.total_sks = tot_sks
            if tot_sks > 0:
                tot_weight = sum(line.credits * line.grade_point for line in rec.line_ids)
                rec.gpa_semester = round(tot_weight / tot_sks, 2)
            else:
                rec.gpa_semester = 0.0

    def action_submit_krs(self):
        self.write({'state': 'submitted'})

    def action_approve_krs(self):
        self.write({'state': 'approved'})

    def action_publish_khs(self):
        self.write({'state': 'graded'})

    def action_sync_krs_to_pddikti(self):
        self.ensure_one()
        gov_cfg = self.env['academic.government.config'].get_active_config()
        res = gov_cfg.pddikti_sync_krs_and_grades(self)
        self.write({
            'pddikti_sync_status': 'synced',
            'pddikti_sync_log': res['result'].get('id_sync', 'SYNCED_OK')
        })

class AcademicKrsLine(models.Model):
    _name = 'academic.krs.line'
    _description = 'Baris Mata Kuliah KRS & Nilai'

    krs_id = fields.Many2one('academic.krs', string="KRS Induk", required=True, ondelete='cascade')
    course_id = fields.Many2one('academic.course', string="Mata Kuliah / Pelajaran", required=True)
    credits = fields.Integer(related='course_id.credits', string="SKS", readonly=True)

    # Numerical Grading 0-100
    grade_assignment = fields.Float(string="Nilai Tugas / Praktikum", default=80.0)
    grade_uts = fields.Float(string="Nilai UTS", default=80.0)
    grade_uas = fields.Float(string="Nilai UAS", default=80.0)
    
    grade_final_num = fields.Float(string="Nilai Akhir (Angka)", compute="_compute_final_grade", store=True)
    grade_letter = fields.Char(string="Nilai Huruf", compute="_compute_final_grade", store=True)
    grade_point = fields.Float(string="Bobot Mutu (0.0 - 4.0)", compute="_compute_final_grade", store=True)
    state = fields.Selection([('ongoing', 'Sedang Ditempuh'), ('passed', 'Lulus'), ('failed', 'Mengulang')], string="Status Matkul", compute="_compute_final_grade", store=True)

    @api.depends('grade_assignment', 'grade_uts', 'grade_uas')
    def _compute_final_grade(self):
        for line in self:
            # Standar Bobot: 30% Tugas + 35% UTS + 35% UAS
            final_num = (line.grade_assignment * 0.3) + (line.grade_uts * 0.35) + (line.grade_uas * 0.35)
            line.grade_final_num = round(final_num, 2)

            if final_num >= 85.0:
                line.grade_letter = 'A'
                line.grade_point = 4.0
                line.state = 'passed'
            elif final_num >= 75.0:
                line.grade_letter = 'B'
                line.grade_point = 3.0
                line.state = 'passed'
            elif final_num >= 65.0:
                line.grade_letter = 'C'
                line.grade_point = 2.0
                line.state = 'passed'
            elif final_num >= 50.0:
                line.grade_letter = 'D'
                line.grade_point = 1.0
                line.state = 'failed'
            else:
                line.grade_letter = 'E'
                line.grade_point = 0.0
                line.state = 'failed'
