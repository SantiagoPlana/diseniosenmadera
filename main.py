import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

import csv


class CsvTableModel(qtc.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)

    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        # original if statement:
        # if role == qtc.Qt.DisplayRole:
        # Add EditRole so that the cell is not cleared when editing
        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):
            return self._data[index.row()][index.column()]

    # Additional features methods:

    def headerData(self, section, orientation, role):

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    # Methods for Read/Write

    def flags(self, index):
        return super().flags(index) | qtc.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    # Methods for inserting or deleting

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(
            parent or qtc.QModelIndex(),
            position,
            position + rows - 1
        )

        for i in range(rows):
            default_row = [''] * len(self._headers)
            self._data.insert(position, default_row)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(
            parent or qtc.QModelIndex(),
            position,
            position + rows - 1
        )
        for i in range(rows):
            del(self._data[position])
        self.endRemoveRows()

    # method for saving
    def save_data(self):
        # commented out code below to fix issue with additional lines being added after saving csv file from the window.
        # with open(self.filename, 'w', encoding='utf-8') as fh:
        with open(self.filename, 'w', newline='', encoding='utf-8') as fh:
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)


class MainWindow(qtw.QMainWindow):

    model = None
    pedidos = {}

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI
        self.setWindowTitle('Diseños en Madera')
        self.resize(1000, 600)
        self.tableview = qtw.QTableView()
        self.tableview.setSortingEnabled(True)
        self.tableview.setAlternatingRowColors(True)
        self.setCentralWidget(self.tableview)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        file_menu.addAction('Open', self.select_file)
        file_menu.addAction('Save', self.save_file)

        edit_menu = menu.addMenu('Edit')
        edit_menu.addAction('Insert Above', self.insert_above)
        edit_menu.addAction('Insert Below', self.insert_below)
        edit_menu.addAction('Remove Row(s)', self.remove_rows)

        # Dock widgets
        dock = qtw.QDockWidget('Pedido')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, dock)
        self.setDockNestingEnabled(True)
        dock2 = qtw.QDockWidget('Filtros')
        self.addDockWidget(qtc.Qt.TopDockWidgetArea, dock2)
        filter_widget = qtw.QWidget()
        filter_widget.setLayout(qtw.QVBoxLayout())
        second_widget = qtw.QWidget()
        second_widget.setLayout(qtw.QGridLayout())
        dock.setWidget(filter_widget)
        dock2.setWidget(second_widget)

        self.articulo = qtw.QComboBox()
        self.material = qtw.QComboBox()
        self.modelo = qtw.QComboBox()
        self.lista = qtw.QListWidget()
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')
        self.nombre_cliente = qtw.QLineEdit(placeholderText='Nombre del cliente')
        self.numero_cliente = qtw.QLineEdit(placeholderText='Número de teléfono')
        self.total = qtw.QLabel('Total: 0')
        # Agregar categorías
        self.material.addItems(
            ['Seleccione material...', 'Pino', 'Algarrobo']
        )
        self.modelo.addItems(['Seleccione modelo...', 'Placard 1,80', 'Placard 1,40',
                              'Barra L', 'Barra Recta'])
        self.articulo.addItems(['Seleccione artículo...', 'Placard', 'Barra'])

        # Botones
        self.btn_agregar = qtw.QPushButton('Agregar Item')
        self.btn_pedido = qtw.QPushButton('Finalizar Pedido')
        self.btn_eliminar = qtw.QPushButton('Eliminar')
        self.btn_cargar = qtw.QPushButton('Cargar Tabla')

        filter_widget.layout().addWidget(self.nombre_cliente)
        filter_widget.layout().addWidget(self.numero_cliente)
        filter_widget.layout().addWidget(self.lista)
        filter_widget.layout().addWidget(self.total)
        filter_widget.layout().addWidget(self.observaciones)
        filter_widget.layout().addWidget(self.btn_pedido)
        second_widget.layout().addWidget(qtw.QLabel('Material'), 1, 1)
        second_widget.layout().addWidget(self.material, 2, 1)
        second_widget.layout().addWidget(qtw.QLabel('Artículo'), 1, 2)
        second_widget.layout().addWidget(self.articulo, 2, 2)
        second_widget.layout().addWidget(qtw.QLabel('Modelo'), 1, 3)

        second_widget.layout().addWidget(self.modelo, 2, 3)

        second_widget.layout().addWidget(self.btn_agregar, 3, 1)
        second_widget.layout().addWidget(self.btn_cargar, 3, 2)

        # Password check
        password = ''
        while password != 'Ok':
            log_in, ok = qtw.QInputDialog.getText(self, "Ingreso",
                                                  "Contraseña:", qtw.QLineEdit.Password,
                                                  )
            if not ok:
                self.close()
                sys.exit()
            else:
                if log_in != '1':
                    qtw.QMessageBox.critical(self, 'Idiota', 'Contraseña incorrecta')
                else:
                    password = 'Ok'

        # Signals

        self.btn_agregar.clicked.connect(self.agregar_item)
        self.btn_pedido.clicked.connect(self.terminar_pedido)
        # End main UI code
        self.show()

    # File methods
    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            'Select a CSV file to open…',
            qtc.QDir.currentPath(),
            'CSV Files (*.csv) ;; All Files (*)'
        )
        if filename:
            self.model = CsvTableModel(filename)
            self.tableview.setModel(self.model)

    def save_file(self):
        if self.model:
            self.model.save_data()

    # Methods for insert/remove

    def insert_above(self):
        selected = self.tableview.selectedIndexes()
        row = selected[0].row() if selected else 0
        self.model.insertRows(row, 1, None)

    def insert_below(self):
        selected = self.tableview.selectedIndexes()
        row = selected[-1].row() if selected else self.model.rowCount(None)
        self.model.insertRows(row + 1, 1, None)

    def remove_rows(self):
        selected = self.tableview.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.model.removeRows(selected[0].row(), num_rows, None)

    # Form methods
    def populate_list(self):
        # self.lista.clear()
        cliente = self.nombre_cliente.text()
        for pedido in self.pedidos.get('Pedido', []):
            orden = (
                f"{pedido['Artículo']} ----  {pedido['Precio']}"
                if pedido['Artículo']
                else 'No hay artículos'
            )
            self.lista.addItem(f'{orden}')

    def agregar_item(self):
        pedido = {'Cliente': self.nombre_cliente.text(),
                  'Artículo': self.tableview.selectedIndexes()[0].data(),
                  'Precio': self.tableview.selectedIndexes()[1].data()}
        # id_us = int(self.tableview.model().data(pedido['Artículo']).toString())
        #print(len(self.tableview.selectedIndexes()))
        articulos = []
        numero_pedido = self.lista.currentRow()
        if numero_pedido == -1:
            articulos.append(pedido)
        else:
            articulos[numero_pedido] = pedido
        self.pedidos['Pedido'] = articulos
        self.populate_list()
        precio = float(self.total.text().split(':')[-1])
        print(precio)
        total = precio + float(pedido['Precio'])
        print(total)
        self.total.setText(f"Total: {total}")

    def terminar_pedido(self):
        self.lista.clear()
        self.total.setText('Total: ')


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
