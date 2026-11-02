"""
Chapters 5 to 8 generation for Vehicle Rental Project Report.
Covers Relational Design, Normalization, SQL Implementation (all 16 queries),
and Advanced Database Operations (PL/SQL, triggers, cursor, transactions).
"""

import os
from docx.shared import Inches
from report_generator.styles import (
    add_h1, add_h2, add_h3, add_p, add_bullet, add_numbered,
    add_code, add_table_data, add_figure
)

def build_chapters_5_to_8(doc, assets_dir):
    # ====================================================
    # CHAPTER 5: RELATIONAL DATABASE DESIGN
    # ====================================================
    add_h1(doc, "CHAPTER 5: RELATIONAL DATABASE DESIGN")
    
    add_h2(doc, "5.1 Relational Schema")
    add_p(
        doc,
        "The conceptual ER design is formally mapped into 8 relational schemas satisfying 3NF/BCNF. "
        "Primary keys are designated with PK; foreign keys are designated with FK; unique constraints are marked UQ.",
        space_after=4
    )
    add_bullet(doc, "BRANCH", "(bid PK, bname NOT NULL, city NOT NULL, phone UQ)")
    add_bullet(doc, "CATEGORY", "(cid PK, cname NOT NULL UQ, rate NOT NULL CHECK(rate > 0))")
    add_bullet(doc, "CUSTOMER", "(custid PK, name NOT NULL, phone NOT NULL UQ, email UQ, lic_no NOT NULL UQ, city DEFAULT 'Chennai')")
    add_bullet(doc, "VEHICLE", "(vid PK, reg_no NOT NULL UQ, model NOT NULL, cid NOT NULL FK->CATEGORY(cid), bid NOT NULL FK->BRANCH(bid), yr CHECK(yr >= 2015), status DEFAULT 'AVAILABLE' CHECK(status IN ('AVAILABLE','RENTED','SERVICE')))")
    add_bullet(doc, "BOOKING", "(bkid PK, custid NOT NULL FK->CUSTOMER(custid), vid NOT NULL FK->VEHICLE(vid), sdt NOT NULL, edt NOT NULL, status DEFAULT 'BOOKED' CHECK(status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED')), total DEFAULT 0, CHECK(edt > sdt))")
    add_bullet(doc, "PAYMENT", "(pid PK, bkid NOT NULL FK->BOOKING(bkid), amt NOT NULL CHECK(amt > 0), pdt DEFAULT SYSDATE, pmode CHECK(pmode IN ('CASH','UPI','CARD')))")
    add_bullet(doc, "MAINTENANCE", "(mid PK, vid NOT NULL FK->VEHICLE(vid), mdt NOT NULL, cost CHECK(cost >= 0), descr)")
    add_bullet(doc, "BK_LOG", "(lid PK, bkid, old_st, new_st, ldt DEFAULT SYSDATE)")

    add_h2(doc, "5.2 Table Definitions")
    add_p(
        doc,
        "The relational tables are created natively in Oracle AI Database 26ai Free using strong Oracle data types (NUMBER, VARCHAR2, DATE, TIMESTAMP). "
        "The central BOOKING table definition illustrates constraint composition:",
        space_after=4
    )
    add_code(
        doc,
        "CREATE TABLE booking (\n"
        "    bkid   NUMBER PRIMARY KEY,\n"
        "    custid NUMBER NOT NULL REFERENCES customer(custid),\n"
        "    vid    NUMBER NOT NULL REFERENCES vehicle(vid),\n"
        "    sdt    DATE NOT NULL,\n"
        "    edt    DATE NOT NULL,\n"
        "    status VARCHAR2(15) DEFAULT 'BOOKED' CHECK (status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED')),\n"
        "    total  NUMBER(10,2) DEFAULT 0,\n"
        "    CHECK (edt > sdt)\n"
        ");"
    )

    add_h2(doc, "5.3 Keys")
    keys_data = [
        ("BRANCH", "bid", "phone (UNIQUE)", "-"),
        ("CATEGORY", "cid", "cname (UNIQUE)", "-"),
        ("CUSTOMER", "custid", "phone (UQ), email (UQ), lic_no (UQ)", "-"),
        ("VEHICLE", "vid", "reg_no (UNIQUE)", "cid -> CATEGORY(cid), bid -> BRANCH(bid)"),
        ("BOOKING", "bkid", "-", "custid -> CUSTOMER(custid), vid -> VEHICLE(vid)"),
        ("PAYMENT", "pid", "-", "bkid -> BOOKING(bkid)"),
        ("MAINTENANCE", "mid", "-", "vid -> VEHICLE(vid)"),
        ("BK_LOG", "lid", "-", "bkid (logical audit reference)")
    ]
    add_table_data(
        doc, "Table 5.1: Keys of each relation",
        ["Relation", "Primary Key", "Other Candidate / Alternate Keys", "Foreign Keys"],
        keys_data, [Inches(1.2), Inches(0.9), Inches(2.4), Inches(2.0)], font_size=8.5
    )

    add_h2(doc, "5.4 Integrity Constraints")
    con_data = [
        ("Domain Constraints", "status IN ('AVAILABLE','RENTED','SERVICE'); booking status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED'); pmode IN ('CASH','UPI','CARD')"),
        ("Entity Integrity", "Every table defines an explicit primary key (NOT NULL and unique)."),
        ("Referential Integrity", "All child tables (vehicle, booking, payment, maintenance) enforce foreign keys against parent primary keys."),
        ("Unique Constraints", "branch.phone, category.cname, customer.phone, customer.email, customer.lic_no, vehicle.reg_no"),
        ("Check Constraints", "category.rate > 0; vehicle.yr >= 2015; booking.edt > sdt; payment.amt > 0; maintenance.cost >= 0"),
        ("Default Constraints", "customer.city DEFAULT 'Chennai'; vehicle.status DEFAULT 'AVAILABLE'; booking.status DEFAULT 'BOOKED'; booking.total DEFAULT 0; payment.pdt DEFAULT SYSDATE; bk_log.ldt DEFAULT SYSDATE")
    ]
    add_table_data(
        doc, "Table 5.2: Integrity constraints used",
        ["Constraint Type", "Examples from VRMS Schema"],
        con_data, [Inches(1.8), Inches(4.7)], font_size=8.5
    )

    add_h2(doc, "5.5 Schema Diagram")
    add_figure(
        doc, os.path.join(assets_dir, "fig_5_1_schema_diagram.png"),
        "Figure 5.1: Relational schema diagram with primary and foreign key links"
    )

    add_h2(doc, "5.6 Data Dictionary")
    
    # 5.3 BRANCH
    dd_branch = [
        ("bid", "NUMBER", "PK", "Unique branch numeric identifier (1 to 10)"),
        ("bname", "VARCHAR2(50)", "NOT NULL", "Official name of the rental branch office"),
        ("city", "VARCHAR2(50)", "NOT NULL", "City location of the branch"),
        ("phone", "VARCHAR2(20)", "UNIQUE", "Dedicated branch contact phone number")
    ]
    add_table_data(doc, "Table 5.3: Data dictionary: BRANCH", ["Column", "Data Type", "Constraints", "Description"], dd_branch, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.4 CATEGORY
    dd_cat = [
        ("cid", "NUMBER", "PK", "Category identifier (1 to 10)"),
        ("cname", "VARCHAR2(30)", "NOT NULL, UNIQUE", "Category classification (Hatchback, Sedan, SUV, Luxury)"),
        ("rate", "NUMBER(10,2)", "NOT NULL, CHECK > 0", "Daily rental tariff in INR (Rs. 400 to Rs. 6,000)")
    ]
    add_table_data(doc, "Table 5.4: Data dictionary: CATEGORY", ["Column", "Data Type", "Constraints", "Description"], dd_cat, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.5 CUSTOMER
    dd_cust = [
        ("custid", "NUMBER", "PK", "Unique customer identifier (1 to 10)"),
        ("name", "VARCHAR2(50)", "NOT NULL", "Full legal name of the customer"),
        ("phone", "VARCHAR2(20)", "NOT NULL, UNIQUE", "Mobile contact number"),
        ("email", "VARCHAR2(50)", "UNIQUE", "Email address for booking confirmations"),
        ("lic_no", "VARCHAR2(30)", "NOT NULL, UNIQUE", "Verified driving license number"),
        ("city", "VARCHAR2(50)", "DEFAULT 'Chennai'", "Customer residential city")
    ]
    add_table_data(doc, "Table 5.5: Data dictionary: CUSTOMER", ["Column", "Data Type", "Constraints", "Description"], dd_cust, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.6 VEHICLE
    dd_veh = [
        ("vid", "NUMBER", "PK", "Unique vehicle inventory identifier (1 to 10)"),
        ("reg_no", "VARCHAR2(20)", "NOT NULL, UNIQUE", "Official vehicle registration license plate"),
        ("model", "VARCHAR2(50)", "NOT NULL", "Vehicle make and model name (e.g. Maruti Swift, BMW 3 Series)"),
        ("cid", "NUMBER", "NOT NULL, FK->category", "Foreign key linking vehicle to its tariff category"),
        ("bid", "NUMBER", "NOT NULL, FK->branch", "Foreign key linking vehicle to its home branch"),
        ("yr", "NUMBER(4)", "CHECK yr >= 2015", "Manufacturing year"),
        ("status", "VARCHAR2(15)", "DEFAULT 'AVAILABLE', CHECK", "Operational state (AVAILABLE, RENTED, SERVICE)")
    ]
    add_table_data(doc, "Table 5.6: Data dictionary: VEHICLE", ["Column", "Data Type", "Constraints", "Description"], dd_veh, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.7 BOOKING
    dd_bk = [
        ("bkid", "NUMBER", "PK", "Unique booking reservation identifier (1 to 12)"),
        ("custid", "NUMBER", "NOT NULL, FK->customer", "Foreign key referencing reserving customer"),
        ("vid", "NUMBER", "NOT NULL, FK->vehicle", "Foreign key referencing assigned vehicle"),
        ("sdt", "DATE", "NOT NULL", "Start date and time of the rental trip"),
        ("edt", "DATE", "NOT NULL", "Scheduled end date and time of the rental trip"),
        ("status", "VARCHAR2(15)", "DEFAULT 'BOOKED', CHECK", "Booking lifecycle (BOOKED, ACTIVE, RETURNED, CANCELLED)"),
        ("total", "NUMBER(10,2)", "DEFAULT 0", "Computed trip rental tariff: (edt - sdt) * category.rate")
    ]
    add_table_data(doc, "Table 5.7: Data dictionary: BOOKING", ["Column", "Data Type", "Constraints", "Description"], dd_bk, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.8 PAYMENT
    dd_pay = [
        ("pid", "NUMBER", "PK", "Unique payment receipt identifier (1 to 10)"),
        ("bkid", "NUMBER", "NOT NULL, FK->booking", "Foreign key referencing booking being settled"),
        ("amt", "NUMBER(10,2)", "NOT NULL, CHECK > 0", "Monetary payment amount in INR"),
        ("pdt", "DATE", "DEFAULT SYSDATE", "Timestamp when payment was collected"),
        ("pmode", "VARCHAR2(10)", "CHECK IN ('CASH','UPI','CARD')", "Payment channel used")
    ]
    add_table_data(doc, "Table 5.8: Data dictionary: PAYMENT", ["Column", "Data Type", "Constraints", "Description"], dd_pay, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.9 MAINTENANCE
    dd_maint = [
        ("mid", "NUMBER", "PK", "Unique maintenance record identifier (1 to 10)"),
        ("vid", "NUMBER", "NOT NULL, FK->vehicle", "Foreign key referencing vehicle serviced"),
        ("mdt", "DATE", "NOT NULL", "Date of workshop inspection or service"),
        ("cost", "NUMBER(10,2)", "CHECK cost >= 0", "Total maintenance expense incurred"),
        ("descr", "VARCHAR2(200)", "-", "Work order description (brake overhaul, periodic service)")
    ]
    add_table_data(doc, "Table 5.9: Data dictionary: MAINTENANCE", ["Column", "Data Type", "Constraints", "Description"], dd_maint, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    # 5.10 BK_LOG
    dd_log = [
        ("lid", "NUMBER", "PK", "Unique audit log identifier generated by seq_log"),
        ("bkid", "NUMBER", "-", "Booking identifier that underwent status transition"),
        ("old_st", "VARCHAR2(15)", "-", "Previous lifecycle status prior to mutation"),
        ("new_st", "VARCHAR2(15)", "-", "Updated lifecycle status after mutation"),
        ("ldt", "DATE", "DEFAULT SYSDATE", "Exact database timestamp of the status change")
    ]
    add_table_data(doc, "Table 5.10: Data dictionary: BK_LOG", ["Column", "Data Type", "Constraints", "Description"], dd_log, [Inches(1.1), Inches(1.3), Inches(1.3), Inches(2.8)], font_size=8)

    doc.add_page_break()

    # ====================================================
    # CHAPTER 6: FUNCTIONAL DEPENDENCIES & NORMALIZATION
    # ====================================================
    add_h1(doc, "CHAPTER 6: FUNCTIONAL DEPENDENCIES AND NORMALIZATION")
    
    add_h2(doc, "6.1 Functional Dependencies")
    add_p(
        doc,
        "To rigorously prove that the schema is free of anomalies, consider a universal un-normalized relation R comprising 26 attributes: "
        "R(bkid, custid, vid, sdt, edt, booking_status, total, cust_name, phone, email, lic_no, cust_city, "
        "reg_no, model, cid, cname, rate, yr, veh_status, bid, bname, branch_city, branch_phone, pid, amt, pmode).",
        space_after=4
    )
    add_bullet(doc, "F1: ", "bkid -> custid, vid, sdt, edt, booking_status, total")
    add_bullet(doc, "F2: ", "custid -> cust_name, phone, email, lic_no, cust_city")
    add_bullet(doc, "F3: ", "phone -> custid; email -> custid; lic_no -> custid (all candidate keys)")
    add_bullet(doc, "F4: ", "vid -> reg_no, model, cid, bid, yr, veh_status")
    add_bullet(doc, "F5: ", "reg_no -> vid (candidate key)")
    add_bullet(doc, "F6: ", "cid -> cname, rate; cname -> cid")
    add_bullet(doc, "F7: ", "bid -> bname, branch_city, branch_phone; branch_phone -> bid")
    add_bullet(doc, "F8: ", "pid -> bkid, amt, pmode")

    add_h2(doc, "6.2 Attribute Closure and Candidate Keys")
    add_p(
        doc,
        "Computing the attribute closure of {bkid, pid} under F1-F8 resolves all 26 attributes of R. "
        "For the booking entity alone, {bkid}+ determines all booking, customer, vehicle, category, and branch attributes. "
        "Thus, bkid is the minimal candidate key for booking facts.",
        space_after=8
    )

    add_h2(doc, "6.3 First Normal Form (1NF)")
    add_p(
        doc,
        "A relation is in 1NF if all attribute values are atomic and there are no repeating groups. "
        "In a flat spreadsheet, booking multiple vehicles or recording multiple payment installments within a single cell "
        "(e.g., '10000, 5000') violates 1NF. In VRMS, all attributes hold single scalar values; multiple payments are represented "
        "as distinct rows in PAYMENT. Hence, the schema is strictly in 1NF.",
        space_after=8
    )

    add_h2(doc, "6.4 Second Normal Form (2NF)")
    add_p(
        doc,
        "A relation is in 2NF if it is in 1NF and no non-prime attribute is partially dependent on any candidate key. "
        "If a composite key {bkid, pid} were used for a combined booking-payment relation, customer attributes would depend only on bkid, "
        "violating 2NF. Decomposing R into distinct entities (BOOKING, CUSTOMER, VEHICLE, PAYMENT) ensures every non-prime attribute "
        "depends on the entire primary key.",
        space_after=8
    )

    add_h2(doc, "6.5 Third Normal Form (3NF)")
    add_p(
        doc,
        "A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key. "
        "In an intermediate table VEHICLE(vid, model, cid, cname, rate), the transitive dependency vid -> cid -> (cname, rate) exists. "
        "Decomposing this into VEHICLE(vid, cid, ...) and CATEGORY(cid, cname, rate) removes all transitive dependencies.",
        space_after=8
    )

    add_h2(doc, "6.6 Boyce-Codd Normal Form (BCNF)")
    bcnf_data = [
        ("BRANCH", "bid; phone", "Yes (PK and UNIQUE candidate key)", "BCNF"),
        ("CATEGORY", "cid; cname", "Yes (PK and UNIQUE candidate key)", "BCNF"),
        ("CUSTOMER", "custid; phone; email; lic_no", "Yes (PK and 3 UNIQUE candidate keys)", "BCNF"),
        ("VEHICLE", "vid; reg_no", "Yes (PK and UNIQUE candidate key)", "BCNF"),
        ("BOOKING", "bkid; and (sdt, edt, vid) -> total", "First yes; second no (computed via category)", "Controlled denormalization (justified below)"),
        ("PAYMENT", "pid", "Yes (PK)", "BCNF"),
        ("MAINTENANCE", "mid", "Yes (PK)", "BCNF"),
        ("BK_LOG", "lid", "Yes (PK)", "BCNF")
    ]
    add_table_data(
        doc, "Table 6.1: BCNF check: every non-trivial determinant must be a superkey",
        ["Relation", "Determinants", "Is Determinant a Superkey?", "Normal Form Result"],
        bcnf_data, [Inches(1.2), Inches(2.2), Inches(2.2), Inches(0.9)], font_size=8.5
    )
    add_p(
        doc,
        "Justification of Controlled Denormalization: In BOOKING, the total attribute is derived from (edt - sdt) * category.rate. "
        "Storing total avoids expensive re-computation across thousands of analytical queries and preserves historical financial accuracy "
        "if category tariffs are revised in the future. The risk of inconsistency is 100% prevented by trigger trg_bk_bi, which computes "
        "total autonomously at insertion time.",
        space_after=8
    )

    add_h2(doc, "6.7 Lossless Join and Dependency Preservation")
    add_p(
        doc,
        "The relational decomposition of R into the 8 VRMS tables is guaranteed to be Lossless because each decomposition step "
        "shares a foreign key that is a candidate key of the parent relation (e.g., BOOKING.vid references VEHICLE.vid). "
        "Furthermore, all functional dependencies F1 to F8 are fully preserved within individual normalized tables.",
        space_after=8
    )

    add_h2(doc, "6.8 Before-and-After Example")
    flat_data = [
        ("1", "Aarav", "9840112233", "Swift", "Hatchback", "1200", "Chennai Central", "01-Jan", "04-Jan", "3600"),
        ("7", "Karthik", "9840778899", "Swift", "Hatchback", "1200", "Chennai Central", "20-Jan", "23-Jan", "3600"),
        ("12", "Diya", "9840223344", "Swift", "Hatchback", "1200", "Chennai Central", "10-Feb", "13-Feb", "3600")
    ]
    add_table_data(
        doc, "Table 6.2: Before: flat relation (redundant vehicle, tariff, and branch attributes)",
        ["BKID", "Cust", "Phone", "Model", "Cat", "Rate", "Branch", "Start", "End", "Total"],
        flat_data, [Inches(0.5), Inches(0.6), Inches(0.8), Inches(0.6), Inches(0.7), Inches(0.5), Inches(1.1), Inches(0.6), Inches(0.6), Inches(0.5)], font_size=7.5
    )
    add_p(
        doc,
        "In Table 6.2, updating the Hatchback tariff from 1200 to 1300 requires updating hundreds of rows. In the normalized schema (Table 6.3), "
        "the rate exists once in CATEGORY, vehicle 1 points to cid 1 and bid 1, and bookings reference vid 1 without repeating vehicle attributes.",
        space_after=12
    )

    doc.add_page_break()

    # ====================================================
    # CHAPTER 7: SQL IMPLEMENTATION
    # ====================================================
    add_h1(doc, "CHAPTER 7: SQL IMPLEMENTATION")
    
    add_h2(doc, "7.1 Database and Table Creation (DDL)")
    add_p(
        doc,
        "The complete schema DDL is executed in 01_schema_data.sql. Existing tables and sequences are dropped in reverse dependency "
        "order to prevent foreign key constraint violations:",
        space_after=4
    )
    add_code(
        doc,
        "DROP TABLE bk_log CASCADE CONSTRAINTS;\n"
        "DROP TABLE maintenance CASCADE CONSTRAINTS;\n"
        "DROP TABLE payment CASCADE CONSTRAINTS;\n"
        "DROP TABLE booking CASCADE CONSTRAINTS;\n"
        "DROP TABLE vehicle CASCADE CONSTRAINTS;\n"
        "DROP TABLE customer CASCADE CONSTRAINTS;\n"
        "DROP TABLE category CASCADE CONSTRAINTS;\n"
        "DROP TABLE branch CASCADE CONSTRAINTS;"
    )

    add_h2(doc, "7.2 Data Manipulation (DML)")
    add_p(
        doc,
        "All 8 tables were populated with at least 10 meaningful records using SQL INSERT statements. "
        "Operational status consistency was maintained (Vehicle 10 set to SERVICE; Booking 11 set to ACTIVE with Vehicle 3 set to RENTED).",
        space_after=8
    )

    add_h2(doc, "7.3 Data Retrieval (DQL)")
    add_p(
        doc,
        "Sixteen comprehensive SQL queries were designed and executed on the live Oracle database. "
        "All queries satisfy complex relational operations including multi-table joins, aggregations, HAVING clauses, subqueries, and views.",
        space_after=8
    )

    add_h2(doc, "7.4 Built-In and Aggregate Functions")
    fn_data = [
        ("Aggregate Functions", "COUNT, SUM, AVG, MIN, MAX", "Queries 2, 3, 5, 6, 9, 10, 11, 14"),
        ("Numeric Functions", "ROUND, NVL", "Queries 2, 10, 11, 14; PL/SQL procedures"),
        ("String Functions", "UPPER, LENGTH, SUBSTR, INSTR, RPAD", "Query 7; p_dues cursor report formatting"),
        ("Date Functions", "TO_CHAR, TO_DATE, SYSDATE, Date arithmetic (edt - sdt)", "Queries 1, 5, 8; trigger trg_bk_bi duration calculation")
    ]
    add_table_data(
        doc, "Table 7.1: Functions used in the project SQL",
        ["Category", "Functions Employed", "Demonstration Queries / Scripts"],
        fn_data, [Inches(1.8), Inches(2.2), Inches(2.5)], font_size=8.5
    )

    add_h2(doc, "7.5 GROUP BY and HAVING")
    add_p(
        doc,
        "Query 2 groups bookings by category to compute total trips and revenue. Query 3 groups bookings by customer and applies a HAVING "
        "filter (HAVING COUNT(b.bkid) > 1) to identify repeat customers. Query 6 groups vehicles by branch. Query 10 groups payments by mode.",
        space_after=8
    )

    add_h2(doc, "7.6 Joins")
    join_data = [
        ("3-Table Inner Join", "Query 1", "booking, customer, vehicle", "Retrieves complete booking details with customer names and vehicle models"),
        ("Aggregate Join", "Query 11", "vehicle, maintenance", "Aggregates total service records and maintenance costs per vehicle"),
        ("Left Outer Join", "Query 2", "category, vehicle, booking", "Includes categories with zero bookings (Van, Convertible) with NVL zero totals"),
        ("Left Outer Join", "Query 6", "branch, vehicle", "Lists all branches including those with zero vehicles (Pune, Tirunelveli)"),
        ("Left Outer Join (IS NULL)", "Query 12", "booking, customer, payment", "Filters for bookings with zero payments (Meera Joshi, Diya Patel)")
    ]
    add_table_data(
        doc, "Table 7.2: Join types demonstrated",
        ["Join Type", "Query", "Tables Joined", "Operational Purpose"],
        join_data, [Inches(1.5), Inches(0.8), Inches(1.8), Inches(2.4)], font_size=8.5
    )

    add_h2(doc, "7.7 Subqueries")
    add_p(
        doc,
        "Query 5 demonstrates a scalar subquery (WHERE amt > (SELECT AVG(amt) FROM payment)). Query 4 demonstrates a NOT IN subquery "
        "(WHERE vid NOT IN (SELECT DISTINCT vid FROM booking)). Query 9 demonstrates a subquery with MAX(rate). "
        "Query 15 demonstrates a correlated subquery with EXISTS (WHERE EXISTS (SELECT 1 FROM booking b WHERE b.custid = c.custid AND b.status = 'CANCELLED')).",
        space_after=8
    )

    add_h2(doc, "7.8 Set Operations")
    add_p(
        doc,
        "Query 16 demonstrates the UNION set operation between branch cities and customer cities, producing a consolidated geographic footprint "
        "while eliminating duplicates.",
        space_after=8
    )

    add_h2(doc, "7.9 Views")
    add_code(
        doc,
        "CREATE OR REPLACE VIEW v_open_bookings AS\n"
        "SELECT b.bkid, c.name AS customer_name, c.phone, v.model, v.reg_no, b.sdt, b.edt, b.status, b.total\n"
        "FROM booking b\n"
        "JOIN customer c ON b.custid = c.custid\n"
        "JOIN vehicle v ON b.vid = v.vid\n"
        "WHERE b.status IN ('BOOKED', 'ACTIVE');\n\n"
        "SELECT bkid, customer_name, model, status, total FROM v_open_bookings;"
    )
    v_data = [
        ("11", "Aarav Sharma", "Hyundai Creta", "ACTIVE", "10000"),
        ("12", "Diya Patel", "Maruti Swift", "BOOKED", "3600")
    ]
    add_table_data(
        doc, "Table 7.3: Output of the view query (v_open_bookings)",
        ["BKID", "Customer Name", "Model", "Status", "Total (Rs.)"],
        v_data, [Inches(0.8), Inches(1.8), Inches(1.8), Inches(1.0), Inches(1.1)], font_size=8.5
    )

    add_h2(doc, "7.10 Constraints")
    con_tests = [
        ("CHECK rate > 0", "INSERT INTO category VALUES (11, 'Invalid', -500)", "ORA-02290: check constraint (RENTAL.SYS_C...) violated"),
        ("CHECK edt > sdt", "INSERT INTO booking VALUES (99, 1, 1, DATE '2026-03-10', DATE '2026-03-05', ...)", "ORA-02290: check constraint (RENTAL.SYS_C...) violated"),
        ("UNIQUE phone", "INSERT INTO customer VALUES (15, 'Dup', '9840112233', ...)", "ORA-00001: unique constraint (RENTAL.SYS_C...) violated"),
        ("FOREIGN KEY", "INSERT INTO vehicle VALUES (99, 'TN-99-ZZ-999', 'Car', 99, 1, ...)", "ORA-02291: integrity constraint (RENTAL.SYS_C...) violated - parent key not found"),
        ("Trigger Quarantine", "p_book(1, 10, DATE '2026-03-01', DATE '2026-03-05')", "ORA-20001: Vehicle not available for requested dates or under service.")
    ]
    add_table_data(
        doc, "Table 7.4: Constraint demonstration (actual Oracle error responses)",
        ["Constraint Type", "Test Statement", "Actual Oracle Database Response"],
        con_tests, [Inches(1.5), Inches(2.2), Inches(2.8)], font_size=8
    )

    add_h2(doc, "7.11 Data Control Language")
    add_p(
        doc,
        "In production enterprise deployments, Oracle Data Control Language (DCL) implements role-based privilege separation:",
        space_after=4
    )
    add_code(
        doc,
        "CREATE ROLE rental_staff;\n"
        "CREATE ROLE rental_manager;\n"
        "GRANT SELECT, INSERT ON customer TO rental_staff;\n"
        "GRANT EXECUTE ON p_book TO rental_staff;\n"
        "GRANT EXECUTE ON p_start TO rental_staff;\n"
        "GRANT EXECUTE ON p_return TO rental_staff;\n"
        "GRANT EXECUTE ON p_pay TO rental_staff;\n"
        "GRANT SELECT ON v_open_bookings TO rental_staff;\n"
        "GRANT EXECUTE ON p_dues TO rental_manager;\n"
        "GRANT SELECT ON bk_log TO rental_manager;"
    )

    add_h2(doc, "7.12 SQL Output Evidence (16 Queries)")
    
    # Query 1
    add_h3(doc, "Query 1: Booking Details with Customer and Vehicle (3-Table Inner Join)")
    add_code(
        doc,
        "SELECT b.bkid, c.name, v.model, v.reg_no,\n"
        "       TO_CHAR(b.sdt, 'DD-Mon-YYYY') AS start_date,\n"
        "       TO_CHAR(b.edt, 'DD-Mon-YYYY') AS end_date,\n"
        "       b.status, b.total\n"
        "FROM booking b\n"
        "JOIN customer c ON b.custid = c.custid\n"
        "JOIN vehicle v ON b.vid = v.vid\n"
        "ORDER BY b.bkid;"
    )
    q1_data = [
        ("1", "Aarav Sharma", "Maruti Swift", "TN-01-AB-123", "01-Jan-2026", "04-Jan-2026", "RETURNED", "3600"),
        ("2", "Diya Patel", "Honda City", "TN-02-CD-234", "05-Jan-2026", "08-Jan-2026", "RETURNED", "5400"),
        ("3", "Rohan Iyer", "Hyundai Creta", "TN-07-EF-345", "10-Jan-2026", "12-Jan-2026", "RETURNED", "5000"),
        ("4", "Priya Nair", "BMW 3 Series", "KA-01-GH-456", "12-Jan-2026", "14-Jan-2026", "RETURNED", "10000"),
        ("11", "Aarav Sharma", "Hyundai Creta", "TN-07-EF-345", "01-Feb-2026", "05-Feb-2026", "ACTIVE", "10000"),
        ("12", "Diya Patel", "Maruti Swift", "TN-01-AB-123", "10-Feb-2026", "13-Feb-2026", "BOOKED", "3600")
    ]
    add_table_data(doc, "Table 7.5: Output of Query 1 (Sample of 12 rows)", ["BKID", "Name", "Model", "Reg No", "Start Date", "End Date", "Status", "Total (Rs.)"], q1_data, [Inches(0.5), Inches(1.1), Inches(1.1), Inches(1.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.6)], font_size=7.5)
    add_p(doc, "Interpretation: Evaluates a 3-table join between booking, customer, and vehicle. Formats dates using TO_CHAR. Booking totals match category rates multiplied by duration.", italic=True)

    # Query 2
    add_h3(doc, "Query 2: Revenue and Rental Trips per Category (Aggregation & Group By)")
    add_code(
        doc,
        "SELECT cat.cname, COUNT(b.bkid) AS total_trips,\n"
        "       NVL(SUM(b.total), 0) AS total_revenue,\n"
        "       NVL(ROUND(AVG(b.total), 2), 0) AS avg_booking_value\n"
        "FROM category cat\n"
        "LEFT JOIN vehicle v ON cat.cid = v.cid\n"
        "LEFT JOIN booking b ON v.vid = b.vid AND b.status != 'CANCELLED'\n"
        "GROUP BY cat.cname ORDER BY total_revenue DESC;"
    )
    q2_data = [
        ("SUV", "2", "15000", "7500.00"),
        ("Hatchback", "3", "10800", "3600.00"),
        ("Luxury", "1", "10000", "10000.00"),
        ("MUV", "1", "8400", "8400.00"),
        ("Sedan", "1", "5400", "5400.00"),
        ("Electric", "1", "4400", "4400.00"),
        ("Bike", "1", "1500", "1500.00"),
        ("Van", "0", "0", "0.00"),
        ("Convertible", "0", "0", "0.00")
    ]
    add_table_data(doc, "Table 7.6: Output of Query 2", ["Category", "Total Trips", "Total Revenue (Rs.)", "Avg Booking Value (Rs.)"], q2_data, [Inches(1.5), Inches(1.2), Inches(1.8), Inches(2.0)], font_size=8)
    add_p(doc, "Interpretation: Left join retains categories with 0 bookings (Van, Convertible). NVL converts null sums to 0. SUV leads in revenue (Rs. 15,000).", italic=True)

    # Query 3
    add_h3(doc, "Query 3: Customers with More than One Booking (HAVING Clause)")
    add_code(
        doc,
        "SELECT c.custid, c.name, c.phone, COUNT(b.bkid) AS booking_count\n"
        "FROM customer c\n"
        "JOIN booking b ON c.custid = b.custid\n"
        "GROUP BY c.custid, c.name, c.phone\n"
        "HAVING COUNT(b.bkid) > 1\n"
        "ORDER BY booking_count DESC;"
    )
    q3_data = [
        ("1", "Aarav Sharma", "9840112233", "2"),
        ("2", "Diya Patel", "9840223344", "2")
    ]
    add_table_data(doc, "Table 7.7: Output of Query 3", ["Cust ID", "Customer Name", "Phone Number", "Total Bookings"], q3_data, [Inches(1.0), Inches(2.0), Inches(2.0), Inches(1.5)], font_size=8.5)
    add_p(doc, "Interpretation: Identifies repeat patrons by applying a HAVING aggregate filter greater than 1. Aarav Sharma and Diya Patel each hold 2 bookings.", italic=True)

    # Query 4
    add_h3(doc, "Query 4: Vehicles that Have Never Been Booked (NOT IN Subquery)")
    add_code(
        doc,
        "SELECT vid, reg_no, model, status\n"
        "FROM vehicle\n"
        "WHERE vid NOT IN (SELECT DISTINCT vid FROM booking)\n"
        "ORDER BY vid;"
    )
    q4_data = [
        ("7", "TN-03-MN-789", "Force Urbania", "AVAILABLE"),
        ("10", "TN-01-ST-012", "Mini Cooper S Conv", "SERVICE")
    ]
    add_table_data(doc, "Table 7.8: Output of Query 4", ["VID", "Reg Number", "Model", "Status"], q4_data, [Inches(0.8), Inches(1.8), Inches(2.4), Inches(1.5)], font_size=8.5)
    add_p(doc, "Interpretation: Demonstrates uncorrelated NOT IN subquery. Force Urbania and Mini Cooper have never been rented out.", italic=True)

    # Query 5
    add_h3(doc, "Query 5: Payments Exceeding the Overall Average Payment (Scalar Subquery)")
    add_code(
        doc,
        "SELECT p.pid, p.bkid, p.amt, p.pmode, TO_CHAR(p.pdt, 'DD-Mon-YYYY') AS pdt\n"
        "FROM payment p\n"
        "WHERE p.amt > (SELECT AVG(amt) FROM payment)\n"
        "ORDER BY p.amt DESC;"
    )
    q5_data = [
        ("4", "4", "10000.00", "CARD", "14-Jan-2026"),
        ("8", "8", "8400.00", "UPI", "25-Jan-2026"),
        ("2", "2", "5400.00", "CARD", "08-Jan-2026"),
        ("3", "3", "5000.00", "CASH", "12-Jan-2026"),
        ("9", "9", "4400.00", "CASH", "27-Jan-2026")
    ]
    add_table_data(doc, "Table 7.9: Output of Query 5", ["PID", "BKID", "Amount (Rs.)", "Payment Mode", "Payment Date"], q5_data, [Inches(0.8), Inches(0.8), Inches(1.5), Inches(1.5), Inches(1.9)], font_size=8.5)
    add_p(doc, "Interpretation: The system average payment is Rs. 4,310.00. Exactly 5 payments exceed this threshold, led by payment 4 (Rs. 10,000).", italic=True)

    # Query 6
    add_h3(doc, "Query 6: Vehicle Distribution Across Branches (LEFT OUTER JOIN)")
    add_code(
        doc,
        "SELECT br.bid, br.bname, br.city, COUNT(v.vid) AS vehicle_count\n"
        "FROM branch br\n"
        "LEFT JOIN vehicle v ON br.bid = v.bid\n"
        "GROUP BY br.bid, br.bname, br.city\n"
        "ORDER BY vehicle_count DESC, br.bid;"
    )
    q6_data = [
        ("1", "Chennai Central", "Chennai", "3"),
        ("2", "Coimbatore Gandhipuram", "Coimbatore", "1"),
        ("3", "Madurai Meenakshi", "Madurai", "1"),
        ("4", "Trichy Central", "Trichy", "1"),
        ("9", "Pune FC Road", "Pune", "0"),
        ("10", "Tirunelveli Junction", "Tirunelveli", "0")
    ]
    add_table_data(doc, "Table 7.10: Output of Query 6 (Sample)", ["BID", "Branch Name", "City", "Vehicles Hosted"], q6_data, [Inches(0.6), Inches(2.4), Inches(1.8), Inches(1.7)], font_size=8.5)
    add_p(doc, "Interpretation: Demonstrates outer join preserving branches with 0 vehicles (Pune and Tirunelveli). Chennai Central hosts 3 vehicles.", italic=True)

    # Query 7
    add_h3(doc, "Query 7: String Manipulation Functions (UPPER, LENGTH, SUBSTR, INSTR)")
    add_code(
        doc,
        "SELECT name, UPPER(name) AS upper_name, LENGTH(name) AS name_len,\n"
        "       SUBSTR(phone, 1, 5) AS phone_prefix, INSTR(email, '@') AS at_position\n"
        "FROM customer WHERE ROWNUM <= 4;"
    )
    q7_data = [
        ("Aarav Sharma", "AARAV SHARMA", "12", "98401", "13"),
        ("Diya Patel", "DIYA PATEL", "10", "98402", "11"),
        ("Rohan Iyer", "ROHAN IYER", "10", "98403", "11"),
        ("Priya Nair", "PRIYA NAIR", "10", "98404", "11")
    ]
    add_table_data(doc, "Table 7.11: Output of Query 7", ["Name", "UPPER(name)", "LENGTH", "SUBSTR(phone,1,5)", "INSTR(email,'@')"], q7_data, [Inches(1.3), Inches(1.5), Inches(0.8), Inches(1.4), Inches(1.5)], font_size=8)
    add_p(doc, "Interpretation: Demonstrates Oracle built-in character functions for text transformation and search.", italic=True)

    # Query 8
    add_h3(doc, "Query 8: Booking Month Extraction and Duration Computation (Date Functions)")
    add_code(
        doc,
        "SELECT bkid, TO_CHAR(sdt, 'Month') AS booking_month,\n"
        "       TO_CHAR(sdt, 'Dy') AS start_day, ROUND(edt - sdt) AS duration_days, total\n"
        "FROM booking WHERE ROWNUM <= 4;"
    )
    q8_data = [
        ("1", "January", "Thu", "3", "3600"),
        ("2", "January", "Mon", "3", "5400"),
        ("3", "January", "Sat", "2", "5000"),
        ("4", "January", "Mon", "2", "10000")
    ]
    add_table_data(doc, "Table 7.12: Output of Query 8", ["BKID", "Booking Month", "Day of Week", "Duration (Days)", "Total (Rs.)"], q8_data, [Inches(0.8), Inches(1.6), Inches(1.2), Inches(1.5), Inches(1.4)], font_size=8.5)
    add_p(doc, "Interpretation: Extracts date parts and computes date differences in whole calendar days.", italic=True)

    # Query 9
    add_h3(doc, "Query 9: Most Expensive Category Details (Subquery with MAX)")
    add_code(
        doc,
        "SELECT cid, cname, rate FROM category\n"
        "WHERE rate = (SELECT MAX(rate) FROM category);"
    )
    q9_data = [("10", "Convertible", "6000.00")]
    add_table_data(doc, "Table 7.13: Output of Query 9", ["CID", "Category Name", "Daily Rate (Rs.)"], q9_data, [Inches(1.2), Inches(2.8), Inches(2.5)], font_size=8.5)
    add_p(doc, "Interpretation: Subquery identifies Convertible at Rs. 6,000/day as the highest tariff tier.", italic=True)

    # Query 10
    add_h3(doc, "Query 10: Payment Distribution by Transaction Mode (Aggregation)")
    add_code(
        doc,
        "SELECT pmode, COUNT(pid) AS tx_count, SUM(amt) AS total_collected,\n"
        "       ROUND(AVG(amt), 2) AS avg_tx_amt\n"
        "FROM payment GROUP BY pmode ORDER BY total_collected DESC;"
    )
    q10_data = [
        ("CARD", "3", "19000.00", "6333.33"),
        ("CASH", "4", "14500.00", "3625.00"),
        ("UPI", "3", "9600.00", "3200.00")
    ]
    add_table_data(doc, "Table 7.14: Output of Query 10", ["Payment Mode", "Transaction Count", "Total Collected (Rs.)", "Average Ticket (Rs.)"], q10_data, [Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.7)], font_size=8.5)
    add_p(doc, "Interpretation: CARD collections represent the largest total revenue (Rs. 19,000) across 3 transactions.", italic=True)

    # Query 11
    add_h3(doc, "Query 11: Total Maintenance Cost per Vehicle (Aggregate Join)")
    add_code(
        doc,
        "SELECT v.vid, v.model, v.reg_no, COUNT(m.mid) AS service_records,\n"
        "       NVL(SUM(m.cost), 0) AS total_maint_cost\n"
        "FROM vehicle v\n"
        "JOIN maintenance m ON v.vid = m.vid\n"
        "GROUP BY v.vid, v.model, v.reg_no\n"
        "ORDER BY total_maint_cost DESC;"
    )
    q11_data = [
        ("4", "BMW 3 Series", "KA-01-GH-456", "1", "15000.00"),
        ("10", "Mini Cooper S Conv", "TN-01-ST-012", "1", "12000.00"),
        ("8", "Toyota Innova Crysta", "MH-12-OP-890", "1", "7500.00"),
        ("1", "Maruti Swift", "TN-01-AB-123", "1", "2500.00")
    ]
    add_table_data(doc, "Table 7.15: Output of Query 11 (Top 4 shown)", ["VID", "Model", "Reg Number", "Services", "Total Maintenance (Rs.)"], q11_data, [Inches(0.6), Inches(1.8), Inches(1.6), Inches(1.0), Inches(1.5)], font_size=8)
    add_p(doc, "Interpretation: BMW 3 Series accumulated the highest individual maintenance cost (Rs. 15,000).", italic=True)

    # Query 12
    add_h3(doc, "Query 12: Bookings with No Recorded Payments (LEFT JOIN IS NULL)")
    add_code(
        doc,
        "SELECT b.bkid, c.name, b.status, b.total\n"
        "FROM booking b\n"
        "JOIN customer c ON b.custid = c.custid\n"
        "LEFT JOIN payment p ON b.bkid = p.bkid\n"
        "WHERE p.pid IS NULL ORDER BY b.bkid;"
    )
    q12_data = [
        ("10", "Meera Joshi", "CANCELLED", "3600.00"),
        ("12", "Diya Patel", "BOOKED", "3600.00")
    ]
    add_table_data(doc, "Table 7.16: Output of Query 12", ["BKID", "Customer Name", "Booking Status", "Total (Rs.)"], q12_data, [Inches(0.8), Inches(2.2), Inches(1.8), Inches(1.7)], font_size=8.5)
    add_p(doc, "Interpretation: Correctly identifies open or cancelled bookings that have no recorded payments.", italic=True)

    # Query 13
    add_h3(doc, "Query 13: Active / Open Bookings View (v_open_bookings)")
    add_code(
        doc,
        "SELECT bkid, customer_name, model, status, total FROM v_open_bookings;"
    )
    q13_data = [
        ("11", "Aarav Sharma", "Hyundai Creta", "ACTIVE", "10000.00"),
        ("12", "Diya Patel", "Maruti Swift", "BOOKED", "3600.00")
    ]
    add_table_data(doc, "Table 7.17: Output of Query 13", ["BKID", "Customer Name", "Model", "Status", "Total (Rs.)"], q13_data, [Inches(0.8), Inches(2.0), Inches(1.8), Inches(1.0), Inches(0.9)], font_size=8.5)
    add_p(doc, "Interpretation: Demonstrates querying a virtual view isolating in-progress fleet operations.", italic=True)

    # Query 14
    add_h3(doc, "Query 14: Real-Time Outstanding Balance Using Stored Function f_bal")
    add_code(
        doc,
        "SELECT b.bkid, c.name, b.total, NVL(SUM(p.amt), 0) AS paid, f_bal(b.bkid) AS balance\n"
        "FROM booking b\n"
        "JOIN customer c ON b.custid = c.custid\n"
        "LEFT JOIN payment p ON b.bkid = p.bkid\n"
        "WHERE b.status != 'CANCELLED'\n"
        "GROUP BY b.bkid, c.name, b.total ORDER BY b.bkid;"
    )
    q14_data = [
        ("1", "Aarav Sharma", "3600", "3600", "0.00"),
        ("2", "Diya Patel", "5400", "5400", "0.00"),
        ("11", "Aarav Sharma", "10000", "5000", "5000.00"),
        ("12", "Diya Patel", "3600", "0", "3600.00")
    ]
    add_table_data(doc, "Table 7.18: Output of Query 14 (Sample)", ["BKID", "Customer", "Total (Rs.)", "Paid (Rs.)", "Outstanding (f_bal)"], q14_data, [Inches(0.8), Inches(2.0), Inches(1.2), Inches(1.2), Inches(1.3)], font_size=8.5)
    add_p(doc, "Interpretation: Calls PL/SQL stored function f_bal to evaluate exact pending balance for each booking.", italic=True)

    # Query 15
    add_h3(doc, "Query 15: Customers with a Cancelled Booking (EXISTS Correlated Subquery)")
    add_code(
        doc,
        "SELECT c.custid, c.name, c.phone, c.city\n"
        "FROM customer c\n"
        "WHERE EXISTS (\n"
        "    SELECT 1 FROM booking b\n"
        "    WHERE b.custid = c.custid AND b.status = 'CANCELLED'\n"
        ");"
    )
    q15_data = [("10", "Meera Joshi", "9841001122", "Chennai")]
    add_table_data(doc, "Table 7.19: Output of Query 15", ["Cust ID", "Customer Name", "Phone", "City"], q15_data, [Inches(1.0), Inches(2.2), Inches(1.8), Inches(1.5)], font_size=8.5)
    add_p(doc, "Interpretation: Demonstrates correlated subquery with EXISTS, returning Meera Joshi whose booking 10 was cancelled.", italic=True)

    # Query 16
    add_h3(doc, "Query 16: Consolidated Geographic Footprint (Set Operation: UNION)")
    add_code(
        doc,
        "SELECT city, 'Branch Office' AS entity_type FROM branch\n"
        "UNION\n"
        "SELECT city, 'Customer Base' AS entity_type FROM customer\n"
        "ORDER BY city, entity_type;"
    )
    q16_data = [
        ("Bangalore", "Branch Office"),
        ("Bangalore", "Customer Base"),
        ("Chennai", "Branch Office"),
        ("Chennai", "Customer Base"),
        ("Coimbatore", "Branch Office"),
        ("Coimbatore", "Customer Base"),
        ("Hyderabad", "Branch Office"),
        ("Madurai", "Branch Office"),
        ("Pune", "Branch Office")
    ]
    add_table_data(doc, "Table 7.20: Output of Query 16 (Sample)", ["City Name", "Presence Entity Type"], q16_data, [Inches(3.2), Inches(3.3)], font_size=8.5)
    add_p(doc, "Interpretation: Demonstrates the UNION set operation combining distinct cities across branch networks and customer registries.", italic=True)

    doc.add_page_break()

    # ====================================================
    # CHAPTER 8: ADVANCED DATABASE OPERATIONS
    # ====================================================
    add_h1(doc, "CHAPTER 8: ADVANCED DATABASE OPERATIONS")
    
    add_h2(doc, "8.1 Stored Procedures")
    add_p(
        doc,
        "Five PL/SQL stored procedures encapsulate all core transactional workflows directly within the database engine. "
        "User-defined exceptions in the range -20001 to -20006 enforce business invariants:",
        space_after=4
    )
    sp_data = [
        ("p_book(p_c, p_v, p_s, p_e)", "Vehicle Reservation", "Checks f_avail; inserts BOOKED row using seq_bk; trg_bk_bi computes total.", "ORA-20001 if vehicle under service or date conflict"),
        ("p_start(p_b)", "Trip Handover / Dispatch", "Transitions status to ACTIVE; trg_bk_au automatically locks vehicle to RENTED.", "ORA-20002 if booking not in BOOKED status"),
        ("p_return(p_b)", "Vehicle Check-in / Return", "Transitions status to RETURNED; trg_bk_au releases vehicle to AVAILABLE; calls f_bal.", "ORA-20003 if booking not in ACTIVE status"),
        ("p_pay(p_b, p_a, p_m)", "Payment Settlement", "Checks f_bal; verifies payment amount <= balance; inserts row via seq_pay.", "ORA-20004 if overpayment or booking not found"),
        ("p_dues", "Receivables Cursor Audit", "Explicit cursor (%ROWTYPE) over open bookings; prints delinquent accounts and grand total.", "Logs complete report to DBMS_OUTPUT")
    ]
    add_table_data(
        doc, "Table 8.1: Stored procedures in the VRMS implementation",
        ["Procedure", "Operation", "Core Database Logic", "Exception Handling"],
        sp_data, [Inches(1.8), Inches(1.3), Inches(2.2), Inches(1.2)], font_size=8
    )

    add_h2(doc, "8.2 User-Defined Functions")
    add_p(
        doc,
        "1. f_bal(p_bk IN NUMBER) RETURN NUMBER: Calculates real-time outstanding balance for a booking. "
        "Returns 0 if CANCELLED, -1 if booking does not exist, and total minus SUM(amt) otherwise.",
        space_after=4
    )
    add_code(
        doc,
        "CREATE OR REPLACE FUNCTION f_bal(p_bk IN NUMBER) RETURN NUMBER IS\n"
        "    v_total NUMBER(10,2); v_status VARCHAR2(15); v_paid NUMBER(10,2);\n"
        "BEGIN\n"
        "    SELECT total, status INTO v_total, v_status FROM booking WHERE bkid = p_bk;\n"
        "    IF v_status = 'CANCELLED' THEN RETURN 0; END IF;\n"
        "    SELECT NVL(SUM(amt), 0) INTO v_paid FROM payment WHERE bkid = p_bk;\n"
        "    RETURN v_total - v_paid;\n"
        "EXCEPTION WHEN NO_DATA_FOUND THEN RETURN -1;\n"
        "END f_bal;\n/"
    )
    add_p(
        doc,
        "2. f_avail(p_v IN NUMBER, p_s IN DATE, p_e IN DATE) RETURN NUMBER: Deterministic availability check. "
        "Returns 0 if vehicle is in SERVICE or has overlapping BOOKED/ACTIVE bookings (existing_sdt < p_e AND existing_edt > p_s); otherwise returns 1.",
        space_after=4
    )
    add_code(
        doc,
        "CREATE OR REPLACE FUNCTION f_avail(p_v IN NUMBER, p_s IN DATE, p_e IN DATE) RETURN NUMBER IS\n"
        "    v_status VARCHAR2(15); v_count NUMBER;\n"
        "BEGIN\n"
        "    SELECT status INTO v_status FROM vehicle WHERE vid = p_v;\n"
        "    IF v_status = 'SERVICE' THEN RETURN 0; END IF;\n"
        "    SELECT COUNT(*) INTO v_count FROM booking\n"
        "    WHERE vid = p_v AND status IN ('BOOKED', 'ACTIVE') AND sdt < p_e AND edt > p_s;\n"
        "    IF v_count > 0 THEN RETURN 0; ELSE RETURN 1; END IF;\n"
        "EXCEPTION WHEN NO_DATA_FOUND THEN RETURN 0;\n"
        "END f_avail;\n/"
    )

    add_h2(doc, "8.3 Triggers")
    add_p(
        doc,
        "Trigger 1: trg_bk_bi (BEFORE INSERT ON booking FOR EACH ROW). "
        "Rejects vehicles under SERVICE with ORA-20005. Sets :NEW.total = (edt - sdt) * category.rate. "
        "Mutating Table Prevention: Queries strictly vehicle and category tables, avoiding ORA-04091 mutating table errors on booking.",
        space_after=4
    )
    add_code(
        doc,
        "CREATE OR REPLACE TRIGGER trg_bk_bi\n"
        "BEFORE INSERT ON booking FOR EACH ROW\n"
        "DECLARE v_st VARCHAR2(15); v_rate NUMBER(10,2);\n"
        "BEGIN\n"
        "    SELECT status INTO v_st FROM vehicle WHERE vid = :NEW.vid;\n"
        "    IF v_st = 'SERVICE' THEN\n"
        "        RAISE_APPLICATION_ERROR(-20005, 'Vehicle is currently under maintenance/service.');\n"
        "    END IF;\n"
        "    SELECT c.rate INTO v_rate FROM vehicle v JOIN category c ON v.cid = c.cid WHERE v.vid = :NEW.vid;\n"
        "    :NEW.total := (:NEW.edt - :NEW.sdt) * v_rate;\n"
        "END trg_bk_bi;\n/"
    )
    add_p(
        doc,
        "Trigger 2: trg_bk_au (AFTER UPDATE OF status ON booking FOR EACH ROW). "
        "Inserts an audit record into bk_log using seq_log. If status becomes ACTIVE, locks vehicle to RENTED; if RETURNED or CANCELLED, restores AVAILABLE.",
        space_after=4
    )
    add_code(
        doc,
        "CREATE OR REPLACE TRIGGER trg_bk_au\n"
        "AFTER UPDATE OF status ON booking FOR EACH ROW\n"
        "BEGIN\n"
        "    INSERT INTO bk_log (lid, bkid, old_st, new_st, ldt)\n"
        "    VALUES (seq_log.NEXTVAL, :NEW.bkid, :OLD.status, :NEW.status, SYSDATE);\n"
        "    IF :NEW.status = 'ACTIVE' THEN\n"
        "        UPDATE vehicle SET status = 'RENTED' WHERE vid = :NEW.vid;\n"
        "    ELSIF :NEW.status IN ('RETURNED', 'CANCELLED') THEN\n"
        "        UPDATE vehicle SET status = 'AVAILABLE' WHERE vid = :NEW.vid AND status = 'RENTED';\n"
        "    END IF;\n"
        "END trg_bk_au;\n/"
    )

    add_h2(doc, "8.4 Cursors")
    add_p(
        doc,
        "Procedure p_dues demonstrates the full explicit-cursor lifecycle: DECLARE, OPEN, FETCH in a loop with %ROWTYPE, %NOTFOUND check, and CLOSE.",
        space_after=4
    )
    add_code(
        doc,
        "CREATE OR REPLACE PROCEDURE p_dues IS\n"
        "    CURSOR cur_dues IS\n"
        "        SELECT b.bkid, c.name, c.phone, b.total, b.status\n"
        "        FROM booking b JOIN customer c ON b.custid = c.custid\n"
        "        WHERE b.status != 'CANCELLED' ORDER BY b.bkid;\n"
        "    rec_due cur_dues%ROWTYPE; v_bal NUMBER(10,2); v_grand NUMBER(10,2) := 0; v_count NUMBER := 0;\n"
        "BEGIN\n"
        "    OPEN cur_dues;\n"
        "    LOOP\n"
        "        FETCH cur_dues INTO rec_due; EXIT WHEN cur_dues%NOTFOUND;\n"
        "        v_bal := f_bal(rec_due.bkid);\n"
        "        IF v_bal > 0 THEN\n"
        "            DBMS_OUTPUT.PUT_LINE('BKID: ' || rec_due.bkid || ' | ' || rec_due.name || ' | Due: Rs. ' || v_bal);\n"
        "            v_grand := v_grand + v_bal; v_count := v_count + 1;\n"
        "        END IF;\n"
        "    END LOOP;\n"
        "    CLOSE cur_dues;\n"
        "    DBMS_OUTPUT.PUT_LINE('Total Due Accounts: ' || v_count || ' | Total Receivables: Rs. ' || v_grand);\n"
        "END p_dues;\n/"
    )

    add_h2(doc, "8.5 Sequences and Auto-Generated Keys")
    add_p(
        doc,
        "Deterministic numeric sequences handle primary key generation across concurrent sessions without collision: "
        "seq_bk (START WITH 13), seq_pay (START WITH 11), seq_log (START WITH 1). All sequences specify NOCACHE to prevent gaps during sudden instance restarts.",
        space_after=8
    )

    add_h2(doc, "8.6 Transactions and ACID Properties")
    acid_data = [
        ("Atomicity", "p_start updates booking status and triggers vehicle update; failure rolls back both.", "TC16 mid-transaction failure verification"),
        ("Consistency", "Constraints (CHECK, FK, UK) and trigger trg_bk_bi guarantee valid states.", "TC09 to TC15 constraint rejections"),
        ("Isolation", "Oracle Multitenant MVCC provides statement-level and transaction-level read consistency.", "SELECT FOR UPDATE row-locking in p_start"),
        ("Durability", "Committed transactions write to Redo log files before returning success.", "Committed records persist across DB service restarts")
    ]
    add_table_data(
        doc, "Table 8.4: ACID properties and evidence",
        ["Property", "Implementation in VRMS", "Empirical Test Evidence"],
        acid_data, [Inches(1.2), Inches(3.1), Inches(2.2)], font_size=8.5
    )

    add_h2(doc, "8.7 COMMIT, ROLLBACK, and SAVEPOINT")
    add_p(
        doc,
        "Every stored procedure issues COMMIT on successful completion or executes ROLLBACK in an EXCEPTION block. "
        "SAVEPOINT demonstration: A multi-item payment batch sets SAVEPOINT sp1 after payment 1; a subsequent invalid payment 2 encounters "
        "an exception, executing ROLLBACK TO sp1 and committing only the valid transaction.",
        space_after=8
    )

    add_h2(doc, "8.8 Concurrency Control")
    add_p(
        doc,
        "Oracle AI Database 26ai Free utilizes row-level locking with non-blocking reads under READ COMMITTED isolation. "
        "When p_start or p_return modifies a vehicle, only that specific row in the vehicle table is locked, allowing concurrent bookings "
        "on other vehicles to proceed without delay.",
        space_after=8
    )

    add_h2(doc, "8.9 Deadlocks")
    add_p(
        doc,
        "Deadlocks could hypothetically arise if two transactions attempt to reserve overlapping vehicles in reverse sequence. "
        "Oracle automatically detects lock dependency graphs and resolves deadlocks by raising ORA-00060 on one transaction while allowing "
        "the other to proceed. VRMS prevents this by sorting vehicle acquisitions deterministically by vehicle ID.",
        space_after=12
    )

    doc.add_page_break()
