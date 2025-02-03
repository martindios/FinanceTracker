from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuración de la conexión a PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'dbfinancialtracker')
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
    #number = request.form.get('number')
    #text = request.form.get('text')

    fecha = request.form.get('date')
    precio = request.form.get('price')
    descripcion = request.form.get('description')

    if not fecha or not precio or not descripcion:
        return jsonify({'error': 'Rellena los campos correctamente'}), 400

    try:
        conn = connect_db()
        cursor = conn.cursor()
        print(DB_NAME)
        cursor.execute("INSERT INTO gastos (fecha, precio, descripcion) VALUES (%s, %s, %s)", (fecha, precio, descripcion))
        #cursor.execute("INSERT INTO form_data (number, text) VALUES (%s, %s)", (number, text))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Datos insertados correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

