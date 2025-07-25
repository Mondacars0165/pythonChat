from flask import Flask, request, jsonify
from gpt4all import GPT4All
import re
import time
import json

app = Flask(__name__)

# Carga tu modelo local (ajusta la ruta si es necesario)
model = GPT4All(r"C:\Users\crist\OneDrive\Desktop\proyecto\gemma-2b-it-Q4_0.gguf")

# Esquema de base de datos con descripción semántica
db_schema_descripciones = {
    "empleados": {
        "id": "Identificador único del empleado",
        "nombre": "Nombre completo del empleado",
        "puesto": "Cargo o rol del empleado, como desarrollador o analista",
        "salario": "Remuneración mensual del empleado en pesos chilenos. También se puede llamar sueldo"
    }
}

@app.route('/generar_sql', methods=['POST'])
def generar_sql():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    if not pregunta:
        return jsonify({"error": "No se recibió una pregunta"}), 400

    schema_json = json.dumps(db_schema_descripciones, indent=2, ensure_ascii=False)

    prompt_sql = f"""
Eres un experto en SQL con acceso al siguiente esquema de base de datos, junto con la descripción de cada campo:

{schema_json}

Responde SOLO con la consulta SQL en formato Oracle (sin explicaciones, sin encabezado, sin comentarios):

Pregunta: {pregunta}
Consulta SQL:
"""

    start = time.time()
    output = model.generate(prompt_sql, max_tokens=100, temp=0.2)
    end = time.time()

    match = re.search(r"(?i)(SELECT[\s\S]*?)(;|\n|$)", output)
    consulta = match.group(1).strip() if match else "-- NO SQL FOUND --"

    return jsonify({
        "sql": consulta,
        "tiempo": round(end - start, 2),
        "raw": output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
