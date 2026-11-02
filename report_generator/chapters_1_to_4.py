"""
Chapters 1 to 4 generation for Vehicle Rental Project Report.
Written in an authentic, clear, and practical student engineering voice.
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
        "Vehicle rental businesses handle everyday operations that involve expensive physical assets and continuous customer interactions. "
        "Every day, staff must register new customers, verify driving licenses, assign vehicles across different branches, manage different daily "
        "tariffs for various vehicle classes, and record payments. In a business like this, even a small mistake is costly. For example, if a car is "
        "booked for two different customers on the same weekend, or if a vehicle that is currently in the workshop for brake repair is handed over "
        "to a customer, it causes severe customer dissatisfaction, safety hazards, and financial loss.",
        space_after=6
    )
    add_p(
        doc,
        "A Relational Database Management System (RDBMS) is the ideal tool for managing this domain. By storing each piece of information once, "
        "linking tables through primary and foreign keys, enforcing rules through constraints and triggers, and grouping multi-step actions into "
        "atomic transactions (ACID), a database ensures that the system stays consistent at all times. In this project, I developed the Vehicle "
        "Rental Management System (VRMS) using Oracle AI Database 26ai Free (SQL and PL/SQL) with a Python Flask web frontend to demonstrate "
        "how core database principles solve real-world problems in vehicle rentals.",
        space_after=8
    )

    add_h2(doc, "1.2 Problem Statement")
    add_p(
        doc,
        "When small rental agencies or training projects rely on spreadsheets or unlinked flat files, several operational problems happen regularly:",
        space_after=4
    )
    add_bullet(
        doc, "Redundant data and update anomalies: ",
        "Customer contact numbers, branch addresses, and vehicle daily rates get re-typed into every rental row. If a customer changes their phone number or a branch moves, updating one row leaves other rows with outdated information."
    )
    add_bullet(
        doc, "Double-booking conflicts: ",
        "Without an automated availability check, two staff members can book the same vehicle for overlapping dates, causing scheduling conflicts."
    )
    add_bullet(
        doc, "Unenforced safety and maintenance rules: ",
        "A car that has been marked for scheduled maintenance or mechanical inspection can accidentally be reserved or dispatched if the maintenance record is stored in a separate sheet."
    )
    add_bullet(
        doc, "Manual rate and billing errors: ",
        "Calculating the total bill manually by multiplying rental days with category tariffs often leads to arithmetic mistakes and billing disputes."
    )
    add_bullet(
        doc, "Lack of an audit trail: ",
        "When an booking moves from BOOKED to ACTIVE to RETURNED, spreadsheets do not keep track of who changed the status, from what to what, or when the change happened."
    )
    add_p(
        doc,
        "The people affected by these problems are retail customers (who face delays or cancelled bookings), branch staff (who struggle with manual paperwork), "
        "and fleet managers (who need accurate revenue figures and maintenance tracking).",
        space_after=8
    )

    add_h2(doc, "1.3 Objectives")
    add_p(
        doc,
        "The main objectives of this course project are:",
        space_after=4
    )
    add_numbered(
        doc, "1.",
        "Design an 8-table relational database schema with appropriate Primary Keys, Foreign Keys, NOT NULL, UNIQUE, CHECK, and DEFAULT constraints, and populate each table with at least 10 realistic records."
    )
    add_numbered(
        doc, "2.",
        "Implement all business rules directly in the Oracle database tier using PL/SQL stored procedures (p_book, p_start, p_return, p_pay, p_dues) and stored functions (f_bal, f_avail)."
    )
    add_numbered(
        doc, "3.",
        "Create database triggers (trg_bk_bi and trg_bk_au) to automatically calculate rental bills, block reservations on vehicles under service, update vehicle availability, and log all status changes into an audit table (bk_log)."
    )
    add_numbered(
        doc, "4.",
        "Implement an explicit cursor with %ROWTYPE (p_dues) to produce an overdue balance report across all active bookings."
    )
    add_numbered(
        doc, "5.",
        "Write and execute 16 meaningful SQL queries demonstrating multi-table joins, GROUP BY with HAVING, subqueries, set operations, string and date functions, and database views."
    )
    add_numbered(
        doc, "6.",
        "Build a working Python Flask web application connecting to Oracle via python-oracledb (Thin mode) with Staff and Manager portals and an interactive table viewer, and verify everything with documented test cases."
    )

    add_h2(doc, "1.4 Scope")
    add_p(
        doc,
        "What is included: Ten branch locations (in Tamil Nadu cities plus Bangalore, Hyderabad, and Pune), ten vehicle categories with daily rates, "
        "ten verified customer profiles, ten fleet vehicles with status tracking (AVAILABLE, RENTED, SERVICE), twelve bookings across different states, "
        "ten payments in multiple modes (CASH, UPI, CARD), ten maintenance records, an automatic audit log table, role-separated web screens for Staff and Manager, "
        "and a live database table inspector. "
        "What is excluded: Live third-party bank payment gateway APIs, real SMS notifications, multi-currency conversion, and cloud deployment. These boundaries "
        "are discussed in Section 12.6 under Limitations.",
        space_after=8
    )

    add_h2(doc, "1.5 Existing System")
    add_p(
        doc,
        "The reference 'existing system' is a spreadsheet or manual ledger where each row records an entire rental trip, repeating customer names, "
        "phone numbers, vehicle details, branch addresses, and rates. Modifying a customer's address requires editing every past booking row. "
        "Integrity rules exist only as verbal instructions to staff, meaning invalid entries (like end date earlier than start date, or negative payments) "
        "can easily be entered without any warning. Chapter 6 examines this as a flat universal relation and shows the anomalies it causes.",
        space_after=8
    )

    add_h2(doc, "1.6 Proposed System")
    add_p(
        doc,
        "In the proposed system, every operational fact is stored once in a normalized 8-table relational schema. All validation and business logic "
        "is placed inside Oracle PL/SQL procedures and triggers, so that the rules cannot be bypassed even if someone accesses the database from SQL Developer "
        "or a command-line script. A Python Flask web interface provides clean, dedicated screens for Staff and Managers without re-implementing database rules in Python. "
        "In this single-student lab project, all database design, PL/SQL coding, backend development, and testing were performed by me (Sarvesh R).",
        space_after=8
    )

    add_h2(doc, "1.7 Organization of the Report")
    add_p(
        doc,
        "The report is organized as follows: Chapter 2 analyzes system requirements and user roles. Chapter 3 explains DBMS concepts and architecture. "
        "Chapters 4 and 5 describe the conceptual ER design and relational schema. Chapter 6 covers functional dependencies and normalization to BCNF. "
        "Chapters 7 and 8 present the SQL queries, stored procedures, functions, triggers, and transactions. Chapter 9 discusses query optimization and indexing. "
        "Chapter 10 covers security, backup, and recovery. Chapter 11 describes the web application implementation with screenshots. Chapter 12 details the testing strategy "
        "and results of 28 test cases. Chapter 13 concludes with learning outcomes and future work. Appendices contain the complete SQL code and sample data.",
        space_after=12
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 2: REQUIREMENTS ANALYSIS
    # ====================================================
    add_h1(doc, "CHAPTER 2: REQUIREMENTS ANALYSIS")
    
    add_h2(doc, "2.1 Stakeholders and User Roles")
    roles_data = [
        ("Retail Customer", "Browses available vehicles, requests reservations, picks up vehicles, makes payments, and receives trip receipts."),
        ("Branch Staff / Desk Agent", "Registers new customers, creates reservations (p_book), dispatches vehicle pickup (p_start), processes returns (p_return), and collects payments (p_pay)."),
        ("Branch Manager / Auditor", "Monitors branch fleet inventory, tracks vehicle maintenance expenses, runs outstanding receivables audits (p_dues), and reviews the immutable audit log (bk_log)."),
        ("Database Administrator (DBA)", "Manages the schema DDL, monitors constraints and indexes, compiles PL/SQL packages, and oversees backup and recovery. In this project, this role is performed by the student.")
    ]
    add_table_data(
        doc, "Table 2.1: User roles and responsibilities",
        ["Role", "Responsibilities in the System"],
        roles_data, [Inches(1.8), Inches(4.7)], font_size=9
    )

    add_h2(doc, "2.2 Functional Requirements")
    fr_data = [
        ("FR1", "Customer Registration", "Register customer with unique phone, email, and valid driving license", "customer table, UNIQUE constraints"),
        ("FR2", "Vehicle Fleet Inventory", "Catalog vehicles linked to branch and category daily tariffs", "category, branch, vehicle tables"),
        ("FR3", "Availability Verification", "Verify vehicle is not in SERVICE and has no overlapping reservations", "f_avail stored function"),
        ("FR4", "Automated Booking Creation", "Reserve vehicle using sequence seq_bk; calculate total automatically", "p_book, trg_bk_bi, seq_bk"),
        ("FR5", "Service Quarantine Enforcement", "Block bookings on vehicles undergoing mechanical maintenance", "trg_bk_bi trigger (ORA-20005)"),
        ("FR6", "Trip Start & Vehicle Lock", "Transition BOOKED to ACTIVE; automatically lock vehicle status to RENTED", "p_start, trg_bk_au trigger"),
        ("FR7", "Vehicle Return & Release", "Transition ACTIVE to RETURNED; restore vehicle status to AVAILABLE", "p_return, trg_bk_au trigger"),
        ("FR8", "Audit Trail Logging", "Record immutable historical entries for every status change", "trg_bk_au trigger -> bk_log table"),
        ("FR9", "Payment Processing", "Record customer payment; reject amounts exceeding balance due", "p_pay procedure, seq_pay, f_bal"),
        ("FR10", "Receivables Cursor Audit", "Iterate over open bookings to list customers with unpaid balances", "p_dues procedure (explicit cursor)"),
        ("FR11", "Analytical SQL Queries", "Execute 16 verified SQL queries for business intelligence", "Queries 1 to 16"),
        ("FR12", "Table Inspection", "Inspect live database tables, columns, and row counts directly in browser", "Manager portal /tables route")
    ]
    add_table_data(
        doc, "Table 2.2: Functional requirements and implementing component",
        ["ID", "Requirement", "Description", "Implementing Component"],
        fr_data, [Inches(0.6), Inches(1.5), Inches(2.6), Inches(1.8)], font_size=8
    )

    add_h2(doc, "2.3 Non-Functional Requirements")
    add_bullet(doc, "Atomicity and Consistency: ", "Multi-table operations (like starting a trip or making a payment) must succeed completely or roll back entirely, leaving no partial updates.")
    add_bullet(doc, "Data Integrity: ", "Invalid data (negative rates, end date before start date, duplicate phone or license numbers) must be rejected by the database itself, not just by HTML forms.")
    add_bullet(doc, "Auditability: ", "Every balance change and vehicle handover must be traceable to the old state, new state, and exact timestamp.")
    add_bullet(doc, "Clear Error Feedback: ", "When a rule is broken, the database returns custom error codes (such as ORA-20001 for date conflict) which the web app presents as clean user alerts.")
    add_bullet(doc, "Offline Reliability: ", "The web application interface uses pure offline CSS3 without external fonts or CDN links, ensuring it runs reliably in an offline lab environment.")

    add_h2(doc, "2.4 Hardware and Software Requirements")
    hw_data = [
        ("Operating System", "Microsoft Windows 10/11 (64-bit), Linux, or macOS"),
        ("Database Engine", "Oracle AI Database 26ai Free (Port 1521, Service: FREEPDB1)"),
        ("Application Backend", "Python 3.12 (Standard Library: http, json, socket)"),
        ("Database Driver", "python-oracledb 26.0.1 (Thin Mode, no Oracle Instant Client required)"),
        ("Frontend Web Stack", "Flask 3.1.3, Jinja2 Templates, 100% Offline Responsive CSS3"),
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
        "Technical Feasibility: Oracle AI Database 26ai Free installed and ran smoothly on my Windows laptop. The python-oracledb driver "
        "connects directly using Thin mode without needing Oracle Instant Client C-libraries. "
        "Operational Feasibility: The user interface divides tasks naturally: Staff handle daily bookings and check-ins, while Managers "
        "access audit logs, overdue balances, and fleet reports. Neither role needs to know SQL commands to use the application. "
        "Economic Feasibility: All tools used (Oracle Free, Python, Flask, VS Code, SQL Developer) are freely available community editions, "
        "so the project required zero financial budget.",
        space_after=8
    )

    add_h2(doc, "2.6 Use-Case Diagram and Descriptions")
    add_figure(
        doc, os.path.join(assets_dir, "fig_2_1_use_case.png"),
        "Figure 2.1: Use-case diagram of the Vehicle Rental Management System (VRMS)"
    )
    
    uc_data = [
        ("Reserve Vehicle", "Customer / Staff", "Select customer, vehicle, and dates; f_avail checks conflicts; booking inserted; trg_bk_bi computes total.", "Vehicle in SERVICE or dates overlap: ORA-20001 raised; transaction rolled back."),
        ("Dispatch Trip", "Branch Staff", "Customer arrives; staff runs p_start; status becomes ACTIVE; trg_bk_au locks vehicle to RENTED.", "Booking not BOOKED: ORA-20002 raised; operation aborted."),
        ("Return Vehicle", "Branch Staff", "Vehicle returned; staff runs p_return; status becomes RETURNED; trg_bk_au restores vehicle to AVAILABLE; calls f_bal.", "Booking not ACTIVE: ORA-20003 raised; return rejected."),
        ("Record Payment", "Staff / Customer", "Customer pays via CASH/UPI/CARD; p_pay verifies amount <= balance; inserts row via seq_pay.", "Amount <= 0 or exceeds balance: ORA-20004 raised; payment rejected."),
        ("Audit Receivables", "Branch Manager", "Manager requests dues audit; p_dues cursor iterates over open bookings; aggregates total dues.", "No unpaid dues: reports 0 overdue balances.")
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
        "A Database Management System (DBMS) is software designed to store, manage, query, and protect structured data. "
        "A Relational DBMS organizes data into tables consisting of rows and columns, with relationships established through key values. "
        "The primary advantages of a relational DBMS are reduced data redundancy, enforced data integrity via constraints, support for "
        "concurrent multi-user access with ACID guarantees, and standard SQL querying. In this project, Oracle Database acts as the centralized "
        "engine that safeguards fleet and financial records.",
        space_after=8
    )

    add_h2(doc, "3.2 File System versus DBMS")
    fs_data = [
        ("Data Redundancy", "Branch and customer data duplicated in every spreadsheet row.", "Stored once in normalized tables; referenced by foreign keys."),
        ("Data Consistency", "Manual edits across files easily lead to conflicting records.", "Enforced through PK, FK, NOT NULL, UNIQUE, CHECK, and triggers."),
        ("Concurrent Sharing", "Coarse file locking; concurrent edits overwrite or lose changes.", "Row-level locking and Multi-Version Concurrency Control (MVCC)."),
        ("Data Security", "Basic file-level OS permissions; no column or role-based security.", "Database user schemas, roles, and granular privilege grants."),
        ("Recovery", "Manual file backups; application crash or power loss corrupts data.", "Write-ahead logging (Redo logs) and undo segments for atomic rollback.")
    ]
    add_table_data(
        doc, "Table 3.1: File system versus DBMS in the vehicle rental context",
        ["Aspect", "Spreadsheet / File System", "Oracle Relational DBMS (This Project)"],
        fs_data, [Inches(1.5), Inches(2.5), Inches(2.5)], font_size=8.5
    )

    add_h2(doc, "3.3 Three-Schema Architecture")
    add_p(
        doc,
        "The Three-Schema Architecture separates the system into three levels of abstraction:",
        space_after=4
    )
    add_bullet(
        doc, "External Level (Views): ",
        "The individual portals shown to users. The Staff portal shows vehicle checkout and check-in forms; the Manager portal shows revenue aggregates and overdue balance reports."
    )
    add_bullet(
        doc, "Conceptual Level (Logical Design): ",
        "The 8-table relational schema with all entity definitions, attributes, data types, primary keys, foreign keys, and integrity constraints."
    )
    add_bullet(
        doc, "Internal Level (Physical Storage): ",
        "How Oracle stores tables and B*Tree indexes in tablespaces, data blocks, and data files on the local disk."
    )

    add_h2(doc, "3.4 Data Independence")
    add_p(
        doc,
        "Logical Data Independence means that adding an optional column or an audit table does not break existing application queries. "
        "For example, when I added the bk_log audit table, the core booking queries continued to function without any changes. "
        "Physical Data Independence means that creating an index or rearranging storage on disk does not require rewriting SQL statements; "
        "the query optimizer automatically adjusts the execution plan while the SQL syntax remains unchanged.",
        space_after=8
    )

    add_h2(doc, "3.5 Data Models")
    add_p(
        doc,
        "Earlier hierarchical and network models used hardcoded physical pointers that made ad-hoc queries difficult. "
        "Document-based NoSQL stores (like MongoDB) allow flexible JSON documents, but lack built-in foreign key constraints and cross-document "
        "ACID guarantees by default. The Relational Model was chosen because vehicle rental operations are inherently structured and require "
        "strict referential integrity between customers, vehicles, bookings, and payments.",
        space_after=8
    )

    add_h2(doc, "3.6 Database Languages")
    lang_data = [
        ("DDL", "Data Definition Language", "Defines and modifies schema structures", "CREATE TABLE, CREATE SEQUENCE, CREATE TRIGGER in 01_schema_data.sql"),
        ("DML", "Data Manipulation Language", "Inserts, updates, and deletes records", "INSERT sample data, UPDATE status, DELETE customer in 01_schema_data.sql"),
        ("DQL", "Data Query Language", "Queries and retrieves data", "The 16 SQL queries in 03_queries_demo.sql"),
        ("DCL", "Data Control Language", "Manages database privileges and user roles", "GRANT CONNECT, RESOURCE to rental; proposed role-based privilege model"),
        ("TCL", "Transaction Control Language", "Manages transaction boundaries", "COMMIT, ROLLBACK, SAVEPOINT executed in stored procedures and test cases")
    ]
    add_table_data(
        doc, "Table 3.2: SQL sub-languages and their use in the project",
        ["Language", "Full Form", "Purpose", "Project Implementation Examples"],
        lang_data, [Inches(0.8), Inches(1.6), Inches(1.8), Inches(2.3)], font_size=8.5
    )

    add_h2(doc, "3.7 Users and Database Administrator")
    add_p(
        doc,
        "In a commercial deployment, different people fulfill the roles of End Users (Desk Staff and Managers), Application Programmers, "
        "Database Designers, and DBAs. In this course project, I performed all these roles: designing the ER model, writing and running the DDL/DML "
        "scripts in SQL Developer, developing the Python Flask backend and templates, and testing the system.",
        space_after=12
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 4: CONCEPTUAL DATABASE DESIGN
    # ====================================================
    add_h1(doc, "CHAPTER 4: CONCEPTUAL DATABASE DESIGN")
    
    add_h2(doc, "4.1 Entity Identification")
    ent_data = [
        ("BRANCH", "Strong Entity", "A physical branch office where vehicles are stationed and rented."),
        ("CATEGORY", "Strong Entity", "A vehicle class (Hatchback, Sedan, SUV, Luxury) setting daily rental rates."),
        ("CUSTOMER", "Strong Entity", "An individual with verified contact details and driving license number."),
        ("VEHICLE", "Strong Entity", "A motor vehicle assigned to a home branch and belonging to a category."),
        ("BOOKING", "Strong Entity", "A rental contract linking a customer to a vehicle for a specified date range."),
        ("PAYMENT", "Strong Entity", "A monetary payment transaction recorded against a specific booking."),
        ("MAINTENANCE", "Strong Entity", "A workshop servicing record tracking vehicle downtime and repair cost."),
        ("BK_LOG", "Strong Entity (Audit)", "An audit entry recording a booking status transition, written by a trigger.")
    ]
    add_table_data(
        doc, "Table 4.1: Entities and their roles",
        ["Entity Name", "Entity Type", "Role in Vehicle Rental Domain"],
        ent_data, [Inches(1.5), Inches(1.5), Inches(3.5)], font_size=8.5
    )

    add_h2(doc, "4.2 Attributes and Attribute Types")
    add_p(
        doc,
        "All attributes across the 8 entities are simple and atomic. Address is stored as a single string and handled atomically by the application. "
        "Derived attributes are used intentionally: booking.total is calculated as (edt - sdt) multiplied by category.rate, computed automatically "
        "by trigger trg_bk_bi. Storing total ensures that past rental invoices remain historically accurate even if category tariffs are updated later.",
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
        ("audits", "BOOKING (1) – BK_LOG (N)", "1 : N", "BK_LOG.bkid (populated by trg_bk_au trigger)")
    ]
    add_table_data(
        doc, "Table 4.2: Relationships and cardinality",
        ["Relationship", "Entities Involved", "Cardinality", "Relational Implementation"],
        rel_data, [Inches(1.2), Inches(2.0), Inches(1.0), Inches(2.3)], font_size=8.5
    )

    add_h2(doc, "4.4 Participation Constraints")
    add_bullet(doc, "Total Participation of VEHICLE in BRANCH and CATEGORY: ", "Every vehicle must be assigned to an existing branch and category (NOT NULL foreign keys).")
    add_bullet(doc, "Partial Participation of BRANCH and CATEGORY: ", "A branch or category can exist before any vehicle is assigned to it.")
    add_bullet(doc, "Total Participation of BOOKING in CUSTOMER and VEHICLE: ", "Every booking must be tied to an existing customer and an existing vehicle.")
    add_bullet(doc, "Partial Participation of CUSTOMER and VEHICLE: ", "A customer can exist without an active booking; a vehicle can exist without any active reservations.")

    add_h2(doc, "4.5 Weak and Strong Entities")
    add_p(
        doc,
        "Every table has its own unique primary key identifier (bid, cid, custid, vid, bkid, pid, mid, lid). "
        "Therefore, there are no weak entities in the strict ER sense. All entities represent distinct real-world domain objects "
        "with their own lifecycles governed by referential integrity.",
        space_after=8
    )

    add_h2(doc, "4.6 ER Diagram")
    add_figure(
        doc, os.path.join(assets_dir, "fig_4_1_er_diagram.png"),
        "Figure 4.1: Entity-Relationship diagram (diamonds = relationships; UK = unique key; PK = primary key)"
    )

    add_h2(doc, "4.7 Design Assumptions")
    add_bullet(doc, "Daily Tariff Calculation: ", "Rental charges are computed as whole calendar days (edt - sdt) multiplied by category daily rate.")
    add_bullet(doc, "Maintenance Quarantine: ", "Vehicles in SERVICE status cannot be reserved or dispatched under any circumstances.")
    add_bullet(doc, "Vehicle State Machine: ", "Transitioning a booking to ACTIVE automatically locks vehicle status to RENTED; returning it restores AVAILABLE.")
    add_bullet(doc, "Payment Settlement: ", "Payments cannot exceed the outstanding balance (f_bal), preventing negative customer balances.")

    doc.add_page_break()
