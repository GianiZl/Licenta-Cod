import matplotlib.pyplot as plt
import numpy as np
import random
import string
import os

# --- CONFIGURARE ---
OUTPUT_FOLDER = "Grafice Sintetice"
NUM_IMAGES_PER_TYPE = 50  # Câte imagini din fiecare tip vrei (Total = 3 * 50 = 150)

# Creăm folderul dacă nu există
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Funcție pentru a genera text aleatoriu (pentru titluri/etichete)
def random_text(length=6):
    letters = string.ascii_uppercase + string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# --- GENERATOR BAR CHART ---
def generate_bar_chart(index):
    plt.figure(figsize=(8, 6))
    
    # Date aleatorii
    num_bars = random.randint(3, 10)
    values = np.random.randint(10, 100, size=num_bars)
    labels = [random_text(4) for _ in range(num_bars)]
    colors = [np.random.rand(3,) for _ in range(num_bars)] # Culori RGB aleatorii

    # Desenare
    plt.bar(labels, values, color=colors)
    plt.title(f"Grafic Sintetic {random_text(5)}")
    plt.xlabel(random_text(4))
    plt.ylabel("Valori")
    
    # Salvare
    path = os.path.join(OUTPUT_FOLDER, f"bar_{index}.jpg")
    plt.savefig(path)
    plt.close() # Important: eliberăm memoria

# --- GENERATOR PIE CHART ---
def generate_pie_chart(index):
    plt.figure(figsize=(8, 6))
    
    # Date aleatorii
    num_slices = random.randint(3, 8)
    values = np.random.randint(5, 50, size=num_slices)
    labels = [random_text(5) for _ in range(num_slices)]
    colors = [np.random.rand(3,) for _ in range(num_slices)]

    # Desenare
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f"Distributie {random_text(5)}")
    
    # Salvare
    path = os.path.join(OUTPUT_FOLDER, f"pie_{index}.jpg")
    plt.savefig(path)
    plt.close()

# --- GENERATOR SCATTER PLOT ---
def generate_scatter_plot(index):
    plt.figure(figsize=(8, 6))
    
    # Date aleatorii
    num_points = random.randint(20, 100)
    x = np.random.randn(num_points)
    y = np.random.randn(num_points)
    colors = np.random.rand(num_points)
    sizes = 100 * np.random.rand(num_points)

    # Desenare
    plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
    plt.title(f"Dispersie {random_text(5)}")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Salvare
    path = os.path.join(OUTPUT_FOLDER, f"scatter_{index}.jpg")
    plt.savefig(path)
    plt.close()

# --- RULARE PRINCIPALĂ ---
print(f"🚀 Încep generarea a {NUM_IMAGES_PER_TYPE * 3} imagini...")

for i in range(NUM_IMAGES_PER_TYPE):
    generate_bar_chart(i)
    generate_pie_chart(i)
    generate_scatter_plot(i)
    
    # Bara de progres simplă
    if i % 10 == 0:
        print(f"Generat setul {i}...")

print(f"✅ Gata! Imaginile sunt în folderul '{OUTPUT_FOLDER}'.")