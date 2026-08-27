# -*- coding: utf-8 -*-
{
    'name': 'Indonesia Academic ERP & Universal Government Bridge (PDDikti, Dapodik, EMIS & PIN SIVIL)',
    'version': '18.0.1.0.0',
    'category': 'Services/Education',
    'summary': 'All-in-One Academic ERP with Universal Government Integration: PDDikti Neo Feeder REST, Dapodik K-12, Kemenag EMIS 4.0, and PIN SIVIL Diploma Verification for Odoo 18',
    'description': """
Comprehensive Indonesian Academic, School, and Campus Management ERP Suite for Odoo 18 Community Edition.
Equipped with an integrated Universal Government Integration Bridge for Indonesian regulatory reporting:

1. PDDikti Neo Feeder REST Gateway (Universitas, Institut, Politeknik, Akademi):
   - Direct JSON-RPC/REST connection to campus Neo Feeder servers (GetToken, InsertMahasiswa, InsertKRSMahasiswa, InsertNilai, InsertAKM).
   - Semester Academic Activity reporting (Aktivitas Kuliah Mahasiswa / AKM: IPS, IPK, SKS).
2. Dapodik Local Web Services (Sekolah K-12: SD, SMP, SMA, SMK):
   - Local WebService integration for Peserta Didik, Rombel, and GTK synchronization.
   - NISN (Kemendikbudristek 10-digit) and NIK validation.
3. EMIS 4.0 Kemenag (Madrasah & Pondok Pesantren):
   - Santri Mukim vs Santri Kalong registry, Asrama management, and BOSP feeder.
4. PIN (Penomoran Ijazah Nasional) & SIVIL Diploma Verification:
   - 14-to-16 digit standardized PIN reservation and cryptographic check-digit calculator.
   - Direct QR Code generation linking to SIVIL Kemendikbud verification portal.
5. Multi-Mode Architecture:
   - Native Offline Sandbox Simulation mode for zero-cost risk-free testing without live API keys.
   - 100% Odoo 18 Community Native - Always Free ($0.00) under LGPL-3.
""",
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': [
        'base',
        'account',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/academic_billing_wizard_views.xml',
        'wizard/academic_government_sync_wizard_views.xml',
        'views/academic_structure_views.xml',
        'views/academic_student_views.xml',
        'views/academic_krs_views.xml',
        'views/government_bridge_views.xml',
        'views/academic_menu_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
