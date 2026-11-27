from unittest.mock import MagicMock

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from src.enrutamiento import (
    construir_paso_clasificacion,
    construir_cadena_con_enrutamiento,
    construir_cadena_problema_segura,
    procesar_mensaje_seguro,
)

def test_cadena_problema_usa_fallback_ante_fallo_del_modelo():
    def fallar_a_proposito(x):
        raise ConnectionError("simulado")
    cadena_problema_falsa = RunnableLambda(fallar_a_proposito)
    cadena_problema_segura = construir_cadena_problema_segura(
        cadena_problema_falsa
    )

    resultado = cadena_problema_segura.invoke(
        {"mensaje": "Las hojas de mis tomates están amarillas"}
    )

    assert resultado == (
        "No fue posible analizar tu consulta sobre el huerto. Evita aplicar tratamientos sin identificar la causa. Intenta nuevamente más tarde."
    )

def test_procesar_mensaje_seguro_no_propaga_excepciones():
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "simulado"
    )

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
    )

    resultado = procesar_mensaje_seguro(
        cadena_falsa, "¿Cuándo debo regar mis tomates?"
    )

    assert "no pudimos procesar" in resultado.lower()

    clasificacion_falsa.assert_called_once()

def test_clasificacion_normaliza_antes_de_comparar():
    modelo_falso = MagicMock(return_value=AIMessage(content=" Problema \n"))
    resultado = construir_paso_clasificacion(
        RunnableLambda(lambda x: modelo_falso(x))
    ).invoke({"mensaje": "Mis tomates tienen pulgones"})
    assert resultado == "problema"


def test_enrutamiento_problema():
    clasificacion_falsa = MagicMock(return_value='problema')
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
        cadena_problema=RunnableLambda(lambda x: "respuesta problema"),
        cadena_registro=RunnableLambda(lambda x: "respuesta registro"),
        cadena_pregunta=RunnableLambda(lambda x: "respuesta pregunta"),
    )
    resultado = cadena.invoke({"mensaje": 'Mis tomates tienen pulgones'})
    assert resultado == "respuesta problema"

def test_enrutamiento_registro():
    clasificacion_falsa = MagicMock(return_value='registro')
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
        cadena_problema=RunnableLambda(lambda x: "respuesta problema"),
        cadena_registro=RunnableLambda(lambda x: "respuesta registro"),
        cadena_pregunta=RunnableLambda(lambda x: "respuesta pregunta"),
    )
    resultado = cadena.invoke({"mensaje": 'Hoy regué los pepinos'})
    assert resultado == "respuesta registro"

def test_enrutamiento_pregunta():
    clasificacion_falsa = MagicMock(return_value='pregunta')
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
        cadena_problema=RunnableLambda(lambda x: "respuesta problema"),
        cadena_registro=RunnableLambda(lambda x: "respuesta registro"),
        cadena_pregunta=RunnableLambda(lambda x: "respuesta pregunta"),
    )
    resultado = cadena.invoke({"mensaje": '¿Cuándo sembrar tomates?'})
    assert resultado == "respuesta pregunta"

def test_enrutamiento_desconocida():
    clasificacion_falsa = MagicMock(return_value='desconocida')
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
        cadena_problema=RunnableLambda(lambda x: "respuesta problema"),
        cadena_registro=RunnableLambda(lambda x: "respuesta registro"),
        cadena_pregunta=RunnableLambda(lambda x: "respuesta pregunta"),
    )
    resultado = cadena.invoke({"mensaje": 'Necesito ayuda'})
    assert resultado == "respuesta pregunta"

def test_enrutamiento_vacia():
    clasificacion_falsa = MagicMock(return_value='')
    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=RunnableLambda(lambda x: clasificacion_falsa(x)),
        cadena_problema=RunnableLambda(lambda x: "respuesta problema"),
        cadena_registro=RunnableLambda(lambda x: "respuesta registro"),
        cadena_pregunta=RunnableLambda(lambda x: "respuesta pregunta"),
    )
    resultado = cadena.invoke({"mensaje": ''})
    assert resultado == "respuesta pregunta"
