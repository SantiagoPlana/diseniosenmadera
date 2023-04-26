import inspect
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtPrintSupport import  QPrinter
from PyQt5.Qt import QFileInfo
import csv
import pandas as pd


class PedidoFinalizado(qtw.QDialog):
    """File dialog para presupuesto de venta."""

    def __init__(self, dic=dict):
        super().__init__(modal=True)
        self.setMinimumSize(400, 400)
        self.grid = qtw.QGridLayout()
        # self.grid.setRowStretch(1, 4)
        self.grid.setSpacing(18)
        self.dic = dic
        self.setLayout(self.grid)
        self.setWindowTitle('Presupuesto')
        self.pixmap = QPixmap('diseñosenmadera2.png')

        self.image = qtw.QLabel(self)
        self.image.setPixmap(self.pixmap)
        self.key = self.dic.keys()
        self.values = list(self.dic.values())
        date = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")

        self.accept_btn = qtw.QPushButton('Emitir', clicked=self.accept)
        self.cancel_btn = qtw.QPushButton('Cancelar', clicked=self.reject)
        self.print_btn = qtw.QPushButton('Exportar a PDF', clicked=self.guardar_pedido)

        # Layout
        self.grid.addWidget(
            qtw.QLabel('<h1>Presupuesto</h1>'), 1, 0
        )
        self.grid.addWidget(self.image, 1, 2, 1, 3)
        self.grid.addWidget(qtw.QLabel(
            f'<b>Fecha: {date}</b>'), 3, 0)
        self.grid.addWidget(qtw.QLabel(f"Cliente: <b>{self.dic['Cliente']}</b>"), 3, 1)
        self.grid.addWidget(qtw.QLabel(f"Contacto: <b>{self.dic['Contacto']}</b>"), 3, 2)
        if len(self.dic['Observaciones']) > 1:
            self.grid.addWidget(qtw.QLabel(f"Observaciones: \n{self.dic['Observaciones']}"), 4, 0)
        self.grid.addWidget(qtw.QLabel(f"<h4>Concepto: </h4>"), 6, 0)
        count = 8
        new_dic = {}
        for i in self.dic['Articulos']:
            if i not in new_dic:
                new_dic[i] = [1]
            else:
                new_dic[i][0] += 1
            idx = self.dic['Articulos'].index(i)
            if len(new_dic[i]) == 1:
                new_dic[i].append(self.dic['Precios'][idx])
            else:
                new_dic[i][1] += self.dic['Precios'][idx]
        for k, v in new_dic.items():
            self.grid.addWidget(
                qtw.QLabel(f'<b>{k}  x{v[0]}</b>'), count, 0)
            self.grid.addWidget(
                qtw.QLabel(f'{v[1]}'), count, 2)
            count += 1

        self.grid.addWidget(qtw.QLabel(' '), count, 0, 1, 4)
        # self.grid.addWidget(self.envio, count + 1, 0)
        self.grid.addWidget(qtw.QLabel(f"<b>{self.dic['Total']}</b>"), count+1, 2)
        self.grid.addWidget(qtw.QLabel(' '), count + 2, 0)
        self.grid.addWidget(self.accept_btn, count + 3, 0)
        self.grid.addWidget(self.cancel_btn, count + 3, 2)
        self.grid.addWidget(self.print_btn, count + 3, 1)

    def guardar_pedido(self):
        """Exportar a PDF"""

        filename, _ = qtw.QFileDialog.getSaveFileName(self,
                                                      'Exportar PDF',
                                                      None,
                                                      'PDF files (.pdf);;All Files (*)')
        if filename != '':
            if QFileInfo(filename).suffix() == '':
                filename += '.pdf'
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(filename)
                # printer = QPrinter()
                # printer.setOutputFormat(QPrinter.PdfFormat)
                # printer.setOutputFileName("Test.pdf")

                painter = QPainter(printer)
                xscale = printer.pageRect().width() / self.width()
                yscale = printer.pageRect().height() / self.height()
                scale = min(xscale, yscale)
                painter.translate(printer.paperRect().center())
                painter.scale(scale, scale)
                painter.translate((self.width() / 2) * -1, (self.height() / 2) * -1)

                self.render(painter)
                painter.end()


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
    float_signal = qtc.pyqtSignal(float)

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
        self.center()
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
        toolbar.addAction('Aplicar', self.porcentaje)
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

        # Widgets
        self.articulo = qtw.QLineEdit()
        self.envio = qtw.QLineEdit(placeholderText='Costo de envío')
        # self.articulo.setStyleSheet('font-size: 15px;')
        # self.articulo.setFixedWidth(150)
        self.filtrar_por = qtw.QComboBox()
        self.lista = qtw.QListWidget()
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')
        self.nombre_cliente = qtw.QLineEdit(placeholderText='Nombre del cliente')
        self.numero_cliente = qtw.QLineEdit(placeholderText='Número de teléfono')
        self.total = qtw.QLabel('Total: 0')

        # Status bar
        self.statusBar().showMessage('...')

        self.lista.setAlternatingRowColors(True)
        # Agregar categorías
        # self.lista.setFont()

        # Botones
        self.btn_agregar = qtw.QPushButton('Agregar Item')
        self.btn_agregar.setFixedWidth(100)
        self.btn_pedido = qtw.QPushButton('Finalizar Pedido')
        self.btn_eliminar = qtw.QPushButton('Eliminar')
        self.btn_porcentaje = qtw.QPushButton('Aplicar')
        # self.btn_cargar = qtw.QPushButton('Cargar Tabla')

        # Layout
        filter_widget.layout().addWidget(self.nombre_cliente, 1, 0)
        filter_widget.layout().addWidget(self.numero_cliente, 2, 0)
        filter_widget.layout().addWidget(self.lista, 3, 0, 1, 4)
        filter_widget.layout().addWidget(self.envio, 4, 0)
        filter_widget.layout().addWidget(self.total, 4, 1)
        filter_widget.layout().addWidget(self.btn_agregar, 5, 0)
        filter_widget.layout().addWidget(self.btn_eliminar, 5, 1)

        filter_widget.layout().addWidget(self.observaciones, 6, 0, 1, 4)
        filter_widget.layout().addWidget(self.btn_pedido, 7, 0)

        second_widget.layout().addWidget(qtw.QLabel('Filtro'), 1, 0)
        second_widget.layout().addWidget(self.articulo, 2, 0)
        second_widget.layout().addWidget(qtw.QLabel('Filtrar por'), 1, 1)
        second_widget.layout().addWidget(self.filtrar_por, 2, 1)

        # Proxy model
        self.filter_proxy_model = qtc.QSortFilterProxyModel()

        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.articulo.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        # Signals
        self.btn_agregar.clicked.connect(self.agregar_art)
        self.btn_eliminar.clicked.connect(self.eliminar_item)
        self.btn_pedido.clicked.connect(self.terminar_pedido)

        self.filtrar_por.currentTextChanged.connect(
            self.filter)

        # self.float_signal.connect(self.calcular_porcentaje)
        # End main UI code
        self.show()

    # Display method
    def center(self):
        geometry = self.frameGeometry()
        dsktp_geo = qtw.QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(dsktp_geo)
        self.move(geometry.topLeft())

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
            # self.tableview.resizeRowsToContents()
            self.tableview.resizeColumnsToContents()

    def cargar_tabla_ventas(self):
        filename = 'Ventas_nuevo.csv'
        self.model = CsvTableModel(filename)
        self.filter_proxy_model.setSourceModel(self.model)
        self.tableview.setModel(self.filter_proxy_model)
        self.filtrar_por.clear()
        self.filtrar_por.addItems(self.model._headers)
        self.statusBar().showMessage('Tabla de ventas')

        self.tableview.resizeRowsToContents()

    def save_file(self):
        if self.model:
            self.model.save_data()
            self.statusBar().showMessage('Archivo guardado correctamente', 1000)

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
    def limpiar_campos(self):
        self.lista.clear()
        self.total.setText('Total: 0')
        self.nombre_cliente.clear()
        self.numero_cliente.clear()
        self.envio.clear()
        self.observaciones.setPlainText('')

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
                self.total.setText(f"Total: {total}")
                self.llenar_lista()
            except Exception as e:
                if 'string' in str(e):
                    msg = qtw.QMessageBox()
                    msg.setIcon(qtw.QMessageBox.Critical)
                    # msg.setText('Error')
                    msg.setText('Seleccione un modelo y el precio deseado')
                    msg.setWindowTitle('Error')
                    msg.exec_()
                else:
                    self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[0].data()))
                    self.pedidos['Articulos'].append(self.tableview.selectedIndexes()[1].data())
                    total = sum(self.pedidos['Precios'])
                    self.pedidos['Total'] = total
                    self.total.setText(f"Total: {total}")
                    self.llenar_lista()

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
            if self.envio.text():
                self.pedidos['Articulos'].append('Envío')
                self.pedidos['Precios'].append(float(self.envio.text()))
                self.pedidos['Total'] += float(self.envio.text())
            self.limpiar_campos()
            self.cargar_venta()
            self.detalle(self.pedidos)

    def cargar_venta(self):
        ventas = pd.read_csv('Ventas_nuevo.csv')
        # ventas.loc[len(ventas) + 1, self.pedidos.keys()] = self.pedidos.values()
        row = len(ventas)
        for k, v in self.pedidos.items():
            try:
                ventas.at[row, k] = v
            except Exception as e:
                pass
        if 'Unnamed: 0' in ventas.columns:
            ventas.drop('Unnamed: 0', axis=1, inplace=True)
        ventas.fillna(value='Sin Detalle', axis=0, inplace=True)
        ventas.to_csv('Ventas_nuevo.csv', index=False)

        self.statusBar().showMessage('Venta cargada correctamente', 2000)

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
        if data:
            print(data)
            del(self.pedidos['Articulos'][row])
            del(self.pedidos['Precios'][row])
            total1 = sum(self.pedidos['Precios'])
            self.pedidos['Total'] = total1
            self.total.setText(f"Total: {total1}")
            self.llenar_lista()

    def porcentaje(self):
        user_input = qtw.QInputDialog()
        porcentaje, ok = user_input.getInt(self,
                                           'Porcentaje',
                                           'Porcentaje: ',
                                           qtw.QLineEdit.Normal,
                                           0, 100)
        # user_input.setDoubleDecimals(10)

        if porcentaje and ok:
            print(porcentaje)
            self.calcular_porcentaje(porcentaje)

    def calcular_porcentaje(self, porcentaje):
        idxs = self.tableview.selectedIndexes()
        # self.tableview.indexAt()
        if idxs:
            msg = qtw.QMessageBox()
            msg.setText(f'¿Está seguro de que desea modificar {len(idxs)} elementos?')
            msg.setWindowTitle(' ')
            msg.exec_()
            if msg.sender():
                print('Accepted')
                for idx in idxs:
                    row = idx.row()
                    col = idx.column()
                    idx = float(idx.data())
                    porcentaje = porcentaje / 100
                    nuevo_precio = idx + (idx * porcentaje)
                    # print(nuevo_precio)
                    self.model._data[row][col] = nuevo_precio
                self.statusBar().showMessage('Valores modificados correctamente.', 10000)

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