import sys
import pandas as pd
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QTextEdit, QMessageBox, QStackedWidget)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Función para convertir tiempo en formato MM:SS a minutos
def tiempo_a_minutos(tiempo):
    minutos, segundos = map(int, tiempo.split(':'))
    return minutos + segundos / 60

# Clase para la pantalla de inicio
class PantallaInicio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Fondo de la pantalla de inicio
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#7EDEEA"))
        self.setPalette(palette)

        titulo_font = QFont('Montserrat', 20, QFont.Bold)
        
        titulo = QLabel('Bienvenido a la Red de Entrega de Paquetes en Lima')
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        nombres = ["U202215705 - Carlos Adrianzén", "U202214406 - Alejandro Barturen", "U202213646 - Rodrigo Salvador"]
        desarrolladores_label = QLabel("Desarrollado por:")
        desarrolladores_label.setFont(QFont('Times New Roman', 16, QFont.Bold))
        desarrolladores_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desarrolladores_label)

        for nombre in nombres:
            nombre_label = QLabel(nombre)
            nombre_label.setFont(QFont('Times New Roman', 16))
            nombre_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(nombre_label)

        iniciar_button = QPushButton('Iniciar Proceso')
        iniciar_button.setFont(QFont('Helvetica', 14))
        iniciar_button.clicked.connect(self.cambiar_a_pantalla_principal)
        layout.addWidget(iniciar_button)

        self.setLayout(layout)

    def cambiar_a_pantalla_principal(self):
        self.parentWidget().setCurrentIndex(1)

# Clase para la pantalla principal de la aplicación
class GraphApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title = 'Red de Entrega de Paquetes en Lima'
        self.G = nx.DiGraph()
        self.df = pd.DataFrame()
        self.node_positions = {}  
        self.initUI()
        self.cargar_datos()

    # Cargar los datos y crear el grafo
    def cargar_datos(self):
        file_path = 'lima_delivery_network3.csv' 
        self.df = pd.read_csv(file_path)
        self.G = nx.DiGraph()

        # Crear un conjunto único de nodos
        nodos = set(self.df['Origen']).union(set(self.df['Destino']))
        if len(nodos) > 1500:
            nodos = set(list(nodos)[:1500]) 

        # Filtrar el DataFrame para incluir solo los nodos seleccionados
        self.df = self.df[self.df['Origen'].isin(nodos) & self.df['Destino'].isin(nodos)]

        # Agregar nodos y aristas al grafo
        for _, row in self.df.iterrows():
            origen = row['Origen']
            destino = row['Destino']
            tiempo = tiempo_a_minutos(row['Tiempo_Recorrido'])
            costo = row['Costo']
            
            self.G.add_edge(origen, destino, weight=tiempo, cost=costo)

        # Calcular posiciones fijas para los nodos
        self.node_positions = nx.spring_layout(self.G, k=0.5, iterations=50)

    # Configuración inicial de la UI
    def initUI(self):
        layout = QVBoxLayout()

        titulo_font = QFont('Montserrat', 16, QFont.Bold)
    
        titulo = QLabel('Red de Entrega de Paquetes en Lima')
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Campos de entrada para origen y destino
        self.origen_label = QLabel('Nodo de origen:')
        layout.addWidget(self.origen_label)
        self.origen_entry = QLineEdit(self)
        layout.addWidget(self.origen_entry)

        self.destino_label = QLabel('Nodo de destino:')
        layout.addWidget(self.destino_label)
        self.destino_entry = QLineEdit(self)
        layout.addWidget(self.destino_entry)

        # Botón para calcular la ruta
        self.calcular_button = QPushButton('Calcular Ruta', self)
        self.calcular_button.clicked.connect(self.calcular_rutas)
        layout.addWidget(self.calcular_button)

        self.cerrar_button = QPushButton('Cerrar Programa', self)
        self.cerrar_button.clicked.connect(self.cerrar_programa)
        layout.addWidget(self.cerrar_button)

        # Campo para mostrar resultados
        self.resultado_label = QTextEdit(self)
        self.resultado_label.setReadOnly(True)
        layout.addWidget(self.resultado_label)

        # mostrar el gráfico
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    # Función para calcular la ruta más corta y la más barata
    def calcular_rutas(self):
        origen_usuario = self.origen_entry.text()
        destino_usuario = self.destino_entry.text()

        if origen_usuario not in self.G.nodes or destino_usuario not in self.G.nodes:
            self.mostrar_error("Uno o ambos nodos no están en el grafo. Asegúrate de que los nodos existan o estén bien escritos y vuelve a intentarlo.")
        else:
            try:
                # Calcular la ruta más corta usando Dijkstra
                ruta_corta = nx.shortest_path(self.G, source=origen_usuario, target=destino_usuario, weight='weight')
                tiempo_total_corto = nx.shortest_path_length(self.G, source=origen_usuario, target=destino_usuario, weight='weight')
                
                # Calcular la ruta más barata usando Dijkstra
                ruta_barata = nx.shortest_path(self.G, source=origen_usuario, target=destino_usuario, weight='cost')
                costo_total_barato = nx.shortest_path_length(self.G, source=origen_usuario, target=destino_usuario, weight='cost')

                # Calcular el costo y tiempo total de las rutas
                costo_total_corto = sum(self.G[u][v]['cost'] for u, v in zip(ruta_corta[:-1], ruta_corta[1:]))
                tiempo_total_barato = sum(self.G[u][v]['weight'] for u, v in zip(ruta_barata[:-1], ruta_barata[1:]))

                # Mostrar los resultados en la interfaz
                resultado = (f"Ruta más corta: {' -> '.join(ruta_corta)}\n"
                             f"Tiempo de recorrido: {tiempo_total_corto:.2f} minutos\n"
                             f"Costo de la ruta: {costo_total_corto:.2f} soles\n\n"
                             f"Ruta más barata: {' -> '.join(ruta_barata)}\n"
                             f"Costo de la ruta: {costo_total_barato:.2f} soles\n"
                             f"Tiempo de recorrido: {tiempo_total_barato:.2f} minutos")

                self.resultado_label.setText(resultado)

                # Visualizar el grafo con ambas rutas
                self.visualizar_grafo(ruta_corta, ruta_barata)

            except nx.NetworkXNoPath:
                self.mostrar_error(f"No se encontró una ruta entre {origen_usuario} y {destino_usuario}.")

    # Función para mostrar mensajes de error
    def mostrar_error(self, mensaje):
        QMessageBox.warning(self, 'Error', mensaje)

    # Función para visualizar el grafo con dos rutas
    def visualizar_grafo(self, ruta_corta, ruta_barata):
        self.canvas.figure.clear()

        ax = self.canvas.figure.add_subplot(111)
        pos = self.node_positions

        # Dibujar nodos
        nx.draw_networkx_nodes(self.G, pos, node_size=50, node_color='lightblue', ax=ax)  # Nodo más pequeño

        # Dibujar todas las aristas (conexiones), con transparencia para mejor visualización
        nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(), width=0.5, alpha=0.3, edge_color='gray', ax=ax)

        # Dibujar etiquetas si es necesario
        nx.draw_networkx_labels(self.G, pos, font_size=6, ax=ax)

        # Dibujar la ruta más corta (en rojo)
        nx.draw_networkx_edges(self.G, pos, edgelist=list(zip(ruta_corta[:-1], ruta_corta[1:])), 
                               edge_color='red', width=2, ax=ax)

        # Dibujar la ruta más barata (en azul)
        nx.draw_networkx_edges(self.G, pos, edgelist=list(zip(ruta_barata[:-1], ruta_barata[1:])), 
                               edge_color='blue', width=2, ax=ax)

        ax.set_title("Red de Entrega de Paquetes en Lima")
        ax.axis('off')

        self.canvas.draw()

    # Función para cerrar el programa
    def cerrar_programa(self):
        sys.exit()

# Clase para gestionar múltiples pantallas
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.pantalla_inicio = PantallaInicio(self)
        self.pantalla_principal = GraphApp(self)

        self.addWidget(self.pantalla_inicio)
        self.addWidget(self.pantalla_principal)

# Inicializar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle('Red de Entrega de Paquetes en Lima')
    main_app.show()
    sys.exit(app.exec_())
