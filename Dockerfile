# Usa una imagen oficial de Python
FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto
WORKDIR /app
COPY . /app

# Instala dependencias Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Prepara el dataset de vacas y entrena el modelo (esto puede tardar)
RUN python convertir_a_yolo.py && \
    python detector_animales.py

# Expone el puerto de Streamlit
EXPOSE 8501

# Comando por defecto: ejecuta la app Streamlit
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
