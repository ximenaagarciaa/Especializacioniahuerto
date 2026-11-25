from unittest.mock import patch, Mock
import pytest
from src.cliente import con_reintento,registrar_costo, COSTO_POR_1000_TOKENS,consultar_modelo , costo_total_sesion
from src.consumir_gemini import enviar_peticion

#@pytest.fixture(autouse=True)
# def reiniciar_costo_total():
#     costo_total_sesion = 0
#     yield

# ================= TESTS ENVIAR PETICIÓN =================

def test_enviar_peticion_credencial_invalida():
    respuesta_falsa = Mock(status_code=401)

    with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(ValueError):
            enviar_peticion("https://ejemplo.invalid",
                            {"pregunta": "test"}
                            )
            
def test_enviar_peticion_limite_de_uso():
     respuesta_falsa = Mock(status_code=429)

     with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
        with pytest.raises(TimeoutError):
             enviar_peticion("https://ejemplo.invalid",{"pregunta": "test"})
            
def test_enviar_peticion_exito():
     respuesta_falsa = Mock(status_code=200)
     respuesta_falsa.json.return_value = {"texto": "respuesta simulada"}

     with patch("src.consumir_gemini.requests.post", return_value=respuesta_falsa):
         resultado = enviar_peticion("https://ejemplo.invalid", {"pregunta": "test"})

     assert resultado == {"texto": "respuesta simulada"}
    
    
# # ================= TESTS CON REINTENTOS =================

def test_con_reintento_agota_intentos():
     def siempre_falla():
         raise TimeoutError("simulado")
    
     with patch("src.cliente.time.sleep"):
         with pytest.raises(TimeoutError):
           con_reintento(siempre_falla, intentos=3,espera_base=2,espera_maxima=30)
          
def test_con_reintento_no_reintenta_value_error():
    operacion = Mock(side_effect=ValueError("simulado"))
    
    with patch("src.cliente.time.sleep") as dormir:
        with pytest.raises(ValueError):
            con_reintento(operacion)
            
    operacion.assert_called_once()
    dormir.assert_not_called()


def test_reintento_exitoso():
    intentos = {"cantidad": 0}

    def funcion_simulada():
        intentos["cantidad"] += 1

        if intentos["cantidad"] == 1:
            raise TimeoutError("Error temporal")

        return "Respuesta correcta"

    with patch("cliente.time.sleep") as espera:
        resultado = con_reintento(
            funcion_simulada, intentos=3
        )

    assert resultado == "Respuesta correcta"
    assert intentos["cantidad"] == 2
    espera.assert_called_once()



def test_no_reintenta_error_permanente():
    funcion = Mock(side_effect=ValueError("API key inválida"))

    with patch("cliente.time.sleep") as espera:
        with pytest.raises(ValueError):
            con_reintento(funcion, intentos=3)

    assert funcion.call_count == 1
    espera.assert_not_called()


    
    
# ================= TESTS REGISTRAR COSTO =================

def test_registrar_costo_acumula():
    respuesta_falsa = {"usageMetadata": 
        {
        "totalTokenCount": 1000
        }
    }
    
    costo = registrar_costo(respuesta_falsa)
    
    assert costo == COSTO_POR_1000_TOKENS
    assert costo_total_sesion == COSTO_POR_1000_TOKENS
    



def test_calculo_costo():
    respuesta = {
        "usageMetadata": {"totalTokenCount": 1000}
    }

    costo = registrar_costo(respuesta)

    assert costo == pytest.approx(
        COSTO_POR_1000_TOKENS
    )


# ================= 4  TESTS CONSULTAR MODELO =================
#Gestiona los errores y devuelve la respuesta del modelo
def test_consultar_modelo_convierte_error():
    error_simulado = TimeoutError("simulado")
    
    with patch(
        "src.cliente.con_reintento",
        side_effect=error_simulado,
        ):
        with pytest.raises(RuntimeError):
            consultar_modelo("¿Cómo prevenir plagas en tomates?")

def test_consulta_credencial_invalida():
    with patch(
        "cliente.con_reintento",
        side_effect=ValueError("Credencial inválida")
    ):
        with pytest.raises(ValueError):
            consultar_modelo(
                "¿Cómo prevenir plagas en tomates?"
            )
