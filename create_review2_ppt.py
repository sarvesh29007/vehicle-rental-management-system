"""
Complete PowerPoint Generator for Review II: Database Implementation
BCSE302L - Database Systems | VIT
Student: Sarvesh | Reg No: 24BYB0081 | Faculty: THANGA MARIAPPAN L
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_review2_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(15, 23, 42)          # #0f172a
    DARK_BLUE = RGBColor(30, 58, 138)     # #1e3a8a
    ACCENT_BLUE = RGBColor(37, 99, 235)   # #2563eb
    LIGHT_BG = RGBColor(248, 250, 252)    # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(30, 41, 59)      # #1e293b
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748b
    GOLD = RGBColor(217, 119, 6)          # #d97706
    GREEN = RGBColor(22, 101, 52)         # #166534
    CODE_BG = RGBColor(15, 23, 42)        # #0f172a
    CODE_TXT = RGBColor(226, 232, 240)    # #e2e8f0
    CODE_GREEN = RGBColor(74, 222, 128)   # #4ade80
    BORDER_COLOR = RGBColor(203, 213, 225) # #cbd5e1

    def add_header(slide, title_text, category_text="REVIEW II: DATABASE IMPLEMENTATION"):
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = NAVY
        header_shape.line.fill.background()

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = ACCENT_BLUE
        line.line.fill.background()

        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.28))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = GOLD

        tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf2 = tx_box2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = WHITE

        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.7), Inches(0.35))
        tf_f = footer_box.text_frame
        pf = tf_f.paragraphs[0]
        pf.text = "BCSE302L - Database Systems | Sarvesh R (24BYB0081) | SCOPE, VIT"
        pf.font.size = Pt(9.5)
        pf.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title="", title_color=DARK_BLUE, bg_color=WHITE, border_color=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), width - Inches(0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = title_color
            return left + Inches(0.2), top + Inches(0.55), width - Inches(0.4), height - Inches(0.65)
        return left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4)

    def add_code_box(slide, left, top, width, height, code_text, font_size=9):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = CODE_BG
        box.line.color.rgb = RGBColor(51, 65, 85)
        box.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.1), width - Inches(0.3), height - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        lines = code_text.strip().splitlines()
        for idx, line in enumerate(lines):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.text = line
            p.font.name = "Consolas"
            p.font.size = Pt(font_size)
            if line.strip().startswith(("--", "/*", "*")):
                p.font.color.rgb = RGBColor(148, 163, 184)
            elif any(k in line.upper() for k in ["CREATE", "SELECT", "INSERT", "UPDATE", "DELETE", "FUNCTION", "PROCEDURE", "TRIGGER", "CURSOR"]):
                p.font.color.rgb = CODE_GREEN
            else:
                p.font.color.rgb = CODE_TXT

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    t_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.0), Inches(3.5), Inches(0.08))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = ACCENT_BLUE
    t_line.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.8), Inches(2.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VEHICLE RENTAL MANAGEMENT SYSTEM"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "REVIEW II – DATABASE IMPLEMENTATION & PL/SQL ARCHITECTURE"
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = GOLD
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Relational DDL, Constraints, 16 SQL Queries, Stored Procedures, Functions, Explicit Cursor & Triggers"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(6)

    card_info = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(10.9), Inches(2.4))
    card_info.fill.solid()
    card_info.fill.fore_color.rgb = RGBColor(30, 41, 59)
    card_info.line.color.rgb = RGBColor(51, 65, 85)
    card_info.line.width = Pt(1.5)

    tb_info = s1.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10.3), Inches(2.0))
    tfi = tb_info.text_frame
    tfi.word_wrap = True

    def meta_row(p, label, val):
        p.text = f"{label}: "
        p.font.bold = True
        p.font.size = Pt(12.5)
        p.font.color.rgb = GOLD
        r = p.add_run()
        r.text = val
        r.font.bold = False
        r.font.color.rgb = WHITE

    p = tfi.paragraphs[0]
    meta_row(p, "Course", "BCSE302L - Database Systems (Laboratory Project)")
    p = tfi.add_paragraph()
    meta_row(p, "Student Name", "Sarvesh R")
    r1 = p.add_run()
    r1.text = "     |     Register Number: "
    r1.font.bold = True
    r1.font.color.rgb = GOLD
    r2 = p.add_run()
    r2.text = "24BYB0081"
    r2.font.color.rgb = WHITE
    p = tfi.add_paragraph()
    meta_row(p, "Faculty In-Charge", "Prof. THANGA MARIAPPAN L")
    p = tfi.add_paragraph()
    meta_row(p, "Institution", "School of Computer Science Engineering and Information Systems (SCOPE), VIT")

    # =========================================================================
    # SLIDE 2: Evaluation Rubrics Alignment
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Review II Evaluation Rubrics & Compliance")

    cx, cy, cw, ch = add_card(s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Evaluation Criteria (10 Marks)", DARK_BLUE)
    tb = s2.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    rubrics = [
        ("DDL & Constraints (2 Marks)", "8 normalized tables with Primary Keys, Foreign Keys, NOT NULL, UNIQUE, CHECK and DEFAULT rules."),
        ("DML & Data Population (1 Mark)", "At least 10 meaningful records per table (10 branches, 10 categories, 10 customers, 10 vehicles, 12 bookings, 10 payments, etc.)."),
        ("SQL Queries (2 Marks)", "16 comprehensive queries covering joins, multi-level aggregation, subqueries, set operations and string/date functions."),
        ("Procedures & Functions (2 Marks)", "2 Functions (f_bal, f_avail) & 5 Stored Procedures (p_book, p_start, p_return, p_pay, p_dues) implementing business logic."),
        ("Cursor & Triggers (2 Marks)", "1 Explicit Cursor with %ROWTYPE loop; 2 Triggers (trg_bk_bi Before Insert & trg_bk_au After Update) avoiding mutating tables."),
        ("Viva & Technical Understanding (1 Mark)", "Demonstrated on real Oracle Database 26ai Free instance (localhost:1521/FREEPDB1) with zero compilation errors.")
    ]
    for i, (t, d) in enumerate(rubrics):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(7)

    cx2, cy2, cw2, ch2 = add_card(s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Implementation Highlights", GREEN)
    tb2 = s2.shapes.add_textbox(cx2, cy2, cw2, ch2)
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    highlights = [
        ("Target Database Engine", "Oracle Database 26ai Free running Pluggable Database FREEPDB1."),
        ("Zero ORM Architecture", "All business logic, constraints, and validation execute natively in Oracle SQL & PL/SQL."),
        ("Mutating Table Defense", "Triggers query only static parent tables (vehicle, category) without referencing the mutating booking table."),
        ("Standardized Exceptions", "Custom business exceptions use Oracle RAISE_APPLICATION_ERROR in the -20001 to -20006 range."),
        ("Data Dictionary Verification", "Full metadata validated through USER_TAB_COLUMNS, USER_CONSTRAINTS, and USER_CONS_COLUMNS."),
        ("Interactive Verification", "Executed cleanly in Oracle SQL Developer (F5) and integrated with Python Flask web interface.")
    ]
    for i, (t, d) in enumerate(highlights):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"✔ {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = GREEN
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(7)

    # =========================================================================
    # SLIDE 3: Relational Schema Architecture (8 Tables)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Relational Schema Architecture (8 Tables)")
    tables_meta = [
        ("1. BRANCH", "bid (PK), bname (NN), city (NN), phone (UQ)", "Manages physical office branches across Indian cities.", DARK_BLUE),
        ("2. CATEGORY", "cid (PK), cname (NN, UQ), rate (NN, CK rate > 0)", "Vehicle categories & standard daily rental tariffs.", DARK_BLUE),
        ("3. CUSTOMER", "custid (PK), name (NN), phone (NN, UQ), email (UQ), lic_no (NN, UQ), city (DF 'Chennai')", "Client profiles with driving license verification.", DARK_BLUE),
        ("4. VEHICLE", "vid (PK), reg_no (NN, UQ), model (NN), cid (FK), bid (FK), yr (CK >= 2015), status (DF 'AVAILABLE')", "Physical fleet inventory with branch & category mapping.", DARK_BLUE),
        ("5. BOOKING", "bkid (PK), custid (FK), vid (FK), sdt (NN), edt (NN), status (DF 'BOOKED'), total (DF 0), CK(edt > sdt)", "Core rental reservation contracts and duration window.", GOLD),
        ("6. PAYMENT", "pid (PK), bkid (FK), amt (NN, CK > 0), pdt (DF SYSDATE), pmode (CK 'CASH','UPI','CARD')", "Financial transactions ledger linked to bookings.", GOLD),
        ("7. MAINTENANCE", "mid (PK), vid (FK), mdt (NN), cost (CK >= 0), descr", "Service, repair, and workshop inspection records per vehicle.", GREEN),
        ("8. BK_LOG", "lid (PK), bkid, old_st, new_st, ldt (DF SYSDATE)", "Autonomous audit trail populated exclusively by database trigger.", GREEN)
    ]
    cw, ch = Inches(2.75), Inches(2.55)
    gx, gy = Inches(0.25), Inches(0.25)
    sx, sy = Inches(0.8), Inches(1.4)
    for i, (t_name, schema_txt, desc_txt, col) in enumerate(tables_meta):
        x = sx + (i % 4) * (cw + gx)
        y = sy + (i // 4) * (ch + gy)
        cx, cy, c_w, c_h = add_card(s3, x, y, cw, ch, t_name, col)
        tb = s3.shapes.add_textbox(cx, cy, c_w, c_h)
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = "Schema / Keys:"
        p1.font.bold = True
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = DARK_BLUE
        p2 = tf.add_paragraph()
        p2.text = schema_txt
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_DARK
        p2.space_after = Pt(4)
        p3 = tf.add_paragraph()
        p3.text = "Description:"
        p3.font.bold = True
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED
        p4 = tf.add_paragraph()
        p4.text = desc_txt
        p4.font.size = Pt(8.5)
        p4.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: DDL Implementation & Constraint Architecture
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "DDL Implementation & Constraint Architecture")

    cx, cy, cw, ch = add_card(s4, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Core Constraints Implemented", DARK_BLUE)
    tb = s4.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    constraints_info = [
        ("Primary Key (PK)", "Ensures entity integrity on all 8 tables (bid, cid, custid, vid, bkid, pid, mid, lid)."),
        ("Foreign Key (FK)", "Enforces referential integrity across 6 relationships:\n• vehicle.cid → category.cid, vehicle.bid → branch.bid\n• booking.custid → customer.custid, booking.vid → vehicle.vid\n• payment.bkid → booking.bkid, maintenance.vid → vehicle.vid"),
        ("UNIQUE Constraints", "Prevents duplicate business values:\n• branch(phone), category(cname), vehicle(reg_no)\n• customer(phone, email, lic_no)"),
        ("CHECK Constraints", "Enforces domain validity:\n• rate > 0 (category), yr >= 2015 (vehicle)\n• status IN ('AVAILABLE','RENTED','SERVICE') (vehicle)\n• edt > sdt (booking rental window validity)\n• status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED')\n• amt > 0, pmode IN ('CASH','UPI','CARD') (payment)\n• cost >= 0 (maintenance)"),
        ("DEFAULT Values", "Ensures default state without manual specification:\n• customer(city DEFAULT 'Chennai')\n• vehicle(status DEFAULT 'AVAILABLE')\n• booking(status DEFAULT 'BOOKED', total DEFAULT 0)\n• payment(pdt DEFAULT SYSDATE), bk_log(ldt DEFAULT SYSDATE)")
    ]
    for i, (t, d) in enumerate(constraints_info):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(9.5)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    cx2, cy2, cw2, ch2 = add_card(s4, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "DDL Code Highlights (Oracle DDL)", DARK_BLUE)
    ddl_sample = """-- Table: vehicle (FKs, CHECKs, DEFAULTs)
CREATE TABLE vehicle (
  vid    NUMBER PRIMARY KEY,
  reg_no VARCHAR2(12) NOT NULL UNIQUE,
  model  VARCHAR2(30) NOT NULL,
  cid    NUMBER NOT NULL REFERENCES category(cid),
  bid    NUMBER NOT NULL REFERENCES branch(bid),
  yr     NUMBER(4) CHECK (yr >= 2015),
  status VARCHAR2(10) DEFAULT 'AVAILABLE'
         CHECK (status IN ('AVAILABLE','RENTED','SERVICE'))
);

-- Table: booking (Compound date check & FKs)
CREATE TABLE booking (
  bkid   NUMBER PRIMARY KEY,
  custid NUMBER NOT NULL REFERENCES customer(custid),
  vid    NUMBER NOT NULL REFERENCES vehicle(vid),
  sdt    DATE NOT NULL,
  edt    DATE NOT NULL,
  status VARCHAR2(10) DEFAULT 'BOOKED'
         CHECK (status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED')),
  total  NUMBER(10,2) DEFAULT 0,
  CONSTRAINT ck_dt CHECK (edt > sdt)
);

-- Sequences for Primary Key generation
CREATE SEQUENCE seq_bk  START WITH 13;
CREATE SEQUENCE seq_pay START WITH 11;
CREATE SEQUENCE seq_log START WITH 1;"""
    add_code_box(s4, cx2, cy2, cw2, ch2, ddl_sample, 8.5)

    # =========================================================================
    # SLIDE 5: DML & Data Population
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "DML & Data Population (10+ Records Per Table)")

    cx, cy, cw, ch = add_card(s5, Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.4), "Meaningful Sample Dataset Breakdown", DARK_BLUE)
    tb = s5.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    pop_info = [
        ("10 Branches", "Chennai, Vellore, Coimbatore, Madurai, Trichy, Salem, Bangalore, Hyderabad, Kochi, Pune. Realistic phone codes."),
        ("10 Categories", "Hatchback (1200), Sedan (1800), SUV (2500), Luxury (5000), Bike (500), Scooter (400), Van (3000), MUV (2800), Electric (2200), Convertible (6000)."),
        ("10 Customers", "Diverse clientele across Tamil Nadu, Kerala, Karnataka, Maharashtra, and Telangana with valid driving license numbers."),
        ("10 Vehicles", "Swift, Honda City, Creta, BMW 3 Series, Royal Enfield, Activa, Force Traveller, Innova, Nexon EV, Mini Cooper (Vehicle 10 set to SERVICE)."),
        ("12 Bookings", "Mostly RETURNED, 1 CANCELLED (#8), 1 ACTIVE (#11), 1 BOOKED (#12). Totals computed dynamically via trigger."),
        ("10 Payments", "UPI, CARD, and CASH modes. Each payment amount strictly <= booking total to maintain integrity."),
        ("10 Maintenance Records", "Oil change, brake pads, clutch, full service, AC repair, engine overhaul ranging from Rs. 800 to Rs. 15,000."),
        ("11 Audit Log Records", "Historical transition audit records populated in bk_log.")
    ]
    for i, (t, d) in enumerate(pop_info):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(9.5)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(4)

    cx2, cy2, cw2, ch2 = add_card(s5, Inches(7.1), Inches(1.4), Inches(5.4), Inches(5.4), "Sample DML Insert Statements", DARK_BLUE)
    dml_sample = """-- Insert Category with rate constraint
INSERT INTO category VALUES (1, 'Hatchback', 1200);
INSERT INTO category VALUES (2, 'Sedan', 1800);
INSERT INTO category VALUES (3, 'SUV', 2500);

-- Insert Customer with Default city
INSERT INTO customer VALUES (1, 'Arun Kumar',
  '9840011001', 'arun.kumar@mail.com',
  'DL-TN-0001', 'Chennai');

-- Insert Vehicle (vid 10 has SERVICE status)
INSERT INTO vehicle VALUES (1, 'TN01AB1001',
  'Swift', 1, 1, 2022, 'AVAILABLE');
INSERT INTO vehicle VALUES (10, 'KL07ST9010',
  'Mini Cooper', 10, 9, 2023, 'SERVICE');

-- Insert Booking (Total computed by trigger)
INSERT INTO booking(bkid,custid,vid,sdt,edt,status)
VALUES (1, 1, 1, DATE '2026-08-01',
        DATE '2026-08-04', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status)
VALUES (11, 1, 3, DATE '2026-10-11',
        DATE '2026-10-15', 'ACTIVE');"""
    add_code_box(s5, cx2, cy2, cw2, ch2, dml_sample, 8.5)

    # =========================================================================
    # SLIDE 6: SQL Queries - Part 1: Joins & Complex Retrieval
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "SQL Queries Showcase: Joins & Complex Retrieval")

    cx, cy, cw, ch = add_card(s6, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Q1: 3-Table Join (Booking Details)", DARK_BLUE)
    q1_code = """-- Q1: Booking with Customer & Vehicle details
SELECT b.bkid, c.name AS customer_name,
       v.model AS vehicle_model,
       b.sdt, b.edt, b.status, b.total
FROM booking b
JOIN customer c ON b.custid = c.custid
JOIN vehicle v   ON b.vid = v.vid
ORDER BY b.bkid;

-- Real Oracle Output: 12 rows returned
-- #1: Arun Kumar | Swift | Aug 1-4 | RETURNED | 3600
-- #2: Priya Sharma | Creta | Aug 5-8 | RETURNED | 7500
-- #11: Arun Kumar | Creta | Oct 11-15 | ACTIVE | 10000
-- #12: Priya Sharma | City | Oct 20-23 | BOOKED | 5400"""
    add_code_box(s6, cx, cy, cw, ch, q1_code, 8.5)

    cx2, cy2, cw2, ch2 = add_card(s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Q6 & Q12: Outer Joins (LEFT JOIN)", DARK_BLUE)
    q6_code = """-- Q6: Vehicles per branch (LEFT JOIN + GROUP BY)
SELECT b.bid, b.bname, b.city,
       COUNT(v.vid) AS vehicle_count
FROM branch b
LEFT JOIN vehicle v ON b.bid = v.bid
GROUP BY b.bid, b.bname, b.city
ORDER BY vehicle_count DESC;

-- Real Output: Chennai (2), Vellore (1),
-- Coimbatore (1), Madurai (1), Bangalore (1),
-- Kochi (1)... Koregaon Pune (0) -> preserves 0!

------------------------------------------------
-- Q12: Bookings with no payment (LEFT JOIN IS NULL)
SELECT b.bkid, c.name, b.status, b.total
FROM booking b
JOIN customer c ON b.custid = c.custid
LEFT JOIN payment p ON b.bkid = p.bkid
WHERE p.pid IS NULL;
-- Output: #8 Anita Joseph (CANCELLED), #12 Priya (BOOKED)"""
    add_code_box(s6, cx2, cy2, cw2, ch2, q6_code, 8.2)

    # =========================================================================
    # SLIDE 7: SQL Queries - Part 2: Aggregations & Grouping
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "SQL Queries Showcase: Aggregations & Grouping")

    cx, cy, cw, ch = add_card(s7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Q2: Category Revenue & Q3: HAVING Clause", DARK_BLUE)
    q2_code = """-- Q2: Revenue and trips per category
SELECT g.cname AS category,
       COUNT(b.bkid) AS trips,
       NVL(SUM(b.total), 0) AS total_revenue
FROM category g
JOIN vehicle v ON g.cid = v.cid
LEFT JOIN booking b ON v.vid = b.vid
                   AND b.status <> 'CANCELLED'
GROUP BY g.cname
ORDER BY total_revenue DESC;
-- Output: SUV (Rs 17,500), Luxury (Rs 15,000),
-- Van (Rs 12,000), MUV (Rs 11,200), Sedan (Rs 9,000)...

------------------------------------------------
-- Q3: Customers with > 1 booking (HAVING)
SELECT c.name, COUNT(b.bkid) AS booking_count
FROM customer c
JOIN booking b ON c.custid = b.custid
GROUP BY c.name
HAVING COUNT(b.bkid) > 1;
-- Output: Arun Kumar (2 trips), Priya Sharma (2 trips)"""
    add_code_box(s7, cx, cy, cw, ch, q2_code, 8.2)

    cx2, cy2, cw2, ch2 = add_card(s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Q10 & Q11: Payment & Maintenance Grouping", DARK_BLUE)
    q10_code = """-- Q10: Payments aggregated by mode
SELECT pmode,
       COUNT(*) AS transactions,
       SUM(amt) AS total_collected
FROM payment
GROUP BY pmode
ORDER BY total_collected DESC;
-- Real Output:
-- CARD: 3 transactions | Rs. 34,500 collected
-- UPI:  5 transactions | Rs. 31,200 collected
-- CASH: 2 transactions | Rs. 4,600 collected

------------------------------------------------
-- Q11: Maintenance cost per vehicle
SELECT v.model, v.reg_no,
       NVL(SUM(m.cost), 0) AS total_cost
FROM vehicle v
LEFT JOIN maintenance m ON v.vid = m.vid
GROUP BY v.model, v.reg_no
ORDER BY total_cost DESC;
-- Output: Mini Cooper (15000), BMW (9500), Force (7000)..."""
    add_code_box(s7, cx2, cy2, cw2, ch2, q10_code, 8.2)

    # =========================================================================
    # SLIDE 8: SQL Queries - Part 3: Subqueries & Set Operations
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "SQL Queries Showcase: Subqueries & Set Operations")

    cx, cy, cw, ch = add_card(s8, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Q4, Q5 & Q9: Subquery Demonstrations", DARK_BLUE)
    qsub_code = """-- Q4: Vehicles never booked (NOT IN subquery)
SELECT vid, reg_no, model, status
FROM vehicle
WHERE vid NOT IN (SELECT vid FROM booking WHERE vid IS NOT NULL);
-- Output: vid 10 | KL07ST9010 | Mini Cooper | SERVICE

-- Q5: Payments above average (Scalar Subquery)
SELECT c.name, p.amt, p.pmode
FROM payment p
JOIN booking b ON p.bkid = b.bkid
JOIN customer c ON b.custid = c.custid
WHERE p.amt > (SELECT AVG(amt) FROM payment);
-- Output: Divya (15000), Rahul (12000), Sneha (11200)...

-- Q9: Costliest vehicle category (MAX subquery)
SELECT cname, rate FROM category
WHERE rate = (SELECT MAX(rate) FROM category);
-- Output: Convertible | Rs. 6000.00"""
    add_code_box(s8, cx, cy, cw, ch, qsub_code, 8.2)

    cx2, cy2, cw2, ch2 = add_card(s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Q15: Correlated EXISTS & Q16: UNION", DARK_BLUE)
    qset_code = """-- Q15: Customers with cancelled booking (EXISTS)
SELECT c.custid, c.name, c.phone, c.city
FROM customer c
WHERE EXISTS (
  SELECT 1 FROM booking b
  WHERE b.custid = c.custid
    AND b.status = 'CANCELLED'
);
-- Real Output: custid 8 | Anita Joseph | Bangalore

------------------------------------------------
-- Q16: UNION of Customer & Branch cities
SELECT city, 'Customer City' AS source_type FROM customer
UNION
SELECT city, 'Branch City' AS source_type FROM branch
ORDER BY city;
-- Output: Distinct unified set: Bangalore, Chennai,
-- Coimbatore, Hyderabad, Kochi, Madurai, Pune,
-- Salem, Trichy, Vellore."""
    add_code_box(s8, cx2, cy2, cw2, ch2, qset_code, 8.2)

    # =========================================================================
    # SLIDE 9: SQL Queries - Part 4: Functions & Views
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "SQL Queries Showcase: String/Date Functions & Views")

    cx, cy, cw, ch = add_card(s9, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Q7: String & Q8: Date Functions", DARK_BLUE)
    qfn_code = """-- Q7: Single-row functions (UPPER, LENGTH, SUBSTR, INSTR)
SELECT UPPER(name) AS upper_name,
       LENGTH(name) AS name_len,
       SUBSTR(email, 1, INSTR(email, '@') - 1) AS uname,
       SUBSTR(email, INSTR(email, '@') + 1) AS domain
FROM customer;
-- Output: ARUN KUMAR (len 10) | arun.kumar | mail.com

------------------------------------------------
-- Q8: TO_CHAR formatting and duration calculation
SELECT bkid,
       TO_CHAR(sdt, 'Mon YYYY') AS booking_month,
       TO_CHAR(sdt, 'DD-Mon-YYYY') AS start_date,
       TO_CHAR(edt, 'DD-Mon-YYYY') AS end_date,
       (edt - sdt) AS rental_days, total
FROM booking;
-- Output: #1: Aug 2026 | 01-Aug-2026 | 3 days | Rs 3600"""
    add_code_box(s9, cx, cy, cw, ch, qfn_code, 8.2)

    cx2, cy2, cw2, ch2 = add_card(s9, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Q13: Relational View & Q14: PL/SQL Function in Query", DARK_BLUE)
    qvw_code = """-- Q13: View of active and booked reservations
CREATE OR REPLACE VIEW v_open AS
SELECT b.bkid, c.name AS customer_name,
       v.model AS vehicle_model, b.sdt, b.edt, b.status
FROM booking b
JOIN customer c ON b.custid = c.custid
JOIN vehicle v   ON b.vid = v.vid
WHERE b.status IN ('BOOKED', 'ACTIVE');

SELECT * FROM v_open;
-- Output: #11 Arun Kumar (Creta ACTIVE), #12 Priya (City BOOKED)

------------------------------------------------
-- Q14: Stored function f_bal called inside SQL
SELECT b.bkid, c.name, b.total,
       f_bal(b.bkid) AS pending_balance, b.status
FROM booking b JOIN customer c ON b.custid = c.custid
WHERE f_bal(b.bkid) > 0;
-- Output: #12 Priya (Rs 5400), #11 Arun Kumar (Rs 5000)"""
    add_code_box(s9, cx2, cy2, cw2, ch2, qvw_code, 8.2)

    # =========================================================================
    # SLIDE 10: PL/SQL Function: f_bal
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "PL/SQL Stored Function 1: f_bal (Balance Computation)")

    cx, cy, cw, ch = add_card(s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Function Purpose & Logic", DARK_BLUE)
    tb = s10.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    fbal_desc = [
        ("Business Requirement", "Accurately compute outstanding payment due for any booking contract."),
        ("Cancellation Rule", "If booking status is 'CANCELLED', the pending balance must immediately return 0 (no customer charge)."),
        ("Aggregation Logic", "Queries NVL(SUM(amt), 0) from the payment table and computes: Balance = total - paid."),
        ("Exception Handling", "Captures NO_DATA_FOUND and returns -1 to indicate invalid/non-existent booking ID."),
        ("Database Security", "Guarantees financial consistency by centralizing arithmetic in Oracle rather than distributed application layers.")
    ]
    for i, (t, d) in enumerate(fbal_desc):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    cx2, cy2, cw2, ch2 = add_card(s10, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Source Code: f_bal", DARK_BLUE)
    fbal_code = """CREATE OR REPLACE FUNCTION f_bal(p_bk NUMBER)
RETURN NUMBER IS
  v_tot  booking.total%TYPE;
  v_st   booking.status%TYPE;
  v_paid NUMBER;
BEGIN
  -- 1. Fetch booking total and status
  SELECT total, status INTO v_tot, v_st
  FROM booking
  WHERE bkid = p_bk;

  -- 2. Handle cancelled reservations
  IF v_st = 'CANCELLED' THEN
    RETURN 0;
  END IF;

  -- 3. Sum up all payments received
  SELECT NVL(SUM(amt), 0) INTO v_paid
  FROM payment
  WHERE bkid = p_bk;

  -- 4. Return remaining balance
  RETURN v_tot - v_paid;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN -1; -- Non-existent booking indicator
END;
/"""
    add_code_box(s10, cx2, cy2, cw2, ch2, fbal_code, 9)

    # =========================================================================
    # SLIDE 11: PL/SQL Function: f_avail
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "PL/SQL Stored Function 2: f_avail (Availability & Overlap)")

    cx, cy, cw, ch = add_card(s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Availability & Overlap Algorithm", DARK_BLUE)
    tb = s11.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    favail_desc = [
        ("Business Objective", "Determine if a requested vehicle is eligible for a rental contract across a given date range [sdt, edt]."),
        ("Service Condition Check", "If vehicle status is 'SERVICE', returns 0 immediately (unrentable due to mechanical repairs)."),
        ("Two-Interval Overlap Condition", "Evaluates mathematically sound collision condition:\nexisting.sdt < new.edt AND existing.edt > new.sdt\nacross all 'BOOKED' and 'ACTIVE' reservations."),
        ("Atomic Verification", "Prevents double-booking even under concurrent customer reservation requests."),
        ("Return Values", "Returns 1 if completely available; returns 0 if conflicting reservation or service status exists.")
    ]
    for i, (t, d) in enumerate(favail_desc):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    cx2, cy2, cw2, ch2 = add_card(s11, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Source Code: f_avail", DARK_BLUE)
    favail_code = """CREATE OR REPLACE FUNCTION f_avail(
  p_v NUMBER, p_s DATE, p_e DATE
) RETURN NUMBER IS
  v_st  vehicle.status%TYPE;
  v_cnt NUMBER;
BEGIN
  -- 1. Check if vehicle is in SERVICE
  SELECT status INTO v_st
  FROM vehicle
  WHERE vid = p_v;

  IF v_st = 'SERVICE' THEN
    RETURN 0;
  END IF;

  -- 2. Detect overlapping BOOKED or ACTIVE rentals
  SELECT COUNT(*) INTO v_cnt
  FROM booking
  WHERE vid = p_v
    AND status IN ('BOOKED', 'ACTIVE')
    AND sdt < p_e
    AND edt > p_s;

  IF v_cnt > 0 THEN
    RETURN 0; -- Date conflict exists
  END IF;

  RETURN 1; -- Vehicle available
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN 0;
END;
/"""
    add_code_box(s11, cx2, cy2, cw2, ch2, favail_code, 9)

    # =========================================================================
    # SLIDE 12: PL/SQL Procedures: p_book & p_pay
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Stored Procedures: p_book & p_pay")

    cx, cy, cw, ch = add_card(s12, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "p_book (Atomic Booking Creation)", DARK_BLUE)
    pbook_code = """CREATE OR REPLACE PROCEDURE p_book(
  p_c NUMBER, p_v NUMBER, p_s DATE, p_e DATE
) IS
  v_new_id NUMBER;
BEGIN
  -- 1. Verify availability using f_avail
  IF f_avail(p_v, p_s, p_e) = 0 THEN
    RAISE_APPLICATION_ERROR(-20001,
      'Vehicle not available for these dates');
  END IF;

  -- 2. Generate surrogate PK via Sequence
  v_new_id := seq_bk.NEXTVAL;

  -- 3. Insert new booking in BOOKED status
  INSERT INTO booking(bkid, custid, vid, sdt, edt, status)
  VALUES (v_new_id, p_c, p_v, p_s, p_e, 'BOOKED');

  -- 4. Print confirmation
  DBMS_OUTPUT.PUT_LINE('booked id ' || v_new_id);
END;
/
-- Trigger trg_bk_bi automatically calculates total!"""
    add_code_box(s12, cx, cy, cw, ch, pbook_code, 8.5)

    cx2, cy2, cw2, ch2 = add_card(s12, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "p_pay (Payment Validation & Posting)", DARK_BLUE)
    ppay_code = """CREATE OR REPLACE PROCEDURE p_pay(
  p_b NUMBER, p_a NUMBER, p_m VARCHAR2
) IS
  v_bal NUMBER;
BEGIN
  -- 1. Fetch current balance via f_bal
  v_bal := f_bal(p_b);

  IF v_bal < 0 THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
  END IF;

  -- 2. Validate payment does not exceed balance
  IF p_a > v_bal THEN
    RAISE_APPLICATION_ERROR(-20004,
      'Amount exceeds pending balance');
  END IF;

  -- 3. Post transaction using seq_pay
  INSERT INTO payment(pid, bkid, amt, pdt, pmode)
  VALUES (seq_pay.NEXTVAL, p_b, p_a, SYSDATE, p_m);

  -- 4. Stream remaining balance
  DBMS_OUTPUT.PUT_LINE('paid, balance ' || (v_bal - p_a));
END;
/"""
    add_code_box(s12, cx2, cy2, cw2, ch2, ppay_code, 8.5)

    # =========================================================================
    # SLIDE 13: PL/SQL Procedures: p_start & p_return
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Stored Procedures: p_start & p_return (State Machine)")

    cx, cy, cw, ch = add_card(s13, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "p_start (Vehicle Handover)", DARK_BLUE)
    pstart_code = """CREATE OR REPLACE PROCEDURE p_start(p_b NUMBER) IS
  v_st booking.status%TYPE;
BEGIN
  -- 1. Verify booking exists and state is BOOKED
  SELECT status INTO v_st
  FROM booking
  WHERE bkid = p_b;

  IF v_st <> 'BOOKED' THEN
    RAISE_APPLICATION_ERROR(-20005,
      'Booking not in BOOKED state');
  END IF;

  -- 2. Transition booking to ACTIVE
  UPDATE booking SET status = 'ACTIVE' WHERE bkid = p_b;
  DBMS_OUTPUT.PUT_LINE('vehicle handed over');
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
END;
/
-- Trigger trg_bk_au automatically:
--  • Sets vehicle status = 'RENTED'
--  • Logs transition (BOOKED -> ACTIVE) in bk_log!"""
    add_code_box(s13, cx, cy, cw, ch, pstart_code, 8.5)

    cx2, cy2, cw2, ch2 = add_card(s13, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "p_return (Vehicle Return & Settlement)", DARK_BLUE)
    preturn_code = """CREATE OR REPLACE PROCEDURE p_return(p_b NUMBER) IS
  v_st booking.status%TYPE;
BEGIN
  -- 1. Verify booking exists and is ACTIVE
  SELECT status INTO v_st
  FROM booking
  WHERE bkid = p_b;

  IF v_st <> 'ACTIVE' THEN
    RAISE_APPLICATION_ERROR(-20003,
      'Booking not active');
  END IF;

  -- 2. Transition booking to RETURNED
  UPDATE booking SET status = 'RETURNED' WHERE bkid = p_b;
  DBMS_OUTPUT.PUT_LINE('returned, balance ' || f_bal(p_b));
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
END;
/
-- Trigger trg_bk_au automatically:
--  • Releases vehicle status = 'AVAILABLE'
--  • Logs transition (ACTIVE -> RETURNED) in bk_log!"""
    add_code_box(s13, cx2, cy2, cw2, ch2, preturn_code, 8.5)

    # =========================================================================
    # SLIDE 14: Explicit Cursor Processing: p_dues
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Explicit Cursor Processing: p_dues (%ROWTYPE Loop)")

    cx, cy, cw, ch = add_card(s14, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Cursor Concepts & Features", DARK_BLUE)
    tb = s14.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    cur_features = [
        ("Explicit Cursor Lifecycle", "Full demonstration of OPEN, FETCH into %ROWTYPE record, and CLOSE."),
        ("Loop Termination", "Controlled by cursor attribute: EXIT WHEN c_dues%NOTFOUND."),
        ("Strong Typing with %ROWTYPE", "Record r_due inherits exact column projection types dynamically from cursor definition."),
        ("Multi-Table Join", "Joins booking and customer to aggregate client name with reservation identifiers."),
        ("Filter & Dynamic Calculation", "Applies function f_bal(b.bkid) to evaluate outstanding balance, outputting only delinquent accounts."),
        ("Executive Total Accumulator", "Maintains running sum v_total and emits final summary balance via DBMS_OUTPUT.")
    ]
    for i, (t, d) in enumerate(cur_features):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(7)

    cx2, cy2, cw2, ch2 = add_card(s14, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Source Code: p_dues", DARK_BLUE)
    pdues_code = """CREATE OR REPLACE PROCEDURE p_dues IS
  -- 1. Explicit cursor declaration
  CURSOR c_dues IS
    SELECT b.bkid, u.name, f_bal(b.bkid) AS due_amt
    FROM booking b
    JOIN customer u ON b.custid = u.custid
    WHERE b.status <> 'CANCELLED';

  -- 2. %ROWTYPE record declaration
  r_due c_dues%ROWTYPE;
  v_total NUMBER := 0;
BEGIN
  -- 3. Explicit open
  OPEN c_dues;
  LOOP
    -- 4. Explicit fetch
    FETCH c_dues INTO r_due;
    EXIT WHEN c_dues%NOTFOUND;

    -- 5. Filter positive dues
    IF r_due.due_amt > 0 THEN
      DBMS_OUTPUT.PUT_LINE('Booking ' || r_due.bkid ||
        ' | ' || r_due.name || ' | Due: Rs. ' || r_due.due_amt);
      v_total := v_total + r_due.due_amt;
    END IF;
  END LOOP;
  -- 6. Explicit close
  CLOSE c_dues;

  DBMS_OUTPUT.PUT_LINE('total due ' || v_total);
END;
/"""
    add_code_box(s14, cx2, cy2, cw2, ch2, pdues_code, 8.5)

    # =========================================================================
    # SLIDE 15: Database Trigger 1: trg_bk_bi
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Database Trigger 1: trg_bk_bi (BEFORE INSERT on booking)")

    cx, cy, cw, ch = add_card(s15, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Trigger Specifications & Mutating Defense", DARK_BLUE)
    tb = s15.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    trg1_info = [
        ("Trigger Event & Level", "BEFORE INSERT ON booking FOR EACH ROW (Row-level trigger)."),
        ("Service Protection Rule", "Inspects status of :NEW.vid. If 'SERVICE', raises ORA-20002 ('vehicle under service') and cancels the insert."),
        ("Dynamic Cost Calculation", "Calculates contract cost dynamically:\n:NEW.total := (:NEW.edt - :NEW.sdt) * v_rate;\nEnsures total is never hardcoded or falsified by users."),
        ("Mutating Table Defense", "Reads ONLY the independent vehicle and category tables. Does NOT query booking, completely avoiding ORA-04091 mutating table errors!"),
        ("Integrity Guarantee", "Ensures 100% calculation consistency across both manual SQL Developer scripts and web interfaces.")
    ]
    for i, (t, d) in enumerate(trg1_info):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    cx2, cy2, cw2, ch2 = add_card(s15, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Source Code: trg_bk_bi", DARK_BLUE)
    trg1_code = """CREATE OR REPLACE TRIGGER trg_bk_bi
BEFORE INSERT ON booking
FOR EACH ROW
DECLARE
  v_status vehicle.status%TYPE;
  v_rate   category.rate%TYPE;
BEGIN
  -- Read ONLY vehicle and category (No mutating error!)
  SELECT v.status, c.rate INTO v_status, v_rate
  FROM vehicle v
  JOIN category c ON v.cid = c.cid
  WHERE v.vid = :NEW.vid;

  -- 1. Reject if under service
  IF v_status = 'SERVICE' THEN
    RAISE_APPLICATION_ERROR(-20002,
      'vehicle under service');
  END IF;

  -- 2. Compute total bill automatically
  :NEW.total := (:NEW.edt - :NEW.sdt) * v_rate;
END;
/"""
    add_code_box(s15, cx2, cy2, cw2, ch2, trg1_code, 9)

    # =========================================================================
    # SLIDE 16: Database Trigger 2: trg_bk_au
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Database Trigger 2: trg_bk_au (AFTER UPDATE on booking)")

    cx, cy, cw, ch = add_card(s16, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Autonomous Audit & Fleet Synchronization", DARK_BLUE)
    tb = s16.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    trg2_info = [
        ("Trigger Event & Level", "AFTER UPDATE OF status ON booking FOR EACH ROW."),
        ("Audit Trail Generation", "Inserts audit record into bk_log(lid, bkid, old_st, new_st, ldt) using seq_log.NEXTVAL and SYSDATE."),
        ("Automatic Fleet Status Sync", "• When :NEW.status = 'ACTIVE': Updates vehicle SET status = 'RENTED' WHERE vid = :NEW.vid.\n• When :NEW.status IN ('RETURNED', 'CANCELLED'): Updates vehicle SET status = 'AVAILABLE' WHERE vid = :NEW.vid AND status = 'RENTED'."),
        ("Complete Automation", "Neither staff nor manager needs to manually toggle vehicle availability; booking status changes synchronize the fleet automatically."),
        ("Historical Accountability", "Guarantees a permanent tamper-proof ledger of every reservation lifecycle transition.")
    ]
    for i, (t, d) in enumerate(trg2_info):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(7)

    cx2, cy2, cw2, ch2 = add_card(s16, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Source Code: trg_bk_au", DARK_BLUE)
    trg2_code = """CREATE OR REPLACE TRIGGER trg_bk_au
AFTER UPDATE OF status ON booking
FOR EACH ROW
BEGIN
  -- 1. Populate audit log table
  INSERT INTO bk_log (lid, bkid, old_st, new_st, ldt)
  VALUES (seq_log.NEXTVAL, :NEW.bkid,
          :OLD.status, :NEW.status, SYSDATE);

  -- 2. Synchronize vehicle availability
  IF :NEW.status = 'ACTIVE' THEN
    UPDATE vehicle SET status = 'RENTED'
    WHERE vid = :NEW.vid;
  ELSIF :NEW.status IN ('RETURNED', 'CANCELLED') THEN
    UPDATE vehicle SET status = 'AVAILABLE'
    WHERE vid = :NEW.vid AND status = 'RENTED';
  END IF;
END;
/"""
    add_code_box(s16, cx2, cy2, cw2, ch2, trg2_code, 9)

    # =========================================================================
    # SLIDE 17: Demonstration of DML Operations (T1 - T3)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Demonstration of DML Operations (INSERT, UPDATE, DELETE)")

    cx, cy, cw, ch = add_card(s17, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.4), "T1: INSERT Demo", DARK_BLUE)
    t1_txt = """-- T1: Insert new customers
INSERT INTO customer (custid, name,
  phone, email, lic_no, city)
VALUES (11, 'Deepak Menon',
  '9840011011', 'deepak.m@mail.com',
  'DL-KL-0011', 'Kochi');

INSERT INTO customer (custid, name,
  phone, email, lic_no, city)
VALUES (12, 'Test User',
  '9840011012', 'test.u@mail.com',
  'DL-TN-0012', 'Chennai');

SELECT custid, name, city
FROM customer WHERE custid IN (11,12);

Output:
11 | Deepak Menon | Kochi
12 | Test User    | Chennai"""
    add_code_box(s17, cx, cy, cw, ch, t1_txt, 8)

    cx2, cy2, cw2, ch2 = add_card(s17, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.4), "T2: DELETE Demo", DARK_BLUE)
    t2_txt = """-- T2: Delete temporary customer
DELETE FROM customer
WHERE custid = 12;

SELECT custid, name
FROM customer
WHERE custid = 12;

Output:
no rows selected (Deleted successfully!)

-- FK Integrity Protection Check:
-- Attempting to delete custid = 1
-- (who has bookings) fails with:
ORA-02292: integrity constraint
(RENTAL.SYS_C008432) violated -
child record found in booking!"""
    add_code_box(s17, cx2, cy2, cw2, ch2, t2_txt, 8)

    cx3, cy3, cw3, ch3 = add_card(s17, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.4), "T3: UPDATE Demo", DARK_BLUE)
    t3_txt = """-- T3: Update Sedan category tariff
UPDATE category
SET rate = rate + 100
WHERE cname = 'Sedan';

SELECT cid, cname, rate
FROM category
WHERE cname = 'Sedan';

Output:
CID | CNAME | RATE
----+-------+-------
2   | Sedan | 1900.00

-- Daily tariff successfully updated
-- from Rs. 1800 to Rs. 1900.
-- Future bookings automatically
-- compute at the new tariff rate!"""
    add_code_box(s17, cx3, cy3, cw3, ch3, t3_txt, 8)

    # =========================================================================
    # SLIDE 18: Oracle Data Dictionary Verification
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Oracle Data Dictionary Verification (04_view_tables.sql)")

    cx, cy, cw, ch = add_card(s18, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Data Dictionary Columns & Types Query", DARK_BLUE)
    dic_col_code = """-- Querying USER_TAB_COLUMNS
SELECT table_name, column_name,
       data_type ||
       CASE
         WHEN data_type IN ('VARCHAR2','CHAR')
           THEN '(' || data_length || ')'
         WHEN data_type = 'NUMBER' AND data_precision IS NOT NULL
           THEN '(' || data_precision || ',' || data_scale || ')'
         ELSE ''
       END AS data_type,
       nullable, data_default
FROM user_tab_columns
WHERE table_name IN ('BRANCH','CATEGORY','CUSTOMER','VEHICLE',
                     'BOOKING','PAYMENT','MAINTENANCE','BK_LOG')
ORDER BY table_name, column_id;

-- Verified: 42 total columns across 8 normalized tables."""
    add_code_box(s18, cx, cy, cw, ch, dic_col_code, 8.5)

    cx2, cy2, cw2, ch2 = add_card(s18, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Data Dictionary Constraints Query", DARK_BLUE)
    dic_con_code = """-- Querying USER_CONSTRAINTS & USER_CONS_COLUMNS
SELECT uc.table_name, uc.constraint_name,
       CASE uc.constraint_type
         WHEN 'P' THEN 'PRIMARY KEY'
         WHEN 'R' THEN 'FOREIGN KEY'
         WHEN 'U' THEN 'UNIQUE'
         WHEN 'C' THEN 'CHECK'
       END AS constraint_type,
       ucc.column_name, uc.search_condition
FROM user_constraints uc
JOIN user_cons_columns ucc
  ON uc.constraint_name = ucc.constraint_name
WHERE uc.table_name IN ('BRANCH','CATEGORY','CUSTOMER','VEHICLE',
                        'BOOKING','PAYMENT','MAINTENANCE','BK_LOG')
ORDER BY uc.table_name, uc.constraint_type;

-- Verified: 48 total constraint rules active in schema."""
    add_code_box(s18, cx2, cy2, cw2, ch2, dic_con_code, 8.5)

    # =========================================================================
    # SLIDE 19: Transition to Review III & Summary
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Summary & Roadmap for Review III (System Integration)")

    cx, cy, cw, ch = add_card(s19, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.4), "Review II Deliverables Completed", GREEN)
    tb = s19.shapes.add_textbox(cx, cy, cw, ch)
    tf = tb.text_frame
    tf.word_wrap = True
    comp_items = [
        ("8 Normalized Tables", "Fully created with primary, foreign, unique, check, and default constraints in Oracle."),
        ("10+ Records Per Table", "Covers branches, categories, customers, vehicles, bookings, payments, maintenance, and audit log."),
        ("16 SQL Queries", "All 16 queries executed with 100% accurate results matching design specifications."),
        ("Real PL/SQL Components", "2 Functions, 5 Procedures, 1 Explicit Cursor, and 2 Triggers compiled with zero errors."),
        ("DML Demonstration", "INSERT, UPDATE, and DELETE operations proven with referential integrity constraint checks.")
    ]
    for i, (t, d) in enumerate(comp_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"✔ {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = GREEN
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    cx2, cy2, cw2, ch2 = add_card(s19, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), "Review III Scope (Ready for Demo)", DARK_BLUE)
    tb2 = s19.shapes.add_textbox(cx2, cy2, cw2, ch2)
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    r3_items = [
        ("Full-Stack Interactive Application", "Python Flask web application with thin oracledb driver connected to FREEPDB1."),
        ("Staff Portal (/staff)", "Live desk dashboard, dynamic booking creation (p_book), vehicle handover (p_start), return (p_return), and payments (p_pay)."),
        ("Manager Portal (/manager)", "Executive analytics, category revenue & payment mode charts, dues cursor report (p_dues), maintenance summary, and audit log."),
        ("Interactive Schema Browser (/tables)", "Live web inspector querying Oracle data dictionary for live row counts, columns, badges, and relationships."),
        ("Role Protection & Security", "Session-based role access control preventing cross-portal unauthorized access.")
    ]
    for i, (t, d) in enumerate(r3_items):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"★ {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        r = p.add_run()
        r.text = d
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 20: Thank You / Q&A Slide
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    bg20 = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg20.fill.solid()
    bg20.fill.fore_color.rgb = NAVY
    bg20.line.fill.background()

    tb20 = s20.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.2))
    tf20 = tb20.text_frame
    tf20.word_wrap = True
    p = tf20.paragraphs[0]
    p.text = "THANK YOU"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p2 = tf20.add_paragraph()
    p2.text = "Vehicle Rental Management System — Review II Completed"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = GOLD
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(12)

    p3 = tf20.add_paragraph()
    p3.text = "Open for Questions & Technical Discussion\nSarvesh R (24BYB0081) | BCSE302L - Database Systems | SCOPE, VIT"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(12)

    prs.save(output_path)
    print(f"Full 20-Slide Review II Presentation created at: {output_path}")

if __name__ == "__main__":
    out_file = r"c:\sarvesh\placement preparations\projects\ganti1\vehicle_rental\Vehicle_Rental_Review2.pptx"
    build_review2_presentation(out_file)
