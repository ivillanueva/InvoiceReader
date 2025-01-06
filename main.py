import sys
import os
import tkinter as tk
from common.objects.invoice import *
from common.common import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

##########################################
############ FUNCTIONS ###################
##########################################
def generar_excel_invoices(invoices, nombre_archivo='invoices.xlsx'):
    """
    Genera un archivo Excel con las columnas Serie, Folio y Fecha a partir de la lista de comprobantes.

    :param invoices: Lista de objetos Comprobante.
    :param nombre_archivo: Nombre del archivo Excel a crear.
    """
    # Definir lista de Tipos de CFDI
    uso_cfdi_gastos = lista_cfdi_gastos()# ['G03','D01','D02','D03', 'D04', 'D08', 'D10']
    uso_cfdi_compras = lista_cfdi_compras() #['G01']

    formas_de_pago = lista_formas_de_pago()
    metodos_de_pago = lista_metodos_de_pago()

    # Crear una lista de diccionarios para almacenar los datos
    datos_compras = []

    for compra in invoices:
        # Agrega un diccionario con los datos de cada comprobante
        if compra.receptor.uso_cfdi in uso_cfdi_compras:
            for concepto in compra.conceptos:
                datos_compras.append({
                    'Folio Fiscal (UUID)' : compra.complemento.uuid,
                    'RFC Emisor': compra.emisor.rfc,
                    'Empresa': compra.emisor.nombre,
                    'Serie': compra.serie,
                    'Folio': compra.folio,
                    'Fecha': compra.fecha,
                    'Forma de Pago': formas_de_pago.get(compra.forma_pago, "Forma de pago no encontrada"),
                    'Método de Pago': metodos_de_pago.get(compra.metodo_pago,"Metodo de pago no encontrado"),
                    'No. Identificación': concepto.no_identificacion,
                    'Descripción': concepto.descripcion,
                    'Clave del Producto (SAT)': concepto.clave_prod_serv,
                    'Cantidad': concepto.cantidad,
                    'Valor Unitario': concepto.valor_unitario,
                    'Importe': concepto.importe,
                    'Descuento': '-',
                    'IVA': concepto.impuestos.traslados.importe,
                    'Total': (concepto.cantidad * concepto.valor_unitario) + concepto.impuestos.traslados.importe
                })

    # Crear un DataFrame de pandas a partir de los datos de Compras
    df_compras = pd.DataFrame(datos_compras)

    # Crear una lista de diccionarios para almacenar los datos de Gastos
    datos_gastos = []

    for gasto in invoices:
        # Agrega un diccionario con los datos de cada gasto
        if gasto.receptor.uso_cfdi in uso_cfdi_gastos:
            datos_gastos.append({
                "Folio Fiscal (UUID)" : gasto.complemento.uuid,
                'RFC Emisor': gasto.emisor.rfc,
                'Empresa': gasto.emisor.nombre,
                'Serie': gasto.serie,
                'Folio': gasto.folio,
                'Fecha': gasto.fecha,
                'Total': gasto.total
            })

    # Crear un DataFrame de pandas a partir de los datos de Gastos
    df_gastos = pd.DataFrame(datos_gastos)



    # Crear una lista de diccionarios para almacenar los datos de Gastos
    datos_pagos20 = []

    for pago20 in invoices:
        # Agrega un diccionario con los datos de cada gasto
        if pago20.receptor.uso_cfdi not in uso_cfdi_gastos and pago20.receptor.uso_cfdi not in uso_cfdi_compras:
            datos_pagos20.append({
                "Folio Fiscal (UUID)" : pago20.complemento.uuid,
                'RFC Emisor': pago20.emisor.rfc,
                'Empresa': pago20.emisor.nombre,
                'Serie': pago20.serie,
                'Folio': pago20.folio,
                'Fecha': pago20.fecha,
                'Total': pago20.total
            })

    # Crear un DataFrame de pandas a partir de los datos de Gastos
    df_pagos20 = pd.DataFrame(datos_pagos20)





    # Guardar el DataFrame en un archivo Excel
    #df.to_excel(nombre_archivo, index=False)

    # Diálogo para guardar el archivo
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Excel files", "*.xlsx"),
                                                              ("All files", "*.*")],                                                            
                                                   title="Guardar archivo como",
                                                   )

    if nombre_archivo:  # Verifica si el usuario no canceló el diálogo
        # Guardar el DataFrame en un archivo Excel
        with pd.ExcelWriter(nombre_archivo) as writer:
            # Escribir el DataFrame de Compras en la hoja "Compras"
            df_compras.to_excel(writer, sheet_name='Compras', index=False)
            # Escribir el DataFrame de Gastos en la hoja "Gastos"
            df_gastos.to_excel(writer, sheet_name='Gastos', index=False)
            # Escribir el DataFrame de Gastos en la hoja "Gastos"
            df_pagos20.to_excel(writer, sheet_name='Sin Clasificacion', index=False)

        print(f"Archivo Excel '{nombre_archivo}' generado exitosamente.")
    else:
        print("Guardado cancelado.")


def create_excelFile():
    """
    Crear el excel.
    """
    invoices = []

    try:
        # Lista todos los archivos en la carpeta
        archivos = os.listdir(root.carpeta_seleccionada)
        i=1
        # Filtra y cuenta solo los archivos con extensión .xml
        for archivo in archivos:
            title_progressinfo_files.config(text=f"Procesando archivo: {archivo} || {i}  de  {root.cantidad_xml} archivos.")
            # Obtiene la ruta completa del archivo XML
            ruta_completa = os.path.join(root.carpeta_seleccionada, archivo)
            # Llama a la función para cargar el comprobante desde el archivo XML
            comprobante = cargar_comprobante_desde_xml(ruta_completa)
            if comprobante:  # Verifica que el comprobante no sea None
                invoices.append(comprobante)
            if (i != root.cantidad_xml):
                i=i+1

        generar_excel_invoices(invoices=invoices, nombre_archivo='test1.xlsx')
        messagebox.showinfo("Proceso Completado", "El archivo Excel ha sido generado exitosamente.")
    
    except FileNotFoundError:
        print("La carpeta especificada no existe.")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return 0


def cargar_comprobante_desde_xml(ruta_archivo_xml):
    # Parsear el archivo XML
    tree = ET.parse(ruta_archivo_xml)
    root = tree.getroot()

    # Namespace
    ns = {
    'cfdi': 'http://www.sat.gob.mx/cfd/4',  # Espacio de nombres para cfdi
    'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'  # Espacio de nombres para tfd
    }

    # Extraer datos del Comprobante
    version = root.attrib.get('Version')
    serie = root.attrib.get('Serie')
    folio = root.attrib.get('Folio')
    fecha = root.attrib.get('Fecha')
    forma_pago = root.attrib.get('FormaPago')
    subtotal = float(root.attrib.get('SubTotal'))
    moneda = root.attrib.get('Moneda')
    total = float(root.attrib.get('Total'))
    sello = root.attrib.get('Sello')
    tipo_de_comprobante = root.attrib.get('TipoDeComprobante')
    exportacion = root.attrib.get('Exportacion')
    metodo_pago = root.attrib.get('MetodoPago')
    lugar_expedicion = root.attrib.get('LugarExpedicion')
    certificado = root.attrib.get('Certificado')
    no_certificado = root.attrib.get('NoCertificado')

    # Crear el objeto Comprobante
    comprobante = Comprobante(version, serie, folio, fecha, forma_pago, subtotal, moneda, total, sello,
                              tipo_de_comprobante, exportacion, metodo_pago, lugar_expedicion, certificado, no_certificado)

    # Extraer Emisor
    emisor_elem = root.find('cfdi:Emisor', ns)
    if emisor_elem is not None:
        rfc = emisor_elem.attrib.get('Rfc')
        nombre = emisor_elem.attrib.get('Nombre')
        regimen_fiscal = emisor_elem.attrib.get('RegimenFiscal')
        comprobante.emisor = Emisor(rfc, nombre, regimen_fiscal)

    # Extraer Receptor
    receptor_elem = root.find('cfdi:Receptor', ns)
    if receptor_elem is not None:
        rfc = receptor_elem.attrib.get('Rfc')
        nombre = receptor_elem.attrib.get('Nombre')
        domicilio_fiscal_receptor = receptor_elem.attrib.get('DomicilioFiscalReceptor')
        regimen_fiscal_receptor = receptor_elem.attrib.get('RegimenFiscalReceptor')
        uso_cfdi = receptor_elem.attrib.get('UsoCFDI')
        comprobante.receptor = Receptor(rfc, nombre, domicilio_fiscal_receptor, regimen_fiscal_receptor, uso_cfdi)

    # Extraer Conceptos
    conceptos_list = []
    conceptos_elem = root.find('cfdi:Conceptos', ns)
    if conceptos_elem is not None:
        for concepto_elem in conceptos_elem.findall('cfdi:Concepto', ns):
            clave_prod_serv = concepto_elem.attrib.get('ClaveProdServ')
            no_identificacion = concepto_elem.attrib.get('NoIdentificacion')
            cantidad = float(concepto_elem.attrib.get('Cantidad'))
            clave_unidad = concepto_elem.attrib.get('ClaveUnidad')
            unidad = concepto_elem.attrib.get('Unidad')
            descripcion = concepto_elem.attrib.get('Descripcion')
            valor_unitario = float(concepto_elem.attrib.get('ValorUnitario'))
            importe = float(concepto_elem.attrib.get('Importe'))
            objeto_imp = concepto_elem.attrib.get('ObjetoImp')

            impuestos_concepto_elem = concepto_elem.find('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado',ns)
            if impuestos_concepto_elem is not None:
                #traslados_impuestos_concepto_elem = impuestos_concepto_elem.find('cfdi:Traslados')
                #if traslados_impuestos_concepto_elem is not None:
                #    for traslado_elem in impuestos_elem.findall('cfdi:Traslados/cfdi:Traslado', ns):
                        basei = float(impuestos_concepto_elem.attrib.get('Base'))
                        impuestoi = impuestos_concepto_elem.attrib.get('Impuesto')
                        tipo_factori = impuestos_concepto_elem.attrib.get('TipoFactor')
                        tasa_ocuotai = float(impuestos_concepto_elem.attrib.get('TasaOCuota'))
                        importei = float(impuestos_concepto_elem.attrib.get('Importe'))
                        trasladoi = Traslado(basei,impuestoi,tipo_factori,tasa_ocuotai,importei)
                        #traslados_list.append(traslado)
                        impuestoi = Impuestos("0")
                        impuestoi.traslados = trasladoi #traslados_list
            # else:
            #      impuestos_concepto_elem = concepto_elem.find('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado',ns)


            concepto = Concepto(clave_prod_serv, no_identificacion, cantidad, clave_unidad, unidad, descripcion,
                                valor_unitario, importe, objeto_imp)
            if impuestos_concepto_elem is not None:
                concepto.impuestos = impuestoi

            conceptos_list.append(concepto)

        comprobante.conceptos = conceptos_list

    # Extraer impuestos del concepto
    
    impuestos_elem = root.find('cfdi:Impuestos', ns)
    if impuestos_elem is not None:
        total_impuestos_trasladodos = impuestos_elem.get('TotalImpuestosTrasladados')
        traslados_elem = impuestos_elem.findall('cfdi:Traslados/cfdi:Traslado', ns)
        if traslados_elem:
            for traslado_elem in impuestos_elem.findall('cfdi:Traslados/cfdi:Traslado', ns):
                base = float(traslado_elem.attrib.get('Base'))
                impuesto = traslado_elem.attrib.get('Impuesto')
                tipo_factor = traslado_elem.attrib.get('TipoFactor')
                tasa_ocuota = float(traslado_elem.attrib.get('TasaOCuota'))
                importe = float(traslado_elem.attrib.get('Importe'))
                traslado = Traslado(base,impuesto,tipo_factor,tasa_ocuota,importe)
                #traslados_list.append(traslado)
                impuesto_comprobante = Impuestos(total_impuestos_trasladodos)
                impuesto.traslados = traslado #traslados_list

            comprobante.impuestos = impuesto_comprobante

    complemento_elem = root.find('cfdi:Complemento', ns)
    if complemento_elem is not None:
        timbrefiscal_elem = complemento_elem.find('tfd:TimbreFiscalDigital', ns)

        if timbrefiscal_elem is not None:
            version = timbrefiscal_elem.attrib.get('Version')
            uuid = timbrefiscal_elem.attrib.get('UUID')
            fecha_timbrado = timbrefiscal_elem.attrib.get('FechaTimbrado')
            rfc_prov_certif = timbrefiscal_elem.attrib.get('RfcProvCertif')
            sello_cfd = timbrefiscal_elem.attrib.get('SelloCFD')
            no_certificado_sat = timbrefiscal_elem.attrib.get('NoCertificadoSAT')
            sello_sat = timbrefiscal_elem.attrib.get('SelloSAT')

        complemento = Complemento(version,uuid,fecha_timbrado,rfc_prov_certif, sello_cfd,no_certificado_sat,sello_sat)
        comprobante.complemento = complemento



        

    return comprobante
    

def seleccionar_carpeta():
    """
    Abre un diálogo para seleccionar una carpeta y cuenta los archivos XML en ella.
    """
    root.carpeta_seleccionada = filedialog.askdirectory(title="Seleccionar Carpeta")
    root.cantidad_xml = 0
    if root.carpeta_seleccionada:
        root.cantidad_xml = contar_archivos_xml(root.carpeta_seleccionada)
       # print(f"Cantidad de archivos XML en la carpeta '{root.carpeta_seleccionada}': {cantidad_xml}")
        # Actualiza el texto del ttk.Label con la cantidad de archivos XML
        title_count_files.config(text=f"Cantidad de archivos XML encontrados: {root.cantidad_xml} archivos.")
        title_selected_folder.config(text=f"Carpeta Seleccionada: {root.carpeta_seleccionada}")

    

def contar_archivos_xml(carpeta):
    """
    Cuenta la cantidad de archivos XML en la carpeta especificada.

    :param carpeta: Ruta de la carpeta donde se buscarán los archivos XML.
    :return: Número de archivos XML encontrados.
    """
    try:
        # Lista todos los archivos en la carpeta
        archivos = os.listdir(carpeta)
        
        # Filtra y cuenta solo los archivos con extensión .xml
        archivos_xml = [archivo for archivo in archivos if archivo.endswith('.xml')]
        
        # Retorna la cantidad de archivos XML
        return len(archivos_xml)
    
    except FileNotFoundError:
        print("La carpeta especificada no existe.")
        return 0
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return 0




##########################################
############ MAIN CODE ###################
##########################################
root = tk.Tk()
root.title("Invoices Reader V1.0.4")
root.iconbitmap("common/invoice.ico")
root.resizable(False, False)
style = ttk.Style(root)
root.main_path = os.getcwd()
root.checklist_list = []
root.entry_txt = []
# Import the tcl file
#root.tk.call('source', 'forest-light.tcl')
theme_file = os.path.join(root.main_path,'common', 'themes', 'forest-dark.tcl')
root.tk.call("source", theme_file)
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.grid(sticky="nsew")
frame.pack()
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

root.carpeta_seleccionada = ""
root.cantidad_xml = 0
# Cargar la imagen

# title_info = ttk.Label(frame, text="Nota: Use el boton para seleccionar la carpeta donde estan guardados los archivos xml.", font=("Arial", 12),foreground="#FFFFFF")
# title_info.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# Crear un Label para mostrar el logo
logo_path = 'common/logo002.png'  # Cambia esto a la ruta de tu imagen
logo_photo = tk.PhotoImage(file=logo_path)  # Cargar la imagen

# Crear un Label para mostrar el logo
logo_label = ttk.Label(frame, image=logo_photo)
logo_label.image = logo_photo  # Mantener una referencia de la imagen
logo_label.grid(row=0, column=0, padx=120, pady=5, sticky="nw")  # Coloca el logo en la parte superior izquierda


# title_info = ttk.Label(frame, text="Invoices Reader", font=("Arial", 20),foreground="black")
# title_info.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")


####

# title_info = ttk.Label(frame, text="Invoices Reader", font=("Arial", 12),foreground="#FFFFFF")
# title_info.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

title_info = ttk.Label(frame, text="Seleccione la carpeta donde estan las facturas en formato XML", font=("Arial", 12),foreground="#FFFFFF")
title_info.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

button_select_folder = ttk.Button(frame, text="Click para selecionar carpeta", command=seleccionar_carpeta)
button_select_folder.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

title_selected_folder = ttk.Label(frame, text="No se ha seleccionado carpeta....", font=("Arial", 10),foreground="#FFFFFF")
title_selected_folder.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

title_count_files = ttk.Label(frame, text="Proceso no iniciado....", font=("Arial", 10),foreground="#FFFFFF")
title_count_files.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

button_create_excelFile = ttk.Button(frame, text="Iniciar proceso", style="Accent.TButton", command=create_excelFile)
button_create_excelFile.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

title_progressinfo_files = ttk.Label(frame, text=" ", font=("Arial", 10),foreground="#FFFFFF")
title_progressinfo_files.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

año_actual = datetime.now().year

title_end = ttk.Label(frame, text=f"©{año_actual} PROCOM SYSTEMS", font=("Arial", 9),foreground="#FFFFFF")
title_end.grid(row=7, column=0, padx=150, pady=10, sticky="nsew")

# # Crear un Label para mostrar el año actual
# label_año = tk.Label(root, text=f"©{año_actual} PROCOM SYSTEMS", font=("Arial", 8))
# label_año.pack(pady=20)  # Añadir un poco de espacio vertical


#end
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()