#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
from PyQt4 import QtGui, QtCore
import vSaldoClInforme, datetime
from pathlib import Path
from operator import attrgetter
from win_unc import UncDirectory, UncDirectoryConnection
import os
import winshell

def archivoALista():
    try:
        simple_unc = UncDirectory(r'\\respaldoadh\archivosventa')  # se crea ruta unc
        # Setup a connection handler:
        conn = UncDirectoryConnection(simple_unc)  # se abre la carpeta unc
        conn.connect()  # se crea conexion con la carpeta

        archivo = open(validacionArchivo(simple_unc,"saldocl.txt"), "r")
        listaDatos = list()
        for linea in archivo.readlines():
            a = RegistroArchivo()
            a.setCliente(linea[0:35])
            a.setPedido(linea[36:42])
            a.setFechaPedido(linea[43:51])
            a.setDescEtiqueta(linea[52:87])
            a.setCodEtiqueta(linea[88:108])
            a.setCantPedida(linea[109:117])
            a.setCantCliente(linea[118:126])
            a.setCantRevisada(linea[127:135])
            a.setCantDespachada(linea[136:144])
            a.setSaldo(linea[147:156])
            a.setPrecio(linea[157:164])
            a.setSaldoValor(linea[165:173])
            a.setDiaDespacho1(linea[174:176])
            a.setMesDespacho1(linea[177:179])
            a.setAnioDespacho1(linea[180:184])
            a.setCantDespacho1(linea[185:193])
            a.setDiaDespacho2(linea[194:196])
            a.setMesDespacho2(linea[197:199])
            a.setAnioDespacho2(linea[200:204])
            a.setCantDespacho2(linea[205:213])
            a.setDiaDespacho3(linea[214:216])
            a.setMesDespacho3(linea[217:219])
            a.setAnioDespacho3(linea[220:224])
            a.setCantDespacho3(linea[225:233])
            a.setFechaPrimeraRevision(linea[234:242])
            a.setFechaultimoDespacho(linea[243:251])
            listaDatos.append(a)
        archivo.close()
        conn.disconnect()  # se desconecta de la carpeta
        assert (not conn.is_connected())
        return sorted(listaDatos, key=attrgetter('mesesStock'),reverse=True)
    except:
        raise Exception("Error al conectarse con la carpeta compartida,"
                        "\nse debe comprobar que no hay cambios de configuracion en rutas\n"
                        "   y si el usuario se encuentra conectado a la red."
                        "\nSi el problema persiste conctarse con el programador:\ns.benaventebravo@gmail.com")
"Generar Libreria de funciones "

def validacionArchivo(conexion,nombreArchivo):

    p = Path(conexion.get_path())
    p = p / "saldocl.txt"
    if p.exists():
        p.resolve()
        return str(p)
    else:
        raise Exception("El archivo {0}, no existe en la carpeta de archivos".format(nombreArchivo))

def MostrarMensaje(e):
    msjBox = QtGui.QMessageBox()
    msjBox.setWindowTitle("Mensaje")
    msjBox.setText(e)
    msjBox.exec_()
def formatoAtributoInforme(cadena,largo):
    listaCandena= list(cadena)
    for i in range(largo - len(cadena)):
        listaCandena.append(" ")
    return "".join(listaCandena)

class RegistroArchivo:
    def __init__(self):
        self.cliente = ""
        self.pedido = ""
        self.fechaPedido = ""
        self.descEtiqueta = ""
        self.codEtiqueta = ""
        self.cantPedida = ""
        self.cantCliente = ""
        self.cantRevisada = ""
        self.cantDespachada = ""
        self.saldo = ""
        self.precio = ""
        self.saldoValor = ""
        self.diaDespacho1 = ""
        self.mesDespacho1 = ""
        self.anioDespacho1 = ""
        self.cantDespacho1 = ""
        self.diaDespacho2 = ""
        self.mesDespacho2 = ""
        self.anioDespacho2 = ""
        self.cantDespacho2 = ""
        self.diaDespacho3 = ""
        self.mesDespacho3 = ""
        self.anioDespacho3 = ""
        self.cantDespacho3 = ""
        self.fechaPrimeraRevision = ""
        self.fechaUltimoDespacho = ""
        self.mesesStock = 0.0

    def getCliente(self):
        return self.cliente
        pass
    def setCliente(self,value):
        self.cliente = value.rstrip(" ")
        pass
    def getPedido(self):
        return self.pedido
        pass
    def setPedido(self, value):
        self.pedido = value
        pass
    def getFechaPedido(self):
        return self.fechaPedido
        pass
    def setFechaPedido(self,value):
        self.fechaPedido = datetime.date(int(value[0:4]),int(value[4:6]),int(value[6:8]))
        pass
    def getDescEtiqueta(self):
        return self.descEtiqueta
        pass
    def setDescEtiqueta(self, value):
        self.descEtiqueta = value.rstrip(" ")
        pass
    def getCodEtiqueta(self):
        return self.codEtiqueta
        pass
    def setCodEtiqueta(self, value):
        self.codEtiqueta = value.rstrip(" ")
        pass
    def getCantPedida(self):
        return self.cantPedida
        pass
    def setCantPedida(self, value):
        self.cantPedida = "{:,}".format(int(value)).replace(',','.')
        pass
    def getCantCliente(self):
        return self.cantCliente
        pass
    def setCantCliente(self, value):
        self.cantCliente = "{:,}".format(int(value)).replace(',','.')
        pass
    def getCantRevisada(self):
        return self.cantRevisada
        pass
    def setCantRevisada(self, value):
        self.cantRevisada = "{:,}".format(int(value)).replace(',','.')
        pass
    def getCantDespachada(self):
        return self.cantDespachada
        pass
    def setCantDespachada(self, value):
        self.cantDespachada = "{:,}".format(int(value)).replace(',','.')
        pass
    def getSaldo(self):
        return self.saldo
        pass
    def setSaldo(self, value):
        cifra = value.split(" ")
        cifra = cifra[len(cifra) - 1]
        self.saldo = cifra
        pass
    def getPrecio(self):
        return self.precio
        pass
    def setPrecio(self, value):
        value = value.lstrip("0")
        if len(value) is 2 or len(value) is 1:
            value = '0' + "," + value
        else:
            value = value[0:len(value) - 2] + "," + value[len(value) - 2:]
        self.precio = value
        pass
    def getSaldoValor(self):
        return self.saldoValor
        pass
    def setSaldoValor(self, value):
        self.saldoValor = "{:,}".format(int(value)).replace(',','.')
        pass

    def getDiaDespacho1(self):
        return self.diaDespacho1
        pass
    def setDiaDespacho1(self, value):
        self.diaDespacho1 = value
        pass
    def getMesDespacho1(self):
        return self.mesDespacho1
        pass
    def setMesDespacho1(self, value):
        self.mesDespacho1 = value
        pass
    def getAnioDespacho1(self):
        return self.anioDespacho1
        pass
    def setAnioDespacho1(self, value):
        self.anioDespacho1 = value
        pass
    def getCantDespacho1(self):
        return self.cantDespacho1
        pass
    def setCantDespacho1(self, value):
        self.cantDespacho1 = value
        pass

    def getDiaDespacho2(self):
        return self.diaDespacho2
        pass

    def setDiaDespacho2(self, value):
        self.diaDespacho2 = value
        pass

    def getMesDespacho2(self):
        return self.mesDespacho2
        pass

    def setMesDespacho2(self, value):
        self.mesDespacho2 = value
        pass

    def getAnioDespacho2(self):
        return self.anioDespacho2
        pass

    def setAnioDespacho2(self, value):
        self.anioDespacho2 = value
        pass

    def getCantDespacho2(self):
        return self.cantDespacho1
        pass

    def setCantDespacho2(self, value):
        self.cantDespacho1 = value
        pass

    def getDiaDespacho3(self):
        return self.diaDespacho3
        pass

    def setDiaDespacho3(self, value):
        self.diaDespacho3 = value
        pass

    def getMesDespacho3(self):
        return self.mesDespacho3
        pass

    def setMesDespacho3(self, value):
        self.mesDespacho3 = value
        pass

    def getAnioDespacho3(self):
        return self.anioDespacho3
        pass

    def getCantDespacho3(self):
        return self.cantDespacho1
        pass

    def setCantDespacho3(self, value):
        self.cantDespacho1 = value
        pass

    def setAnioDespacho3(self, value):
        self.anioDespacho3 = value
        pass
    def getFechaPrimeraRevision(self):
        return self.fechaPrimeraRevision
        pass
    def setFechaPrimeraRevision(self, value):
        self.fechaPrimeraRevision = datetime.date(int(value[0:4]), int(value[4:6]), int(value[6:8]))
        hoy = datetime.date.today()
        self.mesesStock = round(float((hoy - self.getFechaPrimeraRevision()).days) / 30, 2)
        pass
    def getFechaUltimoDespacho(self):
        return self.fechaUltimoDespacho
        pass
    def setFechaultimoDespacho(self, value):
        self.fechaUltimoDespacho = datetime.date(int(value[0:4]),int(value[4:6]),int(value[6:8]))
        pass
    def getMesesStock(self):
        return self.mesesStock
        pass

    def __str__(self):
        return "[{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21}," \
               "{22},{23},{24},{25}]".format(self.getCliente(),self.getPedido(),self.getFechaPedido(),
                                                  self.getDescEtiqueta(),self.getCodEtiqueta(),self.getCantPedida(),
                                                  self.getCantCliente(),self.getCantRevisada(),self.getSaldo(),
                                                  self.getPrecio(),self.getSaldoValor(),self.getDiaDespacho1(),
                                                  self.getMesDespacho1(),self.getAnioDespacho1(),self.getCantDespacho1(),
                                                  self.getDiaDespacho2(),self.getMesDespacho2(),self.getAnioDespacho2(),
                                                  self.getCantDespacho2(),self.getDiaDespacho3(),self.getMesDespacho3(),
                                                  self.getAnioDespacho3(),self.getCantDespacho3(),
                                                  self.getFechaPrimeraRevision(),self.getFechaUltimoDespacho(),
                                                  self.getMesesStock())
    def impresionInformeTodos(self):
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}\n"\
                                       .format(formatoAtributoInforme(self.getCliente(), 35),
                                               formatoAtributoInforme(self.getPedido(), 10),
                                               formatoAtributoInforme(self.getCodEtiqueta(), 20),
                                               formatoAtributoInforme(self.getDescEtiqueta(), 40),
                                               formatoAtributoInforme(self.getCantPedida(), 20),
                                               formatoAtributoInforme(self.getCantRevisada(), 15),
                                               formatoAtributoInforme(self.getCantDespachada(), 15),
                                               formatoAtributoInforme(self.getSaldo(), 15),
                                               formatoAtributoInforme(self.getPrecio(), 15),
                                               formatoAtributoInforme(self.getSaldoValor(), 15),
                                               formatoAtributoInforme(str(self.getFechaPrimeraRevision().
                                                                          year), 15),
                                               formatoAtributoInforme(str(self.getFechaPrimeraRevision().
                                                                          month), 15),
                                               formatoAtributoInforme(self.getFechaPrimeraRevision().
                                                                      strftime("%d-%m-%Y"), 15),
                                               formatoAtributoInforme(str(self.getMesesStock()), 15))
    def impresionInformeCliente(self):
        return "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}\n".format(
                                                       formatoAtributoInforme(self.getPedido(), 10),
                                                       formatoAtributoInforme(self.getCodEtiqueta(), 20),
                                                       formatoAtributoInforme(self.getDescEtiqueta(), 40),
                                                       formatoAtributoInforme(self.getCantPedida(), 20),
                                                       formatoAtributoInforme(self.getCantRevisada(), 15),
                                                       formatoAtributoInforme(self.getCantDespachada(), 15),
                                                       formatoAtributoInforme(self.getSaldo(), 15),
                                                       formatoAtributoInforme(self.getPrecio(), 15),
                                                       formatoAtributoInforme(self.getSaldoValor(), 15),
                                                       formatoAtributoInforme(str(self.getFechaPrimeraRevision().
                                                                                  year), 15),
                                                       formatoAtributoInforme(str(self.getFechaPrimeraRevision().
                                                                                  month), 15),
                                                       formatoAtributoInforme(self.getFechaPrimeraRevision().
                                                                              strftime("%d-%m-%Y"), 15),
                                                       formatoAtributoInforme(str(self.getMesesStock()), 15))
"se recuperan los nombres de todos los clientes"
def nombresClientes(listaDatos):
    conjuntoNombres = set()
    for registro in listaDatos:
        conjuntoNombres.add(registro.getCliente())
    return conjuntoNombres
"Funciones de filtrado por meses"
def filtrarCliente(listaDatos, cliente):
    listaCliente = list()
    for registro in listaDatos:
        if(registro.getCliente()  == cliente):
            listaCliente.append(registro)
    return listaCliente

def filtrarMenores3Meses(listaDatos):
    listaMeses = list()
    for registro in listaDatos:
        if(registro.getMesesStock() < 3.1):
            listaMeses.append(registro)
    return listaMeses

def filtrar3A4Meses(listaDatos):
    listaMeses = list()
    for registro in listaDatos:
        if registro.getMesesStock() >= 3.1 and registro.getMesesStock() < 4.1:
            listaMeses.append(registro)
    return listaMeses

def filtrar4A5Meses(listaDatos):
    listaMeses = list()
    for registro in listaDatos:
        if (registro.getMesesStock() >= 4.1 and registro.getMesesStock() < 5.1):
            listaMeses.append(registro)
    return listaMeses

def filtrarMasDe5Meses(listaDatos):
    listaMeses = list()
    for registro in listaDatos:
        if (registro.getMesesStock() >= 5.1):
            listaMeses.append(registro)
    return listaMeses

def filtrarMesesVariable(listaDatos,limiteInferior, limiteSuperior):
    listaMeses = list()
    for registro in listaDatos:
        if (registro.getMesesStock() >= limiteInferior and registro.getMesesStock() < limiteSuperior):
            listaMeses.append(registro)
    return listaMeses
"funciones de anios de clientes"
def obtenerAnios(listaDatos):
    conjuntoAnios = set()
    for registro in listaDatos:
        conjuntoAnios.add(registro.getFechaPrimeraRevision().year)
    return conjuntoAnios
    pass

def filtrarAnio(listaDatos, anio):
    listaAnio = list()
    for registro in listaDatos:
        if (registro.getFechaPrimeraRevision().year == anio):
            listaAnio.append(registro)
    return listaAnio
    pass
"calculo de saldo "
def calcularSaldo(listaDatos):
    saldoTotal = 0
    for registro in listaDatos:
        valor = registro.getSaldoValor().split('.')
        cantidad = ""
        for cifra in valor:
            cantidad += cifra
        saldoTotal += int(cantidad)
    saldoFinal ='${:,}'.format(saldoTotal).replace(',','.')
    return saldoFinal
"Fecha del ultimo registro"
def obtenerFechaMax(listaDatos):
    conjuntoFechas = set()
    for registro in listaDatos:
        conjuntoFechas.add(registro.getFechaPrimeraRevision())
    fechaMaxima = max(list(conjuntoFechas))
    return fechaMaxima
    pass

class vInforme1(QtGui.QMainWindow):
    def __init__(self, parent = None):
        try:
            QtGui.QWidget.__init__(self, parent)
            self.ui = vSaldoClInforme.Ui_MainWindow()
            self.ui.setupUi(self)
            self.setWindowTitle("Generador de Informes")
            self.listaDatos = archivoALista()
            self.ui.tableWidget.setColumnCount(0)
            self.filtrarTodos = False
            self.ui.cmbAnio.setEnabled(False)
            self.listaActual = list()
            self.filtroAplicado = "Unico Cliente"
            bar = self.menuBar()
            file = bar.addMenu("Utilidades")
            exportar = QtGui.QAction("Exportar Tabla", self)
            file.addAction(exportar)
            exportar.setShortcut("Ctrl+E")
            ayuda = QtGui.QAction("Ayuda", self)
            file.addAction(ayuda)
            ayuda.setShortcut("Ctrl+A")
            quit = QtGui.QAction("Salir", self)
            file.addAction(quit)
            quit.setShortcut("Ctrl+S")
            file.triggered[QtGui.QAction].connect(self.processtrigger)
            pixmap = QtGui.QPixmap('./2.jpg')
            self.ui.label_2.setPixmap(pixmap.scaled(400, 100, QtCore.Qt.KeepAspectRatio))
            pixmap = QtGui.QPixmap('./2.jpg')
            self.ui.label_3.setPixmap(pixmap.scaled(400, 100, QtCore.Qt.KeepAspectRatio))

        except Exception as e:
            MostrarMensaje(e.message)
            sys.exit(1)
        else:
            self.ui.lblFActual.setText("Fecha Actual : " + datetime.date.today().strftime("%d/%m/%Y"))
            self.ui.lblFReporte.setText("Fecha del Archivo: " + obtenerFechaMax(self.listaDatos).strftime("%d/%m/%Y"))
            self.ui.cmbClientes.addItem("----Seleccione Cliente----")
            self.cargarCmbClientes()
            listaCliente = filtrarCliente(self.listaDatos, (self.ui.cmbClientes.currentText()))
            self.cargarDatosCliente(listaCliente)
            self.listaActual = listaCliente
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaCliente)))
            QtCore.QObject.connect(self.ui.rb0A3Meses, QtCore.SIGNAL('clicked()'), self.pb0A3Meses_click)
            QtCore.QObject.connect(self.ui.rb3A4Meses, QtCore.SIGNAL('clicked()'), self.pb3A4Meses_click)
            QtCore.QObject.connect(self.ui.rb4A5Meses, QtCore.SIGNAL('clicked()'), self.pb4A5Meses_click)
            QtCore.QObject.connect(self.ui.rbMasDe5Meses, QtCore.SIGNAL('clicked()'), self.pbMasDe5Meses_click)

            QtCore.QObject.connect(self.ui.cmbClientes, QtCore.SIGNAL('currentIndexChanged(int)'),
                                   self.cmbClientes_currentIndexChanged)
            QtCore.QObject.connect(self.ui.cmbAnio, QtCore.SIGNAL('currentIndexChanged(int)'),
                                   self.cmbAnio_currentIndexChanged)
            QtCore.QObject.connect(self.ui.rbMostrarTodos, QtCore.SIGNAL('clicked(bool)'), self.rbMostrarTodos_click)
            QtCore.QObject.connect(self.ui.rbFiltroAnio1, QtCore.SIGNAL('clicked(bool)'), self.rbFiltroAnio1_checked)
            QtCore.QObject.connect(self.ui.rbFiltroAnio2, QtCore.SIGNAL('clicked(bool)'), self.rbFiltroAnio2_checked)

    def resetearCmbClientes(self):
        self.ui.cmbClientes.clear()
        self.ui.cmbClientes.addItem("----Seleccione Cliente----")
    def processtrigger(self, q):
        correcto = False;
        if q.text() == "Exportar Tabla":
            if len(self.listaActual) > 0:
                try:
                    if self.filtrarTodos:
                        newArchivo, ok = QtGui.QInputDialog.getText(self, "Exportacion de Tabla",
                                                                      "Escriba el nombre del archivo")

                        if ok and (len(newArchivo) != 0):
                            nuevoArchivo = open(str(winshell.desktop()) + "/"+newArchivo+".txt", 'w')
                            nuevoArchivo.write("\tFiltro:{0}".format(self.filtroAplicado)
                                               + "\t Fecha:{0}\n\n".format(datetime.date.today().strftime("%d/%m/%Y")))
                            cabezera = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}{13}\n"\
                                                .format(formatoAtributoInforme('Cliente', 35),
                                                        formatoAtributoInforme('Pedido', 10),
                                                        formatoAtributoInforme('Codigo', 20),
                                                        formatoAtributoInforme('Descripcion', 40),
                                                        formatoAtributoInforme('Cant. Pedida', 20),
                                                        formatoAtributoInforme('Fabricado', 15),
                                                        formatoAtributoInforme('Despachado', 15),
                                                        formatoAtributoInforme('Cant. Saldo', 15),
                                                        formatoAtributoInforme('Precio', 15),
                                                        formatoAtributoInforme('Saldo$', 15),
                                                        formatoAtributoInforme('Anio Ingreso', 15),
                                                        formatoAtributoInforme('Mes Ingreso', 15),
                                                        formatoAtributoInforme('Fecha Ingreso', 15),
                                                        formatoAtributoInforme('Meses Stock', 15))

                            nuevoArchivo.write(cabezera)
                            separador = "\n"
                            nuevoArchivo.write(separador)
                            for registro in self.listaActual:
                                nuevoArchivo.write(registro.impresionInformeTodos())
                            nuevoArchivo.write(separador)
                            nuevoArchivo.write("Saldo $ TOTAL :{0}".format(calcularSaldo(self.listaActual)))
                            nuevoArchivo.close()
                            correcto = True
                        else:
                            pass
                    else:
                        dialog = QtGui.QInputDialog()
                        dialog.resize(200,200)
                        newArchivo, ok = dialog.getText(self, "Exportacion de Tabla",
                                                                    "Escriba el nombre del archivo")
                        if ok and (len(newArchivo) != 0):
                            nuevoArchivo = open(str(winshell.desktop()) + "/"+newArchivo+".txt", 'w')
                            nombreCliente = self.listaActual[0].getCliente()
                            nuevoArchivo.write("Cliente: {0}".format(nombreCliente) + "\tFiltro:{0}".format(self.filtroAplicado)
                                               +"\t Fecha:{0}\n\n".format(datetime.date.today().strftime("%d/%m/%Y")))
                            cabezera = "{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11}{12}\n".format(
                                        formatoAtributoInforme('Pedido', 10),
                                        formatoAtributoInforme('Codigo', 20),
                                        formatoAtributoInforme('Descripcion', 40),
                                        formatoAtributoInforme('Cant. Pedida', 20),
                                        formatoAtributoInforme('Fabricado', 15),
                                        formatoAtributoInforme('Despachado', 15),
                                        formatoAtributoInforme('Cant. Saldo', 15),
                                        formatoAtributoInforme('Precio', 15),
                                        formatoAtributoInforme('Saldo$', 15),
                                        formatoAtributoInforme('Anio Ingreso', 15),
                                        formatoAtributoInforme('Mes Ingreso', 15),
                                        formatoAtributoInforme('Fecha Ingreso', 15),
                                        formatoAtributoInforme('Meses Stock', 15))

                            nuevoArchivo.write(cabezera)
                            separador = "\n"
                            nuevoArchivo.write(separador)
                            for registro in self.listaActual:
                                nuevoArchivo.write(registro.impresionInformeCliente())
                            nuevoArchivo.write(separador)
                            nuevoArchivo.write("Saldo $ TOTAL :{0}".format(calcularSaldo(self.listaActual)))
                            nuevoArchivo.close()
                            correcto = True
                except Exception as e:
                    MostrarMensaje("Error al generar el informe, por favor espere unos segundo y vueva a generar")
                else:
                    if correcto == True:
                        MostrarMensaje("Informe generado con exito!")
                    else:
                        MostrarMensaje("No se pudo generar el informe!")
            else:
                MostrarMensaje("No hay datos para exportar en la tabla")

        elif q.text() == "Ayuda":
            os.system("Manual.pdf &")
        elif q.text() == "Salir":
            sys.exit(0)

    def rbFiltroAnio1_checked(self):
        self.ui.cmbAnio.setEnabled(True)
        self.ui.gbAnio.setEnabled(False)

        self.ui.rb0A3Meses.setAutoExclusive(False)
        self.ui.rb3A4Meses.setAutoExclusive(False)
        self.ui.rb4A5Meses.setAutoExclusive(False)
        self.ui.rbMasDe5Meses.setAutoExclusive(False)

        self.ui.rb0A3Meses.setChecked(False)
        self.ui.rb3A4Meses.setChecked(False)
        self.ui.rb4A5Meses.setChecked(False)
        self.ui.rbMasDe5Meses.setChecked(False)

        self.ui.rb0A3Meses.setAutoExclusive(True)
        self.ui.rb3A4Meses.setAutoExclusive(True)
        self.ui.rb4A5Meses.setAutoExclusive(True)
        self.ui.rbMasDe5Meses.setAutoExclusive(True)

        if self.filtrarTodos:
            self.cargarCmbAniosTodos()
            pass
        else:
            self.cargarCmbAniosCliente()
            pass
    def rbFiltroAnio2_checked(self):
        self.ui.cmbAnio.setEnabled(False)
        self.ui.gbAnio.setEnabled(True)

        self.ui.rb0A3Meses.setAutoExclusive(False)
        self.ui.rb3A4Meses.setAutoExclusive(False)
        self.ui.rb4A5Meses.setAutoExclusive(False)
        self.ui.rbMasDe5Meses.setAutoExclusive(False)

        self.ui.rb0A3Meses.setChecked(False)
        self.ui.rb3A4Meses.setChecked(False)
        self.ui.rb4A5Meses.setChecked(False)
        self.ui.rbMasDe5Meses.setChecked(False)

        self.ui.rb0A3Meses.setAutoExclusive(True)
        self.ui.rb3A4Meses.setAutoExclusive(True)
        self.ui.rb4A5Meses.setAutoExclusive(True)
        self.ui.rbMasDe5Meses.setAutoExclusive(True)

        self.ui.cmbAnio.clear()

        if self.filtrarTodos:
            self.cargarDatos(self.listaDatos)
        else:
            self.cargarDatosCliente(filtrarCliente(self.listaDatos,(self.ui.cmbClientes.currentText())))

    def cargarCmbClientes(self):
        self.resetearCmbClientes()
        for nombre in sorted(list(nombresClientes(self.listaDatos))):
            self.ui.cmbClientes.addItem(nombre)
    def cargarCmbAniosTodos(self):
        self.ui.cmbAnio.clear()
        for anio in sorted(list(obtenerAnios(self.listaDatos))):
            self.ui.cmbAnio.addItem(str(anio))
    def cargarCmbAniosCliente(self):
        self.ui.cmbAnio.clear()
        for anio in sorted(list(obtenerAnios(filtrarCliente(self.listaDatos, str(self.ui.cmbClientes.currentText()))))):
            self.ui.cmbAnio.addItem(str(anio))

    "Tipos de informe"
    def rbMostrarTodos_click(self):
        if self.ui.rbMostrarTodos.isChecked():
            self.ui.cmbClientes.setCurrentIndex(0)
            self.filtrarTodos = True
            self.cargarDatos(self.listaDatos)
            self.cargarCmbAniosTodos()
            self.ui.gbAnio.setEnabled(True)
            self.ui.cmbAnio.clear()
            self.ui.rbFiltroAnio2.setChecked(True)
            self.ui.rb0A3Meses.setAutoExclusive(False)
            self.ui.rb3A4Meses.setAutoExclusive(False)
            self.ui.rb4A5Meses.setAutoExclusive(False)
            self.ui.rbMasDe5Meses.setAutoExclusive(False)

            self.ui.rb0A3Meses.setChecked(False)
            self.ui.rb3A4Meses.setChecked(False)
            self.ui.rb4A5Meses.setChecked(False)
            self.ui.rbMasDe5Meses.setChecked(False)

            self.ui.rb0A3Meses.setAutoExclusive(True)
            self.ui.rb3A4Meses.setAutoExclusive(True)
            self.ui.rb4A5Meses.setAutoExclusive(True)
            self.ui.rbMasDe5Meses.setAutoExclusive(True)
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(self.listaDatos)))
            MostrarMensaje("Se han cargado {0} registros".format(len(self.listaDatos)))
            self.listaActual = self.listaDatos
            self.filtroAplicado = "Todos los Clientes"

    "Filtrado de Meses"
    def pb0A3Meses_click(self):
        listaMeses = list()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        if self.filtrarTodos is True:
            listaMeses = filtrarMenores3Meses(self.listaDatos)
            self.cargarDatos(listaMeses)
            self.filtroAplicado = "Todos los clientes de 0 A 3 Meses de Stock"
        else:
            listaCliente = filtrarCliente(self.listaDatos, str(self.ui.cmbClientes.currentText()))
            listaMeses = filtrarMenores3Meses(listaCliente)
            self.cargarDatosCliente(listaMeses)
            self.filtroAplicado = "0 A 3 Meses de Stock"
        if len(listaMeses) > 0:
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaMeses)))
        else:
            self.ui.lblTotalSaldoCantidad.setText('$0')
            MostrarMensaje("El cliente no tiene pedidos de 0 a 3 meses")
        self.listaActual = listaMeses
    def pb3A4Meses_click(self):
        listaMeses = list()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        if self.filtrarTodos is True:
            listaMeses = filtrar3A4Meses(self.listaDatos)
            self.cargarDatos(listaMeses)
            self.filtroAplicado = "Todos los clientes de 3 A 4 Meses de Stock"
        else:
            listaCliente = filtrarCliente(self.listaDatos,str(self.ui.cmbClientes.currentText()))
            listaMeses = filtrar3A4Meses(listaCliente)
            self.cargarDatosCliente(listaMeses)
            self.filtroAplicado = "3 A 4 Meses de Stock"
        if len(listaMeses) > 0:
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaMeses)))
        else:
            self.ui.lblTotalSaldoCantidad.setText('$0')
            MostrarMensaje("El cliente no tiene pedidos de 3 a 4 meses")

        self.listaActual = listaMeses
    def pb4A5Meses_click(self):
        listaMeses = list()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        if self.filtrarTodos is True:
                listaMeses = filtrar4A5Meses(self.listaDatos)
                self.cargarDatos(listaMeses)
                self.filtroAplicado = "Todos los clientes de 4 A 5 Meses de Stock"
        else:
            listaCliente = filtrarCliente(self.listaDatos,self.ui.cmbClientes.currentText())
            listaMeses = filtrar4A5Meses(listaCliente)
            self.cargarDatosCliente(listaMeses)
            self.filtroAplicado = "4 A 5 Meses de Stock"
        if len(listaMeses) > 0:
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaMeses)))
        else:
            self.ui.lblTotalSaldoCantidad.setText('$0')
            MostrarMensaje("El cliente no tiene pedidos de 4 a 5 meses")

        self.listaActual = listaMeses
    def pbMasDe5Meses_click(self):
        listaMeses = list()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)
        if self.filtrarTodos is True:
                listaMeses = filtrarMasDe5Meses(self.listaDatos)
                self.cargarDatos(listaMeses)
                self.filtroAplicado = "Todos los clientes con mas de 5 meses de Stock"
        else:
            listaCliente = filtrarCliente(self.listaDatos,str(self.ui.cmbClientes.currentText()))
            listaMeses = filtrarMasDe5Meses(listaCliente)
            self.cargarDatosCliente(listaMeses)
            self.filtroAplicado = "Mas de 5 Meses de Stock"
        if len(listaMeses) > 0:
            self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaMeses)))
        else:
            self.ui.lblTotalSaldoCantidad.setText('$0')
            MostrarMensaje("El cliente no tiene pedidos de mas de 5 meses")

        self.listaActual = listaMeses

    "Filtrado de Clientes"
    def cmbClientes_currentIndexChanged(self):
        if(self.ui.cmbClientes.currentText() != "----Seleccione Cliente----"):
            if(int(self.ui.cmbClientes.count()) != 0):
                self.ui.rbMostrarTodos.setChecked(False)
                self.ui.rbFiltroAnio2.setChecked(True)
                self.ui.rb0A3Meses.setAutoExclusive(False)
                self.ui.rb3A4Meses.setAutoExclusive(False)
                self.ui.rb4A5Meses.setAutoExclusive(False)
                self.ui.rbMasDe5Meses.setAutoExclusive(False)

                self.ui.rb0A3Meses.setChecked(False)
                self.ui.rb3A4Meses.setChecked(False)
                self.ui.rb4A5Meses.setChecked(False)
                self.ui.rbMasDe5Meses.setChecked(False)

                self.ui.rb0A3Meses.setAutoExclusive(True)
                self.ui.rb3A4Meses.setAutoExclusive(True)
                self.ui.rb4A5Meses.setAutoExclusive(True)
                self.ui.rbMasDe5Meses.setAutoExclusive(True)
                self.filtroAplicado = "Unico Cliente"
                cliente = self.ui.cmbClientes.itemText(self.ui.cmbClientes.currentIndex())
                listaCliente = filtrarCliente(self.listaDatos, cliente)
                self.filtrarTodos = False
                self.ui.cmbAnio.clear()
                self.ui.gbAnio.setEnabled(True)
                self.ui.cmbAnio.setEnabled(False)
                if len(listaCliente) > 0:
                    self.cargarDatosCliente(listaCliente)
                    self.ui.lblTotalSaldoCantidad.setText(str(calcularSaldo(listaCliente)))
                    self.listaActual = listaCliente
                else:
                    self.ui.lblTotalSaldoCantidad.setText('$0')
                    MostrarMensaje("El cliente no tiene pedidos vigentes")
        else:
            self.ui.tableWidget.setRowCount(0)
    "Filtrado de Anios"
    def cmbAnio_currentIndexChanged(self):
        if (int(self.ui.cmbAnio.count()) != 0):
            listaAnio = list()
            if int(self.ui.cmbAnio.currentText()) == datetime.date.today().year:
                self.ui.gbAnio.setEnabled(True)
                self.ui.gbAnio.setChecked(False)
            else:
                self.ui.gbAnio.setEnabled(False)
                self.ui.gbAnio.setChecked(False)
            if self.filtrarTodos:
                if self.ui.cmbAnio.isEnabled():
                    self.ui.tableWidget.setRowCount(0)
                    self.ui.tableWidget.setColumnCount(0)
                    "cargar datos de todos"
                    listaAnio = filtrarAnio(self.listaDatos, int(self.ui.cmbAnio.currentText()))
                    self.cargarDatos(listaAnio)
                    self.filtroAplicado = "Todos los Clientes, Vista del Año {0}"\
                        .format(int(self.ui.cmbAnio.currentText()))
            else:
                if self.ui.cmbAnio.isEnabled():
                    self.ui.tableWidget.setRowCount(0)
                    self.ui.tableWidget.setColumnCount(0)
                    "cargar datos del cliente"
                    listaCliente = filtrarCliente(self.listaDatos, str(self.ui.cmbClientes.currentText()))
                    anio = int(self.ui.cmbAnio.currentText())
                    listaAnio = filtrarAnio(listaCliente, anio)
                    self.cargarDatosCliente(listaAnio)
                    self.filtroAplicado = "Vista del Año {0}" \
                        .format(int(self.ui.cmbAnio.currentText()))
            self.ui.lblTotalSaldoCantidad.setText(calcularSaldo(listaAnio))
            self.listaActual = listaAnio



        pass
    def cargarDatosCliente(self, listaDatos):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(13)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Pedido','Codigo','Descripcion','Cant. Pedida','Fabricado',
                                                       'Despachado','Saldo Cant.', 'Precio', 'Saldo $',
                                                       "Año Ingreso".decode('utf8'),'Mes Ingreso', 'Fecha Ingreso',
                                                       'Meses Stock'])
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 300)
        self.ui.tableWidget.setColumnWidth(3, 100)
        self.ui.tableWidget.setColumnWidth(4, 80)
        self.ui.tableWidget.setColumnWidth(5, 80)
        self.ui.tableWidget.setColumnWidth(6, 80)
        self.ui.tableWidget.setColumnWidth(7, 50)
        self.ui.tableWidget.setColumnWidth(8, 80)
        self.ui.tableWidget.setColumnWidth(9, 80)
        self.ui.tableWidget.setColumnWidth(10, 80)
        self.ui.tableWidget.setColumnWidth(11, 80)
        self.ui.tableWidget.setColumnWidth(12, 80)

        for rowNum in range(len(listaDatos)):
            self.ui.tableWidget.insertRow(rowNum)
            self.ui.tableWidget.setItem(rowNum, 0, QtGui.QTableWidgetItem(listaDatos[rowNum].getPedido()))
            self.ui.tableWidget.setItem(rowNum, 1, QtGui.QTableWidgetItem(listaDatos[rowNum].getCodEtiqueta()))
            self.ui.tableWidget.setItem(rowNum, 2, QtGui.QTableWidgetItem(listaDatos[rowNum].getDescEtiqueta()))
            self.ui.tableWidget.setItem(rowNum, 3, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantPedida()))
            self.ui.tableWidget.setItem(rowNum, 4, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantRevisada()))
            self.ui.tableWidget.setItem(rowNum, 5, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantDespachada()))
            self.ui.tableWidget.setItem(rowNum, 6, QtGui.QTableWidgetItem(listaDatos[rowNum].getSaldo()))
            self.ui.tableWidget.setItem(rowNum, 7, QtGui.QTableWidgetItem(listaDatos[rowNum].getPrecio()))
            self.ui.tableWidget.setItem(rowNum, 8, QtGui.QTableWidgetItem(listaDatos[rowNum].getSaldoValor()))
            self.ui.tableWidget.setItem(rowNum, 9,
                                        QtGui.QTableWidgetItem(str(listaDatos[rowNum].getFechaPrimeraRevision().year)))
            self.ui.tableWidget.setItem(rowNum, 10,
                                        QtGui.QTableWidgetItem(str(listaDatos[rowNum].getFechaPrimeraRevision().month)))
            self.ui.tableWidget.setItem(rowNum, 11,
                                        QtGui.QTableWidgetItem(listaDatos[rowNum].getFechaPrimeraRevision().
                                                               strftime("%d-%m-%Y")))
            self.ui.tableWidget.setItem(rowNum, 12,QtGui.QTableWidgetItem(str(listaDatos[rowNum].getMesesStock())))
    def cargarDatos(self, listaDatos):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(14)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Cliente','Pedido','Codigo','Descripcion','Cant. Pedida',
                                                       'Fabricado','Despachado','Saldo Cant.', 'Precio', 'Saldo $',
                                                       "Año Ingreso".decode('utf8'),'Mes Ingreso', 'Fecha Ingreso',
                                                       'Meses Stock'])
        self.ui.tableWidget.setColumnWidth(0, 150)
        self.ui.tableWidget.setColumnWidth(1, 50)
        self.ui.tableWidget.setColumnWidth(2, 50)
        self.ui.tableWidget.setColumnWidth(3, 280)
        self.ui.tableWidget.setColumnWidth(4, 100)
        self.ui.tableWidget.setColumnWidth(5, 80)
        self.ui.tableWidget.setColumnWidth(6, 80)
        self.ui.tableWidget.setColumnWidth(7, 80)
        self.ui.tableWidget.setColumnWidth(8, 50)
        self.ui.tableWidget.setColumnWidth(9, 80)
        self.ui.tableWidget.setColumnWidth(10, 80)
        self.ui.tableWidget.setColumnWidth(11, 80)
        self.ui.tableWidget.setColumnWidth(12, 80)
        self.ui.tableWidget.setColumnWidth(13, 80)

        for rowNum in range(len(listaDatos)):
            self.ui.tableWidget.insertRow(rowNum)
            self.ui.tableWidget.setItem(rowNum, 0, QtGui.QTableWidgetItem(listaDatos[rowNum].getCliente()))
            self.ui.tableWidget.setItem(rowNum, 1, QtGui.QTableWidgetItem(listaDatos[rowNum].getPedido()))
            self.ui.tableWidget.setItem(rowNum, 2, QtGui.QTableWidgetItem(listaDatos[rowNum].getCodEtiqueta()))
            self.ui.tableWidget.setItem(rowNum, 3, QtGui.QTableWidgetItem(listaDatos[rowNum].getDescEtiqueta()))
            self.ui.tableWidget.setItem(rowNum, 4, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantPedida()))
            self.ui.tableWidget.setItem(rowNum, 5, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantRevisada()))
            self.ui.tableWidget.setItem(rowNum, 6, QtGui.QTableWidgetItem(listaDatos[rowNum].getCantDespachada()))
            self.ui.tableWidget.setItem(rowNum, 7, QtGui.QTableWidgetItem(listaDatos[rowNum].getSaldo()))
            self.ui.tableWidget.setItem(rowNum, 8, QtGui.QTableWidgetItem(listaDatos[rowNum].getPrecio()))
            self.ui.tableWidget.setItem(rowNum, 9, QtGui.QTableWidgetItem(listaDatos[rowNum].getSaldoValor()))
            self.ui.tableWidget.setItem(rowNum, 10,
                                        QtGui.QTableWidgetItem(str(listaDatos[rowNum].getFechaPrimeraRevision().year)))
            self.ui.tableWidget.setItem(rowNum, 11,
                                        QtGui.QTableWidgetItem(str(listaDatos[rowNum].getFechaPrimeraRevision().month)))
            self.ui.tableWidget.setItem(rowNum, 12,
                                        QtGui.QTableWidgetItem(listaDatos[rowNum].getFechaPrimeraRevision().
                                                               strftime("%d-%m-%Y")))
            self.ui.tableWidget.setItem(rowNum, 13, QtGui.QTableWidgetItem(str(listaDatos[rowNum].getMesesStock())))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWindow = vInforme1()
    myWindow.show()
    sys.exit(app.exec_())