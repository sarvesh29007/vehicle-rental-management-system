-- =====================================================================
-- VEHICLE RENTAL MANAGEMENT SYSTEM
-- Script 01: Schema & Initial Data
-- Database: Oracle (SQL & PL/SQL)
-- =====================================================================

-- Clean up existing objects if any
BEGIN
  FOR t IN (SELECT table_name FROM user_tables WHERE table_name IN ('BK_LOG','PAYMENT','MAINTENANCE','BOOKING','VEHICLE','CUSTOMER','CATEGORY','BRANCH')) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
  FOR s IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN ('SEQ_BK','SEQ_PAY','SEQ_LOG')) LOOP
    EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
  END LOOP;
END;
/

-- ---------------------------------------------------------------------
-- 1. Table: branch
-- ---------------------------------------------------------------------
CREATE TABLE branch (
  bid   NUMBER PRIMARY KEY,
  bname VARCHAR2(40) NOT NULL,
  city  VARCHAR2(30) NOT NULL,
  phone VARCHAR2(10) UNIQUE
);

-- ---------------------------------------------------------------------
-- 2. Table: category
-- ---------------------------------------------------------------------
CREATE TABLE category (
  cid   NUMBER PRIMARY KEY,
  cname VARCHAR2(30) NOT NULL UNIQUE,
  rate  NUMBER(8,2) NOT NULL CHECK (rate > 0)
);

-- ---------------------------------------------------------------------
-- 3. Table: customer
-- ---------------------------------------------------------------------
CREATE TABLE customer (
  custid NUMBER PRIMARY KEY,
  name   VARCHAR2(40) NOT NULL,
  phone  VARCHAR2(10) NOT NULL UNIQUE,
  email  VARCHAR2(50) UNIQUE,
  lic_no VARCHAR2(20) NOT NULL UNIQUE,
  city   VARCHAR2(30) DEFAULT 'Chennai'
);

-- ---------------------------------------------------------------------
-- 4. Table: vehicle
-- ---------------------------------------------------------------------
CREATE TABLE vehicle (
  vid    NUMBER PRIMARY KEY,
  reg_no VARCHAR2(12) NOT NULL UNIQUE,
  model  VARCHAR2(30) NOT NULL,
  cid    NUMBER NOT NULL REFERENCES category(cid),
  bid    NUMBER NOT NULL REFERENCES branch(bid),
  yr     NUMBER(4) CHECK (yr >= 2015),
  status VARCHAR2(10) DEFAULT 'AVAILABLE' CHECK (status IN ('AVAILABLE','RENTED','SERVICE'))
);

-- ---------------------------------------------------------------------
-- 5. Table: booking
-- ---------------------------------------------------------------------
CREATE TABLE booking (
  bkid   NUMBER PRIMARY KEY,
  custid NUMBER NOT NULL REFERENCES customer(custid),
  vid    NUMBER NOT NULL REFERENCES vehicle(vid),
  sdt    DATE NOT NULL,
  edt    DATE NOT NULL,
  status VARCHAR2(10) DEFAULT 'BOOKED' CHECK (status IN ('BOOKED','ACTIVE','RETURNED','CANCELLED')),
  total  NUMBER(10,2) DEFAULT 0,
  CONSTRAINT ck_dt CHECK (edt > sdt)
);

-- ---------------------------------------------------------------------
-- 6. Table: payment
-- ---------------------------------------------------------------------
CREATE TABLE payment (
  pid   NUMBER PRIMARY KEY,
  bkid  NUMBER NOT NULL REFERENCES booking(bkid),
  amt   NUMBER(10,2) NOT NULL CHECK (amt > 0),
  pdt   DATE DEFAULT SYSDATE,
  pmode VARCHAR2(10) CHECK (pmode IN ('CASH','UPI','CARD'))
);

-- ---------------------------------------------------------------------
-- 7. Table: maintenance
-- ---------------------------------------------------------------------
CREATE TABLE maintenance (
  mid   NUMBER PRIMARY KEY,
  vid   NUMBER NOT NULL REFERENCES vehicle(vid),
  mdt   DATE NOT NULL,
  cost  NUMBER(8,2) CHECK (cost >= 0),
  descr VARCHAR2(60)
);

-- ---------------------------------------------------------------------
-- 8. Table: bk_log (Audit table populated exclusively by trigger)
-- ---------------------------------------------------------------------
CREATE TABLE bk_log (
  lid    NUMBER PRIMARY KEY,
  bkid   NUMBER,
  old_st VARCHAR2(10),
  new_st VARCHAR2(10),
  ldt    DATE DEFAULT SYSDATE
);

-- ---------------------------------------------------------------------
-- Sequences
-- ---------------------------------------------------------------------
CREATE SEQUENCE seq_bk  START WITH 13;
CREATE SEQUENCE seq_pay START WITH 11;
CREATE SEQUENCE seq_log START WITH 1;

-- ---------------------------------------------------------------------
-- Triggers (Defined before booking inserts so totals are computed automatically)
-- ---------------------------------------------------------------------

-- Trigger 1: BEFORE INSERT on booking (Row level)
-- Validates vehicle is not under service and calculates total = (edt - sdt) * category rate
CREATE OR REPLACE TRIGGER trg_bk_bi
BEFORE INSERT ON booking
FOR EACH ROW
DECLARE
  v_status vehicle.status%TYPE;
  v_rate   category.rate%TYPE;
BEGIN
  SELECT v.status, c.rate INTO v_status, v_rate
  FROM vehicle v
  JOIN category c ON v.cid = c.cid
  WHERE v.vid = :NEW.vid;

  IF v_status = 'SERVICE' THEN
    RAISE_APPLICATION_ERROR(-20002, 'vehicle under service');
  END IF;

  :NEW.total := (:NEW.edt - :NEW.sdt) * v_rate;
END;
/

-- Trigger 2: AFTER UPDATE OF status on booking (Row level)
-- Logs transition to bk_log and adjusts vehicle availability status
CREATE OR REPLACE TRIGGER trg_bk_au
AFTER UPDATE OF status ON booking
FOR EACH ROW
BEGIN
  INSERT INTO bk_log (lid, bkid, old_st, new_st, ldt)
  VALUES (seq_log.NEXTVAL, :NEW.bkid, :OLD.status, :NEW.status, SYSDATE);

  IF :NEW.status = 'ACTIVE' THEN
    UPDATE vehicle SET status = 'RENTED' WHERE vid = :NEW.vid;
  ELSIF :NEW.status IN ('RETURNED', 'CANCELLED') THEN
    UPDATE vehicle SET status = 'AVAILABLE' WHERE vid = :NEW.vid AND status = 'RENTED';
  END IF;
END;
/

-- ---------------------------------------------------------------------
-- Sample Data (At least 10 rows per table, all constraints respected)
-- ---------------------------------------------------------------------

-- 1. Branches (10 branches)
INSERT INTO branch VALUES (1, 'Central', 'Chennai', '4412340001');
INSERT INTO branch VALUES (2, 'Fort', 'Vellore', '4162340002');
INSERT INTO branch VALUES (3, 'RS Puram', 'Coimbatore', '4222340003');
INSERT INTO branch VALUES (4, 'Anna Nagar', 'Madurai', '4522340004');
INSERT INTO branch VALUES (5, 'Cantonment', 'Trichy', '4312340005');
INSERT INTO branch VALUES (6, 'Fairlands', 'Salem', '4272340006');
INSERT INTO branch VALUES (7, 'MG Road', 'Bangalore', '8012340007');
INSERT INTO branch VALUES (8, 'Banjara', 'Hyderabad', '4012340008');
INSERT INTO branch VALUES (9, 'Marine Drive', 'Kochi', '4842340009');
INSERT INTO branch VALUES (10, 'Koregaon', 'Pune', '2012340010');

-- 2. Categories (10 categories with distinct rates)
INSERT INTO category VALUES (1, 'Hatchback', 1200);
INSERT INTO category VALUES (2, 'Sedan', 1800);
INSERT INTO category VALUES (3, 'SUV', 2500);
INSERT INTO category VALUES (4, 'Luxury', 5000);
INSERT INTO category VALUES (5, 'Bike', 500);
INSERT INTO category VALUES (6, 'Scooter', 400);
INSERT INTO category VALUES (7, 'Van', 3000);
INSERT INTO category VALUES (8, 'MUV', 2800);
INSERT INTO category VALUES (9, 'Electric', 2200);
INSERT INTO category VALUES (10, 'Convertible', 6000);

-- 3. Customers (10 customers)
INSERT INTO customer VALUES (1, 'Arun Kumar', '9840011001', 'arun.kumar@mail.com', 'DL-TN-0001', 'Chennai');
INSERT INTO customer VALUES (2, 'Priya Sharma', '9840011002', 'priya.sharma@mail.com', 'DL-TN-0002', 'Vellore');
INSERT INTO customer VALUES (3, 'Karthik Raj', '9840011003', 'karthik.raj@mail.com', 'DL-TN-0003', 'Coimbatore');
INSERT INTO customer VALUES (4, 'Divya Nair', '9840011004', 'divya.nair@mail.com', 'DL-KL-0004', 'Kochi');
INSERT INTO customer VALUES (5, 'Mohammed Irfan', '9840011005', 'irfan.m@mail.com', 'DL-TN-0005', 'Madurai');
INSERT INTO customer VALUES (6, 'Sneha Reddy', '9840011006', 'sneha.reddy@mail.com', 'DL-TS-0006', 'Hyderabad');
INSERT INTO customer VALUES (7, 'Vignesh S', '9840011007', 'vignesh.s@mail.com', 'DL-TN-0007', 'Trichy');
INSERT INTO customer VALUES (8, 'Anita Joseph', '9840011008', 'anita.joseph@mail.com', 'DL-KA-0008', 'Bangalore');
INSERT INTO customer VALUES (9, 'Rahul Verma', '9840011009', 'rahul.verma@mail.com', 'DL-MH-0009', 'Pune');
INSERT INTO customer VALUES (10, 'Lakshmi Iyer', '9840011010', 'lakshmi.iyer@mail.com', 'DL-TN-0010', 'Salem');

-- 4. Vehicles (10 vehicles; Vehicle 10 is in SERVICE)
INSERT INTO vehicle VALUES (1, 'TN01AB1001', 'Swift', 1, 1, 2022, 'AVAILABLE');
INSERT INTO vehicle VALUES (2, 'TN01AB1002', 'Honda City', 2, 1, 2021, 'AVAILABLE');
INSERT INTO vehicle VALUES (3, 'TN32CD2003', 'Creta', 3, 2, 2023, 'AVAILABLE');
INSERT INTO vehicle VALUES (4, 'TN38EF3004', 'BMW 3 Series', 4, 3, 2022, 'AVAILABLE');
INSERT INTO vehicle VALUES (5, 'TN58GH4005', 'Royal Enfield', 5, 4, 2023, 'AVAILABLE');
INSERT INTO vehicle VALUES (6, 'TN45JK5006', 'Activa', 6, 5, 2022, 'AVAILABLE');
INSERT INTO vehicle VALUES (7, 'TN30LM6007', 'Force Traveller', 7, 6, 2020, 'AVAILABLE');
INSERT INTO vehicle VALUES (8, 'KA03NP7008', 'Innova', 8, 7, 2021, 'AVAILABLE');
INSERT INTO vehicle VALUES (9, 'TS09QR8009', 'Nexon EV', 9, 8, 2024, 'AVAILABLE');
INSERT INTO vehicle VALUES (10, 'KL07ST9010', 'Mini Cooper', 10, 9, 2023, 'SERVICE');

-- 5. Bookings (12 bookings; totals computed by trg_bk_bi trigger)
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (1, 1, 1, DATE '2026-08-01', DATE '2026-08-04', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (2, 2, 3, DATE '2026-08-05', DATE '2026-08-08', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (3, 3, 2, DATE '2026-08-10', DATE '2026-08-12', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (4, 4, 4, DATE '2026-08-15', DATE '2026-08-18', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (5, 5, 5, DATE '2026-08-20', DATE '2026-08-22', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (6, 6, 8, DATE '2026-09-01', DATE '2026-09-05', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (7, 7, 9, DATE '2026-09-10', DATE '2026-09-13', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (8, 8, 6, DATE '2026-09-15', DATE '2026-09-16', 'CANCELLED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (9, 9, 7, DATE '2026-09-20', DATE '2026-09-24', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (10, 10, 1, DATE '2026-10-05', DATE '2026-10-09', 'RETURNED');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (11, 1, 3, DATE '2026-10-11', DATE '2026-10-15', 'ACTIVE');
INSERT INTO booking(bkid,custid,vid,sdt,edt,status) VALUES (12, 2, 2, DATE '2026-10-20', DATE '2026-10-23', 'BOOKED');

-- Ensure active booking vehicle is marked RENTED
UPDATE vehicle SET status = 'RENTED' WHERE vid = 3;

-- 6. Payments (10 payments; each <= booking total)
INSERT INTO payment VALUES (1, 1, 3600, DATE '2026-08-01', 'UPI');
INSERT INTO payment VALUES (2, 2, 7500, DATE '2026-08-05', 'CARD');
INSERT INTO payment VALUES (3, 3, 3600, DATE '2026-08-10', 'CASH');
INSERT INTO payment VALUES (4, 4, 15000, DATE '2026-08-15', 'CARD');
INSERT INTO payment VALUES (5, 5, 1000, DATE '2026-08-20', 'CASH');
INSERT INTO payment VALUES (6, 6, 11200, DATE '2026-09-01', 'UPI');
INSERT INTO payment VALUES (7, 7, 6600, DATE '2026-09-10', 'UPI');
INSERT INTO payment VALUES (8, 9, 12000, DATE '2026-09-20', 'CARD');
INSERT INTO payment VALUES (9, 10, 4800, DATE '2026-10-05', 'UPI');
INSERT INTO payment VALUES (10, 11, 5000, DATE '2026-10-11', 'UPI');

-- 7. Maintenance (10 maintenance records)
INSERT INTO maintenance VALUES (1, 1, DATE '2026-07-10', 2500, 'Oil change');
INSERT INTO maintenance VALUES (2, 2, DATE '2026-07-15', 4200, 'Brake pads');
INSERT INTO maintenance VALUES (3, 3, DATE '2026-07-20', 6000, 'Clutch repair');
INSERT INTO maintenance VALUES (4, 4, DATE '2026-07-25', 9500, 'Full service');
INSERT INTO maintenance VALUES (5, 5, DATE '2026-08-02', 800, 'Chain lubrication');
INSERT INTO maintenance VALUES (6, 6, DATE '2026-08-08', 1200, 'Tyre change');
INSERT INTO maintenance VALUES (7, 7, DATE '2026-08-14', 7000, 'AC repair');
INSERT INTO maintenance VALUES (8, 8, DATE '2026-09-02', 3500, 'General service');
INSERT INTO maintenance VALUES (9, 9, DATE '2026-09-12', 2000, 'Battery check');
INSERT INTO maintenance VALUES (10, 10, DATE '2026-10-01', 15000, 'Engine overhaul');

-- 8. Seed initial log records for the existing bookings
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 1, 'BOOKED', 'RETURNED', DATE '2026-08-04');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 2, 'BOOKED', 'RETURNED', DATE '2026-08-08');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 3, 'BOOKED', 'RETURNED', DATE '2026-08-12');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 4, 'BOOKED', 'RETURNED', DATE '2026-08-18');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 5, 'BOOKED', 'RETURNED', DATE '2026-08-22');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 6, 'BOOKED', 'RETURNED', DATE '2026-09-05');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 7, 'BOOKED', 'RETURNED', DATE '2026-09-13');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 8, 'BOOKED', 'CANCELLED', DATE '2026-09-15');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 9, 'BOOKED', 'RETURNED', DATE '2026-09-24');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 10, 'BOOKED', 'RETURNED', DATE '2026-10-09');
INSERT INTO bk_log VALUES (seq_log.NEXTVAL, 11, 'BOOKED', 'ACTIVE', DATE '2026-10-11');

COMMIT;
