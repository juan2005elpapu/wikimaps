import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 

import folium
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.randomizer import Randomizer
from dataStructures.madeHash import MadeHash  
from utils.comment import agregar_comentario, cola_comentarios
from utils.graph import Graph

app = Flask(__name__)
keyRandomizer = Randomizer() 
app.secret_key = keyRandomizer.generateCode()

userHash = MadeHash(initialCapacity=10)
graph = Graph()
vertex_counter = 0  # Contador global para IDs únicos

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
    
    # Agregar marcadores para cada vértice (MapNode) de la FIFO
    for vertex in graph.get_all_vertices():
        folium.Marker(
            [vertex.lat, vertex.lon],
            popup=f"Puntero {vertex.value}"
        ).add_to(m)
    
    # Agregar caminos (edges) desde la pila LIFO
    for edge in graph.get_all_edges():
        id1, id2, distance = edge
        v1 = graph.get_vertex_by_id(id1)
        v2 = graph.get_vertex_by_id(id2)
        if v1 and v2:
            folium.PolyLine(
                [(v1.lat, v1.lon), (v2.lat, v2.lon)],
                color="blue",
                weight=2.5,
                opacity=1,
                tooltip=f"Camino ({id1}, {id2}) - {distance:.2f} km"
            ).add_to(m)
    
    map_html = m._repr_html_() 
    return render_template("index.html", map_html=map_html, currentUser=currentUser)

@app.route("/add_pointer", methods=["POST"])
def add_pointer():
    global vertex_counter
    data = request.get_json()
    try:
        lat = float(data["lat"])
        lon = float(data["lon"])
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Datos inválidos."})
    
    vertex_counter += 1
    graph.add_vertex(vertex_counter, lat, lon)
    return jsonify({"status": "success", "message": "Puntero agregado correctamente."})

@app.route("/add_path", methods=["POST"])
def add_path():
    data = request.get_json()
    try:
        id1 = int(data["id1"])
        id2 = int(data["id2"])
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Datos inválidos."})
    
    success = graph.add_edge(id1, id2)
    if success:
        return jsonify({"status": "success", "message": "Camino agregado correctamente."})
    else:
        return jsonify({"status": "error", "message": "Error al agregar camino. Verifica los IDs."})

@app.route("/delete_path", methods=["POST"])
def delete_path():
    data = request.get_json()
    try:
        id1 = int(data["id1"])
        id2 = int(data["id2"])
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Datos inválidos."})
    
    success = graph.delete_edge(id1, id2)
    if success:
        return jsonify({"status": "success", "message": "Camino borrado correctamente."})
    else:
        return jsonify({"status": "error", "message": "El camino no existe."})

@app.route("/delete_pointer", methods=["POST"])
def delete_pointer():
    data = request.get_json()
    try:
        id = int(data["id"])
    except (KeyError, ValueError):
        return jsonify({"status": "error", "message": "Datos inválidos."})
    
    success = graph.delete_vertex(id)
    if success:
        return jsonify({"status": "success", "message": "Puntero borrado correctamente."})
    else:
        return jsonify({"status": "error", "message": "El puntero no existe."})

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/error")
def error():
    return render_template("error.html") 

# Nuevo endpoint para agregar comentarios
@app.route("/comments", methods=["GET", "POST"])
def comments():
    if "username" not in session:
        return redirect(url_for("login"))
    currentUser = get_current_user()
    
    if request.method == "POST":
        lugar = request.form.get("lugar", "default").strip() or "default"
        comentario = request.form.get("comentario")
        if comentario:
            agregar_comentario(lugar, comentario)
        return redirect(url_for("comments"))
    
    def render_node(node, is_root=False):
        # Obtener el nodo real si está encapsulado
        tree_node = node.value if hasattr(node, 'value') else node
        
        # Determinar el valor a mostrar
        if hasattr(tree_node, 'value'):
            valor = tree_node.value
        else:
            valor = "Sin valor"
        
        # Si es un nodo raíz (lugar), mostrarlo diferente
        if is_root:
            html = f"<li><strong>Lugar: {valor}</strong><ul>"
            # Procesar hijos (comentarios)
            if hasattr(tree_node, 'hijo') and tree_node.hijo:
                current_child = tree_node.hijo
                while current_child:
                    # Obtener el usuario del comentario
                    usuario = current_child.usuario if hasattr(current_child, 'usuario') and current_child.usuario else "Anónimo"
                    # Obtener el valor del comentario
                    comment_value = current_child.value if hasattr(current_child, 'value') else "Sin comentario"
                    html += f"<li><em>{usuario}</em>: {comment_value}</li>"
                    # Pasar al siguiente hermano (siguiente comentario)
                    current_child = current_child.hermano
            html += "</ul></li>"
        else:
            # Si no es raíz, debería ser un comentario directo (caso que no deberíamos alcanzar con la implementación actual)
            usuario = tree_node.usuario if hasattr(tree_node, 'usuario') and tree_node.usuario else "Anónimo"
            html = f"<li><em>{usuario}</em>: {valor}</li>"
        
        return html
    
    comments_html = "<ul class='list-group'>"
    current = cola_comentarios.head
    while current:
        comments_html += render_node(current, is_root=True)
        current = current.next
    comments_html += "</ul>"
    
    return render_template("comments.html", currentUser=currentUser, comments_html=comments_html)


if __name__ == "__main__":
    app.run(debug=True)