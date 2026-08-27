# Indonesia Academic ERP & Universal Government Bridge (PDDikti, Dapodik, EMIS & PIN SIVIL)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Regulatory: Kemendikbud & Kemenag](https://img.shields.io/badge/Regulatory-Kemendikbud%20%26%20Kemenag%20RI-sky.svg)](https://airiv.id)

An all-in-one Academic and Campus Management ERP built specifically for **Odoo 18.0 Community Edition**. Tailored for Indonesian educational foundations (*Yayasan Pendidikan*), K-12 Schools (SD/SMP/SMA/SMK), Islamic Boarding Schools (*Pondok Pesantren & Madrasah*), and Higher Education Institutions (*Universitas, Institut, Politeknik, Akademi*).

---

## Universal Government Integration Capabilities

### 1. PDDikti Neo Feeder REST Gateway (Higher Education)
* **Direct JSON-RPC / REST Integration**: Connects with campus Neo Feeder instances (`GetToken`, `InsertMahasiswa`, `InsertKRSMahasiswa`, `InsertNilaiPerkuliahanKelas`).
* **AKM (Aktivitas Kuliah Mahasiswa)**: Automated reporting for semester GPA (IPS), cumulative GPA (IPK), total SKS, and student status.
* **Offline Sandbox Simulation**: Built-in mock responder allows complete testing without requiring live server tokens.

### 2. Dapodik Local Web Services (K-12 Schools)
* **Peserta Didik & NISN Validation**: Direct synchronization of Kemendikbud 10-digit NISN, NIK, birth credentials, and guardian details.
* **Rombongan Belajar (Rombel)**: Maps curriculum structures and class assignments directly to Odoo master programs.

### 3. EMIS 4.0 Kemenag (Madrasah & Pesantren)
* **Santri Mukim & Kalong Registry**: Manages boarding and non-boarding students with integrated NSM validation.
* **BOSP Feeder**: Pre-compiles educational operational aid figures.

### 4. PIN (Penomoran Ijazah Nasional) & SIVIL Verification
* **Standardized 14-Digit PIN**: Generates national diploma numbers based on official Dikti algorithms:
  $$\text{PIN Format} = \underbrace{\text{Kode Prodi}}_{5\text{ digit}} + \underbrace{\text{Tahun}}_{4\text{ digit}} + \underbrace{\text{Jenjang}}_{1\text{ digit}} + \underbrace{\text{No. Urut}}_{5\text{ digit}}$$
* **SIVIL QR Code**: Direct QR verification link to `https://ijazah.kemdikbud.go.id`.

### 5. Automated Financial Billing (SPP & UKT)
* **SPP Bulanan**: Batch recurring invoice generator for K-12 and Pesantren.
* **UKT 8-Tiering**: Tiered semester billing for higher education synchronized directly with `account.move`.

---

## Validated Commercial Benchmark (Audited & Tested)

The module was verified under live Odoo 18.0 Community conditions:

1. **PDDikti Neo Feeder Sync**: Verified sandbox token generation and synchronized KRS / Grade payload with unique sync token logging.
2. **Dapodik K-12 Validation**: Verified 10-digit NISN mapping and status transition to `synced_dapodik`.
3. **EMIS 4.0 Kemenag Sync**: Verified Santri Mukim registry transition to `synced_emis`.
4. **PIN SIVIL Generation**: Issued valid 14-digit national diploma PIN `552012026100001` and active SIVIL verification URL.
5. **KRS & KHS Grade Calculation**: Verified SKS credit weights ($3.50$ IPS & IPK across multiple courses).

---

## Installation & Odoo Configuration Guide

1. **Deploy Module**:
   Place `airiv_academic_indonesia` inside your Odoo `custom_addons` directory.

2. **Activate Module**:
   * Navigate to **Apps > Update Apps List**.
   * Search for `Indonesia Academic ERP & Universal Government Bridge` and click **Activate**.

3. **Configure Government Gateway**:
   * Open **Akademik & Kampus > Integrasi Pemerintah > Pengaturan Gateway Pemerintah**.
   * Select your institution tier (Universal, University, School, or Pesantren) and set operation mode to **Offline Sandbox Simulator** or **Live Production**.
   * Execute batch syncs anytime via **Sinkronisasi PDDikti / Dapodik / EMIS**.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (OWL & App Drawer compliant) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `base`, `account`, `mail` |
| **Regulatory Standards** | Kemendikbudristek PDDikti Neo Feeder 3.0, Dapodik WebService, Kemenag EMIS 4.0, PIN SIVIL |
| **Server Overhead** | Zero (Native ORM, direct SQL aggregation) |
