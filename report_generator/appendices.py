"""
Appendices generation for Vehicle Rental Project Report.
Includes Appendix A (SQL Scripts), Appendix B (Sample Data & Additional Screenshots),
and Appendix C (Sample Test Case Table).
"""

import os
from docx.shared import Inches
from report_generator.styles import (
    add_h1, add_h2, add_h3, add_p, add_code, add_table_data, add_figure
)

def build_appendices(doc, assets_dir, screenshots_dir):
    # ====================================================
    # APPENDIX A: SQL SCRIPTS
    # ====================================================
    add_h1(doc, "APPENDIX A: SQL SCRIPTS")
    add_p(
        doc,
        "The scripts below are representative excerpts from the official SQL files in the vehicle_rental/sql/ directory. "
        "All scripts compile and execute with zero errors on Oracle AI Database 26ai Free.",
        space_after=6
    )

    add_h2(doc, "A.1 01_schema_data.sql (Excerpts)")
    add_code(
        doc,
        "-- Sequence Generators\n"
        "CREATE SEQUENCE seq_bk START WITH 13 INCREMENT BY 1 NOCACHE;\n"
        "CREATE SEQUENCE seq_pay START WITH 11 INCREMENT BY 1 NOCACHE;\n"
        "CREATE SEQUENCE seq_log START WITH 1 INCREMENT BY 1 NOCACHE;\n\n"
        "-- Table: BRANCH\n"
        "CREATE TABLE branch (\n"
        "    bid    NUMBER PRIMARY KEY,\n"
        "    bname  VARCHAR2(50) NOT NULL,\n"
        "    city   VARCHAR2(50) NOT NULL,\n"
        "    phone  VARCHAR2(20) UNIQUE\n"
        ");\n\n"
        "-- Table: CATEGORY\n"
        "CREATE TABLE category (\n"
        "    cid    NUMBER PRIMARY KEY,\n"
        "    cname  VARCHAR2(30) NOT NULL UNIQUE,\n"
        "    rate   NUMBER(10,2) NOT NULL CHECK (rate > 0)\n"
        ");\n\n"
        "-- Table: VEHICLE\n"
        "CREATE TABLE vehicle (\n"
        "    vid    NUMBER PRIMARY KEY,\n"
        "    reg_no VARCHAR2(20) NOT NULL UNIQUE,\n"
        "    model  VARCHAR2(50) NOT NULL,\n"
        "    cid    NUMBER NOT NULL REFERENCES category(cid),\n"
        "    bid    NUMBER NOT NULL REFERENCES branch(bid),\n"
        "    yr     NUMBER(4) CHECK (yr >= 2015),\n"
        "    status VARCHAR2(15) DEFAULT 'AVAILABLE' CHECK (status IN ('AVAILABLE','RENTED','SERVICE'))\n"
        ");"
    )

    add_h2(doc, "A.2 02_plsql.sql (Stored Procedures & Functions)")
    add_code(
        doc,
        "-- Procedure: p_book\n"
        "CREATE OR REPLACE PROCEDURE p_book(p_c IN NUMBER, p_v IN NUMBER, p_s IN DATE, p_e IN DATE) IS\n"
        "    v_new_id NUMBER;\n"
        "BEGIN\n"
        "    IF f_avail(p_v, p_s, p_e) = 0 THEN\n"
        "        RAISE_APPLICATION_ERROR(-20001, 'Vehicle not available for requested dates or under service.');\n"
        "    END IF;\n"
        "    v_new_id := seq_bk.NEXTVAL;\n"
        "    INSERT INTO booking (bkid, custid, vid, sdt, edt, status) VALUES (v_new_id, p_c, p_v, p_s, p_e, 'BOOKED');\n"
        "    DBMS_OUTPUT.PUT_LINE('Booking created successfully! Booking ID: ' || v_new_id);\n"
        "END p_book;\n/\n\n"
        "-- Procedure: p_pay\n"
        "CREATE OR REPLACE PROCEDURE p_pay(p_b IN NUMBER, p_a IN NUMBER, p_m IN VARCHAR2) IS\n"
        "    v_bal NUMBER(10,2); v_pid NUMBER;\n"
        "BEGIN\n"
        "    v_bal := f_bal(p_b);\n"
        "    IF v_bal = -1 THEN RAISE_APPLICATION_ERROR(-20004, 'Booking ID does not exist.'); END IF;\n"
        "    IF p_a <= 0 THEN RAISE_APPLICATION_ERROR(-20004, 'Payment amount must be greater than zero.'); END IF;\n"
        "    IF p_a > v_bal THEN RAISE_APPLICATION_ERROR(-20004, 'Payment exceeds outstanding balance of Rs. ' || v_bal); END IF;\n"
        "    v_pid := seq_pay.NEXTVAL;\n"
        "    INSERT INTO payment (pid, bkid, amt, pdt, pmode) VALUES (v_pid, p_b, p_a, SYSDATE, p_m);\n"
        "    DBMS_OUTPUT.PUT_LINE('Payment recorded: Rs. ' || p_a || ' via ' || p_m || ' (Receipt ID: ' || v_pid || ')');\n"
        "END p_pay;\n/"
    )

    doc.add_page_break()

    # ====================================================
    # APPENDIX B: SAMPLE DATA AND SCREENSHOTS
    # ====================================================
    add_h1(doc, "APPENDIX B: SAMPLE DATA AND SCREENSHOTS")
    add_p(
        doc,
        "The following tables represent verified sample records populated across all 8 tables in the Oracle database:",
        space_after=4
    )

    # Table B.1 BRANCH
    b1_data = [
        ("1", "Chennai Central", "Chennai", "044-25381111"),
        ("2", "Coimbatore Gandhipuram", "Coimbatore", "0422-2521111"),
        ("3", "Madurai Meenakshi", "Madurai", "0452-2341111"),
        ("4", "Trichy Central", "Trichy", "0431-2411111"),
        ("5", "Salem Fairlands", "Salem", "0427-2331111"),
        ("6", "Bangalore Indiranagar", "Bangalore", "080-25201111"),
        ("7", "Hyderabad Hitec City", "Hyderabad", "040-23111111"),
        ("8", "Kochi MG Road", "Kochi", "0484-2361111"),
        ("9", "Pune FC Road", "Pune", "020-25531111"),
        ("10", "Tirunelveli Junction", "Tirunelveli", "0462-2331111")
    ]
    add_table_data(doc, "Table B.1: Sample data: BRANCH (10 rows)", ["BID", "Branch Name", "City", "Phone Number"], b1_data, [Inches(0.6), Inches(2.4), Inches(1.8), Inches(1.9)], font_size=8)

    # Table B.2 CATEGORY
    b2_data = [
        ("1", "Hatchback", "1200.00"),
        ("2", "Sedan", "1800.00"),
        ("3", "SUV", "2500.00"),
        ("4", "Luxury", "5000.00"),
        ("5", "Bike", "500.00"),
        ("6", "Scooter", "400.00"),
        ("7", "Van", "3000.00"),
        ("8", "MUV", "2800.00"),
        ("9", "Electric", "2200.00"),
        ("10", "Convertible", "6000.00")
    ]
    add_table_data(doc, "Table B.2: Sample data: CATEGORY (10 rows)", ["CID", "Category Name", "Daily Rental Rate (Rs.)"], b2_data, [Inches(1.0), Inches(3.0), Inches(2.7)], font_size=8)

    # Table B.3 CUSTOMER
    b3_data = [
        ("1", "Aarav Sharma", "9840112233", "aarav@email.com", "DL-TN-2020-0001", "Chennai"),
        ("2", "Diya Patel", "9840223344", "diya@email.com", "DL-TN-2020-0002", "Chennai"),
        ("3", "Rohan Iyer", "9840334455", "rohan@email.com", "DL-TN-2020-0003", "Coimbatore"),
        ("4", "Priya Nair", "9840445566", "priya@email.com", "DL-KA-2020-0004", "Bangalore"),
        ("5", "Vikram Singh", "9840556677", "vikram@email.com", "DL-TS-2020-0005", "Hyderabad")
    ]
    add_table_data(doc, "Table B.3: Sample data: CUSTOMER (Sample of 10 rows)", ["CustID", "Name", "Phone", "Email", "License No", "City"], b3_data, [Inches(0.7), Inches(1.4), Inches(1.2), Inches(1.4), Inches(1.2), Inches(0.8)], font_size=7.5)

    # Table B.4 VEHICLE
    b4_data = [
        ("1", "TN-01-AB-1234", "Maruti Swift", "1", "1", "2022", "AVAILABLE"),
        ("2", "TN-02-CD-2345", "Honda City", "2", "1", "2023", "AVAILABLE"),
        ("3", "TN-07-EF-3456", "Hyundai Creta", "3", "1", "2023", "RENTED"),
        ("4", "KA-01-GH-4567", "BMW 3 Series", "4", "6", "2024", "AVAILABLE"),
        ("10", "TN-01-ST-0123", "Mini Cooper S Conv", "10", "1", "2023", "SERVICE")
    ]
    add_table_data(doc, "Table B.4: Sample data: VEHICLE (Sample of 10 rows)", ["VID", "Reg Number", "Model Name", "CID", "BID", "Year", "Status"], b4_data, [Inches(0.5), Inches(1.3), Inches(1.8), Inches(0.5), Inches(0.5), Inches(0.6), Inches(1.5)], font_size=7.5)

    add_h2(doc, "B.2 Additional Application Screenshots")
    add_figure(
        doc, os.path.join(screenshots_dir, "tables_browser.png"),
        "Figure B.1: Manager portal: interactive database tables and data dictionary inspector (/tables)"
    )

    doc.add_page_break()

    # ====================================================
    # APPENDIX C: SAMPLE TEST CASE TABLE
    # ====================================================
    add_h1(doc, "APPENDIX C: SAMPLE TEST CASE TABLE")
    add_p(
        doc,
        "A representative subset of core test cases matching the required institutional evaluation matrix:",
        space_after=4
    )
    c1_data = [
        ("TC02", "Negative Testing: Duplicate Phone\nINSERT customer with phone='9840112233'", "Rejected by database; table unchanged", "Error: ORA-00001: unique constraint violated; rollback", "Pass"),
        ("TC04", "Integrity Testing: Quarantined Vehicle\np_book(1, 10, '2026-03-01', '2026-03-05')", "Rejected with ORA-20001; no booking created", "Error: ORA-20001: Vehicle not available or under service; rollback", "Pass"),
        ("TC05", "Workflow Testing: Trip Dispatch\np_start(13)", "Booking status=ACTIVE; Vehicle status=RENTED", "Success: Booking 13 ACTIVE; KA-01-GH-456 set to RENTED via trg_bk_au", "Pass"),
        ("TC07", "Validation Testing: Overpayment Guard\np_pay(13, 25000, 'UPI')", "Rejected with ORA-20004; payment exceeding dues blocked", "Error: ORA-20004: Payment exceeds balance of Rs. 20000.00; rollback", "Pass"),
        ("TC09", "Reporting Testing: Receivables Cursor\nEXEC p_dues", "Explicit cursor outputs delinquent accounts with dues > 0", "Cursor report printed: 2 delinquent accounts; Total Receivables: Rs. 8,600", "Pass")
    ]
    add_table_data(
        doc, "Table C.1: Sample test cases",
        ["Test ID", "Test / Input", "Expected Result", "Actual Result", "Status"],
        c1_data, [Inches(0.7), Inches(1.9), Inches(1.8), Inches(1.8), Inches(0.5)], font_size=7.5
    )
