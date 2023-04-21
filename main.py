import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap
import csv
import pandas as pd


class PedidoFinalizado(qtw.QDialog):
    """File dialog for finished sale."""

    def __init__(self, dic=dict):
        super().__init__(modal=True)
        self.setMinimumSize(400, 400)
        grid = qtw.QGridLayout()
        h_box = qtw.QHBoxLayout()
        self.dic = dic
        self.setLayout(grid)
        self.setWindowTitle('Presupuesto')
        self.pixmap = QPixmap('diseñosenmadera1.png')
        self.image = qtw.QLabel(self)
        self.image.setPixmap(self.pixmap)
        self.image.setFixedSize(550, 140)
        self.key = self.dic.keys()
        self.values = list(self.dic.values())
        date = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")
        time = qtc.QTime().currentTime().toString('hh:mm')

        self.accept_btn = qtw.QPushButton('Emitir')
        self.cancel_btn = qtw.QPushButton('Cancelar', clicked=self.reject)

        # Layout
        grid.addWidget(
            qtw.QLabel('<h1>Presupuesto</h1>'), 1, 0
        )
        grid.addWidget(self.image, 2, 0, 1, 3)
        grid.addWidget(qtw.QLabel(
            f'<h3>Fecha: {date}</h3>'), 3, 0)
        grid.addWidget(qtw.QLabel(f"<h3>Cliente: {self.dic['Cliente']}</h3>"), 3, 1)
        grid.addWidget(qtw.QLabel(f"<h3>Contacto: {self.dic['Contacto']}</h3>"), 3, 2)
        grid.addWidget(qtw.QLabel(f"<h4>Concepto: </h4>"), 5, 0)
        count = 6
        for i in range(len(self.dic['Articulos'])):
            # self.layout().setHorizontalSpacing(200)
            grid.addWidget(
                qtw.QLabel(f'{self.dic["Articulos"][i]}'), count, 0)
            grid.addWidget(
                qtw.QLabel(f'{self.dic["Precios"][i]}'), count, 2)
            count += 1
        grid.addWidget(qtw.QLabel(' '), count, 0, 1, 4)
        grid.addWidget(qtw.QLabel(f"<b>Total:  {self.dic['Total']}</b>"), count+1, 2)
        grid.addWidget(qtw.QLabel(' '), count + 2, 0)
        grid.addWidget(self.accept_btn, count + 3, 0)
        grid.addWidget(self.cancel_btn, count + 3, 0)

    def agregate_items(self):
        item_dic = {}
        for i in self.dic['Articulos']:
            if not i in item_dic:
                item_dic[i] = 1
            else:
                item_dic[i] += 1



class CsvTableModel(qtc.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename, encoding='utf-8') as fh:
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
            self._data[index.row()][index.column()] = value.encode('latin-1')
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
            del (self._data[position])
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
    pedidos = {'Fecha': '',
               'Cliente': '',
               'Contacto': '',
               'Articulos': [],
               'Precios': [],
               'Total': 0,
               'Observaciones': ''}

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
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

        # Main UI
        self.setWindowTitle('Diseños en Madera')
        self.resize(1380, 600)
        self.tableview = qtw.QTableView()
        self.tableview.setSortingEnabled(True)
        self.tableview.setAlternatingRowColors(True)
        self.setCentralWidget(self.tableview)

        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu('Archivo')
        file_menu.addAction('Abrir', self.select_file)
        file_menu.addAction('Guardar', self.save_file)

        edit_menu = menu.addMenu('Editar')
        edit_menu.addAction('Insertar Arriba', self.insert_above)
        edit_menu.addAction('Insertar abajo', self.insert_below)
        edit_menu.addAction('Eliminar fila(s)', self.remove_rows)

        toolbar = self.addToolBar('Barra de tareas')
        open_ventas = toolbar.addAction('Cargar Ventas', self.cargar_tabla_ventas)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(qtc.Qt.TopToolBarArea)

        # Dock widgets
        grid_1 = qtw.QGridLayout()
        grid_2 = qtw.QGridLayout()

        dock = qtw.QDockWidget('Pedido')
        dock2 = qtw.QDockWidget('Filtros')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, dock2)
        self.setDockNestingEnabled(True)
        # dock2 = qtw.QDockWidget('Filtros')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, dock)
        filter_widget = qtw.QWidget()
        filter_widget.setLayout(grid_1)
        second_widget = qtw.QWidget()
        second_widget.setLayout(grid_2)
        dock.setWidget(filter_widget)
        dock2.setWidget(second_widget)

        self.articulo = qtw.QLineEdit()
        # self.articulo.setStyleSheet('font-size: 15px;')
        self.articulo.setFixedWidth(150)
        # self.material = qtw.QComboBox()
        # self.modelo = qtw.QComboBox()
        self.filtrar_por = qtw.QComboBox()
        self.lista = qtw.QListWidget()
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')
        self.nombre_cliente = qtw.QLineEdit(placeholderText='Nombre del cliente')
        self.numero_cliente = qtw.QLineEdit(placeholderText='Número de teléfono')
        self.total = qtw.QLabel('Total: 0')
        # Agregar categorías
        self.lista.setAlternatingRowColors(True)
        # self.lista.setFont()
        # Botones
        self.btn_agregar = qtw.QPushButton('Agregar Item')
        self.btn_agregar.setFixedWidth(100)
        self.btn_pedido = qtw.QPushButton('Finalizar Pedido')
        self.btn_eliminar = qtw.QPushButton('Eliminar')
        # self.btn_cargar = qtw.QPushButton('Cargar Tabla')

        filter_widget.layout().addWidget(self.nombre_cliente, 1, 0)
        filter_widget.layout().addWidget(self.numero_cliente, 2, 0)
        filter_widget.layout().addWidget(self.lista, 3, 0, 1, 4)
        filter_widget.layout().addWidget(self.total, 4, 0)
        filter_widget.layout().addWidget(self.btn_agregar, 5, 0)
        filter_widget.layout().addWidget(self.btn_eliminar, 5, 1)

        filter_widget.layout().addWidget(self.observaciones, 6, 0, 1, 4)
        filter_widget.layout().addWidget(self.btn_pedido, 7, 0)
        # second_widget.layout().addWidget(qtw.QLabel('Material'), 1, 1)
        # second_widget.layout().addWidget(self.material, 2, 1)
        second_widget.layout().addWidget(qtw.QLabel('Filtro'), 1, 0)
        second_widget.layout().addWidget(self.articulo, 2, 0)
        second_widget.layout().addWidget(qtw.QLabel('Filtrar por'), 1, 1)
        second_widget.layout().addWidget(self.filtrar_por, 2, 1)
        # second_widget.layout().addWidget(qtw.QLabel('Modelo'), 1, 3)

        self.filter_proxy_model = qtc.QSortFilterProxyModel()

        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.articulo.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        self.btn_agregar.clicked.connect(self.agregar_art)
        self.btn_eliminar.clicked.connect(self.eliminar_item)
        self.btn_pedido.clicked.connect(self.terminar_pedido)

        self.filtrar_por.currentTextChanged.connect(
            self.filter)

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
            self.filtrar_por.clear()
            self.filtrar_por.addItems(self.model._headers)

    def cargar_tabla_ventas(self):
        filename = 'Ventas_nuevo.csv'
        self.model = CsvTableModel(filename)
        self.filter_proxy_model.setSourceModel(self.model)
        self.tableview.setModel(self.filter_proxy_model)
        self.filtrar_por.clear()
        self.filtrar_por.addItems(self.model._headers)

    def save_file(self):
        if self.model:
            self.model.save_data()

    # Methods for insert/remove

    def insert_above(self):
        try:
            selected = self.tableview.selectedIndexes()
            row = selected[0].row() if selected else 0
            self.model.insertRows(row, 1, None)
        except Exception as e:
            pass

    def insert_below(self):
        try:
            selected = self.tableview.selectedIndexes()
            row = selected[-1].row() if selected else self.model.rowCount(None)
            self.model.insertRows(row + 1, 1, None)
        except Exception as e:
            pass

    def remove_rows(self):
        selected = self.tableview.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.model.removeRows(selected[0].row(), num_rows, None)

    # Form methods
    def llenar_lista(self):
        self.lista.clear()
        if len(self.pedidos['Articulos']) > 0:
            for i in range(len(self.pedidos['Articulos'])):
                self.lista.addItem(f"{self.pedidos['Articulos'][i]} --- {self.pedidos['Precios'][i]}")

    def agregar_art(self):
        global total
        if len(self.tableview.selectedIndexes()) == 2:
            try:
                self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[1].data()))
                self.pedidos['Articulos'].append(self.tableview.selectedIndexes()[0].data())
                total = sum(self.pedidos['Precios'])
                self.pedidos['Total'] = total
            except Exception as e:
                self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[0].data()))
                self.pedidos['Articulos'].append(self.tableview.selectedIndexes()[1].data())
                total = sum(self.pedidos['Precios'])
                self.pedidos['Total'] = total

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

        self.total.setText(f"Total: {total}")
        self.llenar_lista()

    def terminar_pedido(self):
        if len(self.pedidos['Articulos']) == 0:
            msg = qtw.QMessageBox()
            # msg.setIcon(qtw.QMessageBox.Critical)
            msg.setText('Seleccione al menos un artículo.')
            msg.setWindowTitle('Pedido vacío')
            print(len(self.nombre_cliente.text()))
            msg.exec_()
        elif len(self.nombre_cliente.text()) == 0 or len(self.numero_cliente.text()) == 0:
            msg = qtw.QMessageBox()
            # msg.setIcon(qtw.QMessageBox.Critical)
            msg.setText('Los datos están incompletos.')
            msg.setWindowTitle('Datos incompletos')
            # msg.addButton('Continuar', clicked=msg.accept)
            msg.exec_()
        else:
            self.pedidos['Fecha'] = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")
            self.pedidos['Cliente'] = self.nombre_cliente.text()
            self.pedidos['Contacto'] = self.numero_cliente.text()
            self.pedidos['Observaciones'] = self.observaciones.toPlainText()
            self.lista.clear()
            self.total.setText('Total: 0')
            self.nombre_cliente.clear()
            self.numero_cliente.clear()
            self.observaciones.setPlainText('')
            self.cargar_venta()
            self.detalle(self.pedidos)

    def cargar_venta(self):
        ventas = pd.read_csv('Ventas_nuevo.csv')
        # ventas.loc[len(ventas) + 1, self.pedidos.keys()] = self.pedidos.values()
        row = len(ventas)
        for k, v in self.pedidos.items():
            print(row)
            try:
                ventas.at[row, k] = v
            except Exception as e:
                pass
        if 'Unnamed: 0' in ventas.columns:
            ventas.drop('Unnamed: 0', axis=1, inplace=True)
        ventas.fillna(value='Sin Detalle', axis=0, inplace=True)
        ventas.to_csv('Ventas_nuevo.csv', index=False)

    def detalle(self, dic):
        """Instancia de clase de FileDialog con detalle de pedido"""
        dialog = PedidoFinalizado(dic)
        dialog.exec()
        for k in self.pedidos.keys():
            if k == 'Total':
                self.pedidos[k] = 0
            elif k == 'Articulos' or k == 'Precios':
                self.pedidos[k] = []
            else:
                self.pedidos[k] = ''

    def eliminar_item(self):
        row = self.lista.currentRow()
        data = self.lista.currentIndex().data()
        del(self.pedidos['Articulos'][row])
        del(self.pedidos['Precios'][row])
        self.llenar_lista()




    @qtc.pyqtSlot()
    def filter(self):
        index = self.filtrar_por.currentIndex()
        self.filter_proxy_model.setFilterKeyColumn(index)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())