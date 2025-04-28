from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner
import os
from dotenv import load_dotenv

# Load environment variables locally (optional)
load_dotenv()

app = FastAPI()

# 🚨 Añadir Middleware CORS aquí
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a tu dominio después
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Comprobar que la API Key esté disponible
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set.")

# Definir el agente
agent = Agent(
    name="Guía de Arazá",
    instructions="""
Eres un experto en guayaba arazá. Tu rol es doble:
- Como vendedor: Convences a los clientes de las maravillas del arazá, destacando sus beneficios, usos, frescura y sabor.
- Como chef: Ofreces recetas simples, deliciosas y creativas donde el arazá es el protagonista.
Hablas de forma entusiasta, amigable, y siempre invitas a probar el arazá.
Responde siempre de manera clara, cálida y motivadora.
""",
    model="gpt-4o"
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    if not user_message:
        return {"reply": "Por favor, envíame un mensaje."}

    result = await Runner.run(agent, user_message)
    return {"reply": result.final_output}
