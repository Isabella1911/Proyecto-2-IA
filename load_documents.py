import os
import time
from dotenv import load_dotenv
from utils.embeddings import EmbeddingManager
import PyPDF2
from tqdm import tqdm

# Cargar variables de entorno
load_dotenv()


def load_text_file(file_path):
    """Cargar archivo de texto"""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_pdf_file(file_path):
    """Extraer texto de PDF"""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return [p for p in text.split("\n") if p.strip()]

def process_documents(file_path):
    """Procesar documentos segun su tipo"""
    if file_path.endswith(".txt"):
        return load_text_file(file_path)
    elif file_path.endswith(".pdf"):
        return load_pdf_file(file_path)
    else:
        raise ValueError("Formato de archivo no soportado")

def main():
    # Inicializar manager de embeddings
    emb_manager = EmbeddingManager()
    emb_manager.create_index_if_not_exists()
    index = emb_manager.get_index()
    
    # Procesar documentos
    documents_dir = "data"
    all_lines = []
    
    # Verificar si el directorio existe
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)
        print(f"Se creo el directorio '{documents_dir}' ya que no existia.")
    
    # Procesar todos los archivos en el directorio data
    files_processed = 0
    for filename in os.listdir(documents_dir):
        if filename.endswith((".txt", ".pdf")):
            file_path = os.path.join(documents_dir, filename)
            lines = process_documents(file_path)
            print(f"Procesando {file_path}: {len(lines)} lineas encontradas")
            all_lines.extend(lines)
            files_processed += 1
    
    # Tambien verificar el directorio de uploads de usuario
    user_uploads_dir = os.path.join(documents_dir, "user_uploads")
    if os.path.exists(user_uploads_dir):
        for filename in os.listdir(user_uploads_dir):
            if filename.endswith((".txt", ".pdf")):
                file_path = os.path.join(user_uploads_dir, filename)
                lines = process_documents(file_path)
                print(f"Procesando {file_path}: {len(lines)} lineas encontradas")
                all_lines.extend(lines)
                files_processed += 1
    
    print(f"Se procesaron {files_processed} archivos con un total de {len(all_lines)} lineas.")
    
    # Requisito de minimo 70 registros 
    if len(all_lines) < 70:
        raise ValueError("No se encontraron registros. Coloca archivos TXT o PDF en el directorio 'data'")
    
    # Crear registros con embeddings
    records = []
    for i, line in enumerate(tqdm(all_lines, desc="Procesando documentos")):
        embedding = emb_manager.get_embedding(line)
        
        record = {
            "id": f"rec_{i+1}",
            "values": embedding,
            "metadata": {
                "text": line,
                "category": "general",
                "source": "documentos_base"
            }
        }
        records.append(record)
    
    # Subir registros en lotes (Pinecone tiene limite de tamaño)
    batch_size = 100
    for i in tqdm(range(0, len(records), batch_size), desc="Subiendo a Pinecone"):
        batch = records[i:i + batch_size]
        index.upsert(vectors=batch)
    
    print(f"📦 {len(records)} registros insertados correctamente en el índice.")

if __name__ == "__main__":
    main()