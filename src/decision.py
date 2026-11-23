from dotenv import load_dotenv #importa variables de entorno


load_dotenv()
def recomendar_estrategia(respuestas):
    puntos = {"RAG": 0, "Fine-tuning completo": 0, "PEFT": 0}
    if respuestas["informacion_cambia_seguido"]:
        puntos["RAG"] += 3
    if respuestas["problema_de_formato_o_tono"]:
        puntos["PEFT"] += 2
        puntos["Fine-tuning completo"] += 1
    if respuestas["dataset_grande_y_de_calidad"]:
        puntos["Fine-tuning completo"] += 2
        puntos["PEFT"] += 1
    if respuestas["presupuesto_limitado_o_iterar_rapido"]:
        puntos["RAG"] += 2
        puntos["PEFT"] += 1
    if respuestas["necesita_multiples_variantes"]:
        puntos["PEFT"] += 2
 
    maximo = max(puntos.values())
    ganadoras = [tecnica for tecnica, p in puntos.items() if p == maximo]
    return puntos, ganadoras
 
if __name__ == "__main__":
# EJEMPLO comentado (no lo uses tal cual): asi luce el diccionario ya respondido
# para el clasificador de errores del cliente de las lecciones anteriores.
# Cada valor es True o False, y al lado queda anotada la evidencia que lo sustenta.
#
    respuestas = {
     "informacion_cambia_seguido": True,        	# Se actualiza por lo menos una vez al mes
     "problema_de_formato_o_tono": False,         	# 15 de 20  la respuesta  trae el JSON esperado
     "dataset_grande_y_de_calidad": False,        	# No requiere
     "presupuesto_limitado_o_iterar_rapido": True,  # No hay presupuesto y no hay urgencia
     "necesita_multiples_variantes": False,      	# No, solo un idioma
 }
 

    
    if any(valor is None for valor in respuestas.values()):
        raise SystemExit("Completa las cinco respuestas con True o False antes de continuar.")
 
puntos, ganadoras = recomendar_estrategia(respuestas)
print(puntos)
print("candidatas:", ganadoras)