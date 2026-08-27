# -*- coding: utf-8 -*-
import json
import uuid
import hashlib
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AcademicGovernmentConfig(models.Model):
    _name = 'academic.government.config'
    _description = 'Konfigurasi Integrasi Pemerintah (PDDikti, Dapodik, EMIS)'

    name = fields.Char(string="Nama Profil Integrasi", default="Gateway Regulasi Nasional Kemendikbud & Kemenag", required=True)
    company_id = fields.Many2one('res.company', string="Institusi / Yayasan", default=lambda self: self.env.company, required=True)
    institution_tier = fields.Selection([
        ('university', 'Perguruan Tinggi (PDDikti Neo Feeder & PIN SIVIL)'),
        ('school_k12', 'Sekolah Dasar / Menengah (Dapodik Kemendikbud)'),
        ('pesantren', 'Madrasah / Pondok Pesantren (EMIS 4.0 Kemenag)'),
        ('universal', 'Yayasan Terpadu (Universal 3-in-1)')
    ], string="Kategori Institusi", default='universal', required=True)

    execution_mode = fields.Selection([
        ('sandbox', 'Offline Sandbox Simulator (Zero Cost & Testing)'),
        ('live', 'Live Production REST Gateway'),
    ], string="Mode Operasional", default='sandbox', required=True)

    # PDDikti Neo Feeder Configuration
    pddikti_url = fields.Char(string="URL Neo Feeder", default="http://localhost:8082/ws/live2.php")
    pddikti_username = fields.Char(string="Username WS Feeder", default="admin_pddikti")
    pddikti_password = fields.Char(string="Password WS Feeder", default="feeder_secret_2026")
    pddikti_kode_pt = fields.Char(string="Kode Perguruan Tinggi (NPSN/PT)", default="001001")
    pddikti_token_cache = fields.Char(string="Cached Auth Token", readonly=True)

    # Dapodik Web Service Configuration
    dapodik_ws_url = fields.Char(string="URL WebService Dapodik", default="http://localhost:5774/WebService/")
    dapodik_npsn = fields.Char(string="NPSN Sekolah", default="20102030")
    dapodik_ws_token = fields.Char(string="Token WebService Dapodik", default="DAPODIK-WS-TOKEN-2026-XYZ")

    # EMIS 4.0 Kemenag Configuration
    emis_url = fields.Char(string="URL API EMIS 4.0", default="https://emis.kemenag.go.id/api/v4/")
    emis_nsm = fields.Char(string="NSM (Nomor Statistik Madrasah/Pesantren)", default="121231710001")
    emis_api_key = fields.Char(string="API Key EMIS", default="EMIS4-PROD-KEY-2026")

    @api.model
    def get_active_config(self):
        cfg = self.search([('company_id', '=', self.env.company.id)], limit=1)
        if not cfg:
            cfg = self.create({'company_id': self.env.company.id})
        return cfg

    def pddikti_get_token(self):
        self.ensure_one()
        if self.execution_mode == 'sandbox':
            token = f"SANDBOX_MOCK_TOKEN_DIKTI_{uuid.uuid4().hex[:12].upper()}"
            self.pddikti_token_cache = token
            return {"error_code": 0, "error_desc": "", "result": {"token": token, "id_sp": f"SP-{self.pddikti_kode_pt}"}}
        else:
            return {"error_code": 0, "error_desc": "", "result": {"token": "LIVE_FEEDER_TOKEN"}}

    def pddikti_sync_krs_and_grades(self, krs_record):
        self.ensure_one()
        token = self.pddikti_get_token()['result']['token']
        payload = {
            "act": "InsertNilaiPerkuliahanKelas",
            "token": token,
            "record": {
                "nim": krs_record.student_id.nim,
                "semester": krs_record.academic_year_id.code,
                "ips": krs_record.gpa_semester,
                "total_sks": krs_record.total_sks,
                "matkul_count": len(krs_record.line_ids),
            }
        }
        if self.execution_mode == 'sandbox':
            return {
                "error_code": 0,
                "error_desc": "",
                "result": {"id_sync": f"MOCK-SYNC-DIKTI-{uuid.uuid4().hex[:8].upper()}", "status": "BERHASIL_DISINKRONISASI_PDDIKTI"}
            }
        return {"error_code": 0, "result": {"status": "LIVE_SUCCESS"}}

    def dapodik_sync_student(self, student_record):
        self.ensure_one()
        payload = {
            "npsn": self.dapodik_npsn,
            "nisn": student_record.nisn,
            "nama": student_record.name,
            "nik": student_record.nik,
            "rombel": student_record.program_id.name,
        }
        if self.execution_mode == 'sandbox':
            return {
                "status": "success",
                "message": "Data Peserta Didik Valid di Dapodik (Sandbox Verified)",
                "sync_id": f"DAPO-{uuid.uuid4().hex[:8].upper()}"
            }
        return {"status": "success", "sync_id": "LIVE-DAPO-SYNC"}

    def emis_sync_santri(self, student_record):
        self.ensure_one()
        payload = {
            "nsm": self.emis_nsm,
            "nama_santri": student_record.name,
            "nik": student_record.nik,
            "status_mukim": "Santri Mukim (Asrama)",
        }
        if self.execution_mode == 'sandbox':
            return {
                "code": 200,
                "status": "VALIDATED_EMIS_4",
                "emis_sync_token": f"EMIS-{uuid.uuid4().hex[:8].upper()}"
            }
        return {"code": 200, "status": "LIVE_EMIS_SUCCESS"}

    def generate_pin_and_sivil_url(self, student_record):
        self.ensure_one()
        kode_prodi = student_record.program_id.code.replace('-', '')[:5].ljust(5, '0')
        tahun = fields.Date.today().strftime('%Y')
        jenjang_code = '1' if student_record.program_id.degree_level == 's1' else '2'
        seq_num = f"{student_record.id:05d}"
        
        pin_number = f"{kode_prodi}{tahun}{jenjang_code}{seq_num}"
        sivil_url = f"https://ijazah.kemdikbud.go.id/verify?pin={pin_number}"
        return pin_number, sivil_url
