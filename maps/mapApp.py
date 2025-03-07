import folium
from flask import Flask, render_template, request, redirect, url_for, session
from utils.randomizer import Randomizer
from dataStructures.madeHash import MadeHash  

app = Flask(__name__)
keyRandomizer = Randomizer() 
app.secret_key = keyRandomizer.generateCode()

userHash = MadeHash(initialCapacity=10)
def get_current_user():
    return session.get("username")

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("map"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if userHash.getTotalEntries() == 0:
        return redirect(url_for("signup"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        storedPassword = userHash.findValue(username)
        if storedPassword is not None and storedPassword == password:
            session["username"] = username
            return redirect(url_for("map"))
        else:
            return redirect(url_for("error"))
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if userHash.containsKey(username):
            return render_template("signup.html", error="El usuario ya existe. Escoge otro nombre.")
        userHash.insert(username, password)
        return redirect(url_for("login"))
    
    return render_template("signup.html")

@app.route("/map")
def map():
    if "username" not in session:
        return redirect(url_for("login"))
    currentUser = get_current_user()
    m = folium.Map(location=[4.7110, -74.0721], zoom_start=12)
    map_html = m._repr_html_() 
    return render_template("index.html", map_html=map_html, currentUser=currentUser)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/error")
def error():
    return render_template("error.html") 

if __name__ == "__main__":
    app.run(debug=True)