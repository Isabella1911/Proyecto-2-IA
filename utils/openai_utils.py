from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIResponseGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.prompt_template = """Eres un asistente técnico experto. Tu tarea es proporcionar respuestas completas, precisas y detalladas a preguntas técnicas.
        
        Utiliza la siguiente información como contexto para responder a la pregunta del usuario.
        Si la información proporcionada no es suficiente para dar una respuesta completa, indica qué parte no puedes responder con certeza, pero proporciona la mejor respuesta posible con lo que sabes.
        
        No copies textualmente el contexto - sintetiza y explica con tus propias palabras de manera didáctica y profesional.
        Estructurará tu respuesta con títulos y subtítulos cuando sea apropiado.
        
        Contexto:
        {context}
        
        Pregunta del usuario: {question}
        
        Tu respuesta completa y detallada:"""
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
    
    def generate_response(self, question, context_texts):
        context = "\n\n".join(context_texts)
        
        chain = self.prompt | self.llm
        
        result = chain.invoke({
            "context": context,
            "question": question
        })
        
        # Resultado: un objeto
        return result.content