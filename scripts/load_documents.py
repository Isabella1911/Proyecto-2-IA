import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Cargar variables de entorno desde .env
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")
region = os.getenv("PINECONE_REGION")
cloud = os.getenv("PINECONE_CLOUD")
model = os.getenv("PINECONE_MODEL")

# Inicializar cliente de Pinecone
pc = Pinecone(api_key=api_key)

# Crear el índice si no existe
if not pc.has_index(index_name):
    print(f"Creando índice '{index_name}' con modelo '{model}'...")
    pc.create_index_for_model(
        name=index_name,
        cloud=cloud,
        region=region,
        embed={
            "model": model,
            "field_map": {"text": "chunk_text"}
        }
    )
    print("✅ Índice creado.")
else:
    print(f"🔍 El índice '{index_name}' ya existe.")

# Leer documentos desde archivo
with open("data/documentos.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Crear registros a insertar
records = [
    {
        "_id": f"rec{i+1}",
        "chunk_text": lines[i],
        "category": "general"
    }
    for i in range(len(lines))
]

# Subir registros al índice
index = pc.Index(index_name)
index.upsert(records=records)

print(f"📦 {len(records)} registros insertados correctamente en el índice '{index_name}'.")
print("✅ Proceso de carga de documentos completado.")
