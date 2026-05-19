from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps

print("🔥 UPDATED CODE RUNNING")

app = Flask(__name__)
app.secret_key = "investpro_secret"

# 🔹 DB connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 📊 REPORT DATA FUNCTION
def get_report_data():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    try:
        cur.execute("SELECT COUNT(*) FROM stocks")
        total_stocks = cur.fetchone()[0]
    except:
        total_stocks = 0

    try:
        cur.execute("SELECT COUNT(*) FROM stocks WHERE status='profit'")
        profit = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM stocks WHERE status='loss'")
        loss = cur.fetchone()[0]
    except:
        profit = 0
        loss = 0

    conn.close()
    return total_users, total_stocks, profit, loss

# 🔐 LOGIN REQUIRED
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

# 🔐 ADMIN REQUIRED
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

# 🏠 HOME
@app.route("/")
def index():
    return render_template("index.html")

# 📝 SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        if cur.fetchone():
            conn.close()
            return render_template(
                "signup.html",
                error="Email already registered!",
                username=username,
                email=email
            )

        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username, email, password, "user")
        )
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")

# 🔑 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM users 
            WHERE (username=? OR email=?) AND password=?
        """, (username_or_email, username_or_email, password))

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin")

            return redirect("/stocks")

        return render_template("login.html", error="Invalid Username or Password")

    return render_template("login.html")

# 🔥 ADMIN DASHBOARD
@app.route("/admin")
@admin_required
def admin():
    return render_template("admin.html")

# 👤 USERS LIST
@app.route("/admin/users")
@admin_required
def manage_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, username, email, password, role FROM users WHERE role='user'")
    users = cur.fetchall()

    conn.close()
    return render_template("users.html", users=users)

# 📊 STOCK PAGE
@app.route("/stocks")
@login_required
def stocks():
    return render_template("select_stock.html")

# 🔥 📊 REPORT PAGE (FIXED + AI + ALERT)
@app.route("/report")
@login_required
def report():
    conn = get_db()
    cur = conn.cursor()

    # Counts
    cur.execute("SELECT COUNT(*) FROM stocks")
    total_stocks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM stocks WHERE status='profit'")
    profit = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM stocks WHERE status='loss'")
    loss = cur.fetchone()[0]

    # Stock list
    cur.execute("SELECT name, price, status FROM stocks")
    stocks = cur.fetchall()

    # 🤖 AI Prediction + 🔔 Alert
    updated_stocks = []

    for stock in stocks:
        price = stock["price"]
        status = stock["status"]

        # 🤖 Prediction
        if status == "profit" and price > 2000:
            prediction = "Strong Buy 📈"
        elif status == "profit":
            prediction = "Buy 👍"
        elif status == "loss" and price < 1000:
            prediction = "High Risk ⚠️"
        else:
            prediction = "Hold ⏳"

        # 🔔 Alert
        if price > 3000:
            alert = "🚀 High Price Alert"
        elif status == "loss" and price < 1000:
            alert = "⚠️ High Risk Stock"
        else:
            alert = "✅ Normal"

        updated_stocks.append({
            "name": stock["name"],
            "price": price,
            "status": status,
            "prediction": prediction,
            "alert": alert
        })

    conn.close()

    return render_template(
        "report.html",
        total_stocks=total_stocks,
        profit=profit,
        loss=loss,
        stocks=updated_stocks
    )

# ℹ️ OTHER PAGES
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/livechart")
@login_required
def livechart():
    return render_template("livechart.html")

@app.route("/risk")
@login_required
def risk():
    return render_template("risk.html")

@app.route("/prediction")
@login_required
def prediction():
    return render_template("prediction.html")

@app.route("/technical")
@login_required
def technical():
    return render_template("technical.html")

@app.route("/market")
@login_required
def market():
    return render_template("market.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)