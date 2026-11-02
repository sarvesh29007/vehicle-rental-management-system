-- =====================================================================
-- VEHICLE RENTAL MANAGEMENT SYSTEM
-- Script 04: View Tables, Columns & Constraints in SQL Developer
-- Database: Oracle (SQL & PL/SQL)
-- =====================================================================

SET PAGESIZE 100;
SET LINESIZE 250;
SET FEEDBACK ON;

PROMPT =================================================================
PROMPT 1. TABLE: BRANCH
PROMPT =================================================================
SELECT * FROM branch ORDER BY bid;

PROMPT =================================================================
PROMPT 2. TABLE: CATEGORY
PROMPT =================================================================
SELECT * FROM category ORDER BY cid;

PROMPT =================================================================
PROMPT 3. TABLE: CUSTOMER
PROMPT =================================================================
SELECT * FROM customer ORDER BY custid;

PROMPT =================================================================
PROMPT 4. TABLE: VEHICLE
PROMPT =================================================================
SELECT * FROM vehicle ORDER BY vid;

PROMPT =================================================================
PROMPT 5. TABLE: BOOKING
PROMPT =================================================================
SELECT * FROM booking ORDER BY bkid;

PROMPT =================================================================
PROMPT 6. TABLE: PAYMENT
PROMPT =================================================================
SELECT * FROM payment ORDER BY pid;

PROMPT =================================================================
PROMPT 7. TABLE: MAINTENANCE
PROMPT =================================================================
SELECT * FROM maintenance ORDER BY mid;

PROMPT =================================================================
PROMPT 8. TABLE: BK_LOG (AUDIT LOG)
PROMPT =================================================================
SELECT * FROM bk_log ORDER BY lid;


PROMPT =================================================================
PROMPT DATA DICTIONARY REPORT: COLUMNS & DATA TYPES
PROMPT =================================================================
SELECT table_name,
       column_name,
       data_type || 
         CASE 
           WHEN data_type IN ('VARCHAR2', 'CHAR') THEN '(' || data_length || ')'
           WHEN data_type = 'NUMBER' AND data_precision IS NOT NULL AND data_scale > 0 THEN '(' || data_precision || ',' || data_scale || ')'
           WHEN data_type = 'NUMBER' AND data_precision IS NOT NULL THEN '(' || data_precision || ')'
           ELSE ''
         END AS data_type,
       nullable AS is_nullable,
       data_default
FROM user_tab_columns
WHERE table_name IN ('BRANCH', 'CATEGORY', 'CUSTOMER', 'VEHICLE', 'BOOKING', 'PAYMENT', 'MAINTENANCE', 'BK_LOG')
ORDER BY table_name, column_id;


PROMPT =================================================================
PROMPT DATA DICTIONARY REPORT: CONSTRAINTS (PK, FK, UNIQUE, CHECK)
PROMPT =================================================================
SELECT uc.table_name,
       uc.constraint_name,
       CASE uc.constraint_type
         WHEN 'P' THEN 'PRIMARY KEY'
         WHEN 'R' THEN 'FOREIGN KEY'
         WHEN 'U' THEN 'UNIQUE'
         WHEN 'C' THEN 'CHECK'
         ELSE uc.constraint_type
       END AS constraint_type,
       ucc.column_name,
       uc.search_condition,
       uc_r.table_name AS r_table_name
FROM user_constraints uc
JOIN user_cons_columns ucc ON uc.constraint_name = ucc.constraint_name
LEFT JOIN user_constraints uc_r ON uc.r_constraint_name = uc_r.constraint_name
WHERE uc.table_name IN ('BRANCH', 'CATEGORY', 'CUSTOMER', 'VEHICLE', 'BOOKING', 'PAYMENT', 'MAINTENANCE', 'BK_LOG')
ORDER BY uc.table_name, uc.constraint_type, uc.constraint_name;
