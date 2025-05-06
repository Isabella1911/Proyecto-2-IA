import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Cargar variables de entorno
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

# Inicializar cliente de Pinecone
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Pregunta del usuario (puedes modificarla o pedirla con input())
query = "¿Cuál es el invento más importante de la historia?"

# Realizar búsqueda semántica
results = index.search(
    namespace="",  # puedes usar namespace si defines uno, si no déjalo vacío
    query={
        "top_k": 5,
        "inputs": {
            "text": query
        }
    }
)

# Mostrar resultados
print(f"🔍 Resultados para: {query}")
print("-" * 80)

for hit in results["result"]["hits"]:
    print(f"🆔 ID: {hit['_id']}")
    print(f"🔢 Score: {round(hit['_score'], 4)}")
    print(f"📄 Texto: {hit['fields']['chunk_text']}")
    print(f"🏷️ Categoría: {hit['fields'].get('category', 'N/A')}")
    print("-" * 80)
