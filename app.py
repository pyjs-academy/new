from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Используй более безопасный ключ в реальных приложениях

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database.get_user(username):
            error_message = "Username already exists"
        else:
            hashed_password = generate_password_hash(password)
            database.add_user(username, hashed_password)
            return redirect(url_for("login"))
    return render_template("register.html", error_message=error_message)


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = database.get_user(username)
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
        error_message = "Invalid username or password"
    return render_template("login.html", error_message=error_message)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
