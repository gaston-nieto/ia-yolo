# Proyecto: Detector de Animales con YOLOv8 y Streamlit

Este proyecto permite entrenar un modelo YOLOv8 para detectar animales en imágenes y desplegar una interfaz web donde el usuario puede subir una imagen y obtener la cantidad de animales detectados.

## 🐄 Descripción del Problema

En el ámbito ganadero, llevar un control preciso del stock de animales es una tarea desafiante. Contar animales a simple vista, especialmente en campos de gran extensión o con animales en movimiento, suele ser impreciso y requiere tiempo. Esto puede derivar en pérdidas económicas ante la falta de detección temprana de animales faltantes o desvíos en el rodeo.

Este proyecto busca resolver esa problemática mediante visión por computadora, permitiendo **contar animales en una imagen de forma automática y confiable** a partir de un modelo de detección entrenado para reconocer vacas.

---

## 🧠 Stack Tecnológico y Justificación

- **YOLOv8s**: Modelo de visión por computadora especializado en detección de objetos en tiempo real. Elegido por su equilibrio entre precisión, velocidad y requerimientos computacionales, ideal para un MVP funcional.
- **Python**: Lenguaje versátil y ampliamente adoptado en el ecosistema de IA, con fuerte soporte en librerías de machine learning y visión por computadora.
- **Streamlit**: Framework liviano para construir interfaces interactivas de forma rápida. Permite exponer el modelo a usuarios no técnicos mediante una UI simple e intuitiva.
- **Docker**: Facilita el despliegue y portabilidad de la aplicación, asegurando que pueda ejecutarse en cualquier entorno sin conflictos de dependencias.

---

## ⚙️ Funcionalidades del MVP

El proyecto, en su versión inicial (MVP), incluye:

- Subida de una imagen con animales.
- Detección automática de vacas presentes utilizando un modelo personalizado.
- Visualización de la imagen con *bounding boxes* para validar detecciones.
- Conteo total de animales detectados, discriminado por especie.

> Próxima mejora propuesta: incorporar un LLM para generar un breve informe con análisis del rodeo a partir de los resultados obtenidos.


## 🚧 Limitaciones Actuales y Mejores Futuras

### Limitaciones

- El modelo fue entrenado con un dataset reducido (aprox. 100 imágenes por clase), lo que limita su capacidad de generalización en escenarios complejos.
- La precisión disminuye cuando los animales se encuentran a gran distancia o parcialmente ocultos, debido al uso de YOLOv8s y restricciones de hardware disponibles para entrenar modelos más grandes.
- El MVP está orientado únicamente a imágenes estáticas y reconoce solo una especie: vacas.

### Mejoras Futuras Propuestas

- Ampliar y diversificar el dataset (distancias, iluminación, razas, ambientes).
- Entrenar variantes más robustas del modelo (YOLOv8x o modelos multimodales).
- Incorporar conteo en video o análisis en tiempo real.
- Agregar un componente de IA generativa que produzca informes y recomendaciones automáticas para el productor, en función de los animales detectados.
- Extender la clasificación del modelo a más especies de interés ganadero.


## Origen de los datos

Las imágenes utilizadas para entrenar este modelo fueron obtenidas del dataset público de Kaggle:
- [Cow Detection Dataset (CVAT/XML)](https://www.kaggle.com/datasets/trainingdatapro/cows-detection-dataset)

## Estructura del proyecto

- `cows-detection-dataset/` — Dataset original de vacas (imágenes y anotaciones XML/CSV)
- `convertir_a_yolo.py` — Script para convertir las anotaciones XML a formato YOLO y organizar el dataset
- `dataset/` — Dataset listo en formato YOLO (se genera automáticamente)
- `cows.yaml` — Archivo de configuración YOLO para el dataset de vacas
- `detector_animales.py` — Script para entrenar el modelo YOLOv8s con los datos preparados
- `runs/` — Carpeta donde se guardan los modelos entrenados por YOLO
- `app_streamlit.py` — Interfaz web para cargar imágenes y detectar vacas usando el modelo entrenado
- `requirements.txt` — Dependencias del proyecto

## Cómo correr el proyecto

### 1. Prepara el dataset
- Clona el repositorio 
- deszip el archivo cows-detection-dataset.zip
- Convertir el dataset con convertir_a_yolo.py para pasarlo a formato YOLO:
  ```bash
  python convertir_a_yolo.py
  ```
  Esto generará la carpeta `dataset/` con imágenes y labels listas para entrenamiento.

### 2. Entrenamiento YOLOv8s

- Entrena el modelo:
  ```bash
  python detector_animales.py
  ```
  El modelo entrenado se guardará en `runs/detect/cows_train/weights/best.pt`.

### 3. Ejecuta la interfaz

- Lanza la app web:
  ```bash
  streamlit run app_streamlit.py
  ```
  Accede a http://localhost:8501 para subir imágenes y ver la cantidad de vacas detectadas.

### 4. (Opcional) Ejecuta todo en Docker

> **Advertencia:** El contenedor Docker realiza el entrenamiento completo del modelo usando todas las imágenes al momento de construir la imagen. Este proceso puede demorar varios minutos, según la cantidad de datos y recursos disponibles.

1. Construye la imagen:
   ```bash
   docker build -t detector-animales .
   ```
2. Ejecuta el contenedor:
   ```bash
   docker run -p 8501:8501 detector-animales
   ```
   Accede a http://localhost:8501 para usar la app web.

Parametros de entrenamiento:
- epochs=100
- imgsz=640
- batch=8
- name="cows_train"


## Requerimientos
- Python 3.8+
- Ver dependencias en `requirements.txt`

Desarrollado para la detección automática de vacas en imágenes usando deep learning y despliegue rápido con Streamlit.
