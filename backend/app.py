from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuración de la conexión a PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'dbFinancialTracker')
DB_USER = os.getenv('DB_USER', 'testuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'testpassword')

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/submit', methods=['POST'])
def submit():

    fecha = request.form.get('date')
    categoria = request.form.get('options')
    precio = request.form.get('price')
    descripcion = request.form.get('description')

    if not fecha or not precio or not categoria:
        return jsonify({'error': 'Rellena los campos correctamente'}), 400

    try:
        conn = connect_db()
        cursor = conn.cursor()
        print(DB_NAME)
        cursor.execute("INSERT INTO gastos (fecha, precio, descripcion, categoria) VALUES (%s, %s, %s, %s)", (fecha, precio, None if descripcion == "" else descripcion, categoria))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Datos insertados correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/db', methods=['GET'])
def show_db():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Generar HTML para mostrar los datos
        html = "<h1>Entradas de la Base de Datos</h1><table border='1'><tr><th>ID</th><th>Fecha</th><th>Categoría</th><th>Precio</th><th>Descripción</th></tr>"
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
        html += "</table>"

        return html
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def show_stats():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(precio) FROM gastos;")
        totalPrecio = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Generar HTML para mostrar los datos
        html = "<h1>Estadísticas</h1>"
        html += f"<p>Total de gastos: {totalPrecio}</p>"
        return html
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
