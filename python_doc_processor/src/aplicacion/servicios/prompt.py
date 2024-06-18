# Más información acá: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design
promptBL = """"
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_bl
mas abajo del documento adjunto. Responde siempre en formato JSON. si la informacion no existe responde con NULL.
datos_bl:
        PUERTO EMBARQUE
        PUERTO DESEMBARQUE
        TIPO DE CARGA
        CIA TRANSPORTADORA
        DCTO TRANSPORTE
        FECHA en formato mm-dd-YYYY
        EMISOR DCTO TRANSPORTE
        TIPO BULTO
        CANTIDAD
        PESO BRUTO
        FLETE
        IDENTIFICACION BULTOS
        OBSERVACIONES BANCO CENTRAL SNA. 
"""

promptCarta = """
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_carta mas abajo del documento adjunto. Responde siempre en formato JSON.
Si la información no existe responde con NULL.
datos_carta:
        Referencia Orden de Compra
        Referencia Carpeta
"""

promptCertificadoOrigen = """
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_certificado_origen mas abajo del documento adjunto. Responde siempre en formato JSON.
Si la información no existe responde con NULL.
datos_certificado_origen:
        Numero de Certificado
        Regimen Importacion
        
"""
# PENDIENTE FALTA ENCONTRAR UNA FACTURA
promptFactura = """
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_factura mas abajo del documento adjunto. Responde siempre en formato JSON.
Si la información no existe responde con NULL.
datos_factura:
        Numero de Certificado
        Regimen Importacion
"""

promptOrdenCompra = """
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_orden_compra mas abajo del documento adjunto. Responde siempre en formato JSON.
Si la información no existe responde con NULL.
datos_orden_compra:
        Numero de Orden
"""

promptPolizaSeguro = """
Eres un agente de aduana, tu responsabilidad es identificar y extraer los datos_poliza_seguro mas abajo del documento adjunto. Responde siempre en formato JSON.
Si la información no existe responde con NULL.
datos_poliza_seguro:
        Numero de Certificado
        Numero de Poliza
        Prima Total
"""
