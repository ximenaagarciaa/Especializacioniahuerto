from dotenv import load_dotenv #importa variables de entorno
##Divide el corpus en fragmentos o chunks ajustados a un tamaño (chunk_size) y solapamiento (chunk_overlap), heredando y propagando automáticamente los metadatos del documento original a cada chunk
from langchain_text_splitters import RecursiveCharacterTextSplitter #función para dividir (chunking)
from langchain_google_genai import GoogleGenerativeAIEmbeddings #embedding de Gemini
from langchain_chroma import Chroma #Chroma = vector store
##DeterministicFakeEmbedding / Document): DeterministicFakeEmbedding genera vectores sintéticos deterministas basados en hash para validar la estructura del código sin consumir cuota de API
##; Document es la clase que encapsula el texto (page_content) y la fuente (metadata) de cada fragmento
from rag_index import cargar_vectorstore


from langchain_core.documents import Document

load_dotenv()
CARPETA_DB = "vectorstore_huerto"
#borra el vs
vs = cargar_vectorstore(CARPETA_DB)
#vs.delete_collection()

datos = vs.get()
 
print("IDs almacenados: ", datos["ids"])
    #print("Chunks almacenados: ", datos["documents"])
print("Chunks indexados: ", len(datos["ids"]))