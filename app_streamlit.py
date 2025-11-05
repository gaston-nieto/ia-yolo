import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import tempfile

# Cargamos el modelo entrenado
MODEL_PATH = 'runs/detect/cows_train/weights/best.pt'
model = YOLO(MODEL_PATH)

st.title('Detector de Animales')
st.write('Sube una imagen y selecciona la clase a detectar.')

# Solo vacas
class_id = 0  # cow

uploaded_file = st.file_uploader('Elige una imagen', type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption='Imagen subida', use_container_width=True)

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img.save(tmp.name)
        results = model(tmp.name)
    boxes = results[0].boxes
    count = 0
    for box in boxes:
        if int(box.cls[0]) == class_id:
            count += 1
    st.success(f'Cantidad de vacas detectadas: {count}')

    res_img = np.array(results[0].plot())
    st.image(res_img, caption='Detecciones', use_container_width=True)

