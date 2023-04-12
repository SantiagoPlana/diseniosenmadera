import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class View(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.articulo = qtw.QComboBox()
        self.material = qtw.QComboBox()
        self.modelo = qtw.QComboBox()
        self.lista = qtw.QListWidget()
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')
        self.nombre_cliente = qtw.QLineEdit(placeholderText='Nombre del cliente')
        self.numero_cliente = qtw.QLineEdit(placeholderText='Número de teléfono')
        self.tableWidget = qtw.QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(5)

        # Botones
        self.btn_agregar = qtw.QPushButton('Agregar')
        self.btn_pedido = qtw.QPushButton('Hacer Pedido')

        main_layout = qtw.QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.tableWidget)
        # self.tableWidget.setSizePolicy(qtw.QSizePolicy.Expanding,
        #                               qtw.QSizePolicy.Expanding)

        right_layout = qtw.QVBoxLayout()
        right_layout.addWidget(qtw.QLabel('Lista'))
        right_layout.addWidget(self.lista)
        right_layout.addWidget(self.btn_pedido)
        main_layout.addLayout(right_layout)
        filtros = qtw.QGroupBox('Filtros')
        right_layout.addWidget(filtros)
        filtros_layout = qtw.QGridLayout()
        filtros.setLayout(filtros_layout)

        filtros_layout.addWidget(self.nombre_cliente, 1, 1, 1, 3)
        filtros_layout.addWidget(self.numero_cliente, 2, 1, 1, 3)
        filtros_layout.addWidget(self.material, 3, 1)
        filtros_layout.addWidget(self.articulo, 3, 2)
        filtros_layout.addWidget(self.modelo, 3, 3)
        filtros_layout.addWidget(self.observaciones, 4, 1, 1, 3)
        filtros_layout.addWidget(self.btn_agregar, 5, 1)


        # self.lista.setSizePolicy(qtw.QSizePolicy.Expanding,
        #                         qtw.QSizePolicy.Expanding)




class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.view = View()
        self.setCentralWidget(self.view)
        self.setWindowTitle('Diseños en Maderas')
        self.show()



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())