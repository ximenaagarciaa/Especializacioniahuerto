from datetime import date
from rag_index import cargar_vectorstore


def precision_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float:
    """
    ids_recuperados los que me trajo el retriever
    De los 'k' chunks que me trajo el retriever, ¿qué fracción realmente sirve?
    Devuelve 0.0 si el retriever no devolvió ningún id
    """
    if not ids_recuperados:
        return 0.0
    
    #Recorro uno por uno cada ID que devolvió el retriever, si acaso existe en ids_relevantes lo agrego a la lista de acertados
    acertados = [i for i in ids_recuperados if i in ids_relevantes] 

    return len(acertados) / len(ids_recuperados)

def recall_at_k(ids_recuperados: list[str], ids_relevantes: set[str]) -> float | None:
    """
    Exhaustividad
    De todos los chunks relevantes que existen en mi corpus, ¿qué fracción logré rescatar?
    Devuelve None si la pregunta no tiene respuesta en corpus (ids_relevantes es vacío)
    """
    if not ids_relevantes:
        return None
    
    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados) / len(ids_relevantes)

def f1_score(precision: float, recall: float | None) -> float:
    """
    Media armónica entre precisión y exhaustividad: equilibrio entre ambos para comparar
    configuraciones distintas de k o chunk_size.
    """
    if recall is None or (precision + recall) == 0:
        return 0.0
    
    return 2 * precision * recall / (precision + recall)

def evaluar_recuperacion(retriever, casos: list[dict], k: int = 3):
    """
    Correr cada caso del conjunto de evaluaciones contra el retriever real de Chroma
    y va a calcular precisión, recall y F1
    """
    resultados = []

    for caso in casos:
        #1.- Consultamos al retriever, cuáles son los chunks que me regresa la invocación. SI GASTA TOKENS
        chunks = retriever.invoke(caso["pregunta"])

        #2.- Extraer los IDs
        ids_recuperados = [c.id for c in chunks]

        #3.- Calculamos las métricas
        p = precision_at_k(ids_recuperados, caso["ids_relevantes"])
        r = recall_at_k(ids_recuperados, caso["ids_relevantes"])
        f1 = f1_score(p, r)

        #4.- Agregar esas métricas a los resultados
        resultados.append({
            "pregunta": caso["pregunta"],
            "ids_recuperados": ids_recuperados,
            "precision": p,
            "recall": r,
            "f1": f1
        })
    
    return resultados

def guardar_reporte(ruta_archivo: str, resultados: list[dict], k: int, chunk_size: int = 200, chunk_overlap: int = 30):
    """Guarda el registro en un .txt para compararlo cuando cambies k o chunk_size."""
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(f"Fecha: {date.today()}\n")
        archivo.write(f"Configuracion: k={k}, chunk_size={chunk_size}, chunk_overlap={chunk_overlap}\n\n")

        for r in resultados:
            recall_txt = "n/a" if r["recall"] is None else f"{r['recall']:.2f}"
            archivo.write(f"P={r['precision']:.2f} | R={recall_txt} | F1={r['f1']:.2f} | {r['pregunta']}\n")
    print(f"\nReporte guardado en '{ruta_archivo}'")

if __name__ == "__main__":
    CARPETA_DB = "vectorstore_huerto"

    K = 3
    vs = cargar_vectorstore(CARPETA_DB)

   # pregunta = "Cuáles son los errores de credenciales inválidas?"
   # ids_relevantes = {"a4bc644f-ffa9-4219-94b2-5fd7cff518be", "5cf57a48-f1b4-4f6a-b8d3-b5e2760a9e37", "25a1d55b-6bed-4aa2-bc7c-db4e718964ca"}

    retriever = vs.as_retriever(search_kwargs={"k": K})
    #chunks = retriever.invoke(pregunta) #Consulta
    
    #print(chunks)
    #ids_recuperados = [c.id for c in chunks]

    #precision = precision_at_k(ids_recuperados, ids_relevantes)
    #print("Precision: ", precision)

    #exhaustividad = recall_at_k(ids_recuperados, ids_relevantes)
    #print("Exhaustividad: ", exhaustividad)

    #f1 = f1_score(precision, exhaustividad)
    
    #print("F1 Score: ", f1)

    casos_evaluacion = [
        # Caso 1: Preguntas sin respuesta en el corpus
        {
            "pregunta": "¿Como hacer siembra directa de tomates?",
            "ids_relevantes": {
                ""
            }
        },
        # Caso 2: Preguntas con más de un chunk relevante
        {
            "pregunta": "¿Variedades de zapallo italiano y sus colores?",
            "ids_relevantes": {
                "6864ed61-1353-4ff9-b9ed-96a6f02d4133", 
                "e967fb16-12b7-4ac5-bbdd-517dc6f37e4a",
                "af3b15a7-ef2c-4f1f-bf30-096ccd041569", 
            }
        },
        # Caso 3:  Respuesta partida entre dos chunks
        {
            "pregunta": "¿Como afectan los gusanos cortadores?",
            "ids_relevantes": {
                "86a9c7ec-b581-4f03-b347-5d9d83a7f0dd", 
                "6d9f4527-f415-465b-b4e2-d9346416ceef", 
           
            }
        },
        # Caso 4: Paráfrasis y vocabulario distinto
        {
            "pregunta": "¿Que tan cerca pueden estar plantados los zapallos?",
            "ids_relevantes": {
                "5e87bb19-4c73-4544-8c19-e36907cebeb1",
                "1df95be6-af01-4d28-8e0b-8f01ee19ae9c", 
            }
        },
         # Caso 5:  Preguntas con términos exactos
                {
                    "pregunta": "¿que es el zapallo italiano?",
               
                    "ids_relevantes": {
                        "a8838bd7-81a3-473e-8fe8-2c47e47cccd1" # 
                        
                    }
                },
        # Caso 6: Preguntas ambiguas o mal redactadas
                {
                            "pregunta": "¿Que distancia de surco?",
                            "ids_relevantes": {
                                "9d337ea9-eccd-407b-9f4c-b08b9ad1ecb9"
                               
                            }
                }
    ]

    resultados = evaluar_recuperacion(retriever, casos_evaluacion, 3)
    print(resultados)

    guardar_reporte("resultados_evaluacion_rag.txt", resultados, 3)

    """
    Precisión: Fórmula: Verdaderos Positivos / (Verdaderos Positivos + Falsos Positivos) 

    Exhaustividad (recall ) :
    Fórmula: Verdaderos Positivos / (Verdaderos Positivos + Falsos Negativos)
    """