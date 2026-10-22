# Local PDF Processing Engine

Motor de procesamiento de documentos PDF ligero y asíncrono, diseñado para ejecutarse localmente sin dependencias en la nube, garantizando la privacidad de los datos. Se comunica mediante Sockets TCP, lo que lo hace ideal como backend en segundo plano para aplicaciones de escritorio (Flutter / C++).

## Características Principales
* **Conversión Estructural:** Transformación de PDF a Word (`.docx`) respetando márgenes y jerarquía de texto.
* **Procesamiento de Lenguaje Natural (NLP):** Integración de `wordninja` y corrector ortográfico para identificar y reconstruir palabras pegadas erróneamente por compiladores como LaTeX.
* **Optimización de Memoria:** Análisis fragmentado y limpieza de repeticiones de texto o saltos de formato para no saturar entornos de hardware limitado.
* **Streaming de Progreso:** Respuestas JSON asíncronas para alimentar barras de carga en tiempo real en la interfaz de usuario del frontend.

## Alcance del Software (Scope)
Este motor está estrictamente diseñado para procesar **documentos ofimáticos formales** (tesis, artículos científicos, contratos, manuales, reportes).

**Fuera del alcance:** No está diseñado para interpretar ni reconstruir archivos de diseño gráfico complejo, currículums estructurados con capas geométricas (ej. Canva), infografías o flyers, ya que estos carecen de un flujo de texto lineal continuo.

## Requisitos
* Python 3.10+
* Entorno virtual de Python (`venv`)

## Instalación y Configuración

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/pdf_engine_backend.git](https://github.com/TU_USUARIO/pdf_engine_backend.git)
   cd pdf_engine_backend
   
2. Crear y activar el entorno virtual:
    # En Linux/macOS
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

    # En Windows
    ```bash
    python -m venv .venv
    .venv\Scripts\activate

3. Instalar las dependencias necesarias:
    ```bash
    pip install -r requirements.txt


## Uso y Ejecución del Servidor
El motor funciona como un servidor local escuchando por defecto en **127.0.0.1:50051**. Para iniciarlo, asegúrate de tener tu entorno virtual activado y ejecuta:
    ```bash
    cd src
    python3 server.py

(El servidor se quedará bloqueado en la terminal esperando peticiones entrantes de tu cliente o puente C++).

## Protocolo de Comunicación (API TCP)
El servidor espera recibir una cadena JSON con la acción a realizar y las rutas absolutas de los archivos.

**Ejemplo de Petición JSON:**
    ```bash
    {
    "action": "pdf_to_word",
    "payload": {
        "input_path": "/ruta/absoluta/al/documento/prueba.pdf",
        "output_path": "/ruta/absoluta/al/documento/resultado.docx"
        }
    }

## Respuestas en Tiempo Real (Streaming)
Dado que el procesamiento de documentos pesados toma tiempo, el socket no espera hasta el final para responder. A medida que avanza por las fases (lectura, extracción, NLP), el servidor emite paquetes JSON de progreso separados por un salto de línea (\n), permitiendo al cliente leer un flujo continuo.

**Ejemplo de salida recibida por el cliente:**
    ```bash
    {"type": "progress", "percent": 10, "message": "Iniciando lectura del PDF..."}
    {"type": "progress", "percent": 40, "message": "Convirtiendo estructura y corrigiendo LaTeX..."}
    {"type": "progress", "percent": 100, "message": "¡Conversión finalizada!"}
    {"type": "result", "status": "ok", "message": "Archivo guardado exitosamente."}

## Licencia y Dependencias
Este proyecto utiliza librerías de código abierto bajo licencias permisivas y virales (como PyMuPDF y pdf2docx). El código de este motor se distribuye de manera abierta para cumplir con los lineamientos de dichas licencias.