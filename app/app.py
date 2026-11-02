"""
=====================================================================
VEHICLE RENTAL MANAGEMENT SYSTEM - FLASK WEB APPLICATION
Database: Oracle (SQL & PL/SQL)
Python Driver: python-oracledb (Thin Mode, No Instant Client Required)
=====================================================================
"""

import functools
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import oracledb

# =====================================================================
# CONFIGURATION BLOCK
# All database connection details and demo accounts are defined here.
# =====================================================================
DB_CONFIG = {
    "user": "rental",
    "password": "rental123",
    "host": "localhost",
    "port": 1521,
    "service_name": "FREEPDB1"   # Use FREEPDB1 for Oracle 23ai/26ai Free, or XEPDB1 for Oracle XE
}

DEMO_USERS = {
    "staff": {
        "password": "staff123",
        "role": "staff",
        "name": "Branch Staff"
    },
    "manager": {
        "password": "manager123",
        "role": "manager",
        "name": "Fleet Manager"
    }
}

app = Flask(__name__)
app.secret_key = "vehicle_rental_secret_key_production_grade"

WHITELISTED_TABLES = [
    "BRANCH", "CATEGORY", "CUSTOMER", "VEHICLE",
    "BOOKING", "PAYMENT", "MAINTENANCE", "BK_LOG"
]

TABLE_RELATIONSHIPS = {
    "BRANCH": [
        "1:N with VEHICLE (branch.bid -> vehicle.bid)"
    ],
    "CATEGORY": [
        "1:N with VEHICLE (category.cid -> vehicle.cid)"
    ],
    "CUSTOMER": [
        "1:N with BOOKING (customer.custid -> booking.custid)"
    ],
    "VEHICLE": [
        "N:1 with BRANCH (vehicle.bid -> branch.bid)",
        "N:1 with CATEGORY (vehicle.cid -> category.cid)",
        "1:N with BOOKING (vehicle.vid -> booking.vid)",
        "1:N with MAINTENANCE (vehicle.vid -> maintenance.vid)"
    ],
    "BOOKING": [
        "N:1 with CUSTOMER (booking.custid -> customer.custid)",
        "N:1 with VEHICLE (booking.vid -> vehicle.vid)",
        "1:N with PAYMENT (booking.bkid -> payment.bkid)",
        "1:N with BK_LOG (booking.bkid -> bk_log.bkid via trigger)"
    ],
    "PAYMENT": [
        "N:1 with BOOKING (payment.bkid -> booking.bkid)"
    ],
    "MAINTENANCE": [
        "N:1 with VEHICLE (maintenance.vid -> vehicle.vid)"
    ],
    "BK_LOG": [
        "Populated exclusively by trg_bk_au on booking(status)"
    ]
}


# =====================================================================
# DATABASE UTILITIES (Bind variables, DBMS_OUTPUT, Clean Error Messages)
# =====================================================================

def get_db_connection():
    """Establish connection to Oracle database using python-oracledb thin mode."""
    return oracledb.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        service_name=DB_CONFIG["service_name"]
    )


def clean_oracle_error(err_str):
    """Translate raw Oracle ORA- error codes into friendly user messages."""
    if "ORA-20001" in err_str:
        return "Vehicle is not available for the selected dates."
    elif "ORA-20002" in err_str:
        return "Vehicle is currently under maintenance service and cannot be booked."
    elif "ORA-20003" in err_str:
        return "Booking is not in ACTIVE state. Only active rentals can be returned."
    elif "ORA-20004" in err_str:
        return "Payment amount exceeds the pending booking balance."
    elif "ORA-20005" in err_str:
        return "Booking is not in BOOKED state. Only booked reservations can be handed over."
    elif "ORA-20006" in err_str:
        return "The requested booking record was not found."
    elif "ORA-00001" in err_str:
        return "Unique constraint violated: a record with these unique details already exists."
    elif "ORA-02292" in err_str:
        return "Cannot delete record: related child records exist in other tables."
    elif "ORA-01400" in err_str:
        return "A required field was left empty."
    elif "ORA-02290" in err_str:
        return "Check constraint violated. Please check input values."
    return f"Database error: {err_str}"


def read_dbms_output(cursor):
    """Retrieve all pending DBMS_OUTPUT lines from the Oracle session."""
    lines = []
    line_var = cursor.var(str)
    status_var = cursor.var(int)
    while True:
        cursor.callproc("dbms_output.get_line", (line_var, status_var))
        if status_var.getvalue() != 0:
            break
        val = line_var.getvalue()
        if val is not None:
            lines.append(val)
    return lines


def run_procedure(proc_name, params=None):
    """Call a PL/SQL stored procedure, commit on success, rollback on error, and capture DBMS_OUTPUT."""
    params = params or []
    con = None
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.callproc("dbms_output.enable")
        cur.callproc(proc_name, params)
        con.commit()
        output_lines = read_dbms_output(cur)
        cur.close()
        return True, output_lines, None
    except Exception as e:
        if con:
            con.rollback()
        return False, [], clean_oracle_error(str(e))
    finally:
        if con:
            con.close()


def query_all(sql, params=None):
    """Execute a query with bind variables and return all rows as dictionaries."""
    params = params or {}
    con = None
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute(sql, params)
        columns = [col[0].lower() for col in cur.description] if cur.description else []
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return rows
    finally:
        if con:
            con.close()


def query_one(sql, params=None):
    """Execute a query with bind variables and return a single row dictionary."""
    rows = query_all(sql, params)
    return rows[0] if rows else None


def execute_dml(sql, params=None):
    """Execute INSERT/UPDATE/DELETE DML with bind variables and commit."""
    params = params or {}
    con = None
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute(sql, params)
        con.commit()
        cur.close()
        return True, None
    except Exception as e:
        if con:
            con.rollback()
        return False, clean_oracle_error(str(e))
    finally:
        if con:
            con.close()


# =====================================================================
# TEMPLATE FORMATTING FILTERS
# =====================================================================

@app.template_filter("format_currency")
def format_currency_filter(val):
    """Format numeric values as Indian Currency: Rs. 12,500"""
    if val is None:
        return "Rs. 0"
    try:
        amount = float(val)
        is_negative = amount < 0
        amount = abs(amount)
        parts = f"{amount:.2f}".split(".")
        int_part = parts[0]
        dec_part = parts[1]

        if len(int_part) > 3:
            last3 = int_part[-3:]
            rest = int_part[:-3]
            formatted_rest = re.sub(r"(\d)(?=(\d{2})+$)", r"\1,", rest)
            formatted = f"{formatted_rest},{last3}"
        else:
            formatted = int_part

        if dec_part != "00":
            formatted += f".{dec_part}"

        return f"-Rs. {formatted}" if is_negative else f"Rs. {formatted}"
    except (ValueError, TypeError):
        return f"Rs. {val}"


@app.template_filter("format_date")
def format_date_filter(val):
    """Format dates into readable Indian standard style: 25 Oct 2026"""
    if val is None:
        return "-"
    if isinstance(val, (datetime, datetime.date)):
        return val.strftime("%d %b %Y")
    try:
        dt = datetime.strptime(str(val)[:10], "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except Exception:
        return str(val)


# =====================================================================
# AUTHENTICATION & ROLE-BASED ACCESS CONTROL
# =====================================================================

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            user_role = session.get("role")
            if user_role != required_role:
                flash("Not allowed for your role. Redirected to your authorized portal.", "error")
                return redirect(url_for("staff_dashboard" if user_role == "staff" else "manager_dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("staff_dashboard" if session.get("role") == "staff" else "manager_dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role_choice = request.form.get("role")
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user_info = DEMO_USERS.get(username)
        if user_info and user_info["password"] == password and user_info["role"] == role_choice:
            session["user"] = username
            session["role"] = user_info["role"]
            session["name"] = user_info["name"]
            flash(f"Welcome back, {user_info['name']}!", "success")
            return redirect(url_for("staff_dashboard" if role_choice == "staff" else "manager_dashboard"))
        else:
            flash("Invalid credentials or role mismatch. Please check demo accounts below.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("login"))


# =====================================================================
# STAFF PORTAL (/staff)
# =====================================================================

@app.route("/staff")
@role_required("staff")
def staff_dashboard():
    # Fetch KPI metrics
    counts = query_one("""
        SELECT 
            NVL(SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END), 0) AS cnt_available,
            NVL(SUM(CASE WHEN status = 'RENTED' THEN 1 ELSE 0 END), 0) AS cnt_rented,
            NVL(SUM(CASE WHEN status = 'SERVICE' THEN 1 ELSE 0 END), 0) AS cnt_service
        FROM vehicle
    """)

    waiting_handover = query_one("SELECT COUNT(*) AS cnt FROM booking WHERE status = 'BOOKED'")
    rented_vehicles = query_all("""
        SELECT b.bkid, c.name AS cust_name, v.model, v.reg_no, b.edt
        FROM booking b
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        WHERE b.status = 'ACTIVE'
        ORDER BY b.edt ASC
    """)

    # Pending collections using PL/SQL function f_bal
    dues_total = query_one("""
        SELECT NVL(SUM(f_bal(bkid)), 0) AS tot_due
        FROM booking
        WHERE status <> 'CANCELLED' AND f_bal(bkid) > 0
    """)

    latest_bookings = query_all("""
        SELECT b.bkid, c.name AS cust_name, v.model, b.sdt, b.edt, b.status, b.total, f_bal(b.bkid) AS bal
        FROM booking b
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        ORDER BY b.bkid DESC
        FETCH FIRST 5 ROWS ONLY
    """)

    return render_template(
        "staff_dashboard.html",
        counts=counts,
        waiting_count=waiting_handover["cnt"] if waiting_handover else 0,
        rented_vehicles=rented_vehicles,
        total_due=dues_total["tot_due"] if dues_total else 0,
        latest_bookings=latest_bookings
    )


@app.route("/staff/new-booking", methods=["GET", "POST"])
@role_required("staff")
def staff_new_booking():
    if request.method == "POST":
        try:
            custid = int(request.form.get("custid"))
            vid = int(request.form.get("vid"))
            sdt_str = request.form.get("sdt")
            edt_str = request.form.get("edt")

            sdt = datetime.strptime(sdt_str, "%Y-%m-%d").date()
            edt = datetime.strptime(edt_str, "%Y-%m-%d").date()

            if edt <= sdt:
                flash("End date must be strictly after start date.", "error")
                return redirect(url_for("staff_new_booking"))

            # Call PL/SQL procedure p_book(p_c, p_v, p_s, p_e)
            success, output_lines, err_msg = run_procedure("p_book", [custid, vid, sdt, edt])
            if success:
                msg = output_lines[0] if output_lines else "Booking created successfully."
                flash(f"Success: {msg}", "success")
                return redirect(url_for("staff_bookings"))
            else:
                flash(err_msg, "error")

        except Exception as e:
            flash(f"Invalid input: {str(e)}", "error")

    customers = query_all("SELECT custid, name, phone, city FROM customer ORDER BY name")
    vehicles = query_all("""
        SELECT v.vid, v.model, v.reg_no, g.cname, g.rate, b.city
        FROM vehicle v
        JOIN category g ON v.cid = g.cid
        JOIN branch b ON v.bid = b.bid
        WHERE v.status = 'AVAILABLE'
        ORDER BY v.model
    """)
    return render_template("staff_new_booking.html", customers=customers, vehicles=vehicles)


@app.route("/staff/bookings")
@role_required("staff")
def staff_bookings():
    tab = request.args.get("tab", "ALL").upper()
    search = request.args.get("q", "").strip()

    sql = """
        SELECT b.bkid, c.custid, c.name AS cust_name, c.phone AS cust_phone,
               v.vid, v.model, v.reg_no, g.cname AS category,
               b.sdt, b.edt, b.status, b.total, f_bal(b.bkid) AS bal
        FROM booking b
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        JOIN category g ON v.cid = g.cid
        WHERE 1=1
    """
    params = {}

    if tab in ["BOOKED", "ACTIVE", "RETURNED", "CANCELLED"]:
        sql += " AND b.status = :status_filter"
        params["status_filter"] = tab

    if search:
        sql += " AND (UPPER(c.name) LIKE :q OR UPPER(v.model) LIKE :q OR UPPER(v.reg_no) LIKE :q OR TO_CHAR(b.bkid) = :q_exact)"
        params["q"] = f"%{search.upper()}%"
        params["q_exact"] = search

    sql += " ORDER BY b.bkid DESC"
    bookings = query_all(sql, params)

    return render_template("staff_bookings.html", bookings=bookings, current_tab=tab, search_query=search)


@app.route("/staff/bookings/<int:bkid>/start", methods=["POST"])
@role_required("staff")
def staff_booking_start(bkid):
    # Call PL/SQL procedure p_start(p_b)
    success, output_lines, err_msg = run_procedure("p_start", [bkid])
    if success:
        msg = output_lines[0] if output_lines else f"Booking #{bkid} marked ACTIVE. Vehicle handed over."
        flash(f"Success: {msg}", "success")
    else:
        flash(err_msg, "error")
    return redirect(url_for("staff_bookings"))


@app.route("/staff/bookings/<int:bkid>/return", methods=["POST"])
@role_required("staff")
def staff_booking_return(bkid):
    # Call PL/SQL procedure p_return(p_b)
    success, output_lines, err_msg = run_procedure("p_return", [bkid])
    if success:
        msg = output_lines[0] if output_lines else f"Booking #{bkid} returned successfully."
        flash(f"Success: {msg}", "success")
    else:
        flash(err_msg, "error")
    return redirect(url_for("staff_bookings"))


@app.route("/staff/bookings/<int:bkid>/pay", methods=["POST"])
@role_required("staff")
def staff_booking_pay(bkid):
    try:
        amt = float(request.form.get("amt", 0))
        pmode = request.form.get("pmode", "UPI").upper()
        if amt <= 0:
            flash("Payment amount must be greater than zero.", "error")
            return redirect(url_for("staff_bookings"))

        # Call PL/SQL procedure p_pay(p_b, p_a, p_m)
        success, output_lines, err_msg = run_procedure("p_pay", [bkid, amt, pmode])
        if success:
            msg = output_lines[0] if output_lines else "Payment recorded successfully."
            flash(f"Success: {msg}", "success")
        else:
            flash(err_msg, "error")
    except Exception as e:
        flash(f"Payment error: {str(e)}", "error")
    return redirect(url_for("staff_bookings"))


@app.route("/staff/bookings/<int:bkid>/cancel", methods=["POST"])
@role_required("staff")
def staff_booking_cancel(bkid):
    # Check if booking is in BOOKED status
    bk = query_one("SELECT status FROM booking WHERE bkid = :bkid", {"bkid": bkid})
    if not bk:
        flash("Booking not found.", "error")
    elif bk["status"] != "BOOKED":
        flash("Only reservations in BOOKED status can be cancelled.", "error")
    else:
        success, err_msg = execute_dml("UPDATE booking SET status = 'CANCELLED' WHERE bkid = :bkid", {"bkid": bkid})
        if success:
            flash(f"Booking #{bkid} has been cancelled.", "success")
        else:
            flash(err_msg, "error")
    return redirect(url_for("staff_bookings"))


@app.route("/staff/customers", methods=["GET", "POST"])
@role_required("staff")
def staff_customers():
    if request.method == "POST":
        # Add customer (INSERT)
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip() or None
        lic_no = request.form.get("lic_no", "").strip()
        city = request.form.get("city", "Chennai").strip() or "Chennai"

        if not name or not phone or not lic_no:
            flash("Name, phone, and license number are mandatory.", "error")
        else:
            max_id = query_one("SELECT NVL(MAX(custid), 0) + 1 AS next_id FROM customer")["next_id"]
            success, err_msg = execute_dml("""
                INSERT INTO customer (custid, name, phone, email, lic_no, city)
                VALUES (:custid, :name, :phone, :email, :lic_no, :city)
            """, {
                "custid": max_id,
                "name": name,
                "phone": phone,
                "email": email,
                "lic_no": lic_no,
                "city": city
            })
            if success:
                flash(f"Customer '{name}' added successfully (ID: {max_id}).", "success")
            else:
                flash(err_msg, "error")
        return redirect(url_for("staff_customers"))

    customers = query_all("""
        SELECT c.custid, c.name, c.phone, c.email, c.lic_no, c.city,
               COUNT(b.bkid) AS total_bookings
        FROM customer c
        LEFT JOIN booking b ON c.custid = b.custid
        GROUP BY c.custid, c.name, c.phone, c.email, c.lic_no, c.city
        ORDER BY c.custid ASC
    """)
    return render_template("staff_customers.html", customers=customers)


@app.route("/staff/customers/<int:custid>/edit", methods=["POST"])
@role_required("staff")
def staff_customer_edit(custid):
    # Edit customer (UPDATE)
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip() or None
    lic_no = request.form.get("lic_no", "").strip()
    city = request.form.get("city", "").strip()

    success, err_msg = execute_dml("""
        UPDATE customer
        SET name = :name, phone = :phone, email = :email, lic_no = :lic_no, city = :city
        WHERE custid = :custid
    """, {
        "custid": custid,
        "name": name,
        "phone": phone,
        "email": email,
        "lic_no": lic_no,
        "city": city
    })
    if success:
        flash(f"Customer #{custid} details updated.", "success")
    else:
        flash(err_msg, "error")
    return redirect(url_for("staff_customers"))


@app.route("/staff/customers/<int:custid>/delete", methods=["POST"])
@role_required("staff")
def staff_customer_delete(custid):
    # Delete customer (DELETE) - triggers constraint check if bookings exist
    success, err_msg = execute_dml("DELETE FROM customer WHERE custid = :custid", {"custid": custid})
    if success:
        flash(f"Customer #{custid} deleted successfully.", "success")
    else:
        flash(err_msg, "error")
    return redirect(url_for("staff_customers"))


@app.route("/staff/vehicles")
@role_required("staff")
def staff_vehicles():
    status_filter = request.args.get("status", "").upper()
    category_filter = request.args.get("category", "")

    sql = """
        SELECT v.vid, v.reg_no, v.model, v.yr, v.status,
               g.cname AS category, g.rate,
               b.bname AS branch, b.city AS branch_city
        FROM vehicle v
        JOIN category g ON v.cid = g.cid
        JOIN branch b ON v.bid = b.bid
        WHERE 1=1
    """
    params = {}
    if status_filter in ["AVAILABLE", "RENTED", "SERVICE"]:
        sql += " AND v.status = :status"
        params["status"] = status_filter
    if category_filter:
        sql += " AND g.cname = :cat"
        params["cat"] = category_filter

    sql += " ORDER BY v.vid ASC"
    vehicles = query_all(sql, params)
    categories = query_all("SELECT DISTINCT cname FROM category ORDER BY cname")
    return render_template("staff_vehicles.html", vehicles=vehicles, categories=categories, current_status=status_filter, current_cat=category_filter)


@app.route("/staff/payments")
@role_required("staff")
def staff_payments():
    payments = query_all("""
        SELECT p.pid, p.bkid, p.amt, p.pdt, p.pmode,
               c.name AS cust_name, v.model AS vehicle_model
        FROM payment p
        JOIN booking b ON p.bkid = b.bkid
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        ORDER BY p.pid DESC
    """)
    return render_template("staff_payments.html", payments=payments)


# =====================================================================
# MANAGER PORTAL (/manager)
# =====================================================================

@app.route("/manager")
@role_required("manager")
def manager_dashboard():
    # Headline KPI Cards
    rev_row = query_one("SELECT NVL(SUM(amt), 0) AS total_revenue FROM payment")
    dues_row = query_one("SELECT NVL(SUM(f_bal(bkid)), 0) AS total_dues FROM booking WHERE status <> 'CANCELLED' AND f_bal(bkid) > 0")
    maint_row = query_one("SELECT NVL(SUM(cost), 0) AS total_maint FROM maintenance")
    rented_row = query_one("SELECT COUNT(*) AS rented_count FROM vehicle WHERE status = 'RENTED'")

    # Revenue by category (bar chart data)
    cat_revenue = query_all("""
        SELECT g.cname, COUNT(b.bkid) AS trips, NVL(SUM(b.total), 0) AS rev
        FROM category g
        JOIN vehicle v ON g.cid = v.cid
        LEFT JOIN booking b ON v.vid = b.vid AND b.status <> 'CANCELLED'
        GROUP BY g.cname
        ORDER BY rev DESC
    """)
    max_cat_rev = max([float(c["rev"]) for c in cat_revenue]) if cat_revenue else 1
    for c in cat_revenue:
        c["pct"] = round((float(c["rev"]) / max_cat_rev) * 100, 1) if max_cat_rev > 0 else 0

    # Payments by mode
    mode_payments = query_all("""
        SELECT pmode, COUNT(*) AS count, NVL(SUM(amt), 0) AS total
        FROM payment
        GROUP BY pmode
        ORDER BY total DESC
    """)
    max_mode_tot = max([float(m["total"]) for m in mode_payments]) if mode_payments else 1
    for m in mode_payments:
        m["pct"] = round((float(m["total"]) / max_mode_tot) * 100, 1) if max_mode_tot > 0 else 0

    # Fleet status breakdown
    fleet_summary = query_one("""
        SELECT 
            COUNT(*) AS total_vehicles,
            NVL(SUM(CASE WHEN status = 'AVAILABLE' THEN 1 ELSE 0 END), 0) AS available,
            NVL(SUM(CASE WHEN status = 'RENTED' THEN 1 ELSE 0 END), 0) AS rented,
            NVL(SUM(CASE WHEN status = 'SERVICE' THEN 1 ELSE 0 END), 0) AS service
        FROM vehicle
    """)

    return render_template(
        "manager_dashboard.html",
        revenue=rev_row["total_revenue"] if rev_row else 0,
        dues=dues_row["total_dues"] if dues_row else 0,
        maintenance=maint_row["total_maint"] if maint_row else 0,
        rented=rented_row["rented_count"] if rented_row else 0,
        cat_revenue=cat_revenue,
        mode_payments=mode_payments,
        fleet=fleet_summary
    )


@app.route("/manager/dues")
@role_required("manager")
def manager_dues():
    # Execute stored procedure p_dues and capture DBMS_OUTPUT
    success, output_lines, err_msg = run_procedure("p_dues")
    
    # Query outstanding balances using f_bal, largest first
    dues_list = query_all("""
        SELECT b.bkid, c.name AS cust_name, c.phone, v.model,
               b.sdt, b.edt, b.status, b.total, f_bal(b.bkid) AS bal
        FROM booking b
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        WHERE b.status <> 'CANCELLED' AND f_bal(b.bkid) > 0
        ORDER BY bal DESC
    """)
    total_due = sum([float(d["bal"]) for d in dues_list])

    return render_template(
        "manager_dues.html",
        dues=dues_list,
        total_due=total_due,
        cursor_output=output_lines,
        err_msg=err_msg
    )


@app.route("/manager/maintenance")
@role_required("manager")
def manager_maintenance():
    # Individual service records
    records = query_all("""
        SELECT m.mid, m.mdt, m.cost, m.descr,
               v.vid, v.model, v.reg_no, v.status
        FROM maintenance m
        JOIN vehicle v ON m.vid = v.vid
        ORDER BY m.mdt DESC
    """)

    # Cost aggregated per vehicle
    vehicle_summary = query_all("""
        SELECT v.vid, v.model, v.reg_no,
               COUNT(m.mid) AS service_count,
               NVL(SUM(m.cost), 0) AS total_cost
        FROM vehicle v
        LEFT JOIN maintenance m ON v.vid = m.vid
        GROUP BY v.vid, v.model, v.reg_no
        ORDER BY total_cost DESC
    """)
    total_cost = sum([float(s["total_cost"]) for s in vehicle_summary])

    return render_template("manager_maintenance.html", records=records, vehicle_summary=vehicle_summary, total_cost=total_cost)


@app.route("/manager/activity")
@role_required("manager")
def manager_activity():
    # Trigger audit log table bk_log, newest first
    logs = query_all("""
        SELECT l.lid, l.bkid, l.old_st, l.new_st, l.ldt,
               c.name AS cust_name, v.model AS vehicle_model
        FROM bk_log l
        LEFT JOIN booking b ON l.bkid = b.bkid
        LEFT JOIN customer c ON b.custid = c.custid
        LEFT JOIN vehicle v ON b.vid = v.vid
        ORDER BY l.lid DESC
    """)
    return render_template("manager_activity.html", logs=logs)


@app.route("/manager/vehicles")
@role_required("manager")
def manager_vehicles():
    vehicles = query_all("""
        SELECT v.vid, v.reg_no, v.model, v.yr, v.status,
               g.cname AS category, g.rate,
               b.bname AS branch, b.city AS branch_city
        FROM vehicle v
        JOIN category g ON v.cid = g.cid
        JOIN branch b ON v.bid = b.bid
        ORDER BY v.vid ASC
    """)
    return render_template("manager_vehicles.html", vehicles=vehicles)


@app.route("/manager/customers")
@role_required("manager")
def manager_customers():
    customers = query_all("""
        SELECT c.custid, c.name, c.phone, c.email, c.lic_no, c.city,
               COUNT(b.bkid) AS total_bookings,
               NVL(SUM(b.total), 0) AS total_spent
        FROM customer c
        LEFT JOIN booking b ON c.custid = b.custid AND b.status <> 'CANCELLED'
        GROUP BY c.custid, c.name, c.phone, c.email, c.lic_no, c.city
        ORDER BY c.custid ASC
    """)
    return render_template("manager_customers.html", customers=customers)


@app.route("/manager/bookings")
@role_required("manager")
def manager_bookings():
    bookings = query_all("""
        SELECT b.bkid, c.name AS cust_name, v.model,
               b.sdt, b.edt, b.status, b.total, f_bal(b.bkid) AS bal
        FROM booking b
        JOIN customer c ON b.custid = c.custid
        JOIN vehicle v ON b.vid = v.vid
        ORDER BY b.bkid DESC
    """)
    return render_template("manager_bookings.html", bookings=bookings)


# =====================================================================
# DATABASE TABLES SCHEMA BROWSER (/tables) - Available to Both Roles
# Strictly Read-Only, Data Dictionary Driven, Whitelisted
# =====================================================================

@app.route("/tables")
@login_required
def view_tables():
    selected_table = request.args.get("t", "BRANCH").upper()

    # Enforce strict whitelist
    if selected_table not in WHITELISTED_TABLES:
        abort(404)

    # 1. Fetch live row counts for all 8 tables
    table_counts = {}
    for tbl in WHITELISTED_TABLES:
        res = query_one(f"SELECT COUNT(*) AS cnt FROM {tbl}")
        table_counts[tbl] = res["cnt"] if res else 0

    # 2. Fetch column definitions from user_tab_columns
    columns = query_all("""
        SELECT column_name, data_type, data_length, data_precision, data_scale,
               nullable, data_default
        FROM user_tab_columns
        WHERE table_name = :tname
        ORDER BY column_id ASC
    """, {"tname": selected_table})

    # 3. Fetch constraint definitions from user_constraints & user_cons_columns
    constraints = query_all("""
        SELECT uc.constraint_name, uc.constraint_type, ucc.column_name, uc.search_condition
        FROM user_constraints uc
        JOIN user_cons_columns ucc ON uc.constraint_name = ucc.constraint_name
        WHERE uc.table_name = :tname
    """, {"tname": selected_table})

    # Map column constraint flags
    col_flags = {}
    for c in columns:
        col_name = c["column_name"].upper()
        col_flags[col_name] = {
            "pk": False,
            "fk": False,
            "uq": False,
            "nn": (c["nullable"] == "N")
        }

    for cons in constraints:
        cname = cons["column_name"].upper()
        ctype = cons["constraint_type"]
        if cname in col_flags:
            if ctype == "P":
                col_flags[cname]["pk"] = True
            elif ctype == "R":
                col_flags[cname]["fk"] = True
            elif ctype == "U":
                col_flags[cname]["uq"] = True

    # 4. Fetch all rows from selected table
    rows = query_all(f"SELECT * FROM {selected_table} ORDER BY 1 ASC")

    # 5. Get relationships metadata
    relationships = TABLE_RELATIONSHIPS.get(selected_table, [])

    return render_template(
        "tables.html",
        tables=WHITELISTED_TABLES,
        table_counts=table_counts,
        selected_table=selected_table,
        columns=columns,
        col_flags=col_flags,
        rows=rows,
        relationships=relationships
    )


# =====================================================================
# ERROR HANDLERS
# =====================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", code=404, message="The requested resource or database table does not exist."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500, message="An internal server error occurred."), 500


if __name__ == "__main__":
    import socket
    port = 5000
    # If port 5000 is occupied by another local service, automatically fall back to 5050
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 5000)) == 0:
            port = 5050
    print("==================================================================")
    print("Vehicle Rental Management System Web Application")
    print(f"Running on http://127.0.0.1:{port}")
    print("Demo Logins: staff / staff123  |  manager / manager123")
    print("==================================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
