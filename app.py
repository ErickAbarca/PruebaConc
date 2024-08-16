from flask import Flask,jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

def ejecutar_stored_procedure(nombre_sp, parametros=None):
    server = 'DESKTOP-HUTR52P'
    database = 'PruebaConcepto'
    username = 'hola'
    password = '12345678'
    conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    try:
        if parametros:
            cursor.execute(f"EXEC {nombre_sp} {parametros}")
        else:
            cursor.execute(f"EXEC {nombre_sp}")

        if cursor.description:
            columnas = [column[0] for column in cursor.description]
            resultados = cursor.fetchall()
            resultados_dict = [dict(zip(columnas, fila)) for fila in resultados]
            return resultados_dict
        else:
            return None
    finally:
        cursor.close()
        conn.close()
    
@app.route('/')
def home():
    return "Hola mundo"

if __name__ == '__main__':
    app.run(debug=True)