# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicStudent(models.Model):
    _name = 'academic.student'
    _description = 'Master Mahasiswa / Siswa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'nim asc, name asc'

    name = fields.Char(string="Nama Lengkap", required=True, tracking=True)
    nim = fields.Char(string="NIM / NISN", required=True, copy=False, index=True, tracking=True)
    nik = fields.Char(string="NIK (KTP)", size=16, tracking=True)
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string="Jenis Kelamin", default='male', required=True)
    email = fields.Char(string="Email", tracking=True)
    phone = fields.Char(string="WhatsApp / No. HP", tracking=True)
    
    # Academic Placement
    faculty_id = fields.Many2one('academic.faculty', string="Fakultas", related="program_id.faculty_id", store=True)
    program_id = fields.Many2one('academic.program', string="Program Studi", required=True, tracking=True)
    academic_year_id = fields.Many2one('academic.year', string="Tahun Masuk (Angkatan)", required=True)
    year_id = fields.Many2one('academic.year', string="Angkatan", related="academic_year_id", store=True)
    academic_advisor_id = fields.Many2one('res.partner', string="Dosen Pembimbing Akademik (PA)", tracking=True)
    
    # Performance & Status
    gpa_cumulative = fields.Float(string="IPK (Kumulatif)", compute="_compute_academic_performance", store=True, digits=(3, 2))
    total_sks_earned = fields.Integer(string="Total SKS Lulus", compute="_compute_academic_performance", store=True)
    current_semester = fields.Integer(string="Semester Berjalan", default=1)
    
    krs_ids = fields.One2many('academic.krs', 'student_id', string="Riwayat KRS")
    
    state = fields.Selection([
        ('active', 'Aktif'),
        ('leave', 'Cuti Akademik'),
        ('graduated', 'Lulus'),
        ('dropout', 'Drop Out / Keluar'),
    ], string="Status Mahasiswa", default='active', required=True, tracking=True)
    
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)

    @api.depends('krs_ids.state', 'krs_ids.total_sks', 'krs_ids.gpa_semester')
    def _compute_academic_performance(self):
        for rec in self:
            approved_krs = rec.krs_ids.filtered(lambda k: k.state in ['approved', 'graded'])
            total_credits = 0
            total_weight = 0.0
            for krs in approved_krs:
                total_credits += krs.total_sks
                total_weight += (krs.gpa_semester * krs.total_sks)
            
            rec.total_sks_earned = total_credits
            rec.gpa_cumulative = (total_weight / total_credits) if total_credits > 0 else 0.0
