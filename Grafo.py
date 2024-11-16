import sys
import pandas as pd
import numpy as np
import networkx as nx
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                           QStackedWidget, QGraphicsOpacityEffect, QMessageBox, 
                           QLineEdit, QTextEdit, QDialog)
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.lines import Line2D

class PantallaInicio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(1024, 768)
        self.initUI()

    def initUI(self):
        # Crear layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Crear y configurar el label de fondo
        self.fondo = QLabel(self)
        self.fondo.setAutoFillBackground(True)

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

    def actualizar_fondo(self):
        self.fondo.setGeometry(0, 0, self.width(), self.height())

        # Actualizar el tamaño y la imagen de fondo
        pixmap = QPixmap("C:/Users/Rodrigo/Documents/Python/proyectopruebas/delivery.jpg")
        scaled_pixmap = pixmap.scaled(
          self.size(),
          Qt.IgnoreAspectRatio,  # Changed from KeepAspectRatioByExpanding
          Qt.SmoothTransformation
    )
        self.fondo.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        # Llamar a la función de actualizar fondo cuando se cambia el tamaño de la ventana
        super().resizeEvent(event)
        self.actualizar_fondo()

    def mostrar_grafo(self):
        self.parentWidget().setCurrentIndex(1)

    def aplicar_dijkstra(self):
        self.parentWidget().setCurrentIndex(2)

    def aplicar_bellman_ford(self):
        self.parentWidget().setCurrentIndex(3)

    def mostrar_integrantes(self):
        self.parentWidget().setCurrentIndex(4)  # Índice de la pantalla de integrantes

class GraphVisualization(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.figure = plt.Figure(figsize=(14, 10))  # Ajuste del tamaño para mejor visualización
        self.canvas = FigureCanvas(self.figure)
        self.initUI()
        self.cargar_y_visualizar_datos()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Título de la visualización
        titulo = QLabel('Visualización del Grafo de Entregas')
        titulo_font = QFont('Helvetica', 16, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00FFFF;")  # Color cian
        layout.addWidget(titulo)

        # Establecer fondo oscuro para toda la ventana
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(43, 43, 43))  # Color oscuro para todo el fondo
        self.setPalette(palette)

        # Canvas para el gráfico
        layout.addWidget(self.canvas)

        # Botón de volver
        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def cargar_y_visualizar_datos(self):
        try:
            # Limpiar la figura
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_title('Grafo Completo de Entregas de Paquetes', color='white')

            # Cargar datos
            self.df = pd.read_csv('lima_delivery_network4.csv')

            # Crear el grafo
            G = nx.DiGraph()

            # Añadir nodos y aristas
            nodos = set(self.df['Origen'].unique()) | set(self.df['Destino'].unique())
            G.add_nodes_from(nodos)

            for _, row in self.df.iterrows():
                origen = row['Origen']
                destino = row['Destino']
                tiempo = tiempo_a_minutos(row['Tiempo_Recorrido'])
                costo = row['Costo']
                G.add_edge(origen, destino, weight=tiempo, cost=costo)

            # Calcular el layout del grafo
            pos = nx.spring_layout(G, k=0.5, iterations=50)

            # Dibujar nodos del grafo
            nx.draw_networkx_nodes(G, pos, node_color='#00FFFF', node_size=120, ax=ax)

            # Dibujar todas las aristas del grafo
            nx.draw_networkx_edges(G, pos, edge_color='grey', arrows=True, alpha=0.7, ax=ax)

            # Configuración del fondo y del gráfico
            ax.set_facecolor('#2B2B2B')  # Fondo oscuro para el gráfico
            self.figure.patch.set_facecolor('#2B2B2B')

            # Ajustes de ejes
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

            # Actualizar el canvas
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar o visualizar los datos: {str(e)}')

    def volver_inicio(self):
        self.parentWidget().setCurrentIndex(0)

class DijkstraApp(QWidget):
    def __init__(self, parent=None, fig_width=12, fig_height=8):
        super().__init__(parent)
        self.G = nx.DiGraph()
        self.df = pd.DataFrame()
        self.node_positions = {}
        self.ruta_tiempo = []
        self.ruta_costo = []
        self.fig_width = fig_width  # Ancho de la figura
        self.fig_height = fig_height  # Alto de la figura
        self.rutas_calculadas = False 
        self.initUI()
        self.cargar_datos()
        
        # Configurar el fondo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))  # Fondo oscuro
        self.setPalette(palette)

    def cargar_datos(self):
        try:
            file_path = 'lima_delivery_network4.csv'
            self.df = pd.read_csv(file_path)
            self.G = nx.DiGraph()

            # Limitar el número de nodos si es necesario
            nodos_origen = set(self.df['Origen'])  # Obtener nodos únicos de origen
            nodos_destino = set(self.df['Destino'])  # Obtener nodos únicos de destino

            if len(nodos_origen) > 1500:
                nodos_origen = set(list(nodos_origen)[:1500])
            if len(nodos_destino) > 1500:
                nodos_destino = set(list(nodos_destino)[:1500])

            # Filtrar el DataFrame para incluir solo los nodos seleccionados
            self.df = self.df[self.df['Origen'].isin(nodos_origen) & self.df['Destino'].isin(nodos_destino)]

            # Crear el grafo con los datos
            for _, row in self.df.iterrows():
                origen = row['Origen']
                destino = row['Destino']
                tiempo = tiempo_a_minutos(row['Tiempo_Recorrido'])
                costo = row['Costo']
                self.G.add_edge(origen, destino, weight=tiempo, cost=costo)

            # Calcular las posiciones de los nodos
            self.node_positions = nx.spring_layout(self.G, k=0.5, iterations=50)
            
            # Llenar los QComboBox después de cargar el grafo
            self.llenar_combo_nodos(nodos_origen, nodos_destino)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar los datos: {str(e)}')

    def llenar_combo_nodos(self, nodos_origen, nodos_destino):
        # Agregar nodos de origen y destino al QComboBox respectivo
        self.origen_entry.addItems(sorted(nodos_origen))  # Ordenar y agregar nodos de origen
        self.destino_entry.addItems(sorted(nodos_destino))  # Ordenar y agregar nodos de destino

    def initUI(self):
        layout = QVBoxLayout()

        # Título con estilo de color
        titulo = QLabel('Algoritmo de Dijkstra - Cálculo de Rutas')
        titulo_font = QFont('Arial Black', 20, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00FFFF;")  # Color cian
        layout.addWidget(titulo)

        layout.addSpacing(20)

        # Entrada para el origen y el destino con estilo de color y diseño
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        origen_label = QLabel('Nodo de origen:')
        origen_label.setStyleSheet("color: white; font-size: 14px;")
        
        # Usar QComboBox para origen
        self.origen_entry = QComboBox()
        self.origen_entry.setStyleSheet("""
            QComboBox {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(origen_label)
        input_layout.addWidget(self.origen_entry)

        destino_label = QLabel('Nodo de destino:')
        destino_label.setStyleSheet("color: white; font-size: 14px;")
        
        # Usar QComboBox para destino
        self.destino_entry = QComboBox()
        self.destino_entry.setStyleSheet("""
            QComboBox {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(destino_label)
        input_layout.addWidget(self.destino_entry)

        layout.addWidget(input_widget)

        # Botón "Calcular Rutas" con estilo
        self.calcular_button = QPushButton('Calcular Rutas')
        self.calcular_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.calcular_button.clicked.connect(self.calcular_rutas)
        layout.addWidget(self.calcular_button)

         # Nuevo botón "Mostrar Todas las Rutas" con estilo similar
        self.mostrar_todas_button = QPushButton('Mostrar Todas las Rutas')
        self.mostrar_todas_button.setStyleSheet("""
           QPushButton {
               background-color: rgba(0, 255, 255, 180);
               color: black;
               border: 2px solid #008B8B;
               border-radius: 15px;
               padding: 10px;
               font-size: 14px;
               font-weight: bold;
           }
           QPushButton:hover {
               background-color: rgba(0, 139, 139, 180);
               color: white;
           }
            QPushButton:disabled {
               background-color: rgba(128, 128, 128, 180);
               border: 2px solid #666666;
               color: #444444;
           }
           """)
        self.mostrar_todas_button.clicked.connect(self.mostrar_todas_rutas)
        self.mostrar_todas_button.setEnabled(False)  
        layout.addWidget(self.mostrar_todas_button)

        # Botón "Visualizar Ruta Corta" con estilo
        self.visualizar_ruta_corta_button = QPushButton('Visualizar Ruta Corta')
        self.visualizar_ruta_corta_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.visualizar_ruta_corta_button.clicked.connect(self.visualizar_ruta_corta)
        layout.addWidget(self.visualizar_ruta_corta_button)

        # Botón "Visualizar Ruta Barata" con estilo
        self.visualizar_ruta_barata_button = QPushButton('Visualizar Ruta Barata')
        self.visualizar_ruta_barata_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.visualizar_ruta_barata_button.clicked.connect(self.visualizar_ruta_barata)
        layout.addWidget(self.visualizar_ruta_barata_button)

        # Área de resultados con estilo y altura limitada
        self.resultado_label = QTextEdit()
        self.resultado_label.setReadOnly(True)
        self.resultado_label.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.resultado_label.setMaximumHeight(120)  # Limitar la altura del área de resultados
        layout.addWidget(self.resultado_label)

        # Nueva área para mostrar todas las rutas
        self.todas_rutas_label = QTextEdit()
        self.todas_rutas_label.setReadOnly(True)
        self.todas_rutas_label.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
         """)
        self.todas_rutas_label.setMaximumHeight(200)  # Altura máxima para la lista de rutas
        self.todas_rutas_label.hide()  # Inicialmente oculto
        layout.addWidget(self.todas_rutas_label)

        # Canvas para el gráfico con tamaño ajustable
        self.figure = plt.Figure(figsize=(14, 10))  # Tamaño de la figura aumentado
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        layout.addSpacing(20)

        # Botón "Volver al Inicio" con estilo
        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def calcular_rutas(self):
        origen = self.origen_entry.currentText()
        destino = self.destino_entry.currentText()

        if not origen or not destino:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese origen y destino')
            return
        
        if origen not in self.G or destino not in self.G:
            QMessageBox.warning(self, 'Error', 'Origen o destino no encontrado en el grafo')
            return

        try:
            self.ruta_tiempo = nx.shortest_path(self.G, origen, destino, weight='weight')
            self.ruta_costo = nx.shortest_path(self.G, origen, destino, weight='cost')

            tiempo_total = sum(self.G[self.ruta_tiempo[i]][self.ruta_tiempo[i+1]]['weight'] for i in range(len(self.ruta_tiempo)-1))
            costo_total = sum(self.G[self.ruta_costo[i]][self.ruta_costo[i+1]]['cost'] for i in range(len(self.ruta_costo)-1))

            resultado = (f"Ruta más corta:\nTiempo total: {tiempo_total:.2f} minutos\nRecorrido: {' -> '.join(self.ruta_tiempo)}\n\n"
                         f"Ruta más barata:\nCosto total: S/. {costo_total:.2f}\nRecorrido: {' -> '.join(self.ruta_costo)}")
            self.resultado_label.setText(resultado)

            # Establecer el estado de rutas calculadas a True
            self.rutas_calculadas = True
            self.mostrar_todas_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al calcular las rutas: {str(e)}')
            self.rutas_calculadas = False
            self.mostrar_todas_button.setEnabled(False)
  
    def mostrar_todas_rutas(self):
        if not self.rutas_calculadas:
            QMessageBox.warning(self, 'Advertencia', 'Calcule las rutas primero.')
            return

        origen = self.origen_entry.currentText()
        destino = self.destino_entry.currentText()
        texto_resultado = "Todas las rutas:\n"

        try:
            for idx, ruta in enumerate(nx.all_simple_paths(self.G, origen, destino), start=1):
                tiempo = sum(self.G[ruta[i]][ruta[i + 1]]['weight'] for i in range(len(ruta) - 1))
                costo = sum(self.G[ruta[i]][ruta[i + 1]]['cost'] for i in range(len(ruta) - 1))
                texto_resultado += f"Ruta {idx}: {' -> '.join(ruta)}\nTiempo: {tiempo:.2f} min, Costo: S/. {costo:.2f}\n\n"
                if idx >= 50:
                    texto_resultado += "Mostrando las primeras 50 rutas.\n"
                    break

            self.todas_rutas_label.setText(texto_resultado)
            self.todas_rutas_label.show()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al mostrar todas las rutas: {str(e)}')


    def visualizar_ruta_corta(self):
        if not self.rutas_calculadas:
           QMessageBox.warning(self, 'Advertencia', 'Primero debe calcular la ruta')
           return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Ruta Más Corta')

        # Obtener el nodo de origen y destino
        origen = self.ruta_tiempo[0]
        destino = self.ruta_tiempo[-1]

        # Nodos y aristas de la ruta más corta
        ruta_edges = list(zip(self.ruta_tiempo[:-1], self.ruta_tiempo[1:]))
        
        # Dibujar nodo de origen en color verde y nodo de destino en color rojo
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[origen], node_color='green', node_size=300, ax=ax)
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[destino], node_color='red', node_size=300, ax=ax)
        
        # Dibujar nodos intermedios en cian
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=self.ruta_tiempo[1:-1], node_color='cyan', node_size=200, ax=ax)
        
        # Dibujar aristas de la ruta en azul claro
        nx.draw_networkx_edges(self.G, self.node_positions, edgelist=ruta_edges, edge_color='lightblue', width=2, ax=ax)
        
        # Etiquetas solo para los nodos de la ruta, con tamaño de letra reducido
        ruta_labels = {node: node for node in self.ruta_tiempo}
        nx.draw_networkx_labels(self.G, self.node_positions, labels=ruta_labels, font_size=8, ax=ax)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Origen (Verde)', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Destino (Rojo)', markerfacecolor='red', markersize=10),
            Line2D([0], [0], color='lightblue', lw=2, label='Ruta más corta (Cian)')
        ]
        ax.legend(handles=legend_elements, loc='lower left')
        self.canvas.draw()

    def visualizar_ruta_barata(self):
        if not self.rutas_calculadas:
           QMessageBox.warning(self, 'Advertencia', 'Primero debe calcular la ruta')
           return
    
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Ruta Más Barata')

        # Obtener el nodo de origen y destino
        origen = self.ruta_costo[0]
        destino = self.ruta_costo[-1]

        # Nodos y aristas de la ruta más barata
        ruta_edges = list(zip(self.ruta_costo[:-1], self.ruta_costo[1:]))
        
        # Dibujar nodo de origen en color verde y nodo de destino en color rojo
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[origen], node_color='green', node_size=300, ax=ax)
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[destino], node_color='red', node_size=300, ax=ax)
        
        # Dibujar nodos intermedios en verde
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=self.ruta_costo[1:-1], node_color='lime', node_size=200, ax=ax)
        
        # Dibujar aristas de la ruta en verde oscuro
        nx.draw_networkx_edges(self.G, self.node_positions, edgelist=ruta_edges, edge_color='darkgreen', width=2, ax=ax)
        
        # Etiquetas solo para los nodos de la ruta, con tamaño de letra reducido
        ruta_labels = {node: node for node in self.ruta_costo}
        nx.draw_networkx_labels(self.G, self.node_positions, labels=ruta_labels, font_size=8, ax=ax)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Origen (Verde)', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Destino (Rojo)', markerfacecolor='red', markersize=10),
            Line2D([0], [0], color='darkgreen', lw=2, label='Ruta más barata (Verde)')
        ]
        ax.legend(handles=legend_elements, loc='lower left')
        self.canvas.draw()

    def volver_inicio(self):
        self.parentWidget().setCurrentIndex(0)

# Nueva clase para la Pantalla del Algoritmo Bellman-Ford
class BellmanFordApp(QWidget):
    def __init__(self, parent=None, fig_width=12, fig_height=8):
        super().__init__(parent)
        self.G = nx.DiGraph()
        self.df = pd.DataFrame()
        self.node_positions = {}
        self.ruta_tiempo = []
        self.ruta_costo = []
        self.fig_width = fig_width  # Ancho de la figura
        self.fig_height = fig_height  # Alto de la figura
        self.rutas_calculadas = False
        self.initUI()
        self.cargar_datos()
        
        # Configurar el fondo
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 40, 40))  # Fondo oscuro
        self.setPalette(palette)

    def cargar_datos(self):
        try:
            file_path = 'lima_delivery_network4.csv'
            self.df = pd.read_csv(file_path)
            self.G = nx.DiGraph()

            # Limitar el número de nodos si es necesario
            nodos_origen = set(self.df['Origen'])  # Obtener nodos únicos de origen
            nodos_destino = set(self.df['Destino'])  # Obtener nodos únicos de destino

            if len(nodos_origen) > 1500:
                nodos_origen = set(list(nodos_origen)[:1500])
            if len(nodos_destino) > 1500:
                nodos_destino = set(list(nodos_destino)[:1500])

            # Filtrar el DataFrame para incluir solo los nodos seleccionados
            self.df = self.df[self.df['Origen'].isin(nodos_origen) & self.df['Destino'].isin(nodos_destino)]

            # Crear el grafo con los datos
            for _, row in self.df.iterrows():
                origen = row['Origen']
                destino = row['Destino']
                tiempo = tiempo_a_minutos(row['Tiempo_Recorrido'])
                costo = row['Costo']
                self.G.add_edge(origen, destino, weight=tiempo, cost=costo)

            # Calcular las posiciones de los nodos
            self.node_positions = nx.spring_layout(self.G, k=0.5, iterations=50)
            
            # Llenar los QComboBox después de cargar el grafo
            self.llenar_combo_nodos(nodos_origen, nodos_destino)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al cargar los datos: {str(e)}')

    def llenar_combo_nodos(self, nodos_origen, nodos_destino):
        # Agregar nodos de origen y destino al QComboBox respectivo
        self.origen_entry.addItems(sorted(nodos_origen))  # Ordenar y agregar nodos de origen
        self.destino_entry.addItems(sorted(nodos_destino))  # Ordenar y agregar nodos de destino

    def initUI(self):
        layout = QVBoxLayout()

        # Título con estilo de color
        titulo = QLabel('Algoritmo de Bellman-Ford - Cálculo de Rutas')
        titulo_font = QFont('Arial Black', 20, QFont.Bold)
        titulo.setFont(titulo_font)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #00FFFF;")  # Color cian
        layout.addWidget(titulo)

        layout.addSpacing(20)

        # Entrada para el origen y el destino con estilo de color y diseño
        input_widget = QWidget()
        input_layout = QVBoxLayout()
        input_widget.setLayout(input_layout)

        origen_label = QLabel('Nodo de origen:')
        origen_label.setStyleSheet("color: white; font-size: 14px;")
        
        # Usar QComboBox para origen
        self.origen_entry = QComboBox()
        self.origen_entry.setStyleSheet("""
            QComboBox {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(origen_label)
        input_layout.addWidget(self.origen_entry)

        destino_label = QLabel('Nodo de destino:')
        destino_label.setStyleSheet("color: white; font-size: 14px;")
        
        # Usar QComboBox para destino
        self.destino_entry = QComboBox()
        self.destino_entry.setStyleSheet("""
            QComboBox {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(destino_label)
        input_layout.addWidget(self.destino_entry)

        layout.addWidget(input_widget)

        # Botón "Calcular Rutas" con estilo
        self.calcular_button = QPushButton('Calcular Rutas')
        self.calcular_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.calcular_button.clicked.connect(self.calcular_rutas)
        layout.addWidget(self.calcular_button)

         # Nuevo botón "Mostrar Todas las Rutas" con estilo similar
        self.mostrar_todas_button = QPushButton('Mostrar Todas las Rutas')
        self.mostrar_todas_button.setStyleSheet("""
           QPushButton {
               background-color: rgba(0, 255, 255, 180);
               color: black;
               border: 2px solid #008B8B;
               border-radius: 15px;
               padding: 10px;
               font-size: 14px;
               font-weight: bold;
           }
           QPushButton:hover {
               background-color: rgba(0, 139, 139, 180);
               color: white;
           }
            QPushButton:disabled {
               background-color: rgba(128, 128, 128, 180);
               border: 2px solid #666666;
               color: #444444;
           }
           """)
        self.mostrar_todas_button.clicked.connect(self.mostrar_todas_rutas)
        self.mostrar_todas_button.setEnabled(False)  
        layout.addWidget(self.mostrar_todas_button)

        # Botón "Visualizar Ruta Corta" con estilo
        self.visualizar_ruta_corta_button = QPushButton('Visualizar Ruta Corta')
        self.visualizar_ruta_corta_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.visualizar_ruta_corta_button.clicked.connect(self.visualizar_ruta_corta)
        layout.addWidget(self.visualizar_ruta_corta_button)

        # Botón "Visualizar Ruta Barata" con estilo
        self.visualizar_ruta_barata_button = QPushButton('Visualizar Ruta Barata')
        self.visualizar_ruta_barata_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        self.visualizar_ruta_barata_button.clicked.connect(self.visualizar_ruta_barata)
        layout.addWidget(self.visualizar_ruta_barata_button)

        # Área de resultados con estilo y altura limitada
        self.resultado_label = QTextEdit()
        self.resultado_label.setReadOnly(True)
        self.resultado_label.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.resultado_label.setMaximumHeight(120)  # Limitar la altura del área de resultados
        layout.addWidget(self.resultado_label)

        # Nueva área para mostrar todas las rutas
        self.todas_rutas_label = QTextEdit()
        self.todas_rutas_label.setReadOnly(True)
        self.todas_rutas_label.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
         """)
        self.todas_rutas_label.setMaximumHeight(200)  # Altura máxima para la lista de rutas
        self.todas_rutas_label.hide()  # Inicialmente oculto
        layout.addWidget(self.todas_rutas_label)

        # Canvas para el gráfico con tamaño ajustable
        self.figure = plt.Figure(figsize=(14, 10))  # Tamaño de la figura aumentado
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        layout.addSpacing(20)

        # Botón "Volver al Inicio" con estilo
        boton_volver = QPushButton("Volver al Inicio")
        boton_volver.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 255, 180);
                color: black;
                border: 2px solid #008B8B;
                border-radius: 15px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
                width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(0, 139, 139, 180);
                color: white;
            }
        """)
        boton_volver.clicked.connect(self.volver_inicio)
        layout.addWidget(boton_volver, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def calcular_rutas(self):
        origen = self.origen_entry.currentText()
        destino = self.destino_entry.currentText()

        if not origen or not destino:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese origen y destino')
            return
        
        if origen not in self.G or destino not in self.G:
            QMessageBox.warning(self, 'Error', 'Origen o destino no encontrado en el grafo')
            return

        try:
            # Calcular la ruta más corta basada en Bellman-Ford (por tiempo)
            self.ruta_tiempo = nx.bellman_ford_path(self.G, origen, destino, weight='weight')
            self.ruta_costo = nx.bellman_ford_path(self.G, origen, destino, weight='cost')

            tiempo_total = sum(self.G[self.ruta_tiempo[i]][self.ruta_tiempo[i+1]]['weight'] for i in range(len(self.ruta_tiempo)-1))
            costo_total = sum(self.G[self.ruta_costo[i]][self.ruta_costo[i+1]]['cost'] for i in range(len(self.ruta_costo)-1))

            resultado = (f"Ruta más corta:\nTiempo total: {tiempo_total:.2f} minutos\nRecorrido: {' -> '.join(self.ruta_tiempo)}\n\n"
                         f"Ruta más barata:\nCosto total: S/. {costo_total:.2f}\nRecorrido: {' -> '.join(self.ruta_costo)}")
            self.resultado_label.setText(resultado)

            self.rutas_calculadas = True
            self.mostrar_todas_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al calcular las rutas: {str(e)}')
            self.rutas_calculadas = False
            self.mostrar_todas_button.setEnabled(False)

    def mostrar_todas_rutas(self):
        if not self.rutas_calculadas:
            QMessageBox.warning(self, 'Advertencia', 'Calcule las rutas primero.')
            return

        origen = self.origen_entry.currentText()
        destino = self.destino_entry.currentText()
        texto_resultado = "Todas las rutas:\n"

        try:
            for idx, ruta in enumerate(nx.all_simple_paths(self.G, origen, destino), start=1):
                tiempo = sum(self.G[ruta[i]][ruta[i + 1]]['weight'] for i in range(len(ruta) - 1))
                costo = sum(self.G[ruta[i]][ruta[i + 1]]['cost'] for i in range(len(ruta) - 1))
                texto_resultado += f"Ruta {idx}: {' -> '.join(ruta)}\nTiempo: {tiempo:.2f} min, Costo: S/. {costo:.2f}\n\n"
                if idx >= 50:
                    texto_resultado += "Mostrando las primeras 50 rutas.\n"
                    break

            self.todas_rutas_label.setText(texto_resultado)
            self.todas_rutas_label.show()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al mostrar todas las rutas: {str(e)}')

    def visualizar_ruta_corta(self):
        if not self.rutas_calculadas:
           QMessageBox.warning(self, 'Advertencia', 'Primero debe calcular la ruta')
           return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Ruta Más Corta')

        # Obtener el nodo de origen y destino
        origen = self.ruta_tiempo[0]
        destino = self.ruta_tiempo[-1]

        # Nodos y aristas de la ruta más corta
        ruta_edges = list(zip(self.ruta_tiempo[:-1], self.ruta_tiempo[1:]))
        
        # Dibujar nodo de origen en color verde y nodo de destino en color rojo
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[origen], node_color='green', node_size=300, ax=ax)
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[destino], node_color='red', node_size=300, ax=ax)
        
        # Dibujar nodos intermedios en azul
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=self.ruta_tiempo[1:-1], node_color='skyblue', node_size=200, ax=ax)
        
        # Dibujar aristas de la ruta en azul oscuro
        nx.draw_networkx_edges(self.G, self.node_positions, edgelist=ruta_edges, edge_color='blue', width=2, ax=ax)
        
        # Etiquetas solo para los nodos de la ruta, con tamaño de letra reducido
        ruta_labels = {node: node for node in self.ruta_tiempo}
        nx.draw_networkx_labels(self.G, self.node_positions, labels=ruta_labels, font_size=8, ax=ax)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Origen (Verde)', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Destino (Rojo)', markerfacecolor='red', markersize=10),
            Line2D([0], [0], color='blue', lw=2, label='Ruta más corta (Azul)')
        ]
        ax.legend(handles=legend_elements, loc='lower left')

        self.canvas.draw()

    def visualizar_ruta_barata(self):
        if not self.rutas_calculadas:
           QMessageBox.warning(self, 'Advertencia', 'Primero debe calcular la ruta')
           return
    
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Ruta Más Barata')

        # Obtener el nodo de origen y destino
        origen = self.ruta_costo[0]
        destino = self.ruta_costo[-1]

        # Nodos y aristas de la ruta más barata
        ruta_edges = list(zip(self.ruta_costo[:-1], self.ruta_costo[1:]))
        
        # Dibujar nodo de origen en color verde y nodo de destino en color rojo
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[origen], node_color='green', node_size=300, ax=ax)
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=[destino], node_color='red', node_size=300, ax=ax)
        
        # Dibujar nodos intermedios en morado
        nx.draw_networkx_nodes(self.G, self.node_positions, nodelist=self.ruta_costo[1:-1], node_color='violet', node_size=200, ax=ax)
        
        # Dibujar aristas de la ruta en púrpura oscuro
        nx.draw_networkx_edges(self.G, self.node_positions, edgelist=ruta_edges, edge_color='purple', width=2, ax=ax)
        
        # Etiquetas solo para los nodos de la ruta, con tamaño de letra reducido
        ruta_labels = {node: node for node in self.ruta_costo}
        nx.draw_networkx_labels(self.G, self.node_positions, labels=ruta_labels, font_size=8, ax=ax)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Origen (Verde)', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Destino (Rojo)', markerfacecolor='red', markersize=10),
            Line2D([0], [0], color='purple', lw=2, label='Ruta más barata (Morado)')
        ]
        ax.legend(handles=legend_elements, loc='lower left')

        self.canvas.draw()

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
        self.pantalla_dijkstra = DijkstraApp(self, fig_width=15, fig_height=10)
        self.pantalla_bellman_ford = BellmanFordApp(self)
        self.pantalla_integrantes = PantallaIntegrantes(self)

        self.addWidget(self.pantalla_inicio)
        self.addWidget(self.pantalla_grafo)
        self.addWidget(self.pantalla_dijkstra)
        self.addWidget(self.pantalla_bellman_ford)
        self.addWidget(self.pantalla_integrantes)
        self.setCurrentIndex(0)

def tiempo_a_minutos(tiempo):
    minutos, segundos = map(int, tiempo.split(':'))
    return minutos + segundos / 60

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.setWindowTitle('PackPath Lima')
    main_app.resize(1024, 768)
    main_app.show()
    sys.exit(app.exec_())
