from flask import Flask, render_template, jsonify,request
from flask_cors import CORS  # Importar CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Configuración de la base de datos
config = {
    'user': 'reservas',
    'password': 'reservas111',
    'host': '10.9.120.5',
    'database': 'reservastheloft'
}

def obtener_paises():
    """Función para obtener la lista de países desde la base de datos"""
    try:
        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa")

        # Crear un cursor
        cursor = conn.cursor()

        # Ejecutar la consulta SELECT
        cursor.execute("SELECT * FROM Pais")

        # Obtener los resultados y los nombres de las columnas
        columnas = [column[0] for column in cursor.description]
        resultados = cursor.fetchall()

        # Convertir los resultados a diccionarios
        lista = [dict(zip(columnas, fila)) for fila in resultados]
        return lista

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        # Cerrar la conexión y el cursor
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/api/pais")
def api_pais():
    """Ruta que devuelve la lista de países en formato JSON"""
    paises = obtener_paises()
    if paises is None:
        return jsonify({"error": "No se pudieron obtener los países"}), 500
    return jsonify(paises)

@app.route('/pais')
def pais():
    paises = obtener_paises()  # Asegúrate de que la función 'obtener_paises' devuelve una lista válida de países
    return render_template('lista_paises.html', paises=paises)

if __name__ == '__main__':
    app.run(debug=True)




@app.route("/api/establecimientos")
def establecimientos():
    
    config = {
    'user': 'reservas',
    'password': 'reservas111',
    'host': '10.9.120.5',
    'database': 'reservastheloft'
}

    try:
         # Crea la conexión
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa")

        # Crea un cursor
        cursor = conn.cursor()

        # Consulta para obtener el establecimiento por ID
        query = "SELECT * FROM Establecimientos"
        cursor.execute(query)
        establecimiento = cursor.fetchall()

        cursor.close()

    except Error as e:
        return jsonify({"error": str(e)}), 500

    if establecimiento:
        return jsonify(establecimiento)
    else:
        return jsonify({"error": "Establecimiento no encontrado"}), 404


@app.route("/api/establecimientos/<int:id>", methods=['GET'])
def obtener_establecimiento(id):
    
        # Configuración de la base de datos
    config = {
    'user': 'reservas',
    'password': 'reservas111',
    'host': '10.9.120.5',
    'database': 'reservastheloft'
}
    try:
         # Crea la conexión
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa")

        # Crea un cursor
        cursor = conn.cursor()
            # Consulta para obtener el establecimiento por ID
        query = "SELECT * FROM establecimientos WHERE id = %s"
        cursor.execute(query, (id,))
        establecimiento = cursor.fetchone()

        cursor.close()

    except Error as e:
        return jsonify({"error": str(e)}), 500


    if establecimiento:
        return jsonify(establecimiento)
    else:
        return jsonify({"error": "Establecimiento no encontrado"}), 404


@app.route("/api/establecimientos/<int:id>", methods=['DELETE'])
def eliminar_establecimiento(id):
# Configuración de la base de datos
    config = {
    'user': 'reservas',
    'password': 'reservas111',
    'host': '10.9.120.5',
    'database': 'reservastheloft'
}


    try:
        # Crea la conexión
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa")

        # Crea un cursor
        cursor = conn.cursor()

        # Consulta para eliminar el establecimiento por ID
        query = "DELETE FROM Establecimientos WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()  # Confirma la transacción

        # Verifica si se eliminó algún registro
        if cursor.rowcount > 0:
            return jsonify({"message": "Establecimiento eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Establecimiento no encontrado"}), 404

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()  # Cierra la conexión


@app.route("/api/pais", methods=['POST'])
def insertar_pais():
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud
    nombre = data.get('Nombre')
# Configuración de la base de datos
    config = {
    'user': 'reservas',
    'password': 'reservas111',
    'host': '10.9.120.5',
    'database': 'reservastheloft'
}
    if not nombre:
        return jsonify({"error": "El nombre del país es requerido"}), 400


    try:
        # Crea la conexión
        conn = mysql.connector.connect(**config)
        print("Conexión exitosa")

        # Crea un cursor
        cursor = conn.cursor()

        # Consulta para insertar un nuevo país
        query = "INSERT INTO Pais (Nombre) VALUES (%s)"
        cursor.execute(query, (nombre,))
        conn.commit()  # Confirma la transacción

        return jsonify({"message": "País insertado exitosamente", "id": cursor.lastrowid}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()  # Cierra la conexión



