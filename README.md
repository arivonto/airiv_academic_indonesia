# Indonesia Academic ERP & Universal Government Bridge

[![Odoo](https://img.shields.io/badge/Odoo-18.0-714B67.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-0f766e.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Author-AIRIV-0891b2.svg)](https://airiv.id)
[![GitHub Actions](https://github.com/arivonto/airiv_academic_indonesia/actions/workflows/odoo-appstore-ci.yml/badge.svg?branch=18.0)](https://github.com/arivonto/airiv_academic_indonesia/actions)
[![Apps Store Ready](https://img.shields.io/badge/Odoo%20Apps%20Store-ready-22c55e.svg)](https://apps.odoo.com/)

AIRIV Academic Indonesia is an Odoo 18 Community academic ERP workspace for Indonesian schools, campuses, and pesantren. It combines academic master data, student lifecycle records, KRS and grading, education billing, and government integration surfaces for PDDikti, Dapodik, EMIS, PIN, and SIVIL workflows.

## Core Capabilities & Architecture

### Core capabilities

- Academic structure: academic year, semester type, faculty, program, education degree, course, SKS/credits, lecturer, and institution context.
- Student registry: student name, NIM/NISN, NIK, gender, email, phone, program, intake year, advisor, lifecycle status, cumulative GPA, and total earned SKS.
- KRS workflow: draft, submitted, approved, and graded states with KRS lines, course credits, weighted score calculation, grade letter, semester GPA, and total SKS.
- Government bridge: configuration surfaces for PDDikti Neo Feeder, Dapodik WebService, EMIS 4.0, and PIN/SIVIL workflows.
- Batch wizards: education billing generator and government synchronization wizard.
- AIRIV OS alignment: application menu integrates with AIRIV OS launchpad and AIRIV store icon assets.

### Architecture

```text
Academic Master Data
  |
  |-- academic.year
  |-- academic.faculty
  |-- academic.program
  |-- academic.course
  v
Student Academic Lifecycle
  |
  |-- academic.student
  |-- academic.krs
  |-- academic.krs.line
  |-- GPA and SKS computation
  v
AIRIV Government Bridge
  |
  |-- academic.government.config
  |-- PDDikti profile
  |-- Dapodik profile
  |-- EMIS profile
  |-- PIN and SIVIL workflow
  v
Operational Wizards
  |
  |-- academic.billing.wizard
  |-- academic.government.sync.wizard
  |-- account.move draft invoices
  |-- sandbox/live sync evidence
```

## Feature & Workflow Automation

1. Build academic structure
   - Create academic years, faculties, programs, courses, SKS values, recommended semesters, and lecturers.

2. Register student records
   - Store student identity, NIM/NISN, NIK, program, intake academic year, advisor, contact data, and lifecycle state.

3. Run academic term workflow
   - Create KRS, submit, approve, enter assessment components, lock grades, and compute total SKS, IPS, and cumulative IPK.

4. Operate regulatory and billing workflows
   - Configure government bridge profile, execute sandbox/live sync workflows, and generate education draft invoices through the billing wizard.

## Technical Specifications

| Item | Detail |
| --- | --- |
| Odoo series | 18.0 |
| Odoo edition | Community |
| Module technical name | `airiv_academic_indonesia` |
| Version | `18.0.1.0.0` |
| License | LGPL-3 |
| Author | AIRIV |
| Category | Services/Education |
| Dependencies | `base`, `account`, `mail`, `airiv_os_core` |
| Main models | `academic.year`, `academic.faculty`, `academic.program`, `academic.course`, `academic.student`, `academic.krs`, `academic.krs.line` |
| Government model | `academic.government.config` |
| Wizards | `academic.billing.wizard`, `academic.government.sync.wizard` |
| Integration surfaces | PDDikti Neo Feeder, Dapodik WebService, EMIS 4.0, PIN SIVIL |
| Store assets | `icon.png`, `banner.png`, `index.html` |

## Installation Guidance

1. Clone the repository branch for Odoo 18:

   ```bash
   git clone -b 18.0 https://github.com/arivonto/airiv_academic_indonesia.git
   ```

2. Place the module in your Odoo addons path.

3. Ensure dependencies are available, including AIRIV OS Core.

4. Restart Odoo.

5. Activate developer mode if needed.

6. Update the Apps list.

7. Search for `Indonesia Academic ERP & Universal Government Bridge`.

8. Install the module.

## Configuration Checklist

- Confirm Base, Accounting, Mail, and AIRIV OS Core are installed.
- Create academic years and semester periods.
- Create faculties or departments.
- Create programs or classes with correct education degree and graduation SKS.
- Create courses with code, SKS/credits, lecturer, and recommended semester.
- Register students with NIM/NISN, NIK, program, intake year, and advisor.
- Configure government bridge profile and keep execution mode in sandbox until live credentials are approved.
- Review KRS and grade records before running government reporting workflow.
- Review generated education draft invoices before posting.

## Repository Layout

```text
airiv_academic_indonesia/
  README.md
  LICENSE
  .github/
    workflows/
      odoo-appstore-ci.yml
    scripts/
      validate_odoo_appstore.py
  airiv_academic_indonesia/
    __manifest__.py
    models/
      academic_structure.py
      academic_student.py
      academic_krs.py
      government_bridge.py
    security/
      ir.model.access.csv
    static/
      description/
        icon.png
        icon_128.png
        airiv_store_icon.png
        airiv_store_icon_128.png
        banner.png
        index.html
    views/
      academic_structure_views.xml
      academic_student_views.xml
      academic_krs_views.xml
      government_bridge_views.xml
      academic_menu_views.xml
    wizard/
      academic_billing_wizard.py
      academic_government_sync_wizard.py
  static/
    description/
      icon.png
      icon_128.png
      airiv_store_icon.png
      airiv_store_icon_128.png
      banner.png
      index.html
```

## Contact Info

| Item | Detail |
| --- | --- |
| Author | AIRIV |
| Website | https://airiv.id |
| GitHub | https://github.com/arivonto |
| Module repository | https://github.com/arivonto/airiv_academic_indonesia |
| Odoo series | 18.0 |

## Quality Gate

This repository is prepared for Odoo Apps Store submission with:

- Parseable Odoo manifest metadata.
- Root and module-level documentation.
- Odoo Apps Store description fragment.
- Required store images.
- LGPL-3 license metadata.
- GitHub Actions Apps Store audit on branch `18.0`.

