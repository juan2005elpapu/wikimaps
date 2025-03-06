import folium
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  

# Temporary storage for users (replace with a database in production)
users = {}

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("map"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if user exists and password is correct
        if username in users and users[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("map"))
        else:
            return "Invalid credentials. Try again."
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "Username already exists. Choose a different one."
        
        users[username] = {"email": email, "password": password}
        return redirect(url_for("login"))
    
    return render_template("signup.html")

@app.route("/map")
def map():
    if "username" not in session:
        return redirect(url_for("login"))
    
    # ✅ Generate Folium map
    m = folium.Map(location=[4.7110, -74.0721], zoom_start=12)
    map_html = m._repr_html_()  # Convert map to HTML
    
    return render_template("index.html", map_html=map_html)  # Pass map HTML

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

