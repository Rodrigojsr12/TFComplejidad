import sys
import pandas as pd
import numpy as np
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                           QStackedWidget, QGraphicsOpacityEffect, QMessageBox, 
                           QLineEdit, QTextEdit)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PantallaInicio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)
        self.initUI()

    def initUI(self):
        # Crear layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Crear y configurar el label de fondo
        self.fondo = QLabel(self)
        self.fondo.setFixedSize(self.size())
        self.fondo.setAutoFillBackground(True)
        self.actualizar_fondo()

        # Configurar el título
        titulo = QLabel('PackPath Lima')
        titulo_font = QFont('Arial Black', 32, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("QLabel { color: #00FFFF; }")
        layout.addWidget(titulo)
        
        # Añadir espacio entre el título y los botones
        layout.addSpacing(50)

        # Configurar los botones principales
        botones = {
            "Mostrar grafo": self.mostrar_grafo,
            "Aplicar algoritmo de Dijkstra": self.aplicar_dijkstra,
            "Aplicar algoritmo de Bellman-Ford": self.aplicar_bellman_ford,
            "Integrantes": self.mostrar_integrantes
        }

        for texto, funcion in botones.items():
            boton = QPushButton(texto)
            boton.setFont(QFont('Arial', 12))
            boton.setFixedWidth(300)
            boton.setMinimumHeight(40)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 255, 255, 180);
                    color: black;
                    border: 2px solid #008B8B;
                    border-radius: 15px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: rgba(0, 139, 139, 180);
                    color: white;
                }
            """)
            boton.clicked.connect(funcion)
            layout.addWidget(boton, alignment=Qt.AlignCenter)
            layout.addSpacing(10)

        # Añadir espacio antes del botón salir
        layout.addSpacing(20)

        # Botón de salir
        boton_salir = QPushButton("Salir")
        boton_salir.setFont(QFont('Arial', 12))
        boton_salir.setFixedWidth(100)
        boton_salir.setMinimumHeight(30)
        boton_salir.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 99, 71, 180);
                color: white;
                border: 2px solid #FF4433;
                border-radius: 15px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 68, 51, 180);
                color: white;
            }
        """)
        boton_salir.clicked.connect(QApplication.instance().quit)
        layout.addWidget(boton_salir, alignment=Qt.AlignRight)

        # Hacer que los widgets estén por encima del fondo
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.actualizar_fondo()

    def actualizar_fondo(self):
        # Actualizar el tamaño y la imagen de fondo
        pixmap = QPixmap("C:/Users/Rodrigo/Documents/Python/proyectopruebas/delivery.jpg") # Aqui se tiene que actualizar con tu direccion
        scaled_pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        
        # Calcular las coordenadas para centrar la imagen
        x = (scaled_pixmap.width() - self.width()) // 2
        y = (scaled_pixmap.height() - self.height()) // 2
        
        # Recortar la imagen para que se ajuste exactamente a la ventana
        cropped_pixmap = scaled_pixmap.copy(
            x, y, self.width(), self.height()
        )
        
        self.fondo.setPixmap(cropped_pixmap)
        self.fondo.setGeometry(0, 0, self.width(), self.height())
        self.fondo.lower()

    def mostrar_grafo(self):
        self.parentWidget().setCurrentIndex(1)

    def aplicar_dijkstra(self):
        self.parentWidget().setCurrentIndex(2)

    def aplicar_bellman_ford(self):
        pass

    def mostrar_integrantes(self):
        self.parentWidget().setCurrentIndex(3)  # Índice de la pantalla de integrantes

class GraphVisualization(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.initUI()
        self.cargar_y_visualizar_datos()

    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('Visualización del Grafo de Entregas')
        titulo_font = QFont('Helvetica', 16, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Canvas para el gráfico
        self.figure = plt.Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Botón de volver
        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver)

        self.setLayout(layout)

    def cargar_y_visualizar_datos(self):
        try:
            # Cargar datos
            self.df = pd.read_csv('lima_delivery_network3.csv')
            
            # Crear el grafo
            G = nx.DiGraph()
            
            # Añadir nodos
            nodos = set(self.df['Origen'].unique()) | set(self.df['Destino'].unique())
            G.add_nodes_from(nodos)
            
            # Calcular el layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Crear el gráfico
            ax = self.figure.add_subplot(111)
            
            # Obtener coordenadas de los nodos
            x_coords = [pos[node][0] for node in G.nodes()]
            y_coords = [pos[node][1] for node in G.nodes()]
            
            # Crear scatter plot solo con los nodos
            scatter = ax.scatter(
                x_coords,
                y_coords,
                c='blue',  # Color único para todos los nodos
                alpha=0.6,
                s=30  # Tamaño un poco más grande para mejor visibilidad
            )

            # Configurar el gráfico
            ax.set_title('Red de Entregas - Nodos')
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Actualizar el canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar o visualizar los datos: {str(e)}')

    def volver_inicio(self):
        self.parentWidget().setCurrentIndex(0)

class DijkstraApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.G = nx.DiGraph()
        self.df = pd.DataFrame()
        self.node_positions = {}
        self.initUI()
        self.cargar_datos()

    def cargar_datos(self):
        file_path = 'lima_delivery_network3.csv'
        self.df = pd.read_csv(file_path)
        self.G = nx.DiGraph()

        nodos = set(self.df['Origen']).union(set(self.df['Destino']))
        if len(nodos) > 1500:
            nodos = set(list(nodos)[:1500])

        self.df = self.df[self.df['Origen'].isin(nodos) & self.df['Destino'].isin(nodos)]

        for _, row in self.df.iterrows():
            origen = row['Origen']
            destino = row['Destino']
            tiempo = tiempo_a_minutos(row['Tiempo_Recorrido'])
            costo = row['Costo']
            self.G.add_edge(origen, destino, weight=tiempo, cost=costo)

        self.node_positions = nx.spring_layout(self.G, k=0.5, iterations=50)

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel('Algoritmo de Dijkstra - Cálculo de Ruta Más Corta')
        titulo_font = QFont('Helvetica', 16, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.origen_entry = QLineEdit(self)
        layout.addWidget(QLabel('Nodo de origen:'))
        layout.addWidget(self.origen_entry)

        self.destino_entry = QLineEdit(self)
        layout.addWidget(QLabel('Nodo de destino:'))
        layout.addWidget(self.destino_entry)

        self.calcular_button = QPushButton('Calcular Ruta', self)
        self.calcular_button.clicked.connect(self.calcular_rutas)
        layout.addWidget(self.calcular_button)

        self.resultado_label = QTextEdit(self)
        self.resultado_label.setReadOnly(True)
        layout.addWidget(self.resultado_label)

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver)

        self.setLayout(layout)

    def calcular_rutas(self):
        pass

    def volver_inicio(self):
        self.parentWidget().setCurrentIndex(0)

# Nueva clase para la pantalla de integrantes
class PantallaIntegrantes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Configurar el layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel('Integrantes del Proyecto')
        titulo_font = QFont('Arial Black', 24, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00FFFF;")
        layout.addWidget(titulo)
        
        layout.addSpacing(40)

        # Lista de integrantes con sus códigos
        integrantes = [
            ('Carlos Adrianzén', 'U202215705'),
            ('Alejandro Barturen', 'U202214406'),
            ('Rodrigo Salvador', 'U202213646')
        ]

        # Crear un widget para cada integrante
        for nombre, codigo in integrantes:
            # Contenedor para cada integrante
            integrante_widget = QWidget()
            integrante_layout = QVBoxLayout()
            integrante_widget.setLayout(integrante_layout)

            # Nombre del integrante
            nombre_label = QLabel(nombre)
            nombre_label.setFont(QFont('Arial', 16, QFont.Bold))
            nombre_label.setStyleSheet("color: white;")
            nombre_label.setAlignment(Qt.AlignCenter)
            
            # Código del integrante
            codigo_label = QLabel(codigo)
            codigo_label.setFont(QFont('Arial', 14))
            codigo_label.setStyleSheet("color: #00FFFF;")
            codigo_label.setAlignment(Qt.AlignCenter)

            integrante_layout.addWidget(nombre_label)
            integrante_layout.addWidget(codigo_label)
            layout.addWidget(integrante_widget)
            
            # Añadir espacio entre integrantes
            layout.addSpacing(20)

        layout.addSpacing(40)

        # Botón de volver
        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.setFont(QFont('Arial', 12))
        boton_volver.setFixedWidth(200)
        boton_volver.setMinimumHeight(40)
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)

        # Configurar el fondo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        self.setPalette(palette)

    def volver_inicio(self):
        self.parentWidget().setCurrentIndex(0)

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.pantalla_inicio = PantallaInicio(self)
        self.pantalla_grafo = GraphVisualization(self)
        self.pantalla_dijkstra = DijkstraApp(self)
        self.pantalla_integrantes = PantallaIntegrantes(self)

        self.addWidget(self.pantalla_inicio)
        self.addWidget(self.pantalla_grafo)
        self.addWidget(self.pantalla_dijkstra)
        self.addWidget(self.pantalla_integrantes)
        self.setCurrentIndex(0)

def tiempo_a_minutos(tiempo):
    minutos, segundos = map(int, tiempo.split(':'))
    return minutos + segundos / 60

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle('PackPath Lima')
    main_app.resize(800, 600)
    main_app.show()
    sys.exit(app.exec_())
