# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AcademicStudent(models.Model):
    _name = 'academic.student'
    _description = 'Master Siswa / Mahasiswa / Santri'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string="Nama Lengkap", required=True, tracking=True)
    student_type = fields.Selection([
        ('school', 'Siswa Sekolah (K-12)'),
        ('pesantren', 'Santri Pesantren'),
        ('university', 'Mahasiswa Perguruan Tinggi'),
    ], string="Status Peserta Didik", default='university', required=True)

    # Indonesian Identification Rails
    nim = fields.Char(string="NIM (Nomor Induk Mahasiswa)", index=True, tracking=True)
    nisn = fields.Char(string="NISN (Kemendikbudristek)", index=True, size=10, help="10 digit nomor NISN nasional")
    nis = fields.Char(string="NIS (Nomor Induk Siswa)", index=True)
    nik = fields.Char(string="NIK KTP / KK (16 Digit)", size=16, tracking=True)
    
    gender = fields.Selection([('male', 'Laki-laki'), ('female', 'Perempuan')], string="Jenis Kelamin", required=True, default='male')
    birth_place = fields.Char(string="Tempat Lahir")
    birth_date = fields.Date(string="Tanggal Lahir")
    
    # Academic Association
    program_id = fields.Many2one('academic.program', string="Program Studi / Jurusan", required=True, tracking=True)
    faculty_id = fields.Many2one(related='program_id.faculty_id', string="Fakultas", readonly=True, store=True)
    current_semester = fields.Integer(string="Semester Berjalan", default=1)
    academic_status = fields.Selection([
        ('active', 'Aktif'),
        ('leave', 'Cuti Akademik'),
        ('graduated', 'Lulus / Alumni'),
        ('dropped_out', 'Keluar / Drop Out'),
    ], string="Status Akademik", default='active', tracking=True)

    # Guardian & WhatsApp Details
    parent_name = fields.Char(string="Nama Wali / Orang Tua")
    parent_mobile = fields.Char(string="WhatsApp Wali / Murid", required=True, tracking=True, help="Nomor WA aktif format +628...")
    address = fields.Text(string="Alamat Domisili")

    # Financial Configuration
    ukt_tier = fields.Selection([
        ('ukt_1', 'Kelompok UKT 1 (Rp 500.000)'),
        ('ukt_2', 'Kelompok UKT 2 (Rp 1.000.000)'),
        ('ukt_3', 'Kelompok UKT 3 (Rp 2.500.000)'),
        ('ukt_4', 'Kelompok UKT 4 (Rp 4.000.000)'),
        ('ukt_5', 'Kelompok UKT 5 (Rp 6.000.000)'),
        ('ukt_6', 'Kelompok UKT 6 (Rp 8.000.000)'),
        ('ukt_7', 'Kelompok UKT 7 (Rp 10.000.000)'),
        ('ukt_8', 'Kelompok UKT 8 (Rp 12.500.000)'),
    ], string="Kelompok UKT (Universitas)", default='ukt_3')

    spp_monthly_amount = fields.Float(string="Tarif SPP Bulanan (Sekolah/Pesantren)", default=750000.0)
    partner_id = fields.Many2one('res.partner', string="Kontak Mitra (Invoicing)", readonly=True)

    # GPA / Academic Performance
    krs_ids = fields.One2many('academic.krs', 'student_id', string="Riwayat KRS / Rapor")
    gpa_cumulative = fields.Float(string="IPK Kumulatif", compute="_compute_cumulative_gpa", store=True)

    # Government Sync Metadata
    gov_sync_status = fields.Selection([
        ('not_synced', 'Belum Sinkron'),
        ('synced_pddikti', 'Terdaftar di PDDikti Feeder'),
        ('synced_dapodik', 'Terdaftar di Dapodik'),
        ('synced_emis', 'Terdaftar di EMIS 4.0 Kemenag'),
    ], string="Status Sinkronisasi Pemerintah", default='not_synced', tracking=True)

    gov_sync_id = fields.Char(string="ID Referensi Registrasi Pemerintah", readonly=True)
    
    # Graduation & PIN / SIVIL Diploma Management
    is_graduated = fields.Boolean(string="Status Kelulusan / Alumni", default=False, tracking=True)
    graduation_date = fields.Date(string="Tanggal Kelulusan (SK Yudisium)")
    pin_ijazah_number = fields.Char(string="PIN (Penomoran Ijazah Nasional)", readonly=True, index=True)
    sivil_verification_url = fields.Char(string="Tautan Verifikasi SIVIL Kemendikbud", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        Partner = self.env['res.partner'].sudo()
        for vals in vals_list:
            partner = Partner.create({
                'name': vals.get('name'),
                'phone': vals.get('parent_mobile'),
                'mobile': vals.get('parent_mobile'),
                'street': vals.get('address'),
                'customer_rank': 1,
            })
            vals['partner_id'] = partner.id
        return super(AcademicStudent, self).create(vals_list)

    @api.depends('krs_ids.gpa_semester', 'krs_ids.total_sks', 'krs_ids.state')
    def _compute_cumulative_gpa(self):
        for student in self:
            approved_krs = student.krs_ids.filtered(lambda k: k.state in ['approved', 'graded'])
            total_sks = sum(approved_krs.mapped('total_sks'))
            if total_sks > 0:
                weighted_sum = sum(k.gpa_semester * k.total_sks for k in approved_krs)
                student.gpa_cumulative = round(weighted_sum / total_sks, 2)
            else:
                student.gpa_cumulative = 0.0

    def action_sync_to_government_portal(self):
        self.ensure_one()
        gov_cfg = self.env['academic.government.config'].get_active_config()
        if self.student_type == 'university':
            token_res = gov_cfg.pddikti_get_token()
            self.gov_sync_status = 'synced_pddikti'
            self.gov_sync_id = f"PDDIKTI-{self.nim}-{gov_cfg.execution_mode.upper()}"
        elif self.student_type == 'school':
            res = gov_cfg.dapodik_sync_student(self)
            self.gov_sync_status = 'synced_dapodik'
            self.gov_sync_id = res.get('sync_id')
        else:
            res = gov_cfg.emis_sync_santri(self)
            self.gov_sync_status = 'synced_emis'
            self.gov_sync_id = res.get('emis_sync_token')

    def action_issue_national_diploma_pin(self):
        self.ensure_one()
        gov_cfg = self.env['academic.government.config'].get_active_config()
        pin, sivil_url = gov_cfg.generate_pin_and_sivil_url(self)
        self.write({
            'is_graduated': True,
            'graduation_date': fields.Date.today(),
            'pin_ijazah_number': pin,
            'sivil_verification_url': sivil_url,
        })
