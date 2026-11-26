# Límites de la métrica de evaluación

## Qué mide

Coincidencia de palabras entre una respuesta generada y una referencia corta escrita por mí, contando repeticiones (precisión, cobertura y F1). No se evalua su  significado, orden ni verdad de los datos.


## Modos de falla conocidos

- Penalización de respuestas extensas que contienen la información esperada.

Caso: 02 — ¿Cuándo es conveniente sembrar zapallo italiano en la zona central de Chile?

Referencia: "Entre septiembre y noviembre, cuando haya pasado el riesgo de heladas."

Respuesta: "En la zona central de Chile, el momento más conveniente para sembrar zapallo italiano [...] es durante la primavera, una vez que ya ha pasado el riesgo de heladas. [...] Entre septiembre y noviembre."

F1: 0.074074.

Hallazgo: La respuesta contiene los meses de siembra esperados y considera el riesgo de heladas. Sin embargo, incorpora información adicional sobre temperaturas, almácigos y condiciones de siembra. Aunque obtiene una cobertura de 90,91 %, su precisión es de apenas 3,86 %. La métrica penaliza la extensión de la respuesta sin distinguir si la información adicional es correcta, relevante o útil para el huertero.

-Incapacidad para reconocer equivalencias semánticas y variaciones gramaticales.

Caso: 11 — ¿Cómo diferenciar un daño por plagas de una deficiencia nutricional?

Referencia: "Las plagas causan daños localizados; las deficiencias provocan patrones de decoloración."

Respuesta: "[...] Deficiencia nutricional: Tiende a ser simétrica y sistemática. [...] Daño por plagas: Tiende a ser localizado, aleatorio y asimétrico. [...] El daño se manifiesta como decoloración (clorosis) [...]".

F1: 0.022099.

Hallazgo: La respuesta desarrolla los conceptos principales de la referencia utilizando expresiones y estructuras gramaticales diferentes, como "localizado" en lugar de "localizados". La métrica no reconoce estas equivalencias y asigna un puntaje muy bajo, a pesar de que la respuesta contiene la distinción principal esperada.

-Incapacidad para distinguir la ausencia de coincidencias de una respuesta incompleta.

Caso: 12 — ¿Qué debo hacer si encuentro hojas amarillas en una planta?

Referencia: "Revisar el riego, los nutrientes, el drenaje y posibles plagas."

Respuesta: "Encontrar hojas amarillas en".

F1: 0.000000.

Hallazgo: La respuesta recibida corresponde a una oración inconclusa y no entrega ninguna recomendación al usuario. El F1 igual a cero permite detectar la falta de coincidencias, pero no identifica que la respuesta está incompleta. La métrica tampoco permite determinar si el problema se originó en el modelo, en la configuración de generación o en el procesamiento de la respuesta.

-Incapacidad para identificar respuestas incompletas cuando existen coincidencias léxicas.

Caso: 19 — ¿Qué bancales tienen cultivos actualmente?

Referencia: "No hay registros disponibles que indiquen la fecha de siembra."

Respuesta: "Para poder decirte qué bancales tienen cultivos actualmente, necesito que me des más información. ¿A qué huerto, jardín".

F1: 0.071429.

Hallazgo: La respuesta termina de manera abrupta y no proporciona la información solicitada. Sin embargo, se encuentra entre los cinco casos con mayor F1 de la evaluación. Esto demuestra que una posición favorable dentro del conjunto de resultados no garantiza que la respuesta sea completa ni funcionalmente útil.

-Incapacidad para reconocer diferencias en rangos numéricos.

Caso: 03 — ¿Qué temperatura favorece la germinación del pepino?

Referencia: "Entre 25 y 30 °C."

Respuesta: "La temperatura ideal para favorecer la germinación de la semilla de pepino se encuentra entre los 20 °C y los 30 °C, siendo los 25 °C la temperatura óptima."

F1: 0.061728.

Hallazgo: La referencia establece un rango de 25 a 30 °C, mientras que la respuesta establece un rango de 20 a 30 °C e identifica los 25 °C como temperatura óptima. La cobertura alcanza el 100 %, porque todos los tokens de la referencia aparecen en la respuesta completa. Sin embargo, esto no garantiza que los valores numéricos representen el mismo rango. La métrica no identifica las relaciones entre los números ni el significado que estos tienen dentro de una recomendación agrícola. Se requiere validación técnica para determinar cuál de los rangos es más apropiado.

-Dependencia de la calidad y pertinencia de la respuesta de referencia.

Caso: 18 — ¿Qué plagas he registrado en mis cultivos?

Referencia: "No hay registros disponibles que indiquen la fecha de siembra."

Respuesta: "Para poder decirte qué plagas has registrado en tus cultivos, necesito que me compartas esa información, ya que soy una inteligencia artificial y no tengo acceso directo a tus registros personales ni a tus campos a menos que me los cuentes. [...]".

F1: 0.080000.

Hallazgo: La respuesta de referencia no corresponde a la consulta realizada, debido a que hace alusión a una fecha de siembra y no al historial de plagas. La métrica realiza correctamente el cálculo matemático, pero no detecta que la referencia es inadecuada. Por lo tanto, el resultado obtenido no constituye una evaluación confiable de la calidad de la respuesta.

-Incapacidad para evaluar la pertinencia de una respuesta respecto de la consulta.

Caso: 20 — ¿Qué cultivos he cosechado durante el último mes?

Referencia: "No hay registros disponibles que indiquen la fecha de siembra."

Respuesta: "Como soy una inteligencia artificial, no tengo acceso a tu información personal, tu jardín, tu huerto ni a las aplicaciones que utilices para llevar el registro de tus cosechas. [...]".

F1: 0.075000.

Hallazgo: La respuesta reconoce que no dispone de los antecedentes necesarios y evita inventar información sobre las cosechas. Sin embargo, la métrica no reconoce este comportamiento como una respuesta pertinente frente a la falta de información. Tampoco permite verificar si el modelo realmente consultó el historial del huerto o si dispone de mecanismos para recuperarlo.

-Incapacidad para evaluar la utilidad práctica de las recomendaciones.

Caso: 05 — ¿Cómo puedo determinar si mis tomates necesitan riego?

Referencia: "Comprueba si el suelo está seco bajo la superficie."

Respuesta: "...Introduce el dedo índice en la tierra cerca de la base de la planta, a una profundidad de unos 3 a 5 centímetros ... Si la tierra se siente seca y tibia a esa profundidad, es hora de regar."

F1: 0.023952.

Hallazgo: La respuesta proporciona un procedimiento concreto que permite al huertero evaluar la humedad del suelo y tomar una decisión sobre el riego. Sin embargo, obtiene uno de los cinco puntajes F1 más bajos. La métrica no considera la utilidad práctica, el nivel de detalle ni la capacidad de una respuesta para orientar la toma de decisiones del usuario.


## Muestra revisada

10 casos de 20 respuestas, revisados el 2026-11-26 con la rúbrica de tres preguntas (corrección factual, completitud, contradicción): los 5 con F1 más bajo, los 5 con F1 más alto y el caso 3 por contener cifras. Detalle en `revision_manual.json`. Limitación: con todos los F1 ≤ 0.10, "más alto" no significa "bueno", y 4 de los 11 casos están cortados y no se pudieron juzgar.

## Recomendación de uso

No usar el F1 actual como criterio de calidad con respuestas largas. Para comparar versiones del cliente (por ejemplo, antes y después de agregar RAG), fijar la misma instrucción de brevedad y comparar cobertura. Descartar o regenerar respuestas cortadas, y revisar siempre a mano cualquier respuesta con temperaturas, fechas de siembra, dosis o que dependa del historial del huerto.

