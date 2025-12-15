import json
from roboflow import Roboflow
import ollama
from PIL import Image

# --- CONFIGURARE ---
API_KEY = "9VIREQ4iCpHzbWB6sEyh"  #Roboflow cheie
PROJECT_NAME = "licenta_analiza_grafice"
VERSION_NUMBER = 1
IMAGE_PATH = r"C:\Users\GianiZlate\Documents\Licenta\Grafice pentru Gemini\bar_chart_2b8a3b38-5d31-4903-92b3-19f8749c0f19.jpg" # Imaginea pe care vrei sa o testezi (cea cu ciocolata)

# 1. INITIALIZARE ROBOFLOW
print("⏳ Conectare la Roboflow...")
rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project(PROJECT_NAME)
model = project.version(VERSION_NUMBER).model

# 2. DETECTIE OBIECTE (YOLO)
print(f"🔍 Analizez imaginea: {IMAGE_PATH}...")
prediction = model.predict(IMAGE_PATH, confidence=10, overlap=30).json()

# Extragem informatiile relevante din JSON-ul de la Roboflow
detected_objects = []
for item in prediction['predictions']:
    obj_info = {
        "class": item['class'],
        "confidence": round(item['confidence'], 2),
        "x": item['x'],
        "y": item['y']
    }
    detected_objects.append(obj_info)

print(f"✅ Roboflow a detectat {len(detected_objects)} elemente.")

# 3. PREGATIREA PROMPTULUI PENTRU OLLAMA
context_str = "Un sistem de Computer Vision a detectat urmatoarele elemente structurale in imagine:\n"
for obj in detected_objects:
    context_str += f"- Un element de tip '{obj['class']}' la pozitia x={obj['x']}, y={obj['y']} cu incredere {obj['confidence']}\n"

prompt = f"""
Te rog sa actionezi ca un expert Data Scientist.
Ai primit o imagine cu un grafic (atasata acestui mesaj).

CONTEXT TEHNIC SUPLIMENTAR:
{context_str}

SARCINA TA:
1. Identifica despre ce este graficul (citeste titlul si axele din imagine).
2. Estimeaza valorile vizuale ale datelor (chiar daca nu sunt perfect clare).
3. Interpreteaza trendul general.
4. Daca este un grafic temporal (zile, luni, ani), fa o PREVIZIUNE logica pentru urmatoarea perioada.

Raspunde scurt si la obiect, in limba romana.
"""

# 4. TRIMITERE CATRE OLLAMA (LLAVA / LLAMA3)
print("🤖 Trimit datele catre Ollama pentru interpretare...")

# Nota: Folosim 'llava' pentru ca este multimodal (vede imagini). 
# Daca nu il ai, ruleaza in terminal: ollama pull llava
response = ollama.chat(
    model='llama3.2-vision', 
    messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': [IMAGE_PATH] # Trimitem si imaginea fizica
        }
    ]
)

# 5. AFISARE REZULTAT
print("\n" + "="*50)
print("REZULTATUL ANALIZEI (AGENT OLLAMA):")
print("="*50)
print(response['message']['content'])