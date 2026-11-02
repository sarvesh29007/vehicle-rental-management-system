-- =====================================================================
-- VEHICLE RENTAL MANAGEMENT SYSTEM
-- Script 02: PL/SQL Functions and Procedures
-- Database: Oracle (SQL & PL/SQL)
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Function: f_bal
-- Returns pending balance for a booking.
-- Returns 0 if CANCELLED, -1 if booking not found.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION f_bal(p_bk NUMBER) RETURN NUMBER IS
  v_tot  booking.total%TYPE;
  v_st   booking.status%TYPE;
  v_paid NUMBER;
BEGIN
  SELECT total, status INTO v_tot, v_st
  FROM booking
  WHERE bkid = p_bk;

  IF v_st = 'CANCELLED' THEN
    RETURN 0;
  END IF;

  SELECT NVL(SUM(amt), 0) INTO v_paid
  FROM payment
  WHERE bkid = p_bk;

  RETURN v_tot - v_paid;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN -1;
END;
/

-- ---------------------------------------------------------------------
-- 2. Function: f_avail
-- Returns 1 if vehicle is available for given period, 0 otherwise.
-- Overlap condition: existing sdt < new edt AND existing edt > new sdt.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION f_avail(p_v NUMBER, p_s DATE, p_e DATE) RETURN NUMBER IS
  v_st  vehicle.status%TYPE;
  v_cnt NUMBER;
BEGIN
  SELECT status INTO v_st
  FROM vehicle
  WHERE vid = p_v;

  IF v_st = 'SERVICE' THEN
    RETURN 0;
  END IF;

  SELECT COUNT(*) INTO v_cnt
  FROM booking
  WHERE vid = p_v
    AND status IN ('BOOKED', 'ACTIVE')
    AND sdt < p_e
    AND edt > p_s;

  IF v_cnt > 0 THEN
    RETURN 0;
  END IF;

  RETURN 1;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN 0;
END;
/

-- ---------------------------------------------------------------------
-- 3. Procedure: p_book
-- Books a vehicle for a customer if available.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE p_book(p_c NUMBER, p_v NUMBER, p_s DATE, p_e DATE) IS
  v_new_id NUMBER;
BEGIN
  IF f_avail(p_v, p_s, p_e) = 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Vehicle not available for these dates');
  END IF;

  v_new_id := seq_bk.NEXTVAL;
  INSERT INTO booking(bkid, custid, vid, sdt, edt, status)
  VALUES (v_new_id, p_c, p_v, p_s, p_e, 'BOOKED');

  DBMS_OUTPUT.PUT_LINE('booked id ' || v_new_id);
END;
/

-- ---------------------------------------------------------------------
-- 4. Procedure: p_start
-- Hands over vehicle: transitions booking from BOOKED to ACTIVE.
-- Trigger trg_bk_au automatically marks vehicle RENTED and writes bk_log.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE p_start(p_b NUMBER) IS
  v_st booking.status%TYPE;
BEGIN
  SELECT status INTO v_st
  FROM booking
  WHERE bkid = p_b;

  IF v_st <> 'BOOKED' THEN
    RAISE_APPLICATION_ERROR(-20005, 'Booking not in BOOKED state');
  END IF;

  UPDATE booking SET status = 'ACTIVE' WHERE bkid = p_b;
  DBMS_OUTPUT.PUT_LINE('vehicle handed over');
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
END;
/

-- ---------------------------------------------------------------------
-- 5. Procedure: p_return
-- Receives returned vehicle: transitions booking from ACTIVE to RETURNED.
-- Trigger trg_bk_au automatically marks vehicle AVAILABLE and writes bk_log.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE p_return(p_b NUMBER) IS
  v_st booking.status%TYPE;
BEGIN
  SELECT status INTO v_st
  FROM booking
  WHERE bkid = p_b;

  IF v_st <> 'ACTIVE' THEN
    RAISE_APPLICATION_ERROR(-20003, 'Booking not active');
  END IF;

  UPDATE booking SET status = 'RETURNED' WHERE bkid = p_b;
  DBMS_OUTPUT.PUT_LINE('returned, balance ' || f_bal(p_b));
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
END;
/

-- ---------------------------------------------------------------------
-- 6. Procedure: p_pay
-- Records payment against a booking. Rejects unknown or over-payment.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE p_pay(p_b NUMBER, p_a NUMBER, p_m VARCHAR2) IS
  v_bal NUMBER;
BEGIN
  v_bal := f_bal(p_b);

  IF v_bal < 0 THEN
    RAISE_APPLICATION_ERROR(-20006, 'No such booking');
  END IF;

  IF p_a > v_bal THEN
    RAISE_APPLICATION_ERROR(-20004, 'Amount exceeds pending balance');
  END IF;

  INSERT INTO payment(pid, bkid, amt, pdt, pmode)
  VALUES (seq_pay.NEXTVAL, p_b, p_a, SYSDATE, p_m);

  DBMS_OUTPUT.PUT_LINE('paid, balance ' || (v_bal - p_a));
END;
/

-- ---------------------------------------------------------------------
-- 7. Procedure: p_dues
-- Explicit cursor over non-cancelled bookings with customer details.
-- Reports all pending balances and prints total outstanding due.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE p_dues IS
  CURSOR c_dues IS
    SELECT b.bkid, u.name, f_bal(b.bkid) AS due_amt
    FROM booking b
    JOIN customer u ON b.custid = u.custid
    WHERE b.status <> 'CANCELLED';
  r_due c_dues%ROWTYPE;
  v_total NUMBER := 0;
BEGIN
  OPEN c_dues;
  LOOP
    FETCH c_dues INTO r_due;
    EXIT WHEN c_dues%NOTFOUND;
    IF r_due.due_amt > 0 THEN
      DBMS_OUTPUT.PUT_LINE('Booking ' || r_due.bkid || ' | ' || r_due.name || ' | Due: Rs. ' || r_due.due_amt);
      v_total := v_total + r_due.due_amt;
    END IF;
  END LOOP;
  CLOSE c_dues;
  DBMS_OUTPUT.PUT_LINE('total due ' || v_total);
END;
/
