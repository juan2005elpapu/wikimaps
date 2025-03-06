import folium
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sys

# Añadir ruta para importar módulos desde database
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'database'))
from auth import UserAuth

app = Flask(__name__)
app.secret_key = os.urandom(24)  

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
        
        # Verificar credenciales con la base de datos
        success, message = UserAuth.login(username, password)
        
        if success:
            session["username"] = username
            return redirect(url_for("map"))
        else:
            return render_template("login.html", error=message)
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # Registrar usuario en la base de datos
        success, message = UserAuth.register(username, password, email)
        
        if success:
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error=message)
    
    return render_template("signup.html")

@app.route("/map")
def map():
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Generate Folium map
    m = folium.Map(location=[4.7110, -74.0721], zoom_start=12)
    map_html = m._repr_html_()
    
    return render_template("index.html", map_html=map_html)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

