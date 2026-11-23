Decisión de personalización: Huerto con IA
## 1. El problema
El proyecto Huerto con IA busca apoyar la gestión de un huerto familiar mediante un asistente de inteligencia artificial que entregue recomendaciones sobre qué sembrar, cómo sembrar, épocas de cultivo, asociaciones de plantas, prevención y tratamiento de plagas, cuidados y cosechas.
El sistema utilizará información técnica sobre horticultura y registros históricos proporcionados por el usuario, como cultivos anteriores, fechas de siembra, problemas detectados, tratamientos aplicados y resultados de las cosechas.
La principal necesidad es que el modelo pueda acceder a esta información específica y utilizarla para entregar respuestas contextualizadas, evitando depender exclusivamente de su conocimiento general.
La personalización se basa en el conocimiento documental y en la historia registrada del huerto.

## 2. Resultado del método de decisión


| Criterio | Respuesta | Fundamento |
|---|---|---|
| ¿La información cambia frecuentemente? | Sí | El historial se actualiza con nuevas siembras, plagas, tratamientos y cosechas. |
| ¿Existe un problema de formato o tono consistente? | No | La necesidad principal es acceder a información específica, no modificar el comportamiento del modelo. |
| ¿Existe un dataset grande y etiquetado? | No | Se dispone de información documental y registros del huerto, no de un conjunto de ejemplos preparados para entrenamiento. |
| ¿El presupuesto es limitado o se necesita iterar rápidamente? | Sí | No existe presupuesto para entrenamiento ni servicios de modelos de pago. |
| ¿Se necesitan múltiples variantes del modelo? | No | Se requiere un único asistente que pueda consultar información de distintos cultivos y del historial del huerto. |


Resultado del método de puntuación:
$ python src/decision.py
{'RAG': 5, 'Fine-tuning completo': 0, 'PEFT': 1}
candidatas: ['RAG']
Es decir
·	RAG: 5 puntos.
·	PEFT: 1 punto.
·	Fine-tuning completo: 0 puntos.
La estrategia mejor puntuada es RAG.

## 3.  Técnica elegida y por qué

Se selecciona RAG (Retrieval-Augmented Generation) como estrategia de personalización para Huerto con IA.
La decisión se fundamenta principalmente en que el proyecto necesita incorporar y consultar conocimiento externo que puede actualizarse continuamente, sin modificar ni reentrenar los parámetros del modelo de lenguaje.
RAG permite indexar documentación técnica sobre horticultura y recuperar fragmentos relevantes junto con los antecedentes históricos del huerto. Por ejemplo, ante una consulta sobre qué sembrar en un bancal, el asistente podría considerar los cultivos anteriores registrados y la información disponible sobre rotación y asociación de cultivos.
Esta estrategia presenta las siguientes ventajas:
·	Actualización del conocimiento: permite incorporar nuevos registros de siembras, plagas y cosechas mediante la actualización del índice, sin reentrenamiento.
·	Menor costo de personalización: no requiere entrenar modelos ni disponer de infraestructura especializada de entrenamiento.
·	Aprovechamiento de información existente: utiliza documentos técnicos y registros históricos sin necesidad de construir un dataset de entrenamiento etiquetado.
·	Trazabilidad: permite relacionar las recomendaciones con la documentación recuperada.
·	Iteración rápida: facilita corregir, ampliar y actualizar el conocimiento disponible.
Se descarta el fine-tuning, porque requiere un volumen importante de ejemplos etiquetados, recursos de entrenamiento y presupuesto que no están disponibles. Además, no responde directamente a la necesidad principal de consultar información histórica y documental.
PEFT, aunque reduce los recursos necesarios respecto del fine-tuning completo, también requiere preparar ejemplos de entrenamiento y realizar un proceso de ajuste del modelo. No se justifica para el problema actual, que está relacionado principalmente con el acceso al conocimiento y no con la modificación del comportamiento.
El soft-prompting tampoco se considera necesario, ya que el proyecto no requiere entrenar representaciones del prompt para modificar el comportamiento del modelo.


## 4. Qué necesitaría para ejecutarla


Para implementar la estrategia RAG se requiere construir y mantener un corpus documental que combine información técnica de horticultura con los antecedentes particulares del huerto familiar.
El corpus se organizará en dos fuentes principales:
Fuente 1: conocimiento técnico
Documentos sobre preparación de suelo, siembra, trasplante, asociaciones y rotación de cultivos, requerimientos de las plantas, identificación y manejo de plagas, fertilización y cosechas.
Fuente 2: historial del huerto
Registros aportados por el usuario sobre cultivos anteriores, fechas de siembra, ubicación de los cultivos en bancales, plagas observadas, tratamientos aplicados y resultados de cosecha.
Se utilizará Python,  base vectorial  ChromaDB y un modelo de embeddings para indexar y recuperar información relevante y  un modelo de lenguaje que genere las respuestas.