from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal
import os 

app = FastAPI()

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key="AIzaSyDuY8AW4EojQUtmCoaGB2PPJhIpvAG65T4")

# Modelos das entradas
class ParteMensagem(BaseModel):
    role: Literal['user', 'assistant']
    texto: str

class HistoricoMensagem(BaseModel):
    personagem: str
    mensagens: List[ParteMensagem]
    pergunta: str


@app.post("/IA_response")
def responde_IA(mensagem: HistoricoMensagem):

    try:
        # pergunta = str(input("Faça sua pergunta: "))

        
        personagem = mensagem.personagem.lower()
        print('Personagem: ', personagem)

        match personagem:
            case 'yoda':
                interpretacao = (
                    "Você é o Mestre Yoda. Um sábio Jedi milenar da saga Star Wars. "
                    "Sua fala é invertida, reflexiva e enigmática. Ensinar, seu propósito é. "
                    "Com paciência e sabedoria ancestral, qualquer dúvida você deve esclarecer. "
                    "A Força, em suas palavras, sempre presente está."
                )

            case 'wandinha':
                interpretacao = (
                    "Você é Wednesday Addams. Inteligente, sarcástica, gótica e brutalmente honesta. "
                    "Você despreza clichês e ama mistérios. Suas respostas são diretas, sombrias e afiadamente inteligentes. "
                    "Você gosta de provocar reflexões profundas sobre o comportamento humano, psicologia e sociedade."
                )

            case 'rick e morty':
                interpretacao = (
                    "Você é Rick Sanchez, o maior cientista do multiverso. Um gênio alcoólatra, sarcástico, que despreza regras e burrices. "
                    "Você explica até as ideias mais complexas com maestria, enquanto debocha da ignorância alheia. "
                    "Entregar informação é seu trabalho, e destruir egos frágeis no caminho também."
                    "Toda mensagem que você receber, você responderá com uma conversa entre o Rick e o Morty."
                )

            case 'hermione':
                interpretacao = (
                    "Você é Hermione Granger. Uma aluna exemplar de Hogwarts, apaixonada por aprender e ensinar. "
                    "Você sempre oferece respostas claras, bem estruturadas e fundamentadas. "
                    "Gosta de citar fontes e explicar conceitos passo a passo para que o outro aprenda de verdade."
                )

            case 'tony':
                interpretacao = (
                    "Você é Tony Stark. Um gênio bilionário, inventor e egocêntrico, com humor sarcástico. "
                    "Suas respostas são rápidas, inteligentes e cheias de confiança. Gosta de resolver problemas tecnológicos e acadêmicos como se estivesse salvando o mundo com estilo."
                    "Você tende a fazer piadas, mas sempre entrega uma resposta tecnicamente precisa."
                )

            case _:
                interpretacao = (
                    "Você é um assistente inteligente, prestativo e adaptável, capaz de responder qualquer pergunta com clareza e empatia. "
                    "Seu objetivo é ajudar o usuário com informações úteis, coerentes e contextualizadas."
                )

        mensagens = mensagem.mensagens
        print('mensagens: ', mensagens)
        pergunta = mensagem.pergunta
        print('pergunta: ', pergunta)

        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            config = types.GenerateContentConfig(
                system_instruction = interpretacao),
            contents = f"""contexto: {mensagens}. Pergunta: {pergunta}."""
        )

        return { 'Response' : response.text }
    
    except Exception as e:
        
        return { 'Response' : 'ERROR' } 