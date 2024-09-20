import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Definir distritos de Lima (ampliado a 20 distritos)
distritos = [
    "Lima Centro", "San Isidro", "Miraflores", "Surco", "La Molina",
    "Barranco", "Chorrillos", "San Borja", "Jesús María", "Lince",
    "San Miguel", "Pueblo Libre", "Magdalena", "Breña", "Rímac",
    "La Victoria", "San Juan de Lurigancho", "Ate", "Los Olivos", "Comas"
]

# Definir tipos de puntos
tipos_puntos = ["Centro de Distribución", "Punto de Entrega"]

# Función para generar coordenadas aleatorias dentro de Lima
def generar_coordenadas():
    lat = random.uniform(-12.2, -11.8)
    lon = random.uniform(-77.2, -76.8)
    return lat, lon

# Función para generar tiempo de recorrido (en minutos y segundos)
def generar_tiempo_recorrido():
    minutos = random.randint(5, 119)
    segundos = random.randint(0, 59)
    return minutos + segundos / 60

# Función para generar distancia
def generar_distancia(tiempo):
    velocidad = random.uniform(10, 50)  # km/h
    return round((tiempo / 60) * velocidad, 2)  # Distancia en km

# Función para generar costo (modificada)
def generar_costo(distancia, tiempo):
    tarifa_base = 5  # Soles
    costo_por_km = random.uniform(0.5, 2)
    costo_por_minuto = random.uniform(0.1, 0.5)
    return round(tarifa_base + (distancia * costo_por_km) + (tiempo * costo_por_minuto), 2)

# Generar dataset
data = []
for _ in range(2000):
    origen = random.choice(distritos)
    destino = random.choice(distritos)
    while destino == origen:
        destino = random.choice(distritos)
    
    tipo_origen = random.choice(tipos_puntos)
    tipo_destino = "Punto de Entrega" if tipo_origen == "Centro de Distribución" else random.choice(tipos_puntos)
    
    tiempo = generar_tiempo_recorrido()
    distancia = generar_distancia(tiempo)
    costo = generar_costo(distancia, tiempo)
    
    lat_origen, lon_origen = generar_coordenadas()
    lat_destino, lon_destino = generar_coordenadas()
    
    fecha_hora = datetime.now() + timedelta(days=random.randint(0, 30))
    
    data.append({
        "Origen": origen,
        "Destino": destino,
        "Tipo_Origen": tipo_origen,
        "Tipo_Destino": tipo_destino,
        "Latitud_Origen": lat_origen,
        "Longitud_Origen": lon_origen,
        "Latitud_Destino": lat_destino,
        "Longitud_Destino": lon_destino,
        "Tiempo_Recorrido": f"{int(tiempo)}:{int((tiempo % 1) * 60):02d}",  # Formato MM:SS
        "Distancia_km": distancia,
        "Costo": costo,
        "Fecha_Hora": fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    })

# Crear DataFrame
df = pd.DataFrame(data)

# Obtener la ruta de la carpeta de Descargas
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

# Crear la ruta completa del archivo
file_path = os.path.join(downloads_path, 'lima_delivery_network2.csv')

# Guardar en CSV en la carpeta de Descargas
df.to_csv(file_path, index=False)

print(f"Dataset generado y guardado como '{file_path}'")
