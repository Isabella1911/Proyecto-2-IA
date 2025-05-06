import streamlit as st
import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Cargar claves desde .env
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

# Inicializar cliente Pinecone
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Título de la app
st.set_page_config(page_title="Asistente Técnico", layout="centered")
st.title("🤖 Asistente de Consulta Técnica")

# Input del usuario
pregunta = st.text_input("📥 Escribe tu pregunta:")

if pregunta:
    with st.spinner("Buscando respuesta..."):
        # Ejecutar búsqueda semántica
        try:
            results = index.search(
                namespace="",
                query={
                    "top_k": 5,
                    "inputs": {
                        "text": pregunta
                    }
                }
            )

            # Mostrar resultados
            st.subheader("📌 Resultados más relevantes:")
            for hit in results["result"]["hits"]:
                st.markdown(f"""
                **ID:** {hit['_id']}  
                **Score:** {round(hit['_score'], 4)}  
                **Texto:** {hit['fields']['chunk_text']}  
                **Categoría:** {hit['fields'].get('category', 'N/A')}  
                ---
                """)

        except Exception as e:
            st.error(f"❌ Error al buscar: {e}")
