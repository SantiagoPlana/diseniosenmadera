import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap, QPainter, QDoubleValidator, QPalette, QColor
from PyQt5.QtPrintSupport import  QPrinter
from PyQt5.Qt import QFileInfo
import csv
import pandas as pd
from pdf import PDF, generate_pdf


class NuevoItemPino(qtw.QDialog):


    def __init__(self, lst):
        super().__init__()

        self.lst = lst
        self.box = qtw.QVBoxLayout()
        self.setLayout(self.box)

        self.l_miel = qtw.QLineEdit()
        self.cont_nat = qtw.QLineEdit()
        self.cont_miel = qtw.QLineEdit()
        self.cont_alg = qtw.QLineEdit()
        self.lista = qtw.QLineEdit()
        self.contado = qtw.QLineEdit()
        self.box.addWidget(qtw.QLabel('<b>Precios para pino</b>'))
        self.box.addWidget(qtw.QLabel('Lista con miel'))
        self.box.addWidget(self.l_miel)
        self.box.addWidget(qtw.QLabel('Contado natural'))
        self.box.addWidget(self.cont_nat)
        self.box.addWidget(qtw.QLabel('Contado con miel'))
        self.box.addWidget(self.cont_miel)
        self.box.addWidget(qtw.QLabel('Contado con algarrobo'))
        self.box.addWidget(self.cont_alg)
        self.box.addWidget(qtw.QLabel('<b>Precios para algarrobo</b>'))
        self.box.addWidget(qtw.QLabel('Precio de lista'))
        self.box.addWidget(self.lista)
        self.box.addWidget(qtw.QLabel('Precio de contado'))
        self.box.addWidget(self.contado)
        self.btn_agregar = qtw.QPushButton('Agregar')
        self.btn_cancelar = qtw.QPushButton('Cancelar')
        self.box.addWidget(self.btn_agregar)
        self.box.addWidget(self.btn_cancelar)

        self.onlyInt = QDoubleValidator()
        self.l_miel.setValidator(self.onlyInt)
        self.cont_nat.setValidator(self.onlyInt)
        self.cont_miel.setValidator(self.onlyInt)
        self.cont_alg.setValidator(self.onlyInt)
        self.lista.setValidator(self.onlyInt)
        self.contado.setValidator(self.onlyInt)

        self.l_miel.setText('0')
        self.cont_nat.setText('0')
        self.cont_miel.setText('0')
        self.cont_alg.setText('0')
        self.lista.setText('0')
        self.contado.setText('0')

        self.btn_agregar.clicked.connect(self.cargar)
        self.btn_cancelar.clicked.connect(self.close)

    @qtc.pyqtSlot()
    def cargar(self):
        self.lst_precios = [self.l_miel.text(), self.cont_nat.text(), self.cont_miel.text(),
                            self.cont_alg.text(),
                            self.lista.text(), self.contado.text()]
        for x in self.lst_precios:
            print(x)
            x = float(x)
            self.lst.append(x)
        print([type(x) for x in self.lst])
        stock = pd.read_csv('Stock.csv')
        stock.loc[-1, stock.columns] = self.lst
        stock.sort_values(by=['Material', 'Tipo de articulo'], inplace=True,
                          ignore_index=True, ascending=False)
        stock.to_csv('Stock.csv', index=False)
        msg = qtw.QMessageBox()
        msg.setWindowTitle(' ')
        msg.setText('Se cargó el producto con éxito.')
        msg.exec_()


class CargarStock(qtw.QDialog):
    """Dialog para carga de stock"""

    signalItemCargado = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setSizeGripEnabled(True)
        self.grid = qtw.QGridLayout()
        self.grid.setSpacing(18)
        self.setLayout(self.grid)
        self.setWindowTitle('Carga de stock')

        self.material = qtw.QComboBox()
        self.tipo = qtw.QLineEdit()
        self.modelo = qtw.QLineEdit()
        self.cantidad = qtw.QSpinBox()

        self.btn_cargar = qtw.QPushButton('Cargar artículos', clicked=self.cargar)
        self.btn_cancelar = qtw.QPushButton('Cancelar', clicked=self.close)

        self.grid.addWidget(qtw.QLabel("Material"), 1, 0)
        self.grid.addWidget(self.material, 2, 0)
        self.grid.addWidget(qtw.QLabel("Tipo de artículo"), 3, 0)
        self.grid.addWidget(self.tipo, 4, 0)
        self.grid.addWidget(qtw.QLabel('Modelo'), 5, 0)
        self.grid.addWidget(self.modelo, 6, 0)
        self.grid.addWidget(qtw.QLabel('Cantidad'), 1, 1)
        self.grid.addWidget(self.cantidad, 2, 1)
        self.grid.addWidget(self.btn_cargar, 7, 0)
        self.grid.addWidget(self.btn_cancelar, 7, 1)

        self.material.addItems(['Pino', 'Algarrobo'])

        self.filename = "Stock.csv"
        self.stock = pd.read_csv(self.filename)
        self.lista_tipos = self.stock['Tipo de articulo'].unique()
        self.lista_modelos = self.stock['Modelo']
        self.completer_tipo = qtw.QCompleter(self.lista_tipos, self)
        self.completer_tipo.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.completer_tipo.setFilterMode(qtc.Qt.MatchContains)
        self.tipo.setCompleter(self.completer_tipo)
        self.material.currentTextChanged.connect(self.set_complete_tipo)
        self.completer_tipo.activated.connect(self.set_complete_modelo)

        self.signalItemCargado.connect(self.msg_display)

        # self.completer_modelo = qtw.QCompleter(self.lista_modelos, self)
        # self.completer_modelo.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        # self.modelo.setCompleter(self.completer_modelo)

    @qtc.pyqtSlot(str)
    def set_complete_tipo(self, string=str):
        print('Signal!')
        subset = self.stock[self.stock['Material'] == string]['Tipo de articulo'].unique()
        self.completer_tipo = qtw.QCompleter(subset, self)
        self.completer_tipo.setFilterMode(qtc.Qt.MatchContains)
        self.completer_tipo.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.tipo.setCompleter(self.completer_tipo)
        self.completer_tipo.activated.connect(self.set_complete_modelo)

    @qtc.pyqtSlot(str)
    def set_complete_modelo(self, string=str):
        print('Signal!')
        subset = self.stock[self.stock['Tipo de articulo'] == string]['Modelo']
        completer = qtw.QCompleter(subset, self)
        completer.setFilterMode(qtc.Qt.MatchContains)
        completer.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.modelo.setCompleter(completer)

    def cargar(self):
        material = self.material.currentText()
        tipo = self.tipo.text()
        modelo = self.modelo.text()
        cantidad = self.cantidad.value()
        print(material, tipo, modelo, cantidad)
        if len(tipo) == 0 or len(modelo) == 0 or cantidad == 0:
            message = "Todos los campos deben estar completos"
            msg = qtw.QMessageBox()
            msg.setText(message)
            msg.setIcon(qtw.QMessageBox.Warning)
            msg.setWindowTitle('Datos insuficientes')
            msg.exec_()
        else:
            # stock = pd.read_csv(self.filename)
            subset = self.stock[(self.stock['Material'] == material) &
                           (self.stock['Tipo de articulo'] == tipo) & (self.stock['Modelo'] == modelo)]
            if subset.empty:
                msg = qtw.QMessageBox()
                msg.setWindowTitle(' ')
                msg.setText('No se encontraron artículos con esas características.'
                            '¿Desea añadirlo como un artículo nuevo? ')
                msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
                msg.setDefaultButton(qtw.QMessageBox.Ok)
                ret = msg.exec_()
                if ret == qtw.QMessageBox.Ok:
                    self.nuevo_articulo()
                else:
                    msg.close()
            else:
                index = subset.index[0]
                self.stock.loc[index, 'Cantidad'] += cantidad
                self.stock.to_csv(self.filename, index=False)
                self.signalItemCargado.emit(
                    f'{tipo} {modelo} de {material} x {cantidad} se cargó correctamente.'
                )

    @qtc.pyqtSlot(str)
    def msg_display(self, string):
        msg = qtw.QMessageBox()
        msg.setText(string)
        msg.setWindowTitle(' ')
        msg.setIcon(qtw.QMessageBox.NoIcon)
        msg.exec_()

    @qtc.pyqtSlot()
    def nuevo_articulo(self):
        material = self.material.currentText()
        tipo = self.tipo.text()
        modelo = self.modelo.text()
        cantidad = self.cantidad.value()
        lst = [material, tipo, modelo, cantidad]
        nuevo = NuevoItemPino(lst)
        nuevo.exec_()


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
        self.print_btn = qtw.QPushButton('Exportar a PDF')

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

        self.print_btn.clicked.connect(lambda: generate_pdf(self.dic, new_dic))

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

                painter = QPainter(printer)
                xscale = printer.pageRect().width() / self.width()
                yscale = (printer.pageRect().height() / self.height())
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
               'Tipo': [],
               'Modelo': [],
               'Articulos': [],
               'Precios': [],
               'Total': 0,
               'Observaciones': ''}

    msg_signal = qtc.pyqtSignal(str)

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
        toolbar.addAction('Abrir Ventas', self.cargar_tabla_ventas)
        toolbar.addAction('Abrir Stock', self.cargar_tabla_stock)
        toolbar.addAction('Aplicar porcentaje', self.porcentaje)
        toolbar.addAction('Cargar stock', self.cargar_stock)
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
        pedido_widget = qtw.QWidget()
        pedido_widget.setLayout(grid_1)
        filter_widget = qtw.QWidget()
        filter_widget.setLayout(grid_2)
        dock.setWidget(pedido_widget)
        dock2.setWidget(filter_widget)

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

        # Config
        self.lista.setAlternatingRowColors(True)
        self.lista.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
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
        pedido_widget.layout().addWidget(self.nombre_cliente, 1, 0)
        pedido_widget.layout().addWidget(self.numero_cliente, 2, 0)
        pedido_widget.layout().addWidget(self.lista, 3, 0, 1, 4)
        pedido_widget.layout().addWidget(self.envio, 4, 0)
        pedido_widget.layout().addWidget(self.total, 4, 1)
        pedido_widget.layout().addWidget(self.btn_agregar, 5, 0)
        pedido_widget.layout().addWidget(self.btn_eliminar, 5, 1)

        pedido_widget.layout().addWidget(self.observaciones, 6, 0, 1, 4)
        pedido_widget.layout().addWidget(self.btn_pedido, 7, 0)

        filter_widget.layout().addWidget(qtw.QLabel('Filtro'), 1, 0)
        filter_widget.layout().addWidget(self.articulo, 2, 0)
        filter_widget.layout().addWidget(qtw.QLabel('Filtrar por'), 1, 1)
        filter_widget.layout().addWidget(self.filtrar_por, 2, 1)

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
        self.tableview.resizeColumnToContents(5)

    def cargar_tabla_stock(self):
        filename = 'Stock.csv'
        self.model = CsvTableModel(filename)
        self.filter_proxy_model.setSourceModel(self.model)
        self.tableview.setModel(self.filter_proxy_model)
        self.filtrar_por.clear()
        self.filtrar_por.addItems(self.model._headers)
        self.statusBar().showMessage('Tabla de stock', 10000)
        self.tableview.resizeColumnsToContents()

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
        # self.lista.setPalette(QPalette.Window)
        # self.lista.setPalette(QPalette.color(QColor.red()))

    def agregar_art(self):
        global total
        if len(self.tableview.selectedIndexes()) == 2:
            try:
                item_idx = self.tableview.selectedIndexes()[0]
                row = item_idx.row()
                col = item_idx.column() - 1
                tipo = self.model._data[row][col]
                modelo = self.tableview.selectedIndexes()[0].data()
                art = tipo + ' ' + modelo
                self.pedidos['Tipo'].append(tipo)
                self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[1].data()))
                self.pedidos['Modelo'].append(modelo)
                self.pedidos['Articulos'].append(art)
                total = round(sum(self.pedidos['Precios']))
                self.pedidos['Total'] = total
                self.total.setText(f"Total: {total}")
                self.llenar_lista()
            except Exception as e:
                if len(self.tableview.selectedIndexes()) > 2:
                    msg = 'Seleccione solo un modelo y el precio deseado'
                    self.display_msg(msg, icon=qtw.QMessageBox.Warning,
                                     windowTitle='Demasiadas celdas seleccionadas')
                    print(e)
                elif len(self.tableview.selectedIndexes()) < 2:
                    msg = 'Seleccione un modelo y el precio deseado.'
                    self.display_msg(msg, icon=qtw.QMessageBox.Warning,
                                     windowTitle='Datos insuficientes')
                else:
                    item_idx = self.tableview.selectedIndexes()[1]
                    row = item_idx.row()
                    col = item_idx.column() - 1
                    tipo = self.model._data[row][col]
                    modelo = self.tableview.selectedIndexes()[1].data()
                    art = tipo + ' ' + modelo
                    self.pedidos['Tipo'].append(tipo)
                    self.pedidos['Precios'].append(float(self.tableview.selectedIndexes()[0].data()))
                    self.pedidos['Modelo'].append(modelo)
                    self.pedidos['Articulos'].append(art)
                    total = round(sum(self.pedidos['Precios']))
                    self.pedidos['Total'] = total
                    self.total.setText(f"Total: {total}")
                    self.llenar_lista()

    def terminar_pedido(self):
        if len(self.pedidos['Articulos']) == 0:
            msg = 'Seleccione al menos un artículo.'
            self.display_msg(msg, icon=qtw.QMessageBox.Warning, windowTitle='Pedido vacío')
        elif len(self.nombre_cliente.text()) == 0 or len(self.numero_cliente.text()) == 0:
            msg = 'Complete los datos del cliente antes de finalizar el pedido.'
            self.display_msg(msg, icon=qtw.QMessageBox.Warning, windowTitle='Datos incompletos')
        else:
            self.pedidos['Fecha'] = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")
            self.pedidos['Cliente'] = self.nombre_cliente.text()
            self.pedidos['Contacto'] = self.numero_cliente.text()
            self.pedidos['Observaciones'] = self.observaciones.toPlainText()
            if self.envio.text():
                self.pedidos['Tipo'].append('Envío')
                self.pedidos['Modelo'].append('Envío')
                self.pedidos['Articulos'].append('Envío')
                self.pedidos['Precios'].append(float(self.envio.text()))
                self.pedidos['Total'] += float(self.envio.text())
            self.limpiar_campos()
            self.cargar_venta()
            self.descontar_stock()
            self.detalle(self.pedidos)

    def descontar_stock(self):
        new_dic = {}
        stock = pd.read_csv('Stock.csv')
        for index in range(len(self.pedidos['Modelo'])):  # Conteo de items
            modelo = self.pedidos['Modelo'][index]
            tipo = self.pedidos['Tipo'][index]
            item = self.pedidos['Articulos'][index]
            if item not in new_dic:
                new_dic[item] = []
                new_dic[item].append(1)
                new_dic[item].append(tipo)
                new_dic[item].append(modelo)
            else:
                new_dic[item][0] += 1
        for i in new_dic:
            try:
                if len(stock[stock['Modelo'] == new_dic[i][2]]['Cantidad']) == 1:  # Si hay un único modelo descontamos
                    index = stock[stock['Modelo'] == new_dic[i][2]].loc[:, 'Cantidad'].index
                    stock.iloc[index, 3] -= new_dic[i][0]
                else:
                    """Check for tipo de artículo"""
                    index = stock[(stock['Modelo'] == new_dic[i][2]) &
                                  (stock['Tipo de articulo'] == new_dic[i][1])].index
                    stock.iloc[index, 3] -= new_dic[i][0]
            except Exception as e:
                print(e)
        stock.to_csv('Stock.csv', index=False)

    def cargar_venta(self):
        ventas = pd.read_csv('Ventas_nuevo.csv')
        row = len(ventas)
        subset = {k: self.pedidos[k] for k in ('Fecha', 'Cliente', 'Contacto',
                                               'Articulos', 'Precios',
                                               'Total', 'Observaciones')}
        print(subset)
        for k, v in subset.items():
            try:
                ventas.at[row, k] = v
            except Exception as e:
                print(str(e))
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
            elif k == 'Articulos' or k == 'Precios' or k == 'Tipo' or k == 'Modelo':
                self.pedidos[k] = []
            else:
                self.pedidos[k] = ''

    def eliminar_item(self):
        rows = []
        for index in self.lista.selectedIndexes():
            rows.append(index.row())
        data = self.lista.currentIndex().data()
        if data:
            for row in sorted(rows, reverse=True):
                del(self.pedidos['Articulos'][row])
                del(self.pedidos['Modelo'][row])
                del(self.pedidos['Tipo'][row])
                del(self.pedidos['Precios'][row])
            total1 = round(sum(self.pedidos['Precios']))
            self.pedidos['Total'] = total1
            self.total.setText(f"Total: {total1}")
            self.llenar_lista()

    def porcentaje(self):
        user_input = qtw.QInputDialog()
        porcentaje, ok = user_input.getDouble(self,
                                              'Porcentaje',
                                              'Porcentaje: ',
                                              qtw.QLineEdit.Normal,
                                              0, 100)
        if porcentaje and ok:
            self.calcular_porcentaje(porcentaje)

    def calcular_porcentaje(self, porcentaje):
        idxs = self.tableview.selectedIndexes()
        if idxs:
            msg = qtw.QMessageBox()
            msg.setText(f'¿Está seguro de que desea modificar {len(idxs)} elementos?')
            msg.setWindowTitle(' ')
            msg.exec_()
            if msg.sender():
                # print('Accepted')
                try:
                    porcentaje = porcentaje / 100
                    for idx in idxs:
                        row = idx.row()
                        col = idx.column()
                        idx = float(idx.data())
                        print(row, col, idx)
                        nuevo_precio = idx + (idx * porcentaje)
                        print(nuevo_precio)
                        self.model._data[row][col] = nuevo_precio
                        self.statusBar().showMessage('Valores modificados correctamente.', 10000)
                except Exception as e:
                    msg = 'Seleccione únicamente celdas que contengan números.'
                    self.display_msg(msg, icon=qtw.QMessageBox.Critical,
                                     informativeText=e, windowTitle='Datos erróneos')

    def cargar_stock(self):
        try:
            stock_window = CargarStock()
            stock_window.exec_()
        except Exception as e:
            self.statusBar().showMessage(str(e))

    @qtc.pyqtSlot()
    def filter(self):
        index = self.filtrar_por.currentIndex()
        self.filter_proxy_model.setFilterKeyColumn(index)

    def display_msg(self, string, **kwargs):
        msg = qtw.QMessageBox()
        msg.setText(string)
        for k, v in kwargs.items():
            setattr(msg, k, v)
        try:
            msg.setInformativeText(str(kwargs.get('informativeText', ' ')))
            msg.setIcon(kwargs.get('icon', None))
            msg.setWindowTitle(str(kwargs.get('windowTitle', ' ')))
        except Exception as e:
            print(e)
        msg.exec_()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
