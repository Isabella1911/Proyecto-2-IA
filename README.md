# Proyecto-2-IA

# EJECUCIÓN
1. Clonar el repositorio: 
git clone https://github.com/Isabella1911/Proyecto-2-IA.git

2. Crear un entorno virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instalar dependencias:
pip install -r requirements.txt  
pip install pinecone langchain langchain_openai pypdf2 tqdm python-dotenv streamlit openai langchain-community

4. Para ejecutar el programa:
python load_documents.py
streamlit run app.py

# DESCRIPCIÓN DE CADA MÓDULO
El archivo app.py contiene la interfaz web desarrollada con Streamlit, permitiendo a los usuarios ingresar preguntas y visualizar respuestas basadas en búsquedas semánticas. 
El script load_documents es responsable de cargar los documentos técnicos desde un archivo de texto y subirlos al índice de Pinecone, creando el índice automáticamente si aún no existe. 
La lógica de consulta está en query_handler, donde se gestiona la conexión con Pinecone y se ejecutan las búsquedas. 
La carpeta data contiene los documentos fuente, mientras que la carpeta utils/ tiene las funciones auxiliares o procesamiento adicional. 
El archivo .env almacena las variables sensibles como las claves de API y la configuración del índice. 
El archivo requirements.txt lista las dependencias necesarias para la ejecución del proyecto.

# REFLEXIÓN
En este proyecto, tuvimos la oportunidad de integrar diversas tecnologías como Pinecone, Streamlit y modelos de lenguaje de OpenAI, lo cual nos permitió explorar de manera práctica cómo funcionan los sistemas de recuperación de información basada en lenguaje natural. En este proyecto logramios entender el flujo de trabajo entre la vectorización de textos, el almacenamiento semántico y la generación de respuestas contextualizadas. También me costo un poco la correcta configuración de Pinecone y el manejo de embeddings. 
