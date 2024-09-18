from flask import Flask
from markupsafe import escape

from flask import render_template
from flask import request

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

    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args
    pusher_client = pusher.Pusher(
      app_id="1864239",
      key="bf61a78167d9920c3d07",
      secret="1251ee86c94608366b0a",
      cluster="us2",
      ssl=True
    )

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
    val = (args["txtusuario"], args["txtcontrasena"]))
    cursor.execute(sql, val)

    con.commit()
    con.close()
 
    pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", args)
    return args

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()

    con.close()

    return registros
