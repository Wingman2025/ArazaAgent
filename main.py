from fastapi import FastAPI, Request
from agents import Agent, Runner
import os

# Asegúrate de tener la variable de entorno OPENAI_API_KEY configurada
# export OPENAI_API_KEY=tu_clave_api

app = FastAPI()

# Definir el agente con instrucciones específicas
agent = Agent(
    name="Guía de Arazá",
    instructions="""
Eres un experto en guayaba arazá. Tu rol es doble:
- Como vendedor: Convences a los clientes de las maravillas del arazá, destacando sus beneficios, usos, frescura y sabor.
- Como chef: Ofreces recetas simples, deliciosas y creativas donde el arazá es el protagonista.
Hablas de forma entusiasta, amigable, y siempre invitas a probar el arazá.
Responde siempre de manera clara, cálida y motivadora.
""",
    model="gpt-4o"  # Puedes cambiar a "gpt-3.5-turbo" si prefieres
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    if not user_message:
        return {"reply": "Por favor, envíame un mensaje."}

    # Ejecutar el agente de forma asíncrona
    result = await Runner.run(agent, user_message)
    return {"reply": result.final_output}
