from gpt4all import GPT4All
import sys

model = GPT4All("llama-3-8b-instruct.Q4_0.gguf")  # Ajusta al modelo descargado

prompt = sys.argv[1]
output = model.generate(prompt, max_tokens=300)

# Extraer solo la consulta SQL
import re
match = re.search(r"(?i)(SELECT .*?;)", output, re.DOTALL)
if match:
    print(match.group(1))
else:
    print("-- NO SQL FOUND --")
