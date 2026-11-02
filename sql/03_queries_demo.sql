-- =====================================================================
-- VEHICLE RENTAL MANAGEMENT SYSTEM
-- Script 03: 16 Queries and 9 Real-World Transactions Demonstration
-- Database: Oracle (SQL & PL/SQL)
-- =====================================================================

SET SERVEROUTPUT ON SIZE UNLIMITED;
SET LINESIZE 200;
SET PAGESIZE 50;
SET FEEDBACK ON;

-- =====================================================================
-- PART 1: 16 SQL QUERIES
-- =====================================================================

PROMPT -----------------------------------------------------------------
PROMPT Q1: Booking details with customer and vehicle (3-table join)
PROMPT -----------------------------------------------------------------
SELECT b.bkid, c.name AS customer_name, v.model AS vehicle_model,
       b.sdt, b.edt, b.status, b.total
FROM booking b
JOIN customer c ON b.custid = c.custid
JOIN vehicle v   ON b.vid = v.vid
ORDER BY b.bkid;

PROMPT -----------------------------------------------------------------
PROMPT Q2: Revenue and trips per category (Aggregation & Grouping)
PROMPT -----------------------------------------------------------------
SELECT g.cname AS category,
       COUNT(b.bkid) AS trips,
       NVL(SUM(b.total), 0) AS total_revenue
FROM category g
JOIN vehicle v ON g.cid = v.cid
LEFT JOIN booking b ON v.vid = b.vid AND b.status <> 'CANCELLED'
GROUP BY g.cname
ORDER BY total_revenue DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q3: Customers with more than one booking (HAVING clause)
PROMPT -----------------------------------------------------------------
SELECT c.custid, c.name, COUNT(b.bkid) AS booking_count
FROM customer c
JOIN booking b ON c.custid = b.custid
GROUP BY c.custid, c.name
HAVING COUNT(b.bkid) > 1
ORDER BY booking_count DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q4: Vehicles never booked (NOT IN subquery)
PROMPT -----------------------------------------------------------------
SELECT vid, reg_no, model, status
FROM vehicle
WHERE vid NOT IN (SELECT vid FROM booking WHERE vid IS NOT NULL)
ORDER BY vid;

PROMPT -----------------------------------------------------------------
PROMPT Q5: Payments above average (Subquery comparison)
PROMPT -----------------------------------------------------------------
SELECT p.pid, p.bkid, c.name AS customer_name, p.amt, p.pmode, p.pdt
FROM payment p
JOIN booking b ON p.bkid = b.bkid
JOIN customer c ON b.custid = c.custid
WHERE p.amt > (SELECT AVG(amt) FROM payment)
ORDER BY p.amt DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q6: Vehicles per branch (LEFT JOIN with aggregation)
PROMPT -----------------------------------------------------------------
SELECT b.bid, b.bname, b.city, COUNT(v.vid) AS vehicle_count
FROM branch b
LEFT JOIN vehicle v ON b.bid = v.bid
GROUP BY b.bid, b.bname, b.city
ORDER BY vehicle_count DESC, b.bid ASC;

PROMPT -----------------------------------------------------------------
PROMPT Q7: Single-row functions on customer data (UPPER, LENGTH, SUBSTR, INSTR)
PROMPT -----------------------------------------------------------------
SELECT custid,
       UPPER(name) AS upper_name,
       LENGTH(name) AS name_len,
       SUBSTR(email, 1, INSTR(email, '@') - 1) AS email_username,
       SUBSTR(email, INSTR(email, '@') + 1) AS email_domain
FROM customer
ORDER BY custid;

PROMPT -----------------------------------------------------------------
PROMPT Q8: Booking month and duration in days (Date function TO_CHAR)
PROMPT -----------------------------------------------------------------
SELECT bkid,
       TO_CHAR(sdt, 'Mon YYYY') AS booking_month,
       TO_CHAR(sdt, 'DD-Mon-YYYY') AS start_date,
       TO_CHAR(edt, 'DD-Mon-YYYY') AS end_date,
       (edt - sdt) AS rental_days,
       total
FROM booking
ORDER BY bkid;

PROMPT -----------------------------------------------------------------
PROMPT Q9: Costliest vehicle category (MAX subquery)
PROMPT -----------------------------------------------------------------
SELECT cid, cname, rate
FROM category
WHERE rate = (SELECT MAX(rate) FROM category);

PROMPT -----------------------------------------------------------------
PROMPT Q10: Payments aggregated by mode (UPI, CARD, CASH)
PROMPT -----------------------------------------------------------------
SELECT pmode,
       COUNT(*) AS transactions,
       SUM(amt) AS total_collected
FROM payment
GROUP BY pmode
ORDER BY total_collected DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q11: Total maintenance cost per vehicle
PROMPT -----------------------------------------------------------------
SELECT v.vid, v.model, v.reg_no,
       NVL(SUM(m.cost), 0) AS total_maintenance_cost,
       COUNT(m.mid) AS service_count
FROM vehicle v
LEFT JOIN maintenance m ON v.vid = m.vid
GROUP BY v.vid, v.model, v.reg_no
ORDER BY total_maintenance_cost DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q12: Bookings with no payment recorded (LEFT JOIN IS NULL)
PROMPT -----------------------------------------------------------------
SELECT b.bkid, c.name, b.status, b.total
FROM booking b
JOIN customer c ON b.custid = c.custid
LEFT JOIN payment p ON b.bkid = p.bkid
WHERE p.pid IS NULL
ORDER BY b.bkid;

PROMPT -----------------------------------------------------------------
PROMPT Q13: View of active and booked reservations (CREATE VIEW & SELECT)
PROMPT -----------------------------------------------------------------
CREATE OR REPLACE VIEW v_open AS
SELECT b.bkid, c.name AS customer_name, v.model AS vehicle_model,
       b.sdt, b.edt, b.status, b.total
FROM booking b
JOIN customer c ON b.custid = c.custid
JOIN vehicle v   ON b.vid = v.vid
WHERE b.status IN ('BOOKED', 'ACTIVE');

SELECT * FROM v_open ORDER BY bkid;

PROMPT -----------------------------------------------------------------
PROMPT Q14: Pending balance for each booking using stored function f_bal
PROMPT -----------------------------------------------------------------
SELECT b.bkid, c.name, b.total, f_bal(b.bkid) AS pending_balance, b.status
FROM booking b
JOIN customer c ON b.custid = c.custid
WHERE f_bal(b.bkid) > 0
ORDER BY pending_balance DESC;

PROMPT -----------------------------------------------------------------
PROMPT Q15: Customers with at least one cancelled booking (EXISTS subquery)
PROMPT -----------------------------------------------------------------
SELECT c.custid, c.name, c.phone, c.city
FROM customer c
WHERE EXISTS (
  SELECT 1 FROM booking b
  WHERE b.custid = c.custid
    AND b.status = 'CANCELLED'
);

PROMPT -----------------------------------------------------------------
PROMPT Q16: Union of all distinct cities where customers or branches exist
PROMPT -----------------------------------------------------------------
SELECT city, 'Customer City' AS source_type FROM customer
UNION
SELECT city, 'Branch City' AS source_type FROM branch
ORDER BY city;


-- =====================================================================
-- PART 2: 9 REAL-WORLD DEMONSTRATION TRANSACTIONS
-- =====================================================================

PROMPT =================================================================
PROMPT T1: INSERT two customers (Demonstrating INSERT)
PROMPT =================================================================
INSERT INTO customer (custid, name, phone, email, lic_no, city)
VALUES (11, 'Deepak Menon', '9840011011', 'deepak.menon@mail.com', 'DL-KL-0011', 'Kochi');

INSERT INTO customer (custid, name, phone, email, lic_no, city)
VALUES (12, 'Test User', '9840011012', 'test.user@mail.com', 'DL-TN-0012', 'Chennai');

SELECT custid, name, phone, city FROM customer WHERE custid IN (11, 12);

PROMPT =================================================================
PROMPT T2: DELETE test customer (Demonstrating DELETE)
PROMPT =================================================================
DELETE FROM customer WHERE custid = 12;
SELECT custid, name FROM customer WHERE custid = 12;

PROMPT =================================================================
PROMPT T3: UPDATE Sedan category rate (Demonstrating UPDATE)
PROMPT =================================================================
UPDATE category SET rate = rate + 100 WHERE cname = 'Sedan';
SELECT cid, cname, rate FROM category WHERE cname = 'Sedan';

PROMPT =================================================================
PROMPT T4: Book vehicle (p_book: uses f_avail, seq_bk, and trg_bk_bi)
PROMPT =================================================================
BEGIN
  -- Customer 11 books BMW 3 Series (vid=4, rate=5000) for 2 days
  p_book(11, 4, DATE '2026-11-01', DATE '2026-11-03');
END;
/
SELECT bkid, custid, vid, sdt, edt, total, status FROM booking WHERE bkid = 13;

PROMPT =================================================================
PROMPT T5: Hand over vehicle (p_start: fires trg_bk_au to set vehicle RENTED & log)
PROMPT =================================================================
BEGIN
  p_start(13);
END;
/
SELECT vid, model, status FROM vehicle WHERE vid = 4;
SELECT * FROM bk_log WHERE bkid = 13 ORDER BY lid;

PROMPT =================================================================
PROMPT T6: Return vehicle (p_return: fires trg_bk_au to set vehicle AVAILABLE)
PROMPT =================================================================
BEGIN
  p_return(13);
END;
/
SELECT vid, model, status FROM vehicle WHERE vid = 4;
SELECT * FROM bk_log WHERE bkid = 13 ORDER BY lid;

PROMPT =================================================================
PROMPT T7: Make payment (p_pay: validates balance, inserts via seq_pay)
PROMPT =================================================================
BEGIN
  -- Pay full balance of Rs. 10000 by CARD
  p_pay(13, 10000, 'CARD');
END;
/
SELECT * FROM payment WHERE bkid = 13;
SELECT bkid, total, f_bal(bkid) AS remaining_balance FROM booking WHERE bkid = 13;

PROMPT =================================================================
PROMPT T8: Dues report (p_dues: uses explicit cursor c_dues)
PROMPT =================================================================
BEGIN
  p_dues;
END;
/

PROMPT =================================================================
PROMPT T9: Error case - Book vehicle under service (must fail with ORA-20001 or ORA-20002)
PROMPT =================================================================
BEGIN
  -- vid 10 (Mini Cooper) has status SERVICE
  p_book(1, 10, DATE '2026-11-05', DATE '2026-11-07');
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Caught Expected Error: ' || SQLERRM);
END;
/

COMMIT;
