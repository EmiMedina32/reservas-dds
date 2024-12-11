from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # Importar CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

def obtener_datos(query, params=None):
    """Función para ejecutar una consulta SQL de forma segura"""
    config = {
        'user': 'reservas',
        'password': 'reservas111',
        'host': '10.9.120.5',
        'database': 'reservastheloft'
    }

    try:
        # Conectar a la base de datos MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)  # Usar dictionary=True para obtener resultados como diccionarios

        # Ejecutar la consulta con los parámetros
        cursor.execute(query, params)
        resultados = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        return resultados  # Retorna una lista de diccionarios

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
    paises = obtener_datos("SELECT * FROM Pais")
    if paises is None:
        return jsonify({"error": "No se pudieron obtener los países"}), 500
    return jsonify(paises)



@app.route('/localidad')
def localidad():
    """Ruta que muestra la lista de localidades"""
   
    localidades = obtener_datos("SELECT Localidad.id, Localidad.Nombre AS localidad_nombre FROM Localidad") 

    return render_template('lista_localidades.html', localidades=localidades)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/detalle_localidad/<int:id>')
def detalle_localidad(id):
    """Ruta que muestra los detalles de una localidad"""
    
    # Consulta SQL para obtener los detalles de la localidad
    query1= """SELECT Localidad.id, Localidad.Nombre AS localidad_nombre, 
               Provincia.Nombre AS provincia_nombre, Pais.Nombre AS pais_nombre 
            FROM Localidad 
            JOIN Provincia ON Localidad.provinciaID = Provincia.id 
            JOIN Pais ON Provincia.paisID = Pais.id
            WHERE Localidad.id = %s;"""
    localidad = obtener_datos(query1, (id,))[0] 
    query2 = """ SELECT Nombre, ID,LocalidadID FROM Establecimientos WHERE localidadID = %s;"""
    establecimientos = obtener_datos(query2, (id,)) 

    if localidad:
        # Si encontramos la localidad, renderizamos la plantilla con los detalles
        return render_template('detalle_localidad.html', localidad=localidad,establecimientos=establecimientos)  
    else:
        # Si no se encuentra la localidad, mostramos un mensaje de error
        return "Localidad no encontrada", 404



 #   
@app.route("/api/establecimientos")
def api_establecimientos():
    """Ruta que devuelve los establecimientos en formato JSON"""
    establecimientos = obtener_datos('SELECT Nombre FROM Establecimientos')  # Obtener establecimientos
    if establecimientos:
        return jsonify(establecimientos)  # Retorna los establecimientos como JSON
    else:
        #
        return jsonify({"error": "Establecimientos no encontrados"}), 404



@app.route('/establecimientos')
def mostrar_establecimientos():
    """Ruta que muestra los establecimientos en una plantilla HTML"""
    # Obtener establecimientos con su ID y Nombre
    establecimientos = obtener_datos(
        """SELECT Nombre, ID
           FROM Establecimientos e """)
    
    return render_template('establecimientos.html', establecimientos=establecimientos)



@app.route('/detalle_establecimiento/<int:id>')
def detalle_establecimiento(id):
    """Ruta que muestra los detalles de un establecimiento"""
    
    # Consulta SQL para obtener el teléfono y correo electrónico del establecimiento
    query = """SELECT e.Nombre, e.Telefono, e.Email, l.nombre AS nombre_localidad , l.id AS id_localidad FROM Establecimientos e            
                JOIN Localidad l ON e.LocalidadID = l.id 
                WHERE e.id = %s"""  # Asegúrate de que los campos estén bien escritos
    establecimiento = obtener_datos(query, (id,))  # Pasamos el id como parámetro

    if establecimiento:
        # Si encontramos el establecimiento, renderizamos la plantilla con los detalles
        return render_template('detalle_establecimiento.html', establecimiento=establecimiento[0])  
    else:
        # Si no se encuentra el establecimiento, mostramos un mensaje de error
        return "Establecimiento no encontrado", 404




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



