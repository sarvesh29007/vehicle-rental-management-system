"""
Chapters 1 to 4 generation for Vehicle Rental Project Report.
Matches the structure and depth of the reference VIT Database Systems report.
"""

import os
from docx.shared import Inches
from report_generator.styles import (
    add_h1, add_h2, add_h3, add_p, add_bullet, add_numbered,
    add_table_data, add_figure
)

def build_chapters_1_to_4(doc, assets_dir):
    # ====================================================
    # CHAPTER 1: INTRODUCTION
    # ====================================================
    add_h1(doc, "CHAPTER 1: INTRODUCTION")
    
    add_h2(doc, "1.1 Background")
    add_p(
        doc,
        "Vehicle rental enterprises handle a continuous stream of critical operational and financial transactions: "
        "onboarding customers with verified identity credentials, allocating physical vehicles across distributed branch locations, "
        "managing dynamic daily rental tariffs, executing reservation bookings across future date intervals, dispatching vehicle handovers, "
        "inspecting returns, tracking scheduled fleet servicing, and recording multi-channel payments. In this environment, an operational mistake "
        "is not merely a software defect; it represents asset damage, legal liability, or direct financial loss. A vehicle double-booked "
        "for overlapping dates, an unrecorded handover of a luxury car, a vehicle dispatched while quarantined in service, or an untracked "
        "payment variance directly impairs business viability.",
        space_after=6
    )
    add_p(
        doc,
        "A Relational Database Management System (RDBMS) provides the natural foundation for this mission-critical domain. "
        "It guarantees data consistency by storing every operational fact exactly once, enforces domain and business integrity declaratively "
        "through constraints, guarantees that multi-step operations execute under ACID transactional semantics, and provides multi-version concurrency "
        "control (MVCC). This project, the Vehicle Rental Management System (VRMS), implements those core database principles in a realistic "
        "fleet rental enterprise using Oracle AI Database 26ai Free (SQL and PL/SQL) combined with a Python Flask web frontend.",
        space_after=8
    )

    add_h2(doc, "1.2 Problem Statement")
    add_p(
        doc,
        "Spreadsheet-based, flat-file, or uncoordinated paper-based systems commonly used in regional rental agencies suffer from "
        "the following severe operational vulnerabilities:",
        space_after=4
    )
    add_bullet(
        doc, "Redundancy and Update Anomalies: ",
        "Customer, category, and branch attributes repeated across each booking record lead to inconsistent data when customer phone numbers or branch managers change."
    )
    add_bullet(
        doc, "Double-Booking and Temporal Collisions: ",
        "Concurrent reservations for the same vehicle across overlapping dates occur when availability checks are handled manually or outside atomic database locks."
    )
    add_bullet(
        doc, "Unenforced Safety Rules: ",
        "Vehicles flagged for critical mechanical maintenance or scheduled overhaul can be mistakenly reserved or dispatched, risking customer safety."
    )
    add_bullet(
        doc, "Manual Tariff and Payment Errors: ",
        "Manual calculation of multi-day rental tariffs and payment reconciliation results in arithmetic errors and revenue leakage."
    )
    add_bullet(
        doc, "Absence of Traceability and Audit Trail: ",
        "Without autonomous database triggers logging state transitions (BOOKED to ACTIVE to RETURNED), it is impossible to determine who authorized an operation or when a vehicle changed custody."
    )
    add_p(
        doc,
        "The primary stakeholders affected by these issues are retail customers (who face reservation cancellations or unsafe vehicles), "
        "branch staff (who manage vehicle dispatches and payment collection), and fleet managers/auditors (who require verifiable revenue audits and maintenance tracking).",
        space_after=8
    )

    add_h2(doc, "1.3 Objectives")
    add_numbered(
        doc, "1.",
        "Design and normalize an 8-table relational schema with appropriate Primary Keys, Foreign Keys, NOT NULL, UNIQUE, CHECK, and DEFAULT constraints, populated with at least 10 meaningful records per table."
    )
    add_numbered(
        doc, "2.",
        "Enforce 100% of the operational business rules directly inside Oracle Database using PL/SQL stored procedures (p_book, p_start, p_return, p_pay, p_dues) and deterministic stored functions (f_bal, f_avail)."
    )
    add_numbered(
        doc, "3.",
        "Implement row-level database triggers (trg_bk_bi, trg_bk_au) to autonomously compute rental tariffs, block bookings for vehicles under service, synchronize vehicle availability states, and populate an immutable audit ledger (bk_log)."
    )
    add_numbered(
        doc, "4.",
        "Demonstrate explicit multi-record cursor processing with %ROWTYPE (p_dues) to generate automated receivables recovery reports."
    )
    add_numbered(
        doc, "5.",
        "Implement and verify 16 comprehensive SQL queries covering multi-table joins, aggregations, HAVING clauses, correlated/uncorrelated subqueries, set operations, single-row string functions, date functions, and views."
    )
    add_numbered(
        doc, "6.",
        "Develop an interactive, 100% offline Python Flask web application connecting via python-oracledb Thin mode, featuring role-based Staff and Manager portals and an interactive database tables browser."
    )

    add_h2(doc, "1.4 Scope")
    add_p(
        doc,
        "Included: Ten branch locations across Tamil Nadu and major technology hubs, ten distinct vehicle categories with daily tariffs, "
        "ten registered customers with driving credentials, ten fleet vehicles with operational status tracking (AVAILABLE, RENTED, SERVICE), "
        "twelve multi-state bookings (BOOKED, ACTIVE, RETURNED, CANCELLED), multi-mode payments (CASH, UPI, CARD), fleet maintenance logs, "
        "an autonomous trigger-populated audit trail, role-based web portals (Staff and Manager), and whitelisted data dictionary inspector. "
        "Not included: External credit-card payment gateway gateways, automated SMS dispatchers, and production GPS telematics integration.",
        space_after=8
    )

    add_h2(doc, "1.5 Existing System")
    add_p(
        doc,
        "The reference 'existing system' is a spreadsheet or uncoordinated departmental ledger where each reservation row "
        "repeats customer names, contact numbers, branch addresses, vehicle models, and daily rates. Data updates require edits across hundreds of "
        "redundant cells, vehicle maintenance schedules are decoupled from rental desk operations, and historical balance revisions are "
        "untraceable. Chapter 6 illustrates this as a concrete universal relation and quantifies the anomalies it produces.",
        space_after=8
    )

    add_h2(doc, "1.6 Proposed System")
    add_p(
        doc,
        "The proposed system establishes a strict, database-centric three-tier architecture. Each operational entity is stored once "
        "in a normalized relational schema (BCNF / 3NF). Business logic is pushed entirely into the Oracle Database tier via PL/SQL routines, "
        "ensuring that business rules remain inviolable regardless of whether commands originate from web forms, SQL Developer, or batch scripts. "
        "The front end consists of a responsive Python Flask application providing intuitive, role-separated portals for Branch Staff and Fleet Managers.",
        space_after=8
    )

    add_h2(doc, "1.7 Organization of the Report")
    add_p(
        doc,
        "Chapter 2 presents the requirements analysis and stakeholder models. Chapter 3 examines foundational DBMS concepts and architecture. "
        "Chapters 4 and 5 detail the conceptual ER model and relational schema. Chapter 6 analyzes functional dependencies and BCNF normalization. "
        "Chapters 7 and 8 document the SQL query suite, PL/SQL stored routines, triggers, cursors, and ACID transactions. "
        "Chapter 9 covers query optimization and indexing. Chapter 10 addresses security, backup, and recovery. "
        "Chapter 11 describes the web application implementation. Chapter 12 details empirical testing and 28 test cases. "
        "Chapter 13 concludes with learning outcomes and future enhancements. Appendices provide complete SQL scripts, sample datasets, and test summaries.",
        space_after=12
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 2: REQUIREMENTS ANALYSIS
    # ====================================================
    add_h1(doc, "CHAPTER 2: REQUIREMENTS ANALYSIS")
    
    add_h2(doc, "2.1 Stakeholders and User Roles")
    roles_data = [
        ("Retail Customer", "Browses vehicle availability across branches, places reservations, takes vehicle delivery, makes payments, and receives trip receipts."),
        ("Branch Staff / Desk Agent", "Validates customer driving credentials, executes bookings (p_book), dispatches vehicle pickup (p_start), processes returns (p_return), and records payments (p_pay)."),
        ("Fleet Manager / Auditor", "Monitors branch inventory and vehicle utilization, reviews maintenance expenses, tracks outstanding receivables via cursor audit (p_dues), and reviews immutable audit logs (bk_log)."),
        ("Database Administrator (DBA)", "Manages schema DDL, tunes indexes, configures tablespaces, monitors lock contention, and manages physical/logical backups via RMAN and Data Pump.")
    ]
    add_table_data(
        doc, "Table 2.1: User roles and responsibilities",
        ["Role", "Responsibilities in the System"],
        roles_data, [Inches(1.8), Inches(4.7)], font_size=9
    )

    add_h2(doc, "2.2 Functional Requirements")
    fr_data = [
        ("FR1", "Customer Onboarding", "Register customer with unique phone, email, and verified driving license", "customer table, UK constraints"),
        ("FR2", "Vehicle Cataloging", "Catalog vehicles categorized with daily rates and branch assignments", "category, branch, vehicle tables"),
        ("FR3", "Temporal Availability Check", "Verify vehicle is not in SERVICE and has no overlapping reservations", "f_avail(p_v, p_s, p_e)"),
        ("FR4", "Automated Booking Creation", "Reserve vehicle using sequence seq_bk; compute total automatically", "p_book, seq_bk, trg_bk_bi"),
        ("FR5", "Service Quarantine Protection", "Prohibit reservation or dispatch of vehicles undergoing maintenance", "trg_bk_bi (ORA-20005)"),
        ("FR6", "Trip Dispatch & State Sync", "Transition BOOKED to ACTIVE; lock vehicle status to RENTED automatically", "p_start, trg_bk_au"),
        ("FR7", "Vehicle Return Processing", "Transition ACTIVE to RETURNED; restore vehicle to AVAILABLE status", "p_return, trg_bk_au"),
        ("FR8", "Audit Trail Logging", "Record immutable historical log of every booking status transition", "trg_bk_au -> bk_log (seq_log)"),
        ("FR9", "Payment Collection & Validation", "Record payments; reject amounts exceeding outstanding balance", "p_pay, seq_pay, f_bal"),
        ("FR10", "Outstanding Receivables Audit", "Iterate over open bookings to report customers with pending balances", "p_dues (explicit cursor)"),
        ("FR11", "Analytical SQL Reporting", "Execute 16 verified SQL queries for management insights", "Queries 1 to 16"),
        ("FR12", "Whitelisted Table Inspection", "Direct interactive inspection of live database tables and constraints", "Manager portal /tables route")
    ]
    add_table_data(
        doc, "Table 2.2: Functional requirements and implementing component",
        ["ID", "Requirement", "Operational Description", "Implementing Component"],
        fr_data, [Inches(0.6), Inches(1.5), Inches(2.6), Inches(1.8)], font_size=8
    )

    add_h2(doc, "2.3 Non-Functional Requirements")
    add_bullet(doc, "Data Integrity & Consistency: ", "Enforced via declarative database constraints (PK, FK, UK, CHECK) and stored procedures with atomic commit and rollback.")
    add_bullet(doc, "Auditability & Non-Repudiation: ", "Every status mutation is autonomously intercepted by trg_bk_au and recorded in bk_log with old status, new status, timestamp, and sequence ID.")
    add_bullet(doc, "Robust Error Handling: ", "Meaningful application error numbers (ORA-20001 to ORA-20005) are raised in PL/SQL and translated into user-friendly alerts in the UI.")
    add_bullet(doc, "Zero Client-Side ORM: ", "Strict boundary enforcement where Python issues direct parameterized SQL and executes stored procedures, avoiding synchronization lag.")
    add_bullet(doc, "Zero-Dependency Offline Operation: ", "Frontend styling is 100% self-contained CSS3 without CDN links, ensuring offline air-gapped operation.")

    add_h2(doc, "2.4 Hardware and Software Requirements")
    hw_data = [
        ("Operating System", "Microsoft Windows 10/11 (64-bit), Linux, or macOS"),
        ("Database Engine", "Oracle AI Database 26ai Free (Port 1521, Service: FREEPDB1)"),
        ("Application Backend", "Python 3.12 (Standard Library: http, json, socket)"),
        ("Database Driver", "python-oracledb 26.0.1 (Thin Mode, no Oracle Instant Client required)"),
        ("Frontend Web Stack", "Flask 3.1.3, Jinja2 Templates, Pure Responsive CSS3"),
        ("Development Tools", "Oracle SQL Developer 26.2.0, Microsoft VS Code, PowerShell 7"),
        ("Minimum Hardware", "4 GB RAM (8 GB recommended for Oracle DB), 15 GB free disk, Dual-Core 2.0 GHz CPU")
    ]
    add_table_data(
        doc, "Table 2.3: Hardware and software requirements",
        ["Item", "Specification / Environment"],
        hw_data, [Inches(2.2), Inches(4.3)], font_size=8.5
    )

    add_h2(doc, "2.5 Feasibility Study")
    add_p(
        doc,
        "Technical Feasibility: Oracle AI Database 26ai Free runs natively as a Windows service and supports all required advanced database "
        "constructs (triggers, sequences, stored packages, %ROWTYPE cursors). python-oracledb operates seamlessly in Thin mode. "
        "Operational Feasibility: The dual-portal interface separates operational workflows for Branch Staff and Fleet Managers, "
        "requiring zero database command knowledge for desk users. Economic Feasibility: All software components utilized "
        "(Oracle Free, Python, Flask) are open-source or free community releases, incurring zero licensing expenditure.",
        space_after=8
    )

    add_h2(doc, "2.6 Use-Case Diagram and Descriptions")
    add_figure(
        doc, os.path.join(assets_dir, "fig_2_1_use_case.png"),
        "Figure 2.1: Use-case diagram of the Vehicle Rental Management System (VRMS)"
    )
    
    uc_data = [
        ("Reserve Vehicle", "Customer / Staff", "Select customer, vehicle, dates; verifies f_avail; inserts BOOKED row; trg_bk_bi computes total.", "Vehicle under SERVICE or date collision: ORA-20001 raised; transaction rolled back."),
        ("Dispatch Trip", "Branch Staff", "Verifies customer arrival; executes p_start; updates status to ACTIVE; trg_bk_au locks vehicle to RENTED.", "Booking not BOOKED: ORA-20002 raised; operation rejected."),
        ("Return Vehicle", "Branch Staff", "Executes p_return; sets status to RETURNED; trg_bk_au unlocks vehicle to AVAILABLE; calls f_bal.", "Booking not ACTIVE: ORA-20003 raised; return rejected."),
        ("Collect Payment", "Staff / Customer", "Customer pays via CASH/UPI/CARD; p_pay verifies amount <= balance; inserts row via seq_pay.", "Amount <= 0 or exceeds balance: ORA-20004 raised."),
        ("Audit Receivables", "Fleet Manager", "Manager requests dues report; p_dues cursor iterates over open bookings; aggregates total dues.", "No open dues: reports 0 overdue balances.")
    ]
    add_table_data(
        doc, "Table 2.4: Key use-case descriptions",
        ["Use Case", "Actors", "Main Operational Flow", "Alternative / Exception Flow"],
        uc_data, [Inches(1.2), Inches(1.1), Inches(2.4), Inches(1.8)], font_size=8
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 3: DBMS CONCEPTS AND ARCHITECTURE
    # ====================================================
    add_h1(doc, "CHAPTER 3: DBMS CONCEPTS AND ARCHITECTURE")
    
    add_h2(doc, "3.1 Introduction to DBMS")
    add_p(
        doc,
        "A Database Management System (DBMS) is specialized system software designed to define, construct, manipulate, and safeguard "
        "persistent datasets. In a Relational DBMS (RDBMS), data is conceptually structured into mathematical relations (tables) comprising "
        "tuples (rows) and attributes (columns). Relationships between entities are established through key values rather than physical "
        "disk pointers. The core benefits include declarative data integrity, reduction of redundancy, concurrent multi-user execution "
        "via ACID transactions, standardized query execution (SQL), and enterprise-grade backup/recovery mechanisms.",
        space_after=8
    )

    add_h2(doc, "3.2 File System versus DBMS")
    fs_data = [
        ("Data Redundancy", "Branch and customer data duplicated across every reservation spreadsheet.", "Stored exactly once in normalized tables; referenced via foreign keys."),
        ("Data Consistency", "Manual cross-sheet synchronization; prone to conflicting values.", "Enforced through PK, FK, NOT NULL, UNIQUE, CHECK, and triggers."),
        ("Concurrent Sharing", "Coarse file locking; simultaneous edits cause data loss or lock conflicts.", "Row-level locking (SELECT FOR UPDATE) and multi-version concurrency control."),
        ("Data Security", "Coarse OS file permissions; no field-level or role-based restrictions.", "Oracle database schemas, roles, and granular privilege grants."),
        ("Transaction Recovery", "Manual file backups; power loss or process crash corrupts data.", "Write-ahead logging (Redo logs) and undo tablespaces for atomic rollback.")
    ]
    add_table_data(
        doc, "Table 3.1: File system versus DBMS in the vehicle rental context",
        ["Evaluation Aspect", "Traditional File / Spreadsheet System", "Oracle RDBMS (This Project)"],
        fs_data, [Inches(1.5), Inches(2.5), Inches(2.5)], font_size=8.5
    )

    add_h2(doc, "3.3 Three-Schema Architecture")
    add_p(
        doc,
        "The ANSI/SPARC Three-Schema Architecture separates database systems into three distinct abstraction tiers:",
        space_after=4
    )
    add_bullet(
        doc, "External Schema (View Level): ",
        "Customized user interfaces presenting only role-relevant data. The Staff portal displays vehicle availability calendars and customer check-in forms. The Manager portal displays financial aggregate summaries, receivables audits, and maintenance schedules."
    )
    add_bullet(
        doc, "Conceptual Schema (Logical Level): ",
        "The global relational schema defining the 8 normalized tables, data types, primary/foreign key relationships, and enterprise business rules independent of storage mechanics."
    )
    add_bullet(
        doc, "Internal Schema (Physical Level): ",
        "The physical layout of the database within Oracle tablespaces, data files, B*Tree index structures, and row formats stored on disk."
    )

    add_h2(doc, "3.4 Data Independence")
    add_p(
        doc,
        "Logical Data Independence is achieved because the Python Flask web application interacts with the database through SQL views "
        "(such as v_open_bookings) and parameterized stored procedures. Adding an operational column or creating audit tables does not break "
        "existing application routes. Physical Data Independence is demonstrated because B*Tree indexes (such as idx_veh_cid_bid) can be "
        "added, rebuilt, or relocated without modifying the application SQL queries.",
        space_after=8
    )

    add_h2(doc, "3.5 Data Models")
    add_p(
        doc,
        "Earlier hierarchical and network data models relied on rigid physical tree pointers and lacked ad-hoc query capabilities. "
        "Document and NoSQL databases provide flexible schema nesting but sacrifice multi-table foreign key enforcement and declarative ACID "
        "guarantees. The Relational Model was chosen because vehicle rental operations are inherently structured, require strict referential "
        "integrity across 8 entities, and demand deterministic financial transactions.",
        space_after=8
    )

    add_h2(doc, "3.6 Database Languages")
    lang_data = [
        ("DDL", "Data Definition Language", "Defines and alters schema structures", "CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER, DROP TABLE in 01_schema_data.sql"),
        ("DML", "Data Manipulation Language", "Inserts, modifies, and deletes data", "INSERT sample data, UPDATE status, DELETE customer in 01_schema_data.sql"),
        ("DQL", "Data Query Language", "Retrieves data matching criteria", "16 comprehensive SQL queries in 03_queries_demo.sql"),
        ("DCL", "Data Control Language", "Manages user privileges and roles", "GRANT CONNECT, RESOURCE to rental; proposed role-based privilege model"),
        ("TCL", "Transaction Control Language", "Controls atomic transaction states", "COMMIT, ROLLBACK, SAVEPOINT executed in stored procedures and test cases")
    ]
    add_table_data(
        doc, "Table 3.2: SQL sub-languages and their use in the project",
        ["Language", "Full Form", "Purpose", "Project Implementation Examples"],
        lang_data, [Inches(0.8), Inches(1.6), Inches(1.8), Inches(2.3)], font_size=8.5
    )

    add_h2(doc, "3.7 Users and Database Administrator")
    add_p(
        doc,
        "In this project, user roles reflect operational banking/rental hierarchies: End Users (Customers and Desk Staff) utilize the web interface; "
        "Application Programmers develop Python Flask endpoints and Jinja2 views; Database Designers formulate the ER diagram and normalized schema; "
        "and the Database Administrator (DBA) establishes the Oracle pluggable database, compiles PL/SQL packages, and oversees data integrity.",
        space_after=12
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 4: CONCEPTUAL DATABASE DESIGN
    # ====================================================
    add_h1(doc, "CHAPTER 4: CONCEPTUAL DATABASE DESIGN")
    
    add_h2(doc, "4.1 Entity Identification")
    ent_data = [
        ("BRANCH", "Strong Entity", "Physical branch location hosting fleet vehicles and customer pickup operations."),
        ("CATEGORY", "Strong Entity", "Classification of vehicles (Sedan, SUV, Luxury) establishing daily rental tariffs."),
        ("CUSTOMER", "Strong Entity", "Verified individual customer holding driving credentials and contact profiles."),
        ("VEHICLE", "Strong Entity", "Physical motor vehicle owned by the agency, assigned to a branch and category."),
        ("BOOKING", "Strong Entity", "Contractual reservation linking a customer to a specific vehicle for a date range."),
        ("PAYMENT", "Strong Entity", "Financial transaction settlement recorded against a specific rental booking."),
        ("MAINTENANCE", "Strong Entity", "Service inspection or repair log documenting downtime and maintenance expense."),
        ("BK_LOG", "Strong Entity (Audit)", "Immutable historical log recording booking status transitions and trigger origins.")
    ]
    add_table_data(
        doc, "Table 4.1: Entities and their roles",
        ["Entity Name", "Entity Type", "Role in Vehicle Rental Domain"],
        ent_data, [Inches(1.5), Inches(1.5), Inches(3.5)], font_size=8.5
    )

    add_h2(doc, "4.2 Attributes and Attribute Types")
    add_p(
        doc,
        "All attributes across the 8 entities are simple and atomic. Composite attributes such as customer address are handled atomically, "
        "and multi-valued attributes are eliminated by establishing separate normalized relations. Derived attributes are deliberately designed: "
        "booking.total is derived from (edt - sdt) multiplied by category.rate, computed autonomously by trg_bk_bi to avoid application-side "
        "calculation discrepancies. Similarly, bk_log captures old_st and new_st to create an unalterable audit ledger.",
        space_after=8
    )

    add_h2(doc, "4.3 Relationships and Cardinality")
    rel_data = [
        ("hosts", "BRANCH (1) – VEHICLE (N)", "1 : N", "VEHICLE.bid (FK referencing BRANCH.bid)"),
        ("classifies", "CATEGORY (1) – VEHICLE (N)", "1 : N", "VEHICLE.cid (FK referencing CATEGORY.cid)"),
        ("places", "CUSTOMER (1) – BOOKING (N)", "1 : N", "BOOKING.custid (FK referencing CUSTOMER.custid)"),
        ("reserves", "VEHICLE (1) – BOOKING (N)", "1 : N", "BOOKING.vid (FK referencing VEHICLE.vid)"),
        ("undergoes", "VEHICLE (1) – MAINTENANCE (N)", "1 : N", "MAINTENANCE.vid (FK referencing VEHICLE.vid)"),
        ("settles", "BOOKING (1) – PAYMENT (N)", "1 : N", "PAYMENT.bkid (FK referencing BOOKING.bkid)"),
        ("audits", "BOOKING (1) – BK_LOG (N)", "1 : N", "BK_LOG.bkid (recorded by trg_bk_au)")
    ]
    add_table_data(
        doc, "Table 4.2: Relationships and cardinality",
        ["Relationship", "Entities Involved", "Cardinality", "Relational Implementation"],
        rel_data, [Inches(1.2), Inches(2.0), Inches(1.0), Inches(2.3)], font_size=8.5
    )

    add_h2(doc, "4.4 Participation Constraints")
    add_bullet(doc, "Total Participation of VEHICLE in BRANCH and CATEGORY: ", "Every vehicle must reference a valid home branch and category (NOT NULL foreign keys).")
    add_bullet(doc, "Partial Participation of BRANCH and CATEGORY: ", "A branch or category may exist before vehicles are assigned to it.")
    add_bullet(doc, "Total Participation of BOOKING in CUSTOMER and VEHICLE: ", "Every booking must be linked to a registered customer and vehicle.")
    add_bullet(doc, "Partial Participation of CUSTOMER and VEHICLE: ", "A customer may exist without placing a booking; a vehicle may exist without current reservations.")

    add_h2(doc, "4.5 Weak and Strong Entities")
    add_p(
        doc,
        "Every entity possesses its own unique primary key surrogate (e.g., bid, cid, custid, vid, bkid, pid, mid, lid). "
        "Consequently, there are no weak entities in the strict ER sense. All entities represent distinct real-world domain objects "
        "with independent lifecycles governed by referential integrity.",
        space_after=8
    )

    add_h2(doc, "4.6 ER Diagram")
    add_figure(
        doc, os.path.join(assets_dir, "fig_4_1_er_diagram.png"),
        "Figure 4.1: Entity-Relationship diagram (diamonds = relationships; UK = unique key; PK = primary key)"
    )

    add_h2(doc, "4.7 Design Assumptions")
    add_bullet(doc, "Tariff Calculation: ", "Rental charges are computed as whole calendar days (edt - sdt) multiplied by category daily rate.")
    add_bullet(doc, "Maintenance Quarantine: ", "Vehicles in SERVICE status cannot be reserved or dispatched under any circumstances.")
    add_bullet(doc, "Vehicle State Machine: ", "Transitioning a booking to ACTIVE automatically locks vehicle status to RENTED; returning it restores AVAILABLE.")
    add_bullet(doc, "Payment Settlement: ", "Payments cannot exceed the outstanding balance (f_bal), preventing negative customer balances.")

    doc.add_page_break()
