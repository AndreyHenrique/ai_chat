from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import os 

app = FastAPI()

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key="AIzaSyDuY8AW4EojQUtmCoaGB2PPJhIpvAG65T4")


# Modelos das entradas
class Mensagem(BaseModel):
    texto: str
    dificuldade: Literal['fácil', 'médio', 'difícil']

@app.post("/quiz_question")
def responde_IA(mensagem: Mensagem):
    try:
        conteudo = mensagem.texto
        dificuldade = mensagem.dificuldade.lower()

        instructions = (
        """Você é uma IA que gera questões de quiz. Sempre retorne sua resposta no seguinte formato JSON, e nada mais:"""

        """{"""
        """pergunta": "Texto da pergunta aqui","""
        """alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"],"""
        """correta": "Texto da alternativa correta"""
        """}"""

        """Não adicione explicações, títulos, comentários ou qualquer texto fora do JSON. Sem /n e nem nada do tip.o. Apenas o JSON puro.
        """
        f"""A pergunta deve ser de nível {dificuldade} de dificuldade. A alternativa correta deve estar entre as listadas."""

        )

        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            config = types.GenerateContentConfig( system_instruction = instructions),
            contents = conteudo
        )
        print(response.text)
        return { 'Response' : response.text }
    
    except Exception as e:
        
        return { 'Response' : 'ERROR' } 