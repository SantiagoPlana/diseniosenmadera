import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QPixmap, QPainter, QDoubleValidator, QIcon
# from PyQt5.QtPrintSupport import QPrinter
# from PyQt5.Qt import QFileInfo
import csv
import pandas as pd
import traceback

import reportlabpdf


class NuevoItem(qtw.QDialog):

    def __init__(self, lst):
        super().__init__()

        self.setWindowIcon(QIcon('diseñosenmadera2.png'))
        self.lst = lst
        self.box = qtw.QVBoxLayout()
        self.setLayout(self.box)

        self.l_natural = qtw.QLineEdit()
        self.l_miel = qtw.QLineEdit()
        self.cont_nat = qtw.QLineEdit()
        self.cont_miel = qtw.QLineEdit()
        self.cont_alg = qtw.QLineEdit()
        self.lista = qtw.QLineEdit()
        self.contado = qtw.QLineEdit()
        self.lista_c_tinta = qtw.QLineEdit()
        self.cont_c_tinta = qtw.QLineEdit()
        self.alg_lista_c_tinta = qtw.QLineEdit()
        self.alg_cont_c_tinta = qtw.QLineEdit()
        # Validators
        self.onlyInt = QDoubleValidator()
        self.l_natural.setValidator(self.onlyInt)
        self.l_miel.setValidator(self.onlyInt)
        self.cont_nat.setValidator(self.onlyInt)
        self.cont_miel.setValidator(self.onlyInt)
        self.cont_alg.setValidator(self.onlyInt)
        self.lista.setValidator(self.onlyInt)
        self.contado.setValidator(self.onlyInt)
        self.lista_c_tinta.setValidator(self.onlyInt)
        self.cont_c_tinta.setValidator(self.onlyInt)
        self.alg_lista_c_tinta.setValidator(self.onlyInt)
        self.alg_cont_c_tinta.setValidator(self.onlyInt)

        self.box.addWidget(qtw.QLabel('<b>Precios para pino</b>'))
        self.box.addWidget(qtw.QLabel('Lista Natural'))
        self.box.addWidget(self.l_natural)
        self.box.addWidget(qtw.QLabel('Contado natural'))
        self.box.addWidget(self.cont_nat)
        self.box.addWidget(qtw.QLabel('Contado con miel'))
        self.box.addWidget(self.cont_miel)
        self.box.addWidget(qtw.QLabel('Contado con algarrobo'))
        self.box.addWidget(self.cont_alg)


        # self.box.addWidget(qtw.QLabel('<b>Precios para algarrobo</b>'))
        self.box.addWidget(qtw.QLabel('Precio de lista'))
        self.box.addWidget(self.lista)
        self.box.addWidget(qtw.QLabel('Precio de contado'))
        self.box.addWidget(self.contado)
        self.box.addWidget(qtw.QLabel('Lista Con Tinta'))
        self.box.addWidget(self.lista_c_tinta)
        self.box.addWidget(qtw.QLabel('Contado con Tinta'))
        self.box.addWidget(self.cont_c_tinta)
        self.box.addWidget(qtw.QLabel('Algarrobo lista c tinta'))
        self.box.addWidget(self.alg_lista_c_tinta)
        self.box.addWidget(qtw.QLabel('Algarrobo contado c tinta'))
        self.box.addWidget(self.alg_cont_c_tinta)

        self.btn_agregar = qtw.QPushButton('Agregar')
        self.btn_cancelar = qtw.QPushButton('Cancelar')
        self.box.addWidget(self.btn_agregar)
        self.box.addWidget(self.btn_cancelar)

        widgets = (self.box.itemAt(i).widget() for i in range(self.box.count()))
        for widget in widgets:
            if isinstance(widget, qtw.QLineEdit):
                widget.setText('0')

        # self.l_miel.setText('0')
        #self.cont_nat.setText('0')

        #self.cont_miel.setText('0')
        #self.cont_alg.setText('0')
        #self.lista.setText('0')
        #self.contado.setText('0')

        self.btn_agregar.clicked.connect(self.cargar)
        self.btn_cancelar.clicked.connect(self.close)

    @qtc.pyqtSlot()
    def cargar(self):
        try:
            self.lst_precios = [self.l_natural.text(), self.cont_nat.text(), self.cont_miel.text(),
                                self.cont_alg.text(),
                                self.lista.text(), self.contado.text(), self.lista_c_tinta.text(),
                                self.cont_c_tinta.text(), self.alg_lista_c_tinta.text(),
                                self.alg_cont_c_tinta.text()]
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
        except Exception as e:
            print(str(e))


class CargarStock(qtw.QDialog):
    """Dialog para carga de stock"""

    signalItemCargado = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('diseñosenmadera2.png'))
        self.setMinimumSize(260, 310)
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
        # print('Signal!')
        subset = self.stock[self.stock['Material'] == string]['Tipo de articulo'].unique()
        self.completer_tipo = qtw.QCompleter(subset, self)
        self.completer_tipo.setFilterMode(qtc.Qt.MatchContains)
        self.completer_tipo.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.tipo.setCompleter(self.completer_tipo)
        self.completer_tipo.activated.connect(self.set_complete_modelo)

    @qtc.pyqtSlot(str)
    def set_complete_modelo(self, string=str):
        # print('Signal!')
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
        # print(material, tipo, modelo, cantidad)
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
        msg.setWindowIcon(QIcon('diseñosenmadera2.png'))
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
        denom_completa = material + tipo + modelo
        lst = [denom_completa, material, tipo, modelo, cantidad]
        nuevo = NuevoItem(lst)
        nuevo.exec_()


class Signals(qtc.QObject):

    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(object)


class Worker(qtc.QRunnable):

    def __init__(self, fn, *args, **kwargs):

        super(Worker, self).__init__()
        print('initiated')
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    @qtc.pyqtSlot()
    def run(self):
        """Inicializa la función"""
        print('running')
        print(self.args, self.kwargs)
        try:
            result = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()


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
            del (self._data[position])
        self.endRemoveRows()

    # method for saving
    def save_data(self):
        # commented out code below to fix issue with additional lines being added after saving csv file from the window.
        # with open(self.filename, 'w', encoding='utf-8') as fh:
        with open(self.filename, 'w', newline='', encoding='utf-8') as fh:
            print(fh)
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)


class Tabla(qtw.QDialog):

    """Ventana para display de tablas"""

    def __init__(self, db):
        super().__init__()

        self.setWindowTitle('Tabla')
        self.resize(1320, 900)
        self.setSizeGripEnabled(True)
        self.setModal(False)
        # database
        self.db = db

        self.threadpool = qtc.QThreadPool()

        # Layouts
        self.v_layout = qtw.QVBoxLayout()
        self.h_layout = qtw.QHBoxLayout()
        self.setLayout(self.v_layout)

        # Table model
        self.table = qtw.QTableView()
        self.model = CsvTableModel(self.db)

        self.filter_proxy_model = qtc.QSortFilterProxyModel()
        self.filter_proxy_model.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.table.setModel(self.filter_proxy_model)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)


        self.filter_proxy_model.setSourceModel(self.model)

        # filtros
        self.filtro = qtw.QComboBox()
        self.text_filtro = qtw.QLineEdit()
        self.filtro.addItems(self.model._headers)
        self.filtro.currentTextChanged.connect(self.cambiar_filtro)
        self.text_filtro.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        # Acciones
        self.eliminar_filas = qtw.QAction('Eliminar fila(s)', self)
        self.eliminar_filas.setShortcut('Del')
        self.eliminar_filas.triggered.connect(self.remove_rows)

        self.guardar = qtw.QAction('Guardar archivo', self)
        self.guardar.setShortcut('Ctrl+S')
        self.guardar.triggered.connect(self.guardar_cambios)

        # otros widgets
        self.menubar = qtw.QMenuBar(objectName='menubar')
        self.menu_archivo = qtw.QMenu('Archivo')
        self.menu_editar = qtw.QMenu('Editar')


        self.menu_archivo.addAction(self.guardar)

        #self.menu_archivo.addAction('Eliminar fila(s)', self.remove_rows)
        self.menu_archivo.addAction(self.eliminar_filas)
        self.menu_editar.addAction('Insertar arriba', self.insert_above)
        self.menu_editar.addAction('Insertar abajo', self.insert_below)
        self.menu_editar.addAction('Modificar valor celdas', self.definir_celdas_dialog)
        self.menubar.addMenu(self.menu_archivo)
        self.menubar.addMenu(self.menu_editar)

        self.layout().addWidget(self.menubar)
        self.layout().addWidget(qtw.QLabel('Filtrar por:'))
        self.v_layout.addLayout(self.h_layout)
        self.layout().addWidget(self.table)

        self.h_layout.addWidget(self.filtro)
        self.h_layout.addWidget(self.text_filtro)

        #self.table.resizeColumnsToContents()
        # style
        # self.table.setStyleSheet('alternate-background-color: lightgray;  background-color: white;'
        #                         'font-size: 12pt; selection-background-color: #FF9B99; ')
        # self.menubar.setStyleSheet('spacing: 3px; font-size: 10pt; color: #F3E5CE;')
        #self.menu_archivo.setStyleSheet('selection-background-color: #FF9B99; color: white; '
        #                                'font-size: 10pt;')
        #self.menu_editar.setStyleSheet('selection-background-color: #FF9B99; color: white; '
        #                                'font-size: 10pt;')


        if self.db.split('/')[-1] == 'Stock.csv':
            self.filtro.setCurrentIndex(0)
            self.menubar.addAction('Agregar porcentaje', self.sumar_porcentaje_dialog)
            self.menubar.addAction('Restar porcentaje', self.descontar_porcentaje_dialog)
            self.menubar.addAction('Cargar Stock', self.cargar_stock)
            self.table.resizeColumnsToContents()
        else:
            self.filtro.setCurrentIndex(4)
            self.resize(750, 800)


    @qtc.pyqtSlot()
    def cambiar_filtro(self):
        index = self.filtro.currentIndex()
        self.filter_proxy_model.setFilterKeyColumn(index)

    def guardar_cambios(self):
        if self.model:
            worker = Worker(self.model.save_data)
            worker.signals.result.connect(lambda: print('funca'))
            self.threadpool.start(worker)
            # self.statusBar().showMessage('Archivo guardado correctamente', 1000)

    def insert_above(self):
        try:
            selected = self.table.selectedIndexes()
            row = selected[0].row() if selected else 0
            self.model.insertRows(row, 1, None)
        except Exception as e:
            pass

    def insert_below(self):
        try:
            selected = self.table.selectedIndexes()
            row = selected[-1].row() if selected else self.model.rowCount(None)
            self.model.insertRows(row + 1, 1, None)
        except Exception as e:
            pass

    def remove_rows(self):
        selected = self.table.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        selected_proxy = [self.filter_proxy_model.mapToSource(idx) for idx in selected]
        print(selected_proxy)
        if selected:
            try:
                for row in range(num_rows):
                    self.model.removeRows(selected_proxy[row].row(), num_rows, None)
            except Exception as e:
                print(str(e))

    def sumar_porcentaje_dialog(self):
        """Input dialog para ingresar porcentaje"""

        user_input = qtw.QInputDialog()

        porcentaje, ok = user_input.getDouble(self,
                                              'Porcentaje',
                                              'Porcentaje: ',
                                              qtw.QLineEdit.Normal,
                                              0, 100)
        if porcentaje and ok:
            self.sumar_porcentaje(porcentaje)

    def descontar_porcentaje_dialog(self):
        """Input dialog para ingresar porcentaje"""

        user_input = qtw.QInputDialog()

        porcentaje, ok = user_input.getDouble(self,
                                              'Porcentaje',
                                              'Porcentaje: ',
                                              qtw.QLineEdit.Normal,
                                              0, 100)
        if porcentaje and ok:
            self.descontar_porcentaje(porcentaje)

    def definir_celdas_dialog(self):
        user_input = qtw.QInputDialog()
        texto, ok = user_input.getText(self,
                                       'Valor',
                                       'Valor: ',
                                       qtw.QLineEdit.Normal,
                                       '')
        if texto and ok:
            self.definir_celdas(texto)

    def descontar_porcentaje(self, porcentaje):
        idxs = self.table.selectedIndexes()
        porcentaje = porcentaje / 100
        if idxs:
            msg = qtw.QMessageBox()
            msg.setText(f'¿Está seguro de que desea modificar {len(idxs)} elementos?')
            msg.setWindowTitle(' ')
            msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == qtw.QMessageBox.Ok:
                # print('Accepted')
                for idx in idxs:
                    try:
                        row = self.filter_proxy_model.mapToSource(idx).row()
                        col = self.filter_proxy_model.mapToSource(idx).column()
                        idx = round(float(idx.data()))
                        nuevo_precio = idx - (idx * porcentaje)
                        self.model._data[row][col] = nuevo_precio
                        # self.statusBar().showMessage('Valores modificados correctamente.', 10000)
                    except Exception as e:
                        msg = 'Seleccione únicamente celdas que contengan números.'
                        self.display_msg(msg, icon=qtw.QMessageBox.Critical,
                                         informativeText=f'Elemento: {idx.data()}',
                                         windowTitle='Error')
                else:
                    msg.close()

    def sumar_porcentaje(self, porcentaje):
        idxs = self.table.selectedIndexes()
        porcentaje = porcentaje / 100
        if idxs:
            msg = qtw.QMessageBox()
            msg.setText(f'¿Está seguro de que desea modificar {len(idxs)} elementos?')
            msg.setWindowTitle(' ')
            msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == qtw.QMessageBox.Ok:
                # print('Accepted')
                for idx in idxs:
                    try:
                        # Map to source hace que todo funcione bien con la tabla filtrada.
                        row = self.filter_proxy_model.mapToSource(idx).row()
                        col = self.filter_proxy_model.mapToSource(idx).column()
                        idx = round(float(idx.data()))
                        # print(row, col, idx)
                        nuevo_precio = idx + (idx * porcentaje)
                        # print(nuevo_precio)
                        self.model._data[row][col] = nuevo_precio
                        # self.statusBar().showMessage('Valores modificados correctamente.', 10000)
                    except Exception as e:
                        text = 'Seleccione únicamente celdas que contengan números.'
                        self.display_msg(text, icon=qtw.QMessageBox.Critical,
                                         informativeText=f'Elemento: {idx.data()}',
                                         windowTitle='Error')
                else:
                    msg.close()

    def definir_celdas(self, texto):
        idxs = self.table.selectedIndexes()
        if idxs:
            msg = qtw.QMessageBox()
            msg.setText(f'¿Está seguro de que desea modificar {len(idxs)} elementos?')
            msg.setWindowTitle(' ')
            msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == qtw.QMessageBox.Ok:
                for idx in idxs:
                    try:
                        row = self.filter_proxy_model.mapToSource(idx).row()
                        col = self.filter_proxy_model.mapToSource(idx).column()
                        self.model._data[row][col] = texto
                    except Exception as e:
                        print(str(e))
            else:
                msg.close()

    def cargar_stock(self):
        try:
            stock_window = CargarStock()
            stock_window.exec_()
        except Exception as e:
            print(str(e))

    def display_msg(self, string, **kwargs):
        msg = qtw.QMessageBox()
        msg.setWindowIcon(QIcon('png_aya.ico'))
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


class MainWindow(qtw.QWidget):

    settings = qtc.QSettings('Diseños en Madera', 'Manager de Datos DeM')
    productos = pd.read_csv('Stock.csv')

    def __init__(self):
        """Main Widget Constructor"""

        super().__init__()

        # self.password()

        self.settings = qtc.QSettings('Diseños en Madera', 'Manager de Datos DeM')

        # Main UI
        self.setWindowTitle('Diseños en Madera')
        self.setWindowIcon(QIcon('diseñosenmadera2.png'))
        #try:
        #    self.resize(self.settings.value('window size'))
        #except Exception:
        self.resize(800, 600)

        """ 
            - Botones para abrir las tablas. 
            - Line edit para buscar los items y que se carguen en una lista. 
            - Opción para poner el "tratamiento" de los productos, y que eso afecte el precio
            - Financiamiento para las tarjetas y métodos de pago, preguntar bien.
            - 
         """
        # Layout
        h_layout = qtw.QHBoxLayout()
        v_layout = qtw.QVBoxLayout()
        # v_layout.addLayout(h_layout)
        self.grid1 = qtw.QGridLayout()
        self.grid2 = qtw.QGridLayout()
        self.grid3 = qtw.QGridLayout()
        v_layout.addLayout(self.grid1)
        h_layout.addLayout(self.grid2)
        h_layout.addLayout(self.grid3)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        # self.layout.setRowStretch(self.layout.rowCount(), 1)
        # self.layout.setColumnStretch(self.layout.columnCount(), 1)

        # Menu Bar

        self.menu_bar = qtw.QMenuBar()
        # self.menu_bar.addMenu('Archivo')
        # self.menu_bar.addMenu('Editar')
        self.menu_bar.addAction('Abrir tabla stock', self.abrir_tabla_stock)
        self.menu_bar.addAction('Abrir tabla presupuestos', self.abrir_tabla_presupuestos)

        # WIDGETS
        self.titulo = qtw.QLabel('Diseños en Madera', objectName='titulo')

        self.combo_productos = qtw.QComboBox(objectName='combo_productos')
        self.combo_productos.setEditable(True)

        self.precio_envio = qtw.QLineEdit()
        self.precio_envio.setEnabled(False)
        self.observaciones = qtw.QTextEdit(placeholderText='Observaciones')

        self.cliente = qtw.QLineEdit(placeholderText='Nombre cliente')
        self.contacto = qtw.QLineEdit(placeholderText='Contacto')



        self.direccion = qtw.QLineEdit()

        self.tratamiento = qtw.QComboBox()

        self.label_display_precio = qtw.QLabel('Precio Unitario: 0')
        self.label_display_stock = qtw.QLabel('Stock: 0')
        # self.checkbox = qtw.QCheckBox('')
        self.lista = qtw.QListWidget()

        self.envio_toggle = qtw.QCheckBox('Envío')


        self.financiamiento = qtw.QComboBox()
        if 'Lista Financiamientos' not in self.settings.allKeys():
            financiamientos = ['Contado', '12%', '15%', '20%', 'Otro']
            self.settings.setValue('Lista Financiamientos', financiamientos)
            self.financiamiento.addItems(financiamientos)
        else:
            self.financiamiento.addItems(self.settings.value('Lista Financiamientos'))

        self.label_total = qtw.QLabel('Total: 0')
        self.label_financiamiento = qtw.QLabel('')
        self.status_bar = qtw.QStatusBar()

        v_layout.setMenuBar(self.menu_bar)

        # Botones

        self.btn_agregar = qtw.QPushButton('Agregar')
        self.btn_agregar.clicked.connect(self.agregar)
        self.btn_orden_trabajo = qtw.QPushButton('Generar venta', objectName='generar_venta')
        self.btn_orden_trabajo.setFixedWidth(120)

        self.btn_generar_pdf = qtw.QPushButton('Generar PDF', objectName='generar_pdf')
        self.btn_borrar = qtw.QPushButton('Borrar formulario')
        self.btn_borrar.setAccessibleDescription('Borrar todos los campos de la ventana')

        self.btn_generar_pdf.setFixedWidth(120)
        self.btn_borrar.setFixedWidth(120)

        self.btn_eliminar_item = qtw.QPushButton('Eliminar Item(s)')
        self.btn_eliminar_item.setShortcut('Del')


        # Layout
        #self.grid1.addItem(qtw.QSpacerItem(43, 30), 0, 0)
        self.grid1.addWidget(self.titulo, 0, 1)
        self.grid1.addItem(qtw.QSpacerItem(10, 10), 1, 1)
        self.grid1.addWidget(self.cliente, 2, 1)
        self.cliente.setFixedWidth(300)

        self.grid1.addWidget(self.contacto, 2, 3)
        self.contacto.setFixedWidth(200)
        self.grid1.addWidget(qtw.QLabel('Nombre producto'), 3, 1)
        self.grid1.addWidget(self.combo_productos, 4, 1)
        self.combo_productos.setFixedWidth(280)
        self.grid1.addWidget(qtw.QLabel('Tratamiento'), 3, 3)
        self.grid1.addWidget(self.tratamiento, 4, 3)
        self.tratamiento.setFixedWidth(200)
        self.grid1.addWidget(self.label_display_stock, 5, 1)
        self.grid1.addWidget(self.label_display_precio, 6, 1)
        self.grid1.addWidget(self.btn_agregar, 7, 1)
        # self.grid1.addWidget(qtw.QLabel('            '), 1, 2)
        self.grid2.addWidget(qtw.QLabel('Lista'), 0, 1)
        self.grid2.addWidget(self.lista, 1, 1)
        self.lista.setFixedSize(400, 200)
        self.grid2.addWidget(self.btn_eliminar_item, 2, 1)
        self.btn_eliminar_item.setFixedWidth(150)
        # self.layout.addWidget(self.label_total, 6, 1)
        self.grid2.addWidget(self.observaciones, 3, 1)
        self.observaciones.setFixedSize(400, 70)
        self.grid1.addWidget(self.envio_toggle, 5, 3)
        self.grid1.addWidget(self.precio_envio, 6, 3)
        self.precio_envio.setFixedWidth(200)
        self.grid3.addWidget(self.btn_orden_trabajo, 1, 1)
        self.grid3.addWidget(self.btn_generar_pdf, 2, 1)
        self.grid3.addWidget(self.btn_borrar, 3, 1)
        self.grid2.addWidget(self.label_total, 4, 1)
        self.grid2.addWidget(self.label_financiamiento, 5, 1)
        self.grid1.addWidget(self.financiamiento, 7, 3)

        self.grid1.addItem(qtw.QSpacerItem(20, 20), 6, 1)
        self.grid3.addItem(qtw.QSpacerItem(10, 10), 4, 1)
        v_layout.addWidget(self.status_bar)
        # self.status_bar.showMessage('toy aqui')
        # self.grid2.addItem(qtw.QSpacerItem(20, 20), 1, 4, 1, 1 )


        # self.grid1.setColumnStretch(1, 1)
        # self.grid1.setRowStretch(self.grid1.rowCount(), 50)
        # self.grid2.setRowStretch(1, 1)
        # self.grid2.setColumnStretch(1, 1)
        # self.grid2.setColumnStretch(0, 1)
        self.combo_productos.addItem(' ')
        self.combo_productos.addItems(self.productos.loc[:, 'Denominación_Completa'])
        self.completer_productos = qtw.QCompleter(
            self.productos.loc[:, 'Denominación_Completa'], self
        )
        self.completer_productos.setCaseSensitivity(qtc.Qt.CaseInsensitive)
        self.completer_productos.setFilterMode(qtc.Qt.MatchContains)
        self.combo_productos.setCompleter(self.completer_productos)

        cols = ['Lista Natural', 'Cont Nat', 'Cont C Miel', 'Cont C Alg',
                'Precio de Lista', 'Precio de Contado', 'Lista C Tinta',
                'Contado C Tinta', 'Alg Lista C Tinta', 'Alg Cont C Tinta']
        self.tratamiento.addItems(cols)


        # Connections
        self.btn_borrar.clicked.connect(self.borrar_formulario)

        self.combo_productos.activated.connect(self.activar_producto)
        self.tratamiento.activated.connect(self.activar_producto)
        self.envio_toggle.clicked.connect(self.activar_envio)

        self.btn_eliminar_item.clicked.connect(self.eliminar_items)
        self.financiamiento.activated.connect(self.calculo_financiamiento)

        self.btn_generar_pdf.clicked.connect(self.finalizar_venta)
        self.btn_orden_trabajo.clicked.connect(self.finalizar_venta)

        # Configs
        self.lista.setAlternatingRowColors(True)
        self.lista.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)

        self.status_bar.showMessage('Mensaje de prueba xxxxxxxxx')


        self.show()


    def get_path(self):
        settings = qtc.QSettings('Diseños en Madera', 'Manager de Datos DeM')
        if 'PDF_Path' in settings.allKeys():
            path = settings.value('PDF_Path')
            print(path)
        else:
            path = qtw.QFileDialog.getExistingDirectory(self,
                                                        'Guardar PDF',
                                                        qtc.QDir.currentPath(),
                                                        qtw.QFileDialog.ShowDirsOnly |
                                                        qtw.QFileDialog.DontResolveSymlinks)
            settings.setValue('PDF_Path', path)
            print(settings.value('PDF_Path'))

        return path

    @qtc.pyqtSlot()
    def agregar(self):
        if len(self.combo_productos.currentText()) > 1:
            try:
                total = float(self.label_total.text().split(':')[-1])
                total = float(total)
                # print(type(total))
                producto = self.combo_productos.currentText()
                tratamiento = self.tratamiento.currentText()
                precio = self.productos[
                    self.productos['Denominación_Completa'] == producto][tratamiento].values[0]
                precio = '%.2f' % float(precio)
                # print(producto, tratamiento, precio)
                self.lista.addItem(f'{producto} | {tratamiento} | {precio}')
                total += float(precio)
                # print(total)
                self.label_total.setText(f'Total: {"%.2f" % total}')
                self.calculo_financiamiento()
            except Exception as e:
                print(str(e))
            # self.calculo_financiamiento()

    @qtc.pyqtSlot()
    def activar_producto(self):
        if len(self.combo_productos.currentText()) != 1:
            # print(self.combo_productos.currentText())
            producto = self.combo_productos.currentText()
            tratamiento = self.tratamiento.currentText()
            precio_unitario = self.productos.loc[
                                self.productos[
                                    'Denominación_Completa'] == producto][tratamiento].values[0]
            precio_unitario = '%.2f' % float(precio_unitario)
            stock = self.productos.loc[
                                self.productos[
                                    'Denominación_Completa'] == producto]['Cantidad'].values[0]
            self.label_display_precio.setText(f'Precio Unitario: {precio_unitario}')
            self.label_display_stock.setText(f'Stock: {stock}')
        else:
            self.label_display_precio.setText('Precio Unitario: 0')
            self.label_display_stock.setText('Stock: 0')

    @qtc.pyqtSlot()
    def borrar_formulario(self):
        for i in range(self.grid1.count()):
            item = self.grid1.itemAt(i).widget()
            if isinstance(item, qtw.QLineEdit):
                item.clear()
            elif isinstance(item, qtw.QComboBox):
                item.clearEditText()
        for i in range(self.grid2.count()):
            item = self.grid2.itemAt(i).widget()
            if isinstance(item, qtw.QListWidget) or isinstance(item, qtw.QTextEdit):
                item.clear()
        self.label_total.setText('Total: 0')

    @qtc.pyqtSlot()
    def activar_envio(self):
        if self.envio_toggle.isChecked():
            self.precio_envio.setEnabled(True)
        else:
            self.precio_envio.setEnabled(False)
            self.precio_envio.clear()

    def eliminar_items(self):
        if self.lista.selectedItems():
            rows = self.lista.selectedIndexes()
            total = float(self.label_total.text().split(':')[-1])
            print(total)
            for row in reversed(rows):
                # print(row.data())
                try:
                    total -= float(str(row.data()).split('|')[-1])
                    self.lista.takeItem(row.row())
                except Exception as e:
                    print(str(e))
            print(total)
            total = '%.2f' % total
            self.label_total.setText(f'Total: {total}')
            self.calculo_financiamiento()

    def calculo_financiamiento(self):
        financiamiento = self.financiamiento.currentText()
        if financiamiento != 'Contado' and financiamiento != 'Otro':
            pctje = float(financiamiento.split('%')[0]) / 100
            total = float(self.label_total.text().split(':')[-1])
            total = total + (total * pctje)
            total = '%.2f' % total
            #self.label_total.setText(f'Total: {total}')

            self.label_financiamiento.setText(f'Financiamiento ({financiamiento}): {total}')

        elif financiamiento == 'Contado':
            self.label_financiamiento.setText('')

        elif financiamiento == 'Otro':
            dialog = qtw.QInputDialog()
            texto, ok = dialog.getDouble(self,
                                         'Nuevo valor de financiamiento',
                                         'Porcentaje: ',
                                         qtw.QLineEdit.Normal,
                                         0, 100)
            if texto and ok:
                index = self.financiamiento.count() + 1
                self.financiamiento.insertItem(index, f'{texto}%')
                self.financiamiento.setCurrentIndex(index - 1)
                total = float(self.label_total.text().split(':')[-1])
                total = total + (total * float(texto) / 100)
                total = '%.2f' % total
                self.label_financiamiento.setText(f'Financiamiento ({texto}%): {total}')
                # self.settings.value('Lista Financiamientos').append(f"{texto} + '%'")
                new_list = self.settings.value('Lista Financiamientos') + [f'{texto}%']
                self.settings.setValue('Lista Financiamientos', new_list)

    @qtc.pyqtSlot()
    def finalizar_venta(self):
        fecha = qtc.QDateTime().currentDateTime().date().toString("dd-MM-yyyy")
        datos = {'Cliente': self.cliente.text() or '', 'Contacto': self.contacto.text() or '',
                 'Fecha': fecha, 'Total': self.label_total.text().split(':')[-1].strip(' '),
                 'Observaciones': self.observaciones.toPlainText(),
                 'Tarjeta': self.financiamiento.currentText()}
        if datos['Tarjeta'] != 'Contado':
            datos['Total'] = self.label_financiamiento.text().split(':')[-1]
        # print('First checkpoint')
        dic_productos = {}
        # productos = []
        for i in range(self.lista.count()):
            # nombre producto
            producto = self.lista.item(i).text().split('|')[0]
            precio = float(self.lista.item(i).text().split('|')[-1])
            if producto not in dic_productos.keys():
                # [cantidad, precio]
                dic_productos[producto] = [1, precio]
            else:
                # Cantidad
                dic_productos[producto][0] += 1
                # Suma a Precio Total
                dic_productos[producto][1] += precio
        # Formatear decimales en precio
        if self.precio_envio.text():
            dic_productos['Envío'] = [1, float(self.precio_envio.text())]

        for k in dic_productos.keys():
            dic_productos[k][-1] = '%.2f' % dic_productos[k][1]
        # print('Second checkpoint')

        # solo generar pdf
        path = self.get_path()
        # print(datos)
        # print(dic_productos)
        if self.sender().objectName() == 'generar_pdf':
            reportlabpdf.generate(datos, dic_productos, path)
            print('Third checkpoint')
            self.status_bar.showMessage('PDF generado correctamente.')
        # cargar venta Y generar pdf
        elif self.sender().objectName() == 'generar_venta':
            reportlabpdf.generate(datos, dic_productos, path)
            self.cargar_venta(dic_productos, datos)
            self.status_bar.showMessage('Venta cargada y PDF generado correctamente.')
            # función para cargar venta

    def cargar_venta(self, item_dic, datos_dic):
        presupuestos = pd.read_csv('Ventas_nuevo.csv')
        row = len(presupuestos)
        subset = {k: datos_dic[k] for k in ('Fecha', 'Cliente', 'Contacto',
                                            'Total', 'Observaciones')}
        subset['Articulos'] = [item for item in item_dic.keys()]
        subset['Articulos'] = [[item] * item_dic[item][0] for item in subset['Articulos']]
        # subset['Precios'] = [precio[-1] for precio in item_dic.values()]
        subset['Precios'] = []
        for k, v in subset.items():
            try:
                presupuestos.at[row, k] = v
            except Exception as e:
                print(str(e))
        presupuestos.fillna(value='Sin Detalle', axis=0, inplace=True)
        presupuestos.to_csv('Ventas_nuevo.csv', index=False)
        self.descontar_stock(item_dic)

    def descontar_stock(self, item_dic):
        stock = pd.read_csv('Stock.csv')
        for k, v in item_dic.items():
            index = stock[stock['Denominación_Completa'] == k].loc[:, 'Cantidad'].index
            stock.iloc[index, 3] -= v[0]
        stock.to_csv('Stock.csv', index=False)
        # print('Done')

    def abrir_tabla_stock(self):
        self.tabla = Tabla('Stock.csv')
        self.tabla.exec_()

    def abrir_tabla_presupuestos(self):
        self.tabla = Tabla('Ventas_nuevo.csv')
        self.tabla.exec_()



stylesheet = """ 



QWidget {background-color: #C7C1A9;}

#titulo {
color: #2F323A; 
font: bold; 
font-size: 24pt;
font-family: Calibri;
}

QLabel {
font-size: 13pt;
color: #2F323A;
}

QComboBox {
font-size: 11pt;
background-color: ivory;
color: black;
selection-background-color: #B1740F;
selection-color: solidblack;
border-style: solid;
border-radius: 5px;
}
QComboBox:hover {
border: 1px #B1740F
}

QLineEdit:enabled {
background-color: ivory;
size: 12 pt;
}

QPushButton {
font-size: 10pt;
padding: 2px;
color: ivory;
size: 15px;
background-color: #332C23;
}

QPushButton:hover {background: ivory;
color: #2F323A;
}

#menu {spacing: 3px; font-size: 10pt; color: #F3E5CE;}
#menu::item {padding: 1px 4px; background: transparent; border-radius: 6px;}
#menu::item:selected {background: #FF9B99;}

QStatusBar {
family-font: Calibri;
color: #2F323A;
font-size: 11pt;
}

QListWidget {
alternate-background-color: #FFE8C2;
background-color: ivory;
font-size: 11pt;
selection-background-color: blue;
}
"""


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    # mw.settings.setValue('fullscreen', mw.isFullScreen())
    sys.exit(app.exec())

