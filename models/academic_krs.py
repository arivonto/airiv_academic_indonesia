# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicCourse(models.Model):
    _name = 'academic.course'
    _description = 'Mata Kuliah / Pelajaran'
    _order = 'code asc'

    name = fields.Char(string="Nama Mata Kuliah", required=True)
    code = fields.Char(string="Kode MK", required=True)
    sks = fields.Integer(string="Bobot SKS", default=3, required=True)
    credits = fields.Integer(string="Credits / SKS", default=3, required=True)
    semester_recommended = fields.Integer(string="Semester Rekomendasi", default=1)
    program_id = fields.Many2one('academic.program', string="Program Studi", required=True)
    faculty_id = fields.Many2one('academic.faculty', string="Fakultas", related="program_id.faculty_id", store=True)
    lecturer_id = fields.Many2one('res.partner', string="Dosen Pengampu")
    is_active = fields.Boolean(string="Aktif", default=True)
    state = fields.Selection([
        ('active', 'Aktif'),
        ('inactive', 'Nonaktif'),
    ], string="Status", default='active', required=True)
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)

    @api.onchange('sks')
    def _onchange_sks(self):
        if self.sks:
            self.credits = self.sks

    @api.onchange('credits')
    def _onchange_credits(self):
        if self.credits:
            self.sks = self.credits


class AcademicKrs(models.Model):
    _name = 'academic.krs'
    _description = 'Kartu Rencana Studi (KRS) Mahasiswa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string="Nomor KRS", default="New", copy=False, readonly=True)
    student_id = fields.Many2one('academic.student', string="Mahasiswa / Siswa", required=True, tracking=True)
    nim = fields.Char(string="NIM / NISN", related="student_id.nim", readonly=True)
    program_id = fields.Many2one('academic.program', string="Program Studi", related="student_id.program_id", readonly=True)
    
    # Dual-aliased Year ID for compatibility
    academic_year_id = fields.Many2one('academic.year', string="Tahun Akademik", required=True, tracking=True)
    year_id = fields.Many2one('academic.year', string="Tahun Akademik (Alias)", related="academic_year_id", store=True, readonly=False)
    semester_type = fields.Selection(string="Semester", related="academic_year_id.semester_type", readonly=True)
    semester = fields.Selection(string="Semester (Alias)", related="academic_year_id.semester_type", readonly=True)
    
    line_ids = fields.One2many('academic.krs.line', 'krs_id', string="Daftar Mata Kuliah")
    total_sks = fields.Integer(string="Total SKS", compute="_compute_total_sks", store=True)
    gpa_semester = fields.Float(string="IPS (Indeks Prestasi Semester)", compute="_compute_gpa", store=True, digits=(3, 2))
    
    state = fields.Selection([
        ('draft', 'Draft (Pengisian)'),
        ('submitted', 'Diajukan'),
        ('approved', 'Disetujui Dosen PA'),
        ('graded', 'Nilai Terkunci'),
    ], string="Status KRS", default='draft', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('academic_year_id') and vals.get('year_id'):
                vals['academic_year_id'] = vals.get('year_id')
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('academic.krs') or _('KRS/%s') % fields.Date.today().strftime('%Y%m%d')
        return super().create(vals_list)

    @api.depends('line_ids.sks', 'line_ids.credits')
    def _compute_total_sks(self):
        for rec in self:
            rec.total_sks = sum(line.sks or line.credits or 0 for line in rec.line_ids)

    @api.depends('line_ids.grade_point', 'line_ids.sks', 'line_ids.credits')
    def _compute_gpa(self):
        for rec in self:
            total_weight = 0.0
            total_credits = 0
            for line in rec.line_ids:
                c = line.sks or line.credits or 0
                if c > 0 and line.grade_point is not False:
                    total_weight += (line.grade_point * c)
                    total_credits += c
            rec.gpa_semester = (total_weight / total_credits) if total_credits > 0 else 0.0

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_lock_grades(self):
        self.write({'state': 'graded'})


class AcademicKrsLine(models.Model):
    _name = 'academic.krs.line'
    _description = 'Item Mata Kuliah KRS'

    krs_id = fields.Many2one('academic.krs', string="KRS Header", ondelete='cascade', required=True)
    course_id = fields.Many2one('academic.course', string="Mata Kuliah", required=True)
    sks = fields.Integer(string="SKS", related="course_id.sks", readonly=True, store=True)
    credits = fields.Integer(string="Credits", related="course_id.credits", readonly=True, store=True)
    lecturer_id = fields.Many2one('res.partner', string="Dosen", related="course_id.lecturer_id", readonly=True)
    score_attendance = fields.Float(string="Presensi (10%)", default=100.0)
    score_assignment = fields.Float(string="Tugas (20%)", default=0.0)
    score_uts = fields.Float(string="UTS (30%)", default=0.0)
    score_uas = fields.Float(string="UAS (40%)", default=0.0)
    score_final = fields.Float(string="Nilai Akhir", compute="_compute_score_final", store=True, digits=(5, 2))
    grade_letter = fields.Selection([
        ('A', 'A (4.00)'),
        ('AB', 'AB (3.50)'),
        ('B', 'B (3.00)'),
        ('BC', 'BC (2.50)'),
        ('C', 'C (2.00)'),
        ('D', 'D (1.00)'),
        ('E', 'E (0.00)'),
    ], string="Huruf Mutu", compute="_compute_score_final", store=True)
    grade_point = fields.Float(string="Bobot Angka", compute="_compute_score_final", store=True, digits=(3, 2))

    @api.depends('score_attendance', 'score_assignment', 'score_uts', 'score_uas')
    def _compute_score_final(self):
        for line in self:
            final = (line.score_attendance * 0.10) + (line.score_assignment * 0.20) + (line.score_uts * 0.30) + (line.score_uas * 0.40)
            line.score_final = final
            if final >= 85:
                line.grade_letter, line.grade_point = 'A', 4.00
            elif final >= 75:
                line.grade_letter, line.grade_point = 'AB', 3.50
            elif final >= 65:
                line.grade_letter, line.grade_point = 'B', 3.00
            elif final >= 60:
                line.grade_letter, line.grade_point = 'BC', 2.50
            elif final >= 55:
                line.grade_letter, line.grade_point = 'C', 2.00
            elif final >= 40:
                line.grade_letter, line.grade_point = 'D', 1.00
            else:
                line.grade_letter, line.grade_point = 'E', 0.00
