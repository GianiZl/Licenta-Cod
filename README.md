Fisierul generator_grafice face ceea ce îi spune și numele, adică, generează 3 tipuri de grafice. 
Cele 3 tipuri de grafice sunt: 
  - Bar Chart
  - Pie Chart
  - Scatter Plot.
Toate aceste grafice sunt făcute cu python.

În fișierul main script-ul  face următorul flux:

Ia o imagine.

O trimite la Roboflow pentru detecție.

Pregătește datele.

O trimite la Ollama pentru interpretare și predicție.

Am adaugat si un fisier de test app.py

Am reusit sa obtin o precizie de aproape 80% in roboflow. Prin intermediul acestuia, cand incarc o imagine in acel streamlit, reusesc sa adnotez aproape toate elementele din grafice. 
Agentul inca nu functioneaza asa cum mi-as dori.
