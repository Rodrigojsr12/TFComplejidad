import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Prefijos y nombres comunes para generar nombres adicionales
prefijos = ["Av. ", "Jr. ", "Calle ", "Ctra. ", "Pasaje ", "Paseo ", "Ruta ", "Camino ", "Bulevar ", "Diagonal "]

nombres = [
    "San Juan", "José Pardo", "Las Flores", "El Sol", "La Marina", "Brasil", "La Paz",
    "Universitaria", "Arequipa", "Angamos", "Benavides", "Colón", "La Molina",
    "Granados", "Mendoza", "Olaya", "Sucre", "Vargas", "Barranco", "Miraflores",
    "Surco", "Pueblo Libre", "Lince", "San Borja", "San Isidro", "Cercado",
    "La Victoria", "Callao", "Pachacamac", "San Juan de Lurigancho", "Comas",
    "Carabayllo", "Chorrillos", "Santa Anita", "Ate", "Puente Piedra",
    "Villa El Salvador", "Santa Rosa", "San Miguel", "San Martín",
    "Santa María", "El Agustino", "San Juan de Miraflores", "Santa Lucía",
    "Magdalena del Mar", "San Luis", "Rímac", "Jesús María", "Villa María del Triunfo",
    "La Punta", "San Bartolo", "Lurín", "Pucusana", "Chaclacayo",
]

# Generar nombres adicionales
def generar_nombres_adicionales(prefijos, nombres, cantidad):
    nombres_generados = set()
    while len(nombres_generados) < cantidad:
        prefijo = random.choice(prefijos)
        nombre = random.choice(nombres)
        numero = random.randint(1, 500)  
        nombre_completo = f"{prefijo}{nombre} {numero}"
        nombres_generados.add(nombre_completo)
    return list(nombres_generados)

# Lista existente de calles y avenidas
calles_avenidas_existentes = [
    "Av. Arequipa", "Av. Javier Prado", "Av. La Marina", "Av. Universitaria", "Jr. de la Unión",
    "Av. Larco", "Av. Benavides", "Av. Angamos", "Calle San Martín", "Av. Brasil", 
    "Av. Salaverry", "Av. Pardo y Aliaga", "Calle Alcanfores", "Calle Berlín", "Calle Porta", 
    "Av. El Polo", "Av. Primavera", "Av. Caminos del Inca", "Av. El Derby", "Calle Dos de Mayo", 
    "Av. Pershing", "Av. Aramburú", "Av. Tomás Marsano", "Av. Guardia Civil", "Av. Velasco Astete", 
    "Av. El Sol", "Av. Canadá", "Av. Colonial", "Calle Tarapacá", "Av. San Luis", 
    "Av. Petit Thouars", "Av. Abancay", "Calle Belén", "Calle Libertad", "Calle General Suárez", 
    "Av. Garcilaso de la Vega", "Av. Abtao", "Av. Huaylas", "Av. Túpac Amaru", "Av. Nicolás Arriola", 
    "Av. San Felipe", "Av. Aviación", "Av. Huánuco", "Calle Berlín", "Calle Colina", 
    "Av. Guardia Republicana", "Av. Ejército", "Av. Sucre", "Calle Conde de la Vega", "Calle Las Dalias", 
    "Av. Los Próceres", "Av. Canto Grande", "Calle Chiclayo", "Av. César Vallejo", "Calle Francia", 
    "Calle Aljovín", "Calle Las Flores", "Calle Lima", "Calle Madrid", "Calle Narciso de la Colina", 
    "Calle Montevideo", "Calle Colón", "Av. Paseo de la República", "Calle Los Laureles", "Calle Tiziano", 
    "Calle Mendiburu", "Calle Batalla de Junín", "Calle Bolognesi", "Av. El Ejercito", "Calle Francia", 
    "Av. 28 de Julio", "Av. Sáenz Peña", "Calle Sucre", "Av. Alfonso Ugarte", "Av. Dueñas", 
    "Calle Hernando de Lavalle", "Calle Bolívar", "Calle Montero Rosas", "Av. Faucett", "Av. Los Frutales", 
    "Av. Separadora Industrial", "Av. Próceres de la Independencia", "Av. Óscar R. Benavides", "Av. Colonial", 
    "Calle Puno", "Calle Amazonas", "Av. La Paz", "Av. Pardo", "Av. Gregorio Escobedo", 
    "Av. Alfredo Mendiola", "Av. Panamericana Norte", "Calle José Galvez", "Av. Guillermo Prescott", 
    "Calle Manuel Tovar", "Av. Enrique Meiggs", "Av. República de Panamá", "Av. Elmer Faucett", 
    "Calle Las Musas", "Av. Costanera", "Av. Los Insurgentes", "Calle Gamarra", "Calle Domingo Orué", 
    "Calle Berlín", "Calle Angamos Oeste", "Calle Mártir Olaya", "Av. Santo Toribio", 
    "Av. Guardia Civil Sur", "Calle Las Magnolias", "Calle Monte Rosa", "Calle Medrano Silva", 
    "Calle Santa Rosa", "Calle Las Rosas", "Calle Los Manzanos", "Calle Los Robles", "Calle Los Ficus", 
    "Av. Palmeras", "Calle Melchor Paz", "Calle Manuel Almenara", "Av. Defensores del Morro", 
    "Calle Flora Tristán", "Av. Primavera", "Av. Los Pinos", "Av. Velasco Astete", "Av. César Vallejo", 
    "Calle Fernando Faura", "Av. Tingo María", "Calle Colón", "Calle Manco Cápac", "Calle Los Gladiolos", 
    "Calle Las Violetas", "Calle Los Jazmines", "Calle Las Gardenias", "Av. Los Quechuas", "Calle San Borja Sur", 
    "Calle Diego de Almagro", "Av. Pardo de Zela", "Av. Parque Norte", "Calle Los Nogales", 
    "Calle Los Castaños", "Calle Ignacio Merino", "Calle Pérez de Cuéllar", "Av. Parque Sur", 
    "Av. Caminos del Inca", "Av. Central", "Av. Santa Rosa", "Av. San Juan", "Calle José Santos Chocano", 
    "Calle Mariano Melgar", "Calle María Parado de Bellido", "Calle Inti Raymi", "Av. Universitaria", 
    "Calle Conde de la Vega", "Calle San Francisco", "Calle La Mar", "Calle Grau", "Calle Loreto", 
    "Calle El Carmen", "Av. Alfredo Mendiola", "Calle Los Cedros", "Calle Los Álamos", 
    "Av. El Sol", "Av. El Corregidor", "Av. Las Palmeras", "Av. La Molina", "Calle Nicanor Arteaga", 
    "Calle Gerardo Unger", "Av. San Juan", "Av. San Germán", "Calle Hermanos Catari", 
    "Av. San Borja Norte", "Calle Cantuarias", "Calle Recavarren", "Calle Bellavista", 
    "Calle Berlín", "Calle Nicolás de Piérola", "Av. Argentina", "Av. México", "Av. Colonial", 
    "Calle José Balta", "Calle Junín", "Calle Bolognesi", "Calle Lord Cochrane", "Calle Las Lilas", 
    "Calle Los Pinos", "Calle Santa Inés", "Av. Raúl Ferrero", "Av. Guardia Civil Norte", "Av. Brasil", 
    "Av. Iquitos", "Calle Las Orquídeas", "Calle Miguel Grau", "Calle Ignacio Merino", 
    "Calle Antonio Raymondi", "Calle Huancavelica", "Calle José Olaya", "Calle Camaná", 
    "Calle Ucayali", "Calle Huancavelica", "Av. Próceres de la Independencia", "Av. Malecón Checa", 
    "Av. Víctor Larco Herrera", "Av. San Felipe", "Av. Almirante Grau", "Calle Gonzales Prada",
    "Av. Los Álamos", "Calle La Luz", "Calle Santa Inés", "Av. La Paz", "Av. Central", 
    "Calle Chancay", "Calle Conde de Superunda", "Calle Augusto Durand", "Calle Miroquesada", 
    "Calle Las Magnolias", "Av. 2 de Mayo", "Calle Talara", "Calle Las Lomas", "Calle Bartolomé Herrera", 
    "Av. Belén", "Calle Pisco", "Calle Zorritos", "Calle Francisco Lazo", "Calle Mariano Carranza", 
    "Av. Santa Anita", "Av. Pizarro", "Calle Enrique Villar", "Calle Las Camelias", "Av. Naciones Unidas",
    "Calle Sánchez Cerro", "Calle Rodríguez de Mendoza", "Av. Alcázar", "Calle Miguel Aljovín", 
    "Calle Cayetano Heredia", "Calle Enrique Palacios", "Av. Grau", "Calle Pardo de Zela", 
    "Calle Ramón Zavala", "Calle Los Laureles", "Calle Chacaltana", "Av. Cápac Yupanqui", 
]

# Calcular cuántos nombres adicionales necesitas
objetivo_total = 1500
nombres_faltantes = objetivo_total - len(calles_avenidas_existentes)

# Generar nombres adicionales
nombres_adicionales = generar_nombres_adicionales(prefijos, nombres, nombres_faltantes)

# Combinar las listas
calles_avenidas_completas = calles_avenidas_existentes + nombres_adicionales

# Asegurar que no haya duplicados
calles_avenidas_completas = list(set(calles_avenidas_completas))

print(f"Total de calles y avenidas: {len(calles_avenidas_completas)}")

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

# Función para generar costo
def generar_costo(distancia, tiempo):
    tarifa_base = 5  # Soles
    costo_por_km = random.uniform(0.5, 2)
    costo_por_minuto = random.uniform(0.1, 0.5)
    return round(tarifa_base + (distancia * costo_por_km) + (tiempo * costo_por_minuto), 2)

# Generar dataset
data = []
for _ in range(5000):
    origen = random.choice(calles_avenidas_completas)
    destino = random.choice(calles_avenidas_completas)
    while destino == origen:
        destino = random.choice(calles_avenidas_completas)
    
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
    })

# Crear DataFrame
df = pd.DataFrame(data)

# Obtener la ruta de la carpeta de Descargas
downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')

# Crear la ruta completa del archivo
file_path = os.path.join(downloads_path, 'lima_delivery_network3.csv')

# Guardar en CSV en la carpeta de Descargas
df.to_csv(file_path, index=False)

print(f"Dataset generado y guardado como '{file_path}'")
