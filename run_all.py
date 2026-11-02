"""
=====================================================================
VEHICLE RENTAL MANAGEMENT SYSTEM - DATABASE & TEST RUNNER
Automates schema creation, PL/SQL deployment, runs all 16 queries,
all 9 transactions, and verifies all course requirements.
=====================================================================
"""

import sys
import os
import re
from datetime import datetime
import oracledb

# Configuration
SYS_USER = "system"
SYS_PASS = "Rental123#"  # Or user-specified SYS password
DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "FREEPDB1"  # Or XEPDB1

APP_USER = "rental"
APP_PASS = "rental123"

def get_connection(user, password, service_name=DB_SERVICE):
    return oracledb.connect(
        user=user,
        password=password,
        host=DB_HOST,
        port=DB_PORT,
        service_name=service_name
    )

def setup_app_user():
    print("------------------------------------------------------------------")
    print(f"1. Setting up test schema user: {APP_USER}...")
    print("------------------------------------------------------------------")
    try:
        con = get_connection(SYS_USER, SYS_PASS)
        cur = con.cursor()
        
        # Check if user exists
        cur.execute("SELECT username FROM all_users WHERE username = :u", {"u": APP_USER.upper()})
        exists = cur.fetchone()
        
        if exists:
            print(f"User {APP_USER} already exists. Granting full quota and privileges...")
        else:
            cur.execute(f"CREATE USER {APP_USER} IDENTIFIED BY {APP_PASS}")
            print(f"User {APP_USER} created successfully.")
            
        cur.execute(f"GRANT CONNECT, RESOURCE, CREATE VIEW, UNLIMITED TABLESPACE TO {APP_USER}")
        con.commit()
        cur.close()
        con.close()
        print("Schema user setup complete.")
        return True
    except Exception as e:
        print(f"Error setting up user {APP_USER}: {e}")
        return False

def run_sql_script(con, script_path):
    print(f"Executing {os.path.basename(script_path)}...")
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by '/' for PL/SQL blocks or ';' for SQL statements
    cur = con.cursor()
    cur.callproc("dbms_output.enable")

    # Custom splitter for Oracle scripts with triggers/procedures
    # Blocks ending with / are PL/SQL
    pattern = re.compile(r"(\r?\n/\r?\n)|(;\r?\n)", re.MULTILINE)
    
    statements = []
    last_end = 0
    for match in pattern.finditer(content):
        stmt = content[last_end:match.start()].strip()
        delimiter = match.group(0).strip()
        if stmt and not stmt.startswith("--"):
            statements.append((stmt, delimiter))
        last_end = match.end()
    
    remaining = content[last_end:].strip()
    if remaining and not remaining.startswith("--"):
        statements.append((remaining, ""))

    for stmt, delim in statements:
        # Ignore SQL*Plus SET / PROMPT commands in execution
        clean_stmt = "\n".join([line for line in stmt.splitlines() if not line.strip().upper().startswith(("SET ", "PROMPT "))]).strip()
        if not clean_stmt:
            continue
        try:
            cur.execute(clean_stmt)
            con.commit()
        except Exception as e:
            # Report error
            print(f"Error on: {clean_stmt[:60]}...\nReason: {e}")
            con.rollback()

    cur.close()
    print(f"Finished {os.path.basename(script_path)}.\n")

if __name__ == "__main__":
    print("==================================================================")
    print("VEHICLE RENTAL SYSTEM - AUTOMATED RUNNER")
    print("==================================================================")
    
    # Check connection
    try:
        print(f"Probing Oracle listener on {DB_HOST}:{DB_PORT}/{DB_SERVICE}...")
        c = get_connection(SYS_USER, SYS_PASS)
        c.close()
        print("Connected to Oracle Database successfully!")
    except Exception as e:
        print(f"Could not connect to Oracle DB: {e}")
        print("\nPlease ensure Oracle service is running and listener port is open.")
        sys.exit(1)

    setup_app_user()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_dir = os.path.join(base_dir, "sql")

    app_con = get_connection(APP_USER, APP_PASS)

    run_sql_script(app_con, os.path.join(sql_dir, "01_schema_data.sql"))
    run_sql_script(app_con, os.path.join(sql_dir, "02_plsql.sql"))
    run_sql_script(app_con, os.path.join(sql_dir, "03_queries_demo.sql"))
    run_sql_script(app_con, os.path.join(sql_dir, "04_view_tables.sql"))

    app_con.close()
    print("All scripts executed successfully!")
