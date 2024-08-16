import pyodbc
from flask import Flask, request, jsonify

app = Flask(__name__)

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
        # Revertir la transacción en caso de error
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

    # Devolver el código de resultado como respuesta
    return jsonify({'OutResulTCode': out_result_code})


if __name__ == '__main__':
    app.run(debug=True)
