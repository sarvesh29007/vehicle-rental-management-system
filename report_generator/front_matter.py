"""
Front matter generation for the Vehicle Rental Project Report.
Refined for an authentic, high-scoring student report voice.
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_generator.styles import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TEXT,
    add_h1, add_h2, add_p, add_bullet, add_table_data
)

def build_front_matter(doc, assets_dir):
    # ----------------------------------------------------
    # PAGE 1: TITLE PAGE
    # ----------------------------------------------------
    logo_path = os.path.join(assets_dir, "page_1_img_1.jpeg")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(20)
        p_logo.paragraph_format.space_after = Pt(12)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(3.2))
        
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst1 = p_inst.add_run("School of Computer Science Engineering and Information Systems\n")
    r_inst1.font.name = 'Times New Roman'
    r_inst1.font.size = Pt(13)
    r_inst1.font.bold = True
    r_inst1.font.color.rgb = COLOR_TEXT
    r_inst2 = p_inst.add_run("VIT, Vellore\n\n\n")
    r_inst2.font.name = 'Times New Roman'
    r_inst2.font.size = Pt(13)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = COLOR_TEXT

    r_sub = p_inst.add_run("DATABASE SYSTEMS\n\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_PRIMARY

    r_rep = p_inst.add_run("PROJECT REPORT\n\n\n")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(14)
    r_rep.font.bold = True
    r_rep.font.color.rgb = COLOR_TEXT

    r_title = p_inst.add_run("\"Vehicle Rental Management System\"\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(17)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    r_subt = p_inst.add_run("A Relational Database with Triggers, Transactions and a Web Application\n\n\n\n")
    r_subt.font.name = 'Times New Roman'
    r_subt.font.size = Pt(11)
    r_subt.font.color.rgb = COLOR_TEXT

    r_subm = p_inst.add_run("Submitted by\n")
    r_subm.font.name = 'Times New Roman'
    r_subm.font.size = Pt(12)
    r_subm.font.bold = True
    r_subm.font.color.rgb = COLOR_TEXT

    r_name = p_inst.add_run("Sarvesh R\n")
    r_name.font.name = 'Times New Roman'
    r_name.font.size = Pt(13)
    r_name.font.bold = True
    r_name.font.color.rgb = COLOR_TEXT

    r_reg = p_inst.add_run("24BYB0081\n\n\n\n")
    r_reg.font.name = 'Times New Roman'
    r_reg.font.size = Pt(11)
    r_reg.font.color.rgb = COLOR_TEXT

    r_ay = p_inst.add_run("Academic Year: 2026–2027\n\n")
    r_ay.font.name = 'Times New Roman'
    r_ay.font.size = Pt(12)
    r_ay.font.bold = True
    r_ay.font.color.rgb = COLOR_TEXT

    r_code = p_inst.add_run("Full code: ")
    r_code.font.name = 'Times New Roman'
    r_code.font.size = Pt(10.5)
    r_link = p_inst.add_run("GitHub Link")
    r_link.font.name = 'Times New Roman'
    r_link.font.size = Pt(10.5)
    r_link.font.underline = True
    r_link.font.color.rgb = RGBColor(37, 99, 235)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 2: CERTIFICATE
    # ----------------------------------------------------
    add_h1(doc, "CERTIFICATE")
    add_p(
        doc,
        "This is to certify that the project report entitled \"Vehicle Rental Management System\" is a bona fide "
        "record of the work carried out by Sarvesh R (Register No: 24BYB0081) in partial fulfilment of the requirements "
        "of the course BCSE302L Database Systems at the School of Computer Science Engineering and Information "
        "Systems (SCOPE), VIT, Vellore, during the academic year 2026–2027.",
        space_after=28
    )
    add_p(doc, "Dr. THANGA MARIAPPAN L", bold_prefix="Faculty Guide: ", space_after=6)
    add_p(doc, "02/11/2026", bold_prefix="Date: ", space_after=12)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 3: DECLARATION
    # ----------------------------------------------------
    add_h1(doc, "DECLARATION")
    add_p(
        doc,
        "I hereby declare that this project report entitled \"Vehicle Rental Management System\" is the result of my "
        "own work, carried out under the guidance of Dr. THANGA MARIAPPAN L. It has not been submitted to any other "
        "course, degree, or institution. Where ideas, text, SQL queries, or code from other sources have been used, "
        "they have been properly cited in the References. All data used in this project is fictitious and contains "
        "no real personal, vehicle registration, or financial information.",
        space_after=20
    )
    
    p_sig_lbl = doc.add_paragraph()
    p_sig_lbl.paragraph_format.space_before = Pt(8)
    p_sig_lbl.paragraph_format.space_after = Pt(4)
    r_sig_lbl = p_sig_lbl.add_run("Signature:\n")
    r_sig_lbl.font.name = 'Times New Roman'
    r_sig_lbl.font.size = Pt(11)
    r_sig_lbl.font.bold = True
    r_sig_lbl.font.color.rgb = COLOR_TEXT

    # Digital Signature Image
    sig_path = os.path.join(assets_dir, "signature_sarvesh.jpg")
    if os.path.exists(sig_path):
        p_sig_img = doc.add_paragraph()
        p_sig_img.paragraph_format.space_before = Pt(0)
        p_sig_img.paragraph_format.space_after = Pt(8)
        r_sig_img = p_sig_img.add_run()
        r_sig_img.add_picture(sig_path, width=Inches(1.8))
        
    add_p(doc, "Sarvesh R", bold_prefix="Name: ", space_after=4)
    add_p(doc, "02/11/2026", bold_prefix="Date: ", space_after=12)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 4: ACKNOWLEDGEMENT & ABSTRACT
    # ----------------------------------------------------
    add_h1(doc, "ACKNOWLEDGEMENT")
    add_p(
        doc,
        "I express my sincere thanks to my faculty guide Dr. THANGA MARIAPPAN L, School of Computer Science "
        "Engineering and Information Systems (SCOPE), VIT, Vellore, for his continuous guidance, valuable suggestions, "
        "and laboratory support throughout this semester. His insights helped me understand how theoretical database "
        "concepts like normalization, triggers, and cursors apply in practice.",
        space_after=18
    )

    add_h1(doc, "ABSTRACT")
    add_p(
        doc,
        "Car and bike rental agencies handle valuable vehicles, dynamic daily rental rates, and strict customer schedules. "
        "When managed manually with spreadsheets, common problems arise: two customers get booked for the same car on the same weekend, "
        "a car sent for repair is mistakenly handed out, rental totals are miscalculated, and pending balances go untracked. "
        "This project presents a practical Vehicle Rental Management System (VRMS) built to solve these problems by moving "
        "all business logic, validation rules, and rate calculations directly into an Oracle relational database.",
        space_after=6
    )
    add_p(
        doc,
        "The database is designed with eight normalized tables (branch, category, customer, vehicle, booking, payment, "
        "maintenance, and bk_log) enforcing primary key, foreign key, NOT NULL, UNIQUE, and CHECK constraints. "
        "To keep the application fast and reliable, booking totals are calculated automatically from category daily rates "
        "using an Oracle BEFORE INSERT trigger (trg_bk_bi), which also blocks any booking on a vehicle that is currently in SERVICE. "
        "An AFTER UPDATE trigger (trg_bk_au) automatically marks the car as RENTED when the trip starts and AVAILABLE when returned, "
        "while writing an unalterable history into an audit log table (bk_log). Stored procedures (p_book, p_start, p_return, p_pay) "
        "and functions (f_bal, f_avail) handle the operations, and an explicit cursor (p_dues) generates a report of customers "
        "with unpaid dues. A clean Python Flask web application connects to the database via python-oracledb (Thin mode) to provide "
        "simple Staff and Manager screens without needing any external CSS libraries or CDNs. All sixteen course queries and twenty-eight "
        "test cases were executed and verified against real database outputs.",
        space_after=10
    )
    add_p(
        doc,
        "Database Management System, ER Model, Oracle 26ai, SQL, Normalization, PL/SQL, Transactions, Triggers, Vehicle Rental, Python Flask",
        bold_prefix="Keywords: ",
        italic=True,
        space_after=14
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGES 5-7: TABLE OF CONTENTS & LISTS
    # ----------------------------------------------------
    add_h1(doc, "TABLE OF CONTENTS")
    
    toc_data = [
        ("Certificate", "2"),
        ("Declaration", "3"),
        ("Acknowledgement", "4"),
        ("Abstract", "4"),
        ("List of Figures", "5"),
        ("List of Tables", "7"),
        ("List of Abbreviations", "8"),
        ("Chapter 1 – Introduction", "9"),
        ("Chapter 2 – Requirements Analysis", "12"),
        ("Chapter 3 – DBMS Concepts and Architecture", "15"),
        ("Chapter 4 – Conceptual Database Design", "17"),
        ("Chapter 5 – Relational Database Design", "20"),
        ("Chapter 6 – Functional Dependencies and Normalization", "25"),
        ("Chapter 7 – SQL Implementation", "27"),
        ("Chapter 8 – Advanced Database Operations", "37"),
        ("Chapter 9 – Query Processing and Optimization", "41"),
        ("Chapter 10 – Database Security, Transactions and Recovery", "43"),
        ("Chapter 11 – Application Development and Connectivity", "45"),
        ("Chapter 12 – Testing and Results", "51"),
        ("Chapter 13 – Conclusion and Future Enhancements", "54"),
        ("References", "54"),
        ("Appendix A – SQL Scripts", "56"),
        ("Appendix B – Sample Data and Screenshots", "58"),
        ("Appendix C – Sample Test Case Table", "60")
    ]
    
    add_table_data(
        doc, "", ["Chapter / Section", "Page"],
        toc_data, [Inches(5.2), Inches(1.3)], font_size=9.5
    )
    
    add_h1(doc, "LIST OF FIGURES")
    figures_data = [
        ("Figure 2.1: Use-case diagram of the Vehicle Rental Management System", "14"),
        ("Figure 4.1: Entity-Relationship diagram (diamonds = relationships; UK = unique key)", "18"),
        ("Figure 5.1: Relational schema diagram with primary and foreign key links", "22"),
        ("Figure 11.1: Three-tier architecture of the Vehicle Rental Management System", "45"),
        ("Figure 11.2: Web application: role-based authentication portal", "47"),
        ("Figure 11.3: Staff portal: operations dashboard and live fleet metrics", "47"),
        ("Figure 11.4: Staff portal: new reservation booking with trigger validation", "48"),
        ("Figure 11.5: Staff portal: active rental tracking, trip dispatch, and return", "48"),
        ("Figure 11.6: Manager portal: executive KPI dashboard and fleet revenue", "49"),
        ("Figure 11.7: Manager portal: outstanding receivables audit report via cursor", "49"),
        ("Figure B.1: Manager portal: interactive database tables and data dictionary inspector", "59")
    ]
    add_table_data(
        doc, "", ["Figure Caption", "Page"],
        figures_data, [Inches(5.2), Inches(1.3)], font_size=9
    )
    
    doc.add_page_break()

    add_h1(doc, "LIST OF TABLES")
    tables_data = [
        ("Table 2.1: User roles and responsibilities", "12"),
        ("Table 2.2: Functional requirements and implementing component", "12"),
        ("Table 2.3: Hardware and software requirements", "13"),
        ("Table 2.4: Key use-case descriptions", "14"),
        ("Table 3.1: File system versus DBMS in the vehicle rental context", "15"),
        ("Table 3.2: SQL sub-languages and their use in the project", "16"),
        ("Table 4.1: Entities and their roles", "17"),
        ("Table 4.2: Relationships and cardinality", "17"),
        ("Table 5.1: Keys of each relation", "20"),
        ("Table 5.2: Integrity constraints used", "21"),
        ("Table 5.3: Data dictionary: BRANCH", "22"),
        ("Table 5.4: Data dictionary: CATEGORY", "22"),
        ("Table 5.5: Data dictionary: CUSTOMER", "22"),
        ("Table 5.6: Data dictionary: VEHICLE", "23"),
        ("Table 5.7: Data dictionary: BOOKING", "23"),
        ("Table 5.8: Data dictionary: PAYMENT", "23"),
        ("Table 5.9: Data dictionary: MAINTENANCE", "24"),
        ("Table 5.10: Data dictionary: BK_LOG", "24"),
        ("Table 6.1: BCNF check: every non-trivial determinant must be a superkey", "26"),
        ("Table 6.2: Before: flat relation (redundant vehicle, tariff, and branch attributes)", "26"),
        ("Table 7.1: Functions used in the project SQL", "27"),
        ("Table 7.2: Join types demonstrated", "28"),
        ("Table 7.3: Output of the view query (v_open_bookings)", "28"),
        ("Table 7.4: Constraint demonstration (actual Oracle error responses)", "29"),
        ("Table 7.5 to 7.20: Outputs of Queries 1 to 16", "29–36"),
        ("Table 8.1: Procedures in the running implementation", "37"),
        ("Table 8.2: Seeded booking totals versus category tariffs", "37"),
        ("Table 8.4: ACID properties and evidence", "39"),
        ("Table 8.5: Savepoint demonstration values", "40"),
        ("Table 8.6: Concurrency and row-level locking experiment", "40"),
        ("Table 9.1: Automatic and explicit indexes in the database", "41"),
        ("Table 9.2: Execution plans (EXPLAIN PLAN actual output)", "41"),
        ("Table 9.3: Query 4 plan with foreign key index", "42"),
        ("Table 9.4: Effect of the composite index on query latency", "42"),
        ("Table 10.1: Permitted and denied operations (security test results)", "44"),
        ("Table 11.1: Technology stack", "45"),
        ("Table 11.2: CRUD workflows and application routes", "46"),
        ("Table 12.1: Test cases and actual results (28 tests)", "51"),
        ("Table 12.2: Manual verification of query results", "53"),
        ("Table B.1 to B.8: Sample data for all 8 tables", "58–59"),
        ("Table C.1: Sample test cases summary", "60")
    ]
    add_table_data(
        doc, "", ["Table Title", "Page"],
        tables_data, [Inches(5.2), Inches(1.3)], font_size=8.5
    )

    add_h1(doc, "LIST OF ABBREVIATIONS")
    abbrev_list = [
        ("DBMS", "Database Management System"),
        ("RDBMS", "Relational Database Management System"),
        ("SQL", "Structured Query Language"),
        ("DDL", "Data Definition Language"),
        ("DML", "Data Manipulation Language"),
        ("DQL", "Data Query Language"),
        ("DCL", "Data Control Language"),
        ("TCL", "Transaction Control Language"),
        ("PL/SQL", "Procedural Language extension to SQL (Oracle)"),
        ("ER", "Entity–Relationship"),
        ("ACID", "Atomicity, Consistency, Isolation, Durability"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("PK / FK / UQ", "Primary Key / Foreign Key / Unique constraint"),
        ("BCNF", "Boyce–Codd Normal Form"),
        ("3NF", "Third Normal Form"),
        ("FD", "Functional Dependency"),
        ("DL", "Driving License Number"),
        ("API", "Application Programming Interface"),
        ("REST", "Representational State Transfer"),
        ("JSON", "JavaScript Object Notation"),
        ("PDB", "Pluggable Database (Oracle Multitenant Architecture)"),
        ("VRMS", "Vehicle Rental Management System")
    ]
    for ab, desc in abbrev_list:
        add_bullet(doc, f"{ab} – ", desc)
        
    doc.add_page_break()
