'''
Este manejará:
-Validación del RUT.
-Extracción de d1 a d8.
-Generación aleatoria.
-Chequeos.
Validación y generación de RUT
'''

from core.rut_aleatorio import generar_varios_ruts

def limpiar_ruts(texto):
    """
    Limpia el texto y devuelve una tupla con:
    - Lista de RUTs bien formateados (8 dígitos + DV)
    - Lista de RUTs descartados por ser muy cortos
    """
    ruts = texto.replace(",", "\n").splitlines()
    ruts_limpios = []
    ruts_cortos = []

    for rut in ruts:
        rut_original = rut.strip()
        rut = rut_original.replace(".", "").replace("-", "").upper()
        if not rut:
            continue
        if len(rut) < 2:
            continue

        cuerpo = rut[:-1]
        dv = rut[-1]

        # Verificar si el RUT es muy corto (menos de 7 dígitos en el cuerpo)
        if len(cuerpo) < 7:
            ruts_cortos.append(rut_original)
            continue
        
        # Asegurar cuerpo de 8 dígitos
        if len(cuerpo) == 7:
            cuerpo = "0" + cuerpo
        elif len(cuerpo) != 8:
            continue  # descartar RUT mal formado

        ruts_limpios.append(f"{cuerpo}-{dv}")
    
    return ruts_limpios, ruts_cortos
def es_rut_valido(rut):
    """
    Valida sintácticamente un RUT chileno (formato y dígito verificador).
    """
    rut = rut.upper().replace("-", "").replace(".", "")
    if len(rut) < 9 or not rut[:-1].isdigit():
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2
    for d in reversed(cuerpo):
        suma += int(d) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1

    resto = 11 - (suma % 11)
    dv_calc = 'K' if resto == 10 else '0' if resto == 11 else str(resto)
    return dv == dv_calc

def generar_ruts_validos(n=3):
    return generar_varios_ruts(n)
