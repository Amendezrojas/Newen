# -*- coding: utf-8 -*-
import numpy as np
import math as m
import requests

# --- Constantes y Tarifas de Cotización ---
PRECIO_LITRO_BENCINA = 1000
CONSUMO_BARREDORA_LT_HR = 8
COSTO_TRASLADO_KM = 2300
TARIFA_RESIDUOS_NO_PELIGROSOS_KG = 120
COSTO_TRASLADO_GRAN_CONCEPCION_NO_PEL = 50000
ARRIENDO_TOLVA_PELIGROSOS = 100000
TRANSPORTE_PELIGROSOS_FIJO = 250000
COORD_COPIULEMU_LAT = -36.9038
COORD_COPIULEMU_LON = -72.8239
COORD_HIDRONOR_LAT = -36.6806
COORD_HIDRONOR_LON = -73.0805

# --- Vehículos disponibles ---
EQUIPOS = {
    "barredoras": [
        "GPSR-67 - Tennant Sentinel 2014",
        "KFLB-43 - Tennant Sentinel 2012",
        "BLHF-31 - Tennant 6650 X 2008",
        "S/PTE - Dulevo 2008"
    ],
    "camiones": [
        "FKHB-88 - Freightliner M2 106 2013",
        "HLHC-28 - JMC Carrying Pucs EIV 2016",
        "KBXJ-67 - JAC Runner 1135 2018"
    ],
    "camionetas": [
        "JBTY-72 - Mahindra New Pick up XL D Cab 2.2 2016",
        "LRYR-40 - KYC Gran Mamut Cabina Simple 1.5 2020",
        "BVJR-94 - KIA Frontier Plus DCAB. 2.5 2009",
        "RPGC67 - Chevrolet Silverado DCAB. 4X4 5.3 AT 2022",
        "FPTL-14 - Mitsubishi L200 Work D CAB.2.5 2013",
        "JBTH-36 - Changan MS 201 DCAM 1.2 2016",
        "RWTJ-12 - Chevrolet Silverado DCAB 4X4 5.3 AT 2022",
        "VDBZ53 - Maxus T60 4X4 AUT 2025"
    ],
    "retroexcavadoras": [
        "DVTP89 - Hidromex HMK 102B 2012"
    ],
    "excavadoras": [
        "LTJB11 - JCB JS 205 LC 2019"
    ],
    "motoniveladoras": [
        "PB6688 - Champion 730 A 1996"
    ],
    "furgones": [
        "JCZC-57 - Peugeot 2016",
        "JKBK19 - Peugeot Partner 2017"
    ]
}

# --- Funciones auxiliares ---
def dms_to_decimal(dms_str):
    dms_str = dms_str.replace('°', ' ').replace('′', ' ').replace('″', ' ').strip()
    parts = dms_str.split()
    if len(parts) < 3:
        raise ValueError("Formato incorrecto. Se esperan grados, minutos y segundos.")
    degrees, minutes, seconds = float(parts[0]), float(parts[1]), float(parts[2])
    decimal_value = degrees + (minutes / 60) + (seconds / 3600)
    if 'sur' in dms_str.lower() or 'oeste' in dms_str.lower():
        decimal_value *= -1
    return decimal_value

def get_coordinates_from_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "MiAppCotizacion/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def get_route_distance(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
    params = {"overview": "false", "steps": "false", "alternatives": "false"}
    headers = {"User-Agent": "MiAppCotizacion/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data and data['code'] == 'Ok' and data['routes']:
            return data['routes'][0]['distance'] / 1000
    except:
        pass
    return None

# Aquí deben integrarse las funciones: cotizar_barredora(), cotizar_residuos_no_peligrosos(),
# cotizar_residuos_peligrosos(), y un menú principal. Cada función debe incluir:
# - Captura de datos del cliente
# - Selección de equipo si aplica
# - Cálculo de costos (combustible, transporte, disposición, tolvas)
# - Coordinadas y distancia si aplica
# - Observaciones estándar
# - Impresión de cotización completa

