from flask import Flask, request, jsonify
from gpt4all import GPT4All
import re
import time
import json

app = Flask(__name__)

model = GPT4All(r"C:\Users\crist\OneDrive\Desktop\proyecto\Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# Define aquí tu esquema de base de datos (tablas y columnas)
db_schema = {
    "empleados": {
        "id": "NUMBER",
        "nombre": "VARCHAR2(100)",
        "puesto": "VARCHAR2(100)",
        "salario": "NUMBER"
    },
    # agrega más tablas según necesites
}

@app.route('/generar_sql', methods=['POST'])
def generar_sql():
    data = request.get_json()
    pregunta = data.get("pregunta", "")
    if not pregunta:
        return jsonify({"error": "No se recibió una pregunta"}), 400

    # Convierte el esquema a JSON con indentación para legibilidad en prompt
    schema_json = json.dumps(db_schema, indent=2)

    prompt_sql = f"""
Eres un experto en SQL con el siguiente esquema de base de datos:

{schema_json}

Solo escribe la consulta SQL que responde esta pregunta, nada más, sin explicaciones:

Pregunta: {pregunta}
Consulta SQL:
"""
    start = time.time()
    output = model.generate(prompt_sql, max_tokens=50)
    end = time.time()

    match = re.search(r"(?i)(SELECT .*?;)", output, re.DOTALL)
    consulta = match.group(1) if match else "-- NO SQL FOUND --"

    return jsonify({
        "sql": consulta,
        "tiempo": round(end - start, 2),
        "raw": output
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
