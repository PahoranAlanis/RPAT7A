# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()

    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()

    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

# Código usado en las prácticas
def notificarActualizacionUsuario():
    pusher_client = pusher.Pusher(
        app_id="1864239",
        key="bf61a78167d9920c3d07",
        secret="1251ee86c94608366b0a",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosTemperaturaHumedad", "registroTemperaturaHumedad", args)

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios
    ORDER BY Id_Usuario DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()

    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    usuario = request.form["usuario"]
    contrasena     = request.form["contrasena"]
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE tst0_usuarios SET
        Nombre_Usuario = %s,
        Contrasena     = %s
        WHERE Id_Usuario = %s
        """
        val = (usuario, contrasena, id)
    else:
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena)
                        VALUES (%s,          %s)
        """
        val =                  (usuario, contrasena)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionUsuario()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    notificarActualizacionUsuario()

    return make_response(jsonify({}))
