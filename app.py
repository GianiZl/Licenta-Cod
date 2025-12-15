import streamlit as st
from roboflow import Roboflow
import ollama
from PIL import Image
import io

# --- CONFIGURARE ---
API_KEY = "9VIREQ4iCpHzbWB6sEyh" #cheia din roboflow
PROJECT_NAME = "licenta_analiza_grafice"
VERSION = 2  # versiunea 2 

st.set_page_config(page_title="Licenta AI", page_icon="📊")

st.title("Analiza Graficelor")
st.markdown("Sistem hibrid: **YOLOv11** (Vizual) + **LLAMA3.2-VISION**")

# 1. Încărcare Imagine
uploaded_file = st.file_uploader("Încarcă un grafic (JPG/PNG)...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Afișare imagine
    image = Image.open(uploaded_file)
    st.image(image, caption='Imaginea Încărcată', use_container_width=True)
    
    # Buton de acțiune
    if st.button("Analizează Graficul"):
        with st.spinner('1/2: Roboflow detectează structura graficului...'):
            
            # Salvare temporară pentru a o trimite la API
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            # --- PASUL A: ROBOFLOW ---
            try:
                rf = Roboflow(api_key=API_KEY)
                project = rf.workspace().project(PROJECT_NAME)
                model = project.version(VERSION).model
                
                # Facem predicția pe fișierul temporar
                # Nota: Roboflow accepta path local, aici salvam temp
                with open("temp_image.jpg", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                prediction = model.predict("temp_image.jpg", confidence=20, overlap=30).json()
                
                # Extragem datele
                detected_text = ""
                for item in prediction['predictions']:
                    detected_text += f"- Element '{item['class']}' (Confidență: {item['confidence']:.2f})\n"
                
                st.success(f"Roboflow a detectat {len(prediction['predictions'])} elemente!")
                with st.expander("Vezi datele brute (JSON)"):
                    st.json(prediction)

            except Exception as e:
                st.error(f"Eroare la Roboflow: {e}")
                st.stop()

        with st.spinner('2/2: Agentul Ollama interpretează datele...'):
            # --- PASUL B: OLLAMA ---
            prompt = f"""
            Ești un analist de date expert.
            Am detectat următoarea structură vizuală în grafic:
            {detected_text}
            
            Sarcina ta:
            1. Ce tip de grafic este?
            2. Care este trendul general?
            3. Dacă sunt date financiare, fă o scurtă predicție.
            
            Răspunde în limba română, concis.
            """
            
            try:
                # Trimitem imaginea si promptul la LLaVA
                response = ollama.chat(
                    model='llama3.2-vision', 
                    messages=[{
                        'role': 'user',
                        'content': prompt,
                        'images': ["temp_image.jpg"]
                    }]
                )
                
                st.subheader("Interpretarea AI:")
                st.write(response['message']['content'])
                
            except Exception as e:
                st.error(f"Eroare la Ollama (asigură-te că ai rulat 'ollama serve'): {e}")