from collections import Counter
from pipeline_limpieza import procesar_texto
from cliente import consultar_modelo
import json
from pathlib import Path


def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):
    tokens_referencia = procesar_texto(texto_referencia)
    tokens_respuesta = procesar_texto(texto_respuesta)
    
    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )
def resumir_metricas(resultados):

    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }

    n = len(resultados)

    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,

        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,

        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }

casos = [
    (
        "¿Qué condiciones necesita el tomate para desarrollarse adecuadamente?", 
        "Sol directo, temperaturas cálidas, suelo fértil, buen drenaje y riego regular.",
    ),
    (
        "¿Cuándo es conveniente sembrar zapallo italiano en la zona central de Chile?",
        "Entre septiembre y noviembre, cuando haya pasado el riesgo de heladas.",
    ),
    (
        "¿Qué temperatura favorece la germinación del pepino?",
        "Entre 25 y 30 °C.",
    ),
    (
        "¿Qué condiciones requiere la lechuga durante su crecimiento?",
        "Temperaturas frescas, suelo fértil, humedad constante y buena iluminación.",
    ),
    (
        "¿Cómo puedo determinar si mis tomates necesitan riego?",
        "Comprueba si el suelo está seco bajo la superficie.",
    ),
    (
        "¿Qué problemas puede provocar el exceso de riego en un bancal?",
        "Asfixia radicular, pudrición de raíces, enfermedades fúngicas y pérdida de nutrientes.",
    ),
    (
        "¿Cómo debería ajustar el riego después de una lluvia?",
        "Suspender el riego hasta que disminuya la humedad del suelo.",
    ),
    (
        "¿Qué señales indican falta de agua en una planta de pepino?",
        "Hojas marchitas, suelo seco, crecimiento lento y frutos deformados.",
    ),
    (
        "¿Cómo identificar una infestación de pulgones?",
        "Colonias de pulgones, hojas deformadas y melaza pegajosa.",
    ),
    (
        "¿Qué medidas iniciales puedo tomar si encuentro pulgones en tomates?",
        "Eliminar pulgones con agua y aplicar jabón potásico si persisten.",
    ),
    (
        "¿Cómo diferenciar un daño por plagas de una deficiencia nutricional?",
        "Las plagas causan daños localizados; las deficiencias provocan patrones de decoloración.",
    ),
    (
        "¿Qué debo hacer si encuentro hojas amarillas en una planta?",
        "Revisar el riego, los nutrientes, el drenaje y posibles plagas.",
    ),
    (
        "¿Cómo reconocer si el compost está maduro?",
        "Color oscuro, olor a tierra y textura homogénea.",
    ),
    (
        "¿Qué características debe tener el suelo para cultivar zanahorias?",
        "Suelo suelto, profundo, bien drenado y libre de piedras.",
    ),
    (
        "¿Qué consecuencias puede tener un exceso de fertilización?",
        "Quemaduras radiculares, salinización y desequilibrios nutricionales.",
    ),
    (
        "¿Cómo mejorar un suelo muy compactado?",
        "Airear e incorporar materia orgánica.",
    ),
    (
        "Según el historial, ¿cuándo sembré tomates?",
        "No hay registros disponibles que indiquen la fecha de siembra.",
    ),
    (
        "¿Qué plagas he registrado en mis cultivos?",
        "No hay registros disponibles que indiquen la fecha de siembra.",
    ),
    (
        "¿Qué bancales tienen cultivos actualmente?",
        "No hay registros disponibles que indiquen la fecha de siembra.",
    ),
    (
        "¿Qué cultivos he cosechado durante el último mes?",
        "No hay registros disponibles que indiquen la fecha de siembra.",
    ),
]

# for consulta, referencia in casos:

#     respuesta = consultar_modelo(consulta)

#     metricas = calcular_metricas(referencia, respuesta)

#     print(consulta, metricas)
import json


resultados = []

for consulta, referencia in casos:

    respuesta = consultar_modelo(consulta)

    metricas = calcular_metricas(referencia, respuesta)

    resultados.append({
        "consulta": consulta,
        "respuesta": respuesta,
        **metricas,
    })


with open(
    "resultados_metricas.json", "w", encoding="utf-8"
) as archivo:

    json.dump(resultados, archivo, indent=2, ensure_ascii=False)
####resumen de metricas##
print("resumen metricas")
print(resumir_metricas(resultados))


#######los peores resultados #########
print("peores casos")
peores_casos = sorted(resultados, key=lambda r: r["f1"])

muestra_para_revisar = peores_casos[:10] + peores_casos[-10:]


for caso in muestra_para_revisar:

    print(caso["consulta"], caso["f1"])

######guarda el resultado
# raiz = Path(__file__).resolve().parents[1]
# ruta_resultados = raiz / "resultados_metricas.json"

# # Recupera las respuestas guardadas en una ejecución anterior.
# if ruta_resultados.exists():
#     with ruta_resultados.open(
#         "r",
#         encoding="utf-8"
#     ) as archivo:
#         resultados = json.load(archivo)
# else:
#     resultados = []

# # Identifica los casos ya completados.
# completados = {
#     (caso["consulta"], caso["referencia"])
#     for caso in resultados
# }

# for numero, (consulta, referencia) in enumerate( casos,  start=1):
#     # Continúa sin repetir las consultas ya guardadas.
#     if (consulta, referencia) in completados:
#         print("Ya guardada:", consulta)
#         continue

#     try:
#         respuesta = consultar_modelo(
#             consulta,
#             system_instruction=(
#                 "Responde en español con una definición breve, "
#                 "en una sola oración de máximo 15 palabras. "
#                 "Sin listas, ejemplos ni introducciones."
#             )
#         )

#     except RuntimeError as error:
#         print("\nSe detuvo la generación:", error)
#         print(f"Respuestas guardadas: {len(resultados)}")
#         break

#     metricas = calcular_metricas(referencia, respuesta)

#     resultados.append({
#         "id": numero,
#         "consulta": consulta,
#         "referencia": referencia,
#         "respuesta": respuesta,
#         **metricas,
#     })

#     # Guarda inmediatamente después de cada respuesta.
#     with ruta_resultados.open(
#         "w",
#         encoding="utf-8"
#     ) as archivo:
#         json.dump(
#             resultados,
#             archivo,
#             indent=2,
#             ensure_ascii=False
#         )

#     completados.add((consulta, referencia))

    # print("\nConsulta:", consulta)
    # print("Respuesta:", respuesta)
    # print("Métricas:", metricas)
    # print(f"Guardadas: {len(resultados)}/{len(casos)}")

# def resumir_metricas(resultados):
#     if not resultados:
#         return {
#             "precision_promedio": 0,
#             "cobertura_promedio": 0,
#             "f1_promedio": 0,
#         }
#     n = len(resultados)
#     return {
#         "precision_promedio": sum(
#             r["precision"] for r in resultados
#         ) / n,
#         "cobertura_promedio": sum(
#             r["cobertura"] for r in resultados
#         ) / n,
#         "f1_promedio": sum(r["f1"] for r in resultados) / n,
#     }
    
# print("Promedios")
# print(resumir_metricas(resultados))
    
# peores_casos = sorted(resultados, key=lambda r: r["f1"])

# for caso in peores_casos[:3]:
#     print(caso["consulta"], caso["f1"])
###########################################################################################
# referencia = procesar_texto(
#     "¿Qué temperatura favorece la germinación del pepino?"
# )

# texto_respuesta = consultar_modelo("¿Qué temperatura favorece la germinación del pepino?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)
