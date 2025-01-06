def lista_formas_de_pago():
    data =  {
    "01": "Efectivo: Pago realizado en efectivo.",
    "02": "Cheque nominativo: Pago mediante cheque nominativo.",
    "03": "Transferencia electrónica de fondos: Pago realizado a través de una transferencia bancaria electrónica.",
    "04": "Tarjeta de crédito: Pago mediante tarjeta de crédito.",
    "05": "Monedero electrónico: Pago a través de monederos electrónicos (como vales de despensa autorizados).",
    "06": "Dinero electrónico: Pago a través de dinero electrónico (ej. criptomonedas).",
    "08": "Vales de despensa: Pago con vales de despensa.",
    "12": "Dación en pago: Liquidación de una deuda mediante la entrega de un bien distinto al dinero.",
    "13": "Pago por subrogación: Pago realizado por otra persona en nombre del deudor.",
    "14": "Pago por consignación: Pago depositado en un lugar o con una persona designada.",
    "15": "Condonación: Perdón de la deuda.",
    "17": "Compensación: Pago mediante la compensación de obligaciones mutuas.",
    "23": "Novación: Sustitución de la deuda original por una nueva.",
    "24": "Confusión: Extinción de la deuda cuando el acreedor y deudor se convierten en la misma persona.",
    "25": "Remisión de deuda: Extinción de la deuda sin intercambio de bienes o dinero.",
    "26": "Prescripción o caducidad: Cuando la deuda prescribe por el paso del tiempo.",
    "27": "A satisfacción del acreedor: Pago que se realiza de una forma que satisface al acreedor.",
    "28": "Tarjeta de débito: Pago realizado con tarjeta de débito.",
    "29": "Tarjeta de servicios: Pago mediante tarjeta de servicios (ej. tarjetas de beneficios corporativos).",
    "30": "Aplicación de anticipos: Liquidación mediante la aplicación de anticipos previamente dados.",
    "31": "Intermediario de pagos: Pago realizado a través de intermediarios autorizados.",
    "99": "Por definir: Usado cuando aún no se ha definido la forma de pago, especialmente en operaciones a crédito."
    }
    return data

def lista_cfdi_gastos():
    data = ['G03','D01','D02','D03', 'D04', 'D08', 'D10']
    return data

def lista_cfdi_compras():
    data = ['G01']
    return data

def lista_metodos_de_pago():
    data = {
        "PUE":"Pago en una sola exhibición",
        "PPD":"Pago en parcialidades o diferido"
    }
    return data