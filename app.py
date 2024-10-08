import pyodbc
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos
def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ERICKPC;'
        'DATABASE=tarea1;'
        'UID=hola;'
        'PWD=123'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para ejecutar el procedimiento almacenado
@app.route('/insertar_empleado', methods=['POST'])
def insertar_empleado():
    nombre = request.json.get('nombre')
    salario = request.json.get('salario')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Declarar y ejecutar el procedimiento almacenado con OUTPUT
        cursor.execute("""
                DECLARE	@return_value int,
		            @OutResulTCode int

                EXEC	@return_value = [dbo].[InsertarEmpleado]
		            @Nombre = ?,
		            @Salario = ?,
		            @OutResulTCode = @OutResulTCode OUTPUT

                SELECT	@OutResulTCode as N'@OutResultCode'
                """, (nombre, salario))

        # Obtener el valor del código de resultado
        out_result_code = cursor.fetchone()[0]

        # Confirmar la transacción si todo es exitoso
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

    # Devolver el código de resultado como respuesta
    return jsonify({'OutResultCode': out_result_code})

# Ruta para obtener los empleados
@app.route('/listar_empleados', methods=['GET'])
def listar_empleados():
    conn = get_db_connection()
    cursor = conn.cursor()

    empleados = []
    out_result_code = 0

    try:
        cursor.execute("""
            DECLARE @OutResulTCode INT;
            EXEC [dbo].[ListarEmpleado] @OutResulTCode = @OutResulTCode OUTPUT;
            SELECT @OutResulTCode;
        """)

        # Obtener el valor del código de resultado
        out_result_code = cursor.fetchone()[0]

        # Obtener la lista de empleados
        cursor.nextset() #Obtener los resultados, no el código de resultado
        for row in cursor.fetchall():
            empleado = {
                'Id': row.Id,
                'Nombre': row.Nombre,
                'Salario': row.Salario
            }
            empleados.append(empleado)

        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({'OutResultCode': out_result_code, 'Empleados': empleados})



if __name__ == '__main__':
    app.run(debug=True)
