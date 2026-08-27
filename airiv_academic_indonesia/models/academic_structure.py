# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Tahun Ajaran / Tahun Akademik'
    _order = 'name desc'

    name = fields.Char(string="Tahun Akademik", required=True, placeholder="misal: 2026/2027 Ganjil")
    code = fields.Char(string="Kode Periode", required=True, placeholder="20261")
    semester_type = fields.Selection([
        ('ganjil', 'Semester Ganjil'),
        ('genap', 'Semester Genap'),
        ('pendek', 'Semester Pendek / Antara'),
    ], string="Tipe Semester", default='ganjil', required=True)

    date_start = fields.Date(string="Tanggal Mulai", required=True)
    date_end = fields.Date(string="Tanggal Selesai", required=True)
    is_active = fields.Boolean(string="Semester Aktif", default=True)

class AcademicFaculty(models.Model):
    _name = 'academic.faculty'
    _description = 'Fakultas / Unit Pendidikan'

    name = fields.Char(string="Nama Fakultas / Unit", required=True, placeholder="misal: Fakultas Ilmu Komputer")
    code = fields.Char(string="Kode Fakultas", required=True)
    dean_name = fields.Char(string="Nama Dekan / Kepala Unit")

class AcademicProgram(models.Model):
    _name = 'academic.program'
    _description = 'Program Studi / Jenjang Kelas'
    _order = 'name asc'

    name = fields.Char(string="Nama Program Studi / Jurusan", required=True, placeholder="misal: S1 Informatika / XII MIPA 1")
    code = fields.Char(string="Kode Prodi", required=True)
    faculty_id = fields.Many2one('academic.faculty', string="Fakultas / Unit")
    
    tier = fields.Selection([
        ('school_k12', 'K-12 (SD / SMP / SMA / SMK)'),
        ('pesantren', 'Pondok Pesantren / Madrasah'),
        ('academy', 'Akademi / Vokasi (D3/D4)'),
        ('university', 'Universitas (S1 / S2 / Profesi)'),
    ], string="Jenjang Institusi", default='university', required=True)

    degree_level = fields.Selection([
        ('sd', 'Sekolah Dasar (SD/MI)'),
        ('smp', 'Sekolah Menengah Pertama (SMP/MTs)'),
        ('sma', 'Sekolah Menengah Atas (SMA/SMK/MA)'),
        ('d3', 'Diploma Tiga (D3)'),
        ('s1', 'Sarjana (S1)'),
        ('s2', 'Magister (S2)'),
    ], string="Tingkat Kelulusan", default='s1')

class AcademicCourse(models.Model):
    _name = 'academic.course'
    _description = 'Mata Pelajaran / Mata Kuliah'

    name = fields.Char(string="Nama Mata Kuliah / Pelajaran", required=True)
    code = fields.Char(string="Kode Matkul / Mapel", required=True)
    program_id = fields.Many2one('academic.program', string="Program Studi / Jurusan", required=True)
    credits = fields.Integer(string="Bobot SKS / Jam", default=3, required=True)
    semester_recommended = fields.Integer(string="Semester Rekomendasi", default=1)
