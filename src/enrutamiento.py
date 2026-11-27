from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #Modelo
from langchain_core.prompts import PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta y la transforma en solo textos
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones

import logging #Generar un archivo de log con los errores que se presenten

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", #2026-11-04 16:40 [WARNING] main: No se pudo ejecutar x
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log",
    filemode="a", #Agrega al final del archivo la nueva línea
    encoding="utf-8",
    force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(   
     "Clasifica el siguiente mensaje de un huertero "
    "en una sola palabra: pregunta, problema o registro. "
    "Responde solo con esa palabra.\n\n{mensaje}"
)

def construir_paso_clasificacion(modelo):
    return (
        plantilla_clasificacion
        | modelo
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

paso_clasificacion = construir_paso_clasificacion(modelo)

cadena_pregunta = (
    PromptTemplate.from_template(  "Responde esta pregunta sobre el manejo de un "
        "huerto urbano de la zona central de Chile "
        "con precisión:\n\n{mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_problema = (
    PromptTemplate.from_template(  "Analiza este problema del huerto, identifica "
        "sus posibles causas y recomienda medidas "
        "seguras:\n\n{mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_registro = (
    PromptTemplate.from_template(        "Identifica y resume las actividades realizadas "
        "por el huertero sin inventar información:"
        "\n\n{mensaje}")
    | modelo
    | StrOutputParser()
)

# Fallback específico de la ruta problema
# Se activa ante excepciones, no ante respuestas vacías por sí solas.
def fallback_con_log(x):
    logger.warning("Cadena problema falló. Error: %s", type(x.get("error")).__name__)
    return (
        "No fue posible analizar tu consulta sobre el huerto. "
        "Evita aplicar tratamientos sin identificar la causa. "
        "Intenta nuevamente más tarde."
    )

respuesta_generica = RunnableLambda(fallback_con_log)


def construir_cadena_problema_segura(cadena_problema):
    return cadena_problema.with_fallbacks(
        [respuesta_generica], exception_key="error"
    )

cadena_problema_segura = construir_cadena_problema_segura(cadena_problema)


# Bifurcación con componentes reemplazables para las pruebas
def construir_cadena_con_enrutamiento(
    paso_clasificacion,
    cadena_problema=cadena_problema_segura,
    cadena_registro=cadena_registro,
    cadena_pregunta=cadena_pregunta,
):
    bifurcacion = RunnableBranch(
        (lambda x: x["clasificacion"] == "problema", cadena_problema),
        (lambda x: x["clasificacion"] == "registro", cadena_registro),
        cadena_pregunta
    )
    return (
        RunnablePassthrough.assign(clasificacion=paso_clasificacion)
        | bifurcacion
    )

cadena_con_enrutamiento = construir_cadena_con_enrutamiento(paso_clasificacion)

# Se conserva el nombre de entrada, con protección específica y try/except general.
cadena_robusta = cadena_con_enrutamiento

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        logger.error("Error procesando mensaje: %s", type(error).__name__)
        return "No pudimos procesar tu mensaje en este momento. Intenta de nuevo más tarde"

if __name__ == "__main__": #Solamente ejecuta el siguiente bloque de código si la ejecución es directa del archivo. NO EJECUTES si es import
    mensaje = "Las hojas de mis tomates están amarillas."
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))
