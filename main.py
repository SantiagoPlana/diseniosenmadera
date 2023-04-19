import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import csv


class PedidoFinalizado(qtw.QDialog):
    """File dialog for finished sale."""

    def __init__(self, dic=dict):
        super().__init__(modal=True)
        self.setMinimumSize(500, 400)
        v_box = qtw.QVBoxLayout()
        h_box = qtw.QHBoxLayout()
        self.dic = dic
        self.setLayout(v_box)
        self.setWindowTitle('Presupuesto')
        self.layout().addWidget(
            qtw.QLabel('<h1>Presupuesto</h1>'),
        )
        self.key = self.dic.keys()
        self.values = list(self.dic.values())
        date = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")
        time = qtc.QTime().currentTime().toString('hh:mm')
        self.layout().addWidget(qtw.QLabel(
            f'<h3>Fecha: {date} - {time}</h3>'))
        v_box.addLayout(h_box)
        h_box.addWidget(qtw.QLabel(f"<h3>Cliente: {self.dic['Cliente']}</h3>"))
        h_box.addWidget(qtw.QLabel(f"<h3>Contacto: {self.dic['Contacto']}</h3>"))
        v_box.addWidget(qtw.QLabel(f"<h4>Concepto: </h4>"))
        for i in range(len(self.dic['Artículos'])):
            # self.layout().setHorizontalSpacing(200)
            self.layout().addWidget(
                qtw.QLabel(f'{self.dic["Artículos"][i]}'))
            self.layout().addWidget(
                qtw.QLabel(f'{self.dic["Precios"][i]}'))
        self.layout().addWidget(qtw.QLabel(' '))
        self.layout().addWidget(qtw.QLabel(f"<b>Total:  {self.dic['Total']}</b>"))

        self.accept_btn = qtw.QPushButton('Emitir')
        self.cancel_btn = qtw.QPushButton('Cancelar', clicked=self.reject)
        self.layout().addWidget(self.accept_btn)
        self.layout().addWidget(self.cancel_btn)


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
            if not value:
                return False
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
    pedidos = {'Cliente': '',
               'Contacto': '',
               'Artículos': [],
               'Precios': [],
               'Total': 0,
               'Observaciones': ''}

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI
        self.setWindowTitle('Diseños en Madera')
        self.resize(1380, 600)
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
        dock2 = qtw.QDockWidget('Filtros')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, dock2)
        self.setDockNestingEnabled(True)
        # dock2 = qtw.QDockWidget('Filtros')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, dock)
        filter_widget = qtw.QWidget()
        filter_widget.setLayout(qtw.QVBoxLayout())
        second_widget = qtw.QWidget()
        second_widget.setLayout(qtw.QGridLayout())
        dock.setWidget(filter_widget)
        dock2.setWidget(second_widget)

        self.articulo = qtw.QLineEdit()
        self.articulo.setStyleSheet('font-size: 15px;')
        self.articulo.setFixedWidth(150)
        # self.material = qtw.QComboBox()
        # self.modelo = qtw.QComboBox()
        self.lista = qtw.QListWidget()
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')
        self.nombre_cliente = qtw.QLineEdit(placeholderText='Nombre del cliente')
        self.numero_cliente = qtw.QLineEdit(placeholderText='Número de teléfono')
        self.total = qtw.QLabel('Total: 0')
        # Agregar categorías
        # self.material.addItems(['Seleccione material...', 'Pino', 'Algarrobo'])
        # self.modelo.addItems(['Seleccione modelo...', 'Placard 1,80', 'Placard 1,40','Barra L', 'Barra Recta'])
        # self.articulo.addItems(['Seleccione artículo...', 'Placard', 'Barra'])

        self.lista.setAlternatingRowColors(True)
        # self.lista.setFont()
        # Botones
        self.btn_agregar = qtw.QPushButton('Agregar Item')
        self.btn_agregar.setFixedWidth(100)
        self.btn_pedido = qtw.QPushButton('Finalizar Pedido')
        self.btn_eliminar = qtw.QPushButton('Eliminar')
        # self.btn_cargar = qtw.QPushButton('Cargar Tabla')

        filter_widget.layout().addWidget(self.nombre_cliente)
        filter_widget.layout().addWidget(self.numero_cliente)
        filter_widget.layout().addWidget(self.lista)
        filter_widget.layout().addWidget(self.total)
        filter_widget.layout().addWidget(self.observaciones)
        filter_widget.layout().addWidget(self.btn_pedido)
        # second_widget.layout().addWidget(qtw.QLabel('Material'), 1, 1)
        # second_widget.layout().addWidget(self.material, 2, 1)
        second_widget.layout().addWidget(qtw.QLabel('Artículo'), 1, 0)
        second_widget.layout().addWidget(self.articulo, 2, 0)
        # second_widget.layout().addWidget(qtw.QLabel('Modelo'), 1, 3)

        # second_widget.layout().addWidget(self.modelo, 2, 3)

        second_widget.layout().addWidget(self.btn_agregar, 3, 0)
        # second_widget.layout().addWidget(self.btn_cargar, 3, 2)

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

        self.filter_proxy_model = qtc.QSortFilterProxyModel()

        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.articulo.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        # Signals

        self.btn_agregar.clicked.connect(self.agregar_art)
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
            self.filter_proxy_model.setSourceModel(self.model)
            self.tableview.setModel(self.filter_proxy_model)

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

    def filtering(self, tipo, material):
        self.model.itemData()

    # Form methods
    def populate_list(self):
        # self.lista.clear()
        for pedido in self.pedidos.get('Pedido', []):
            orden = (
                f"{pedido['Artículo']} ----  {pedido['Precio']}"
                # if pedido['Artículo']
                # else 'No hay artículos'
            )
            self.lista.addItem(f'{orden}')

    def agregar_item(self):
        pedido = {'Cliente': self.nombre_cliente.text(),
                  'Artículo': self.tableview.selectedIndexes()[0].data(),
                  'Precio': self.tableview.selectedIndexes()[1].data(),
                  'Observaciones': self.observaciones.toPlainText()
                  }
        articulos = []
        numero_pedido = self.lista.currentRow()
        print(numero_pedido)
        if numero_pedido == -1:
            articulos.append(pedido)
        else:
            articulos[numero_pedido] = pedido
        self.pedidos['Pedido'] = articulos
        # print(f'global: {self.pedidos}')
        # print(f'local: {pedido}')
        precio = float(self.total.text().split(':')[-1])
        total = precio + float(pedido['Precio'])
        print(total)
        self.total.setText(f"Total: {total}")
        self.populate_list()

    def llenar_lista(self):
        # print('hey')
        self.lista.clear()
        for i in range(len(self.pedidos['Artículos'])):

            self.lista.addItem(f"{self.pedidos['Artículos'][i]} --- {self.pedidos['Precios'][i]}")

    def agregar_art(self):
        self.pedidos['Cliente'] = self.nombre_cliente.text()
        self.pedidos['Contacto'] = self.numero_cliente.text()
        len(self.tableview.selectedIndexes())
        if len(self.tableview.selectedIndexes()) == 2:
            self.pedidos['Artículos'].append(self.tableview.selectedIndexes()[0].data())
            self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[1].data()))

        elif len(self.tableview.selectedIndexes()) > 2:
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Critical)
            # msg.setText('Error')
            msg.setText('Seleccione solo un modelo y el precio deseado')
            msg.setWindowTitle('Error')
            msg.exec_()
        else:
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Critical)
            # msg.setText('Error')
            msg.setText('Seleccione un modelo y el precio deseado')
            msg.setWindowTitle('Error')
            msg.exec_()

        self.pedidos['Observaciones'] = self.observaciones.toPlainText()
        print(self.pedidos)
        # numero_pedido = self.lista.currentRow()
        total = sum(self.pedidos['Precios'])
        self.pedidos['Total'] = total

        #print(self.tableview.row)
        self.total.setText(f"Total: {total}")
        self.llenar_lista()


    def terminar_pedido(self):
        self.lista.clear()
        self.total.setText('Total: 0')
        self.nombre_cliente.clear()
        self.numero_cliente.clear()
        self.observaciones.setPlainText('')

        self.detalle(self.pedidos)

    def detalle(self, dic):
        """Instancia de clase de FileDialog con detalle de pedido"""
        dialog = PedidoFinalizado(dic)
        dialog.exec()
        self.pedidos['Cliente'] = ''
        self.pedidos['Contacto'] = ''
        self.pedidos['Artículos'] = []
        self.pedidos['Precios'] = []
        self.pedidos['Observaciones'] = ''
        self.pedidos['Total'] = 0
        # pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
