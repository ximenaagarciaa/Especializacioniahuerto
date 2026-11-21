# Plantilla de repositorio base — IA Generativa aplicada a la gestión de huerto



## Cómo empezar


1. Clona este repositorio utilizando el comando git clone https://github.com/ximenaagarciaa/especializacionia.git
2. Crea tu entorno virtual de Python usando el comando python -m venv venv y activalo usando el comando source venv/Scripts/activate
3. Instala las dependencias del proyecto usando el comando 
pip install -r requirements.txt para poder usarlas en la aplicacion.
4. Copia `.env.example` a un archivo nuevo llamado `.env`, y completa ahí tus credenciales reales (llaves de API, tokens). El archivo `.env` nunca se sube al repositorio: ya está excluido en `.gitignore`.
5. Para comprobar que este bien la instalación , ejecuta python  src/consumir_gemini_ref.py


## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).


