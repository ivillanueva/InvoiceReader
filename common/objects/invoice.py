class Comprobante:
    def __init__(self, version, serie, folio, fecha, forma_pago, subtotal, moneda, total, sello,
                 tipo_de_comprobante, exportacion, metodo_pago, lugar_expedicion, certificado, no_certificado):
        self.version = version
        self.serie = serie
        self.folio = folio
        self.fecha = fecha
        self.forma_pago = forma_pago
        self.subtotal = subtotal
        self.moneda = moneda
        self.total = total
        self.sello = sello
        self.tipo_de_comprobante = tipo_de_comprobante
        self.exportacion = exportacion
        self.metodo_pago = metodo_pago
        self.lugar_expedicion = lugar_expedicion
        self.certificado = certificado
        self.no_certificado = no_certificado
        self.emisor = None
        self.receptor = None
        self.conceptos = []
        self.impuestos = None
        self.complemento = None


class Emisor:
    def __init__(self, rfc, nombre, regimen_fiscal):
        self.rfc = rfc
        self.nombre = nombre
        self.regimen_fiscal = regimen_fiscal


class Receptor:
    def __init__(self, rfc, nombre, domicilio_fiscal_receptor, regimen_fiscal_receptor, uso_cfdi):
        self.rfc = rfc
        self.nombre = nombre
        self.domicilio_fiscal_receptor = domicilio_fiscal_receptor
        self.regimen_fiscal_receptor = regimen_fiscal_receptor
        self.uso_cfdi = uso_cfdi


class Concepto:
    def __init__(self, clave_prod_serv, no_identificacion, cantidad, clave_unidad, unidad, descripcion, 
                 valor_unitario, importe, objeto_imp):
        self.clave_prod_serv = clave_prod_serv
        self.no_identificacion = no_identificacion
        self.cantidad = cantidad
        self.clave_unidad = clave_unidad
        self.unidad = unidad
        self.descripcion = descripcion
        self.valor_unitario = valor_unitario
        self.importe = importe
        self.objeto_imp = objeto_imp
        self.impuestos = None
        self.partes = []


class Impuestos:
    def __init__(self, total_impuestos_trasladados):
        self.total_impuestos_trasladados = total_impuestos_trasladados
        self.traslados = None #[]


class Traslado:
    def __init__(self, base, impuesto, tipo_factor, tasa_ocuota, importe):
        self.base = base
        self.impuesto = impuesto
        self.tipo_factor = tipo_factor
        self.tasa_ocuota = tasa_ocuota
        self.importe = importe


class Complemento:
    def __init__(self, version, uuid, fecha_timbrado, rfc_prov_certif, sello_cfd, no_certificado_sat, sello_sat):
        self.version = version
        self.uuid = uuid
        self.fecha_timbrado = fecha_timbrado
        self.rfc_prov_certif = rfc_prov_certif
        self.sello_cfd = sello_cfd
        self.no_certificado_sat = no_certificado_sat
        self.sello_sat = sello_sat