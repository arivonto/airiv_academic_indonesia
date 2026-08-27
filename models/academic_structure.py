# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Tahun Akademik & Kurikulum'
    _order = 'code desc, id desc'

    name = fields.Char(string="Tahun Akademik", required=True)
    code = fields.Char(string="Kode Periode", required=True)
    semester_type = fields.Selection([
        ('ganjil', 'Semester Ganjil'),
        ('genap', 'Semester Genap'),
        ('pendek', 'Semester Antara / Pendek'),
    ], string="Tipe Semester", default='ganjil', required=True)
    semester = fields.Selection([
        ('ganjil', 'Semester Ganjil'),
        ('genap', 'Semester Genap'),
        ('pendek', 'Semester Antara / Pendek'),
    ], string="Semester", default='ganjil')
    date_start = fields.Date(string="Tanggal Mulai", required=True)
    date_end = fields.Date(string="Tanggal Selesai", required=True)
    is_active = fields.Boolean(string="Status Aktif", default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Aktif'),
        ('closed', 'Tutup Buku'),
    ], string="Status", default='active', required=True)
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)

    @api.onchange('semester_type')
    def _onchange_semester_type(self):
        if self.semester_type:
            self.semester = self.semester_type

    @api.onchange('semester')
    def _onchange_semester(self):
        if self.semester:
            self.semester_type = self.semester


class AcademicFaculty(models.Model):
    _name = 'academic.faculty'
    _description = 'Fakultas / Departemen'
    _order = 'code asc'

    name = fields.Char(string="Nama Fakultas", required=True)
    code = fields.Char(string="Kode Fakultas", required=True)
    dekan_id = fields.Many2one('res.partner', string="Dekan / Pimpinan")
    program_ids = fields.One2many('academic.program', 'faculty_id', string="Program Studi")
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)


class AcademicProgram(models.Model):
    _name = 'academic.program'
    _description = 'Program Studi / Jurusan'
    _order = 'code asc'

    name = fields.Char(string="Nama Program Studi", required=True)
    code = fields.Char(string="Kode Prodi (PDDikti)", required=True)
    degree = fields.Selection([
        ('d3', 'Diploma 3 (D3)'),
        ('d4', 'Sarjana Terapan (D4)'),
        ('s1', 'Sarjana (S1)'),
        ('s2', 'Magister (S2)'),
        ('s3', 'Doktor (S3)'),
        ('k12', 'Pendidikan Dasar/Menengah'),
        ('pesantren', 'Pondok Pesantren'),
    ], string="Jenjang Pendidikan", default='s1', required=True)
    faculty_id = fields.Many2one('academic.faculty', string="Fakultas")
    kaprodi_id = fields.Many2one('res.partner', string="Ketua Program Studi")
    total_sks_graduation = fields.Integer(string="Beban SKS Kelulusan", default=144)
    company_id = fields.Many2one('res.company', string="Institusi", default=lambda self: self.env.company)


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
