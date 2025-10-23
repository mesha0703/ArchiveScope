# my_app/config.py
from core.sinumerik_components import ParameterContainer, Parameter, ParamBitconfig, AdaptationPlotParams

APP_NAME = "ArchiveScope"
APP_VERSION = "1.0.0"
ACTIVATE_LOGGING_IN_FILE = True

MAX_PARALLEL_ARCHIVES = 2  # Maximum number of archives that can be added

# ===== UI Configuration =====
LANGUAGE = 'ger'  # Default language for the UI (currently only works for Controller Info)
DEFAULT_TEXT_COLOR = [0, 0, 0]  # Default text color
VALUE_CHANGED_TEXT_COLOR = [125, 125, 0] # Color for text when value is changed
COMPARE_MODE_SAME_COLOR = [0, 255, 0]  # Color for same values in compare mode
COMPARE_MODE_DIFF_COLOR = [255, 0, 0]  # Color for different values in compare mode
DECIMAL_DIGITS = 4  # Number of decimal digits for float values

# ===== Filter Parameteres =====
"""
These settings can be extracted from the Sinumerik documentation:
https://support.industry.siemens.com/cs/mdm/109783558?c=112054908043&dl=sk&lc=en-PY
"""
PARAM_NUM_ACTIVATED_FILTERS_1_4 = 'p1656[0]' # Number of activated filters (1-4)
PARAM_NUM_ACTIVATED_FILTERS_5_10 = 'p5200[0]' # Number of activated filters (5-10)
MAX_ACTIVE_CURRENT_SETPOINT_FILTERS = 10 # Maximum number of active filters
MAX_ACTIVE_SPEED_SETPOINT_FILTERS = 2 # Maximum number of active speed setpoint filters
MAX_ACTIVE_ACTUAL_SPEED_FILTERS = 1 # Maximum number of active actual speed filters

# Denominator and numerator for frequency have same min and max values
FREQ_DEFAULT = 2000.0 # Default denominator/numerator frequency (Nennerfrequenz) in Hz
MIN_FREQ = 0.5 # Minimum denominator frequency (Nennerfrequenz) in Hz
MAX_FREQ = 16000.0 # Maximum denominator frequency (Nennerfrequenz) in Hz

DAMPING_DEFAULT = 0.7 # Default denominator damping (Nenner-Dämpfung)
MIN_DAMPING = 0.001 # Minimum denominator damping (Nenner-Dämpfung)
MAX_DAMPING = 10.000 # Maximum denominator damping (Nenner-Dämpfung)

TIME_CONSTANT_DEFAULT = 0.0 # Default time constant (Zeitkonstante) in ms
MIN_TIME_CONSTANT = 0.0 # Minimum time constant (Zeitkonstante) in ms
MAX_TIME_CONSTANT = 5000.0 # Maximum time constant (Zeitkonstante) in ms

MIN_BLOCK_FREQ = MIN_FREQ
MAX_BLOCK_FREQ = MAX_FREQ

MIN_BAND_FREQ = 0.0001 # Minimum band frequency (Bandfrequenz) in Hz
MAX_BAND_FREQ = 1000.000 # Maximum band frequency (Bandfrequenz) in Hz
DEFAULT_BAND_FREQ = 100.0 # Default band frequency (Bandfrequenz) in Hz

MIN_NOTCH_DEPTH = -230.0 # Minimum notch depth (Absenkung) in dB
MAX_NOTCH_DEPTH = 25.0 # Maximum notch depth (Absenkung) in dB
DEFAULT_NOTCH_DEPTH = -20.0 # Default notch depth (Absenkung) in dB

MIN_ATTENUATION = -180.0 # Minimum attenuation in dB
MAX_ATTENUATION = 180.0 # Maximum attenuation in dB
DEFAULT_ATTENUATION = 0.0 # Default attenuation in dB

# ===== GUI Configuration =====
STANDARD_FILTER_COLORS = [[1, 153, 153], [0, 255, 0], [255, 0, 0], [255, 255, 0],
                          [255, 0, 255], [0, 255, 255], [128, 0, 128], [128, 128, 0],
                          [0, 128, 128], [192, 192, 192], [255, 165, 0]] # Standard colors for filters

# ===== Drive Parameters =====

drive_name_param = 'p199'

# ===== Current Setpoint Filter (ger. Stromsollwert-Filter) Parameters =====
current_setpoint_filter1 = {
    'type_param': 'p1657[0]', # Type of filter (1=low-pass PT2, 2=2nd order filter)
    'fn_param': 'p1658[0]',   # denominator frequency (Nennerfrequenz)
    'dn_param': 'p1659[0]',   # denominator damping (Nenner-Dämpfung)
    'fz_param': 'p1660[0]',   # numerator frequency (Zählerfrequenz)
    'dz_param': 'p1661[0]'    # numerator damping (Zähler-Dämpfung)
}

current_setpoint_filter2 = {
    'type_param': 'p1662[0]',
    'fn_param': 'p1663[0]',
    'dn_param': 'p1664[0]',
    'fz_param': 'p1665[0]',
    'dz_param': 'p1666[0]'
}

current_setpoint_filter3 = {
    'type_param': 'p1667[0]',
    'fn_param': 'p1668[0]',
    'dn_param': 'p1669[0]',
    'fz_param': 'p1670[0]',
    'dz_param': 'p1671[0]'
}

current_setpoint_filter4 = {
    'type_param': 'p1672[0]',
    'fn_param': 'p1673[0]',
    'dn_param': 'p1674[0]',
    'fz_param': 'p1675[0]',
    'dz_param': 'p1676[0]'
}

current_setpoint_filter5 = {
    'type_param': 'p5201[0]',
    'fn_param': 'p5202[0]',
    'dn_param': 'p5203[0]',
    'fz_param': 'p5204[0]',
    'dz_param': 'p5205[0]'
}

current_setpoint_filter6 = {
    'type_param': 'p5206[0]',
    'fn_param': 'p5207[0]',
    'dn_param': 'p5208[0]',
    'fz_param': 'p5209[0]',
    'dz_param': 'p5210[0]'
}

current_setpoint_filter7 = {
    'type_param': 'p5211[0]',
    'fn_param': 'p5212[0]',
    'dn_param': 'p5213[0]',
    'fz_param': 'p5214[0]',
    'dz_param': 'p5215[0]'
}

current_setpoint_filter8 = {
    'type_param': 'p5216[0]',
    'fn_param': 'p5217[0]',
    'dn_param': 'p5218[0]',
    'fz_param': 'p5219[0]',
    'dz_param': 'p5220[0]'
}

current_setpoint_filter9 = {
    'type_param': 'p5221[0]',
    'fn_param': 'p5222[0]',
    'dn_param': 'p5223[0]',
    'fz_param': 'p5224[0]',
    'dz_param': 'p5225[0]'
}

current_setpoint_filter10 = {
    'type_param': 'p5226[0]',
    'fn_param': 'p5227[0]',
    'dn_param': 'p5228[0]',
    'fz_param': 'p5229[0]',
    'dz_param': 'p5230[0]'
}


current_setpoint_filter_list = [
    current_setpoint_filter1, current_setpoint_filter2, current_setpoint_filter3, current_setpoint_filter4,
    current_setpoint_filter5, current_setpoint_filter6, current_setpoint_filter7, current_setpoint_filter8,
    current_setpoint_filter9, current_setpoint_filter10
]

# ===== Speed Setpoint Filter (ger. Drehzahlollwert-Filter) Parameters =====

speed_setpoint_filter1 = {
    'type_param': 'p1415[0]', # Type of filter (0=low-pass PT1, 1=low-pass PT2, 2=general 2nd order filter)
    'time_constant_param': 'p1416[0]', # Time constant (Zeitkonstante). Filter is active when time constant is > 0
    'fn_param': 'p1417[0]',   # denominator frequency (Nennerfrequenz)
    'dn_param': 'p1418[0]',   # denominator damping (Nenner-Dämpfung)
    'fz_param': 'p1419[0]',   # numerator frequency (Zählerfrequenz)
    'dz_param': 'p1420[0]'    # numerator damping (Zähler-Dämpfung)
}

speed_setpoint_filter2 = {
    'type_param': 'p1421[0]',
    'time_constant_param': 'p1422[0]',
    'fn_param': 'p1423[0]',
    'dn_param': 'p1424[0]',
    'fz_param': 'p1425[0]',
    'dz_param': 'p1426[0]'
}

speed_setpoint_filter_list = [
    speed_setpoint_filter1, speed_setpoint_filter2
]

# ===== Actual speed filter (ger. Drehzahlistwert-Filter) Parameters =====

actual_speed_filter = {
    'activate_param': 'p1413[0]', # Activate filter (Filter aktivieren)
    'type_param': 'p1446[0]', # Type of filter (1=low-pass PT2, 2=general 2nd order filter)
    'fn_param': 'p1447[0]',   # denominator frequency (Nennerfrequenz)
    'dn_param': 'p1448[0]',   # denominator damping (Nenner-Dämpfung)
    'fz_param': 'p1449[0]',   # numerator frequency (Zählerfrequenz)
    'dz_param': 'p1450[0]'    # numerator damping (Zähler-Dämpfung)
}

# ===== Controller Parameters =====

# Current Controller (ger. Stromregler) Parameters
# *n* means all parameters with the same prefix (p115[0], p115[1], ..., p115[n])
# Order for normal parameters: param tag, {language: meaning}, min, max, factory setting, step, decimal digits,, data type, default language
# Order for bitconfig parameters: param tag, {language: meaning for spec. bit}, factory setting, bit meanings dict, bit save amount, default language

# DRIVE CONTROLLERS

current_controller_param_list = [
    Parameter('p115[0]', {'ger': "Abtastzeit Stromregelkreis [us]"}, 0.0, 16000.0, 250.0, 125.0, 0, "float32", default_lang=LANGUAGE),
    Parameter('p115[1]', {'ger': "Abtastzeit Drehzahlregelkreis [µs]"}, 0.0, 16000.0, 1000.0, 125.0, 0, "float32", default_lang=LANGUAGE),
    Parameter('p391[*n*]', {'ger': "Stromregler Adaption Einst. unten [A]"}, 0.0, 6000.0, 1.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p392[*n*]', {'ger': "Stromregler Adaption Einst. oben [A]"}, 0.0, 6000.0, 0.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p393[*n*]', {'ger': "Stromregler P Skalierung [%]"}, 0.0, 1000.0, 100.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1715[*n*]', {'ger': "Stromregler P Verstärkung"}, 0.0, 100000.0, 1.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1717[*n*]', {'ger': "Stromregler Nachstellzeit [ms]"}, 0.0, 1000.0, 2.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
]

current_controller = ParameterContainer(
    {'ger': "Stromregler"},
    current_controller_param_list,
    default_lang=LANGUAGE
)

speed_controller_param_list = [
    AdaptationPlotParams({'ger': "Proportionalverstärkung"}, {'ger': "Nachstellzeit [ms]"}, 'p1460[0]', 'p1461[0]', 'p1462[0]', 'p1463[0]', 'p1464[0]', 'p1465[0]', default_lang=LANGUAGE),
    Parameter('p1460[0]', {'ger': "Drehzahlregler P Verstärkung (A-Seite) [%]"}, -100.0, 1000.0, 0.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1462[0]', {'ger': "Drehzahlregler P Verstärkung (B-Seite) [%]"}, -100.0, 1000.0, 0.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1433[0]', {'ger': "Referenzmodell Eigenfrequenz [Hz]"}, 0.0, 8000.0, 0.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1434[0]', {'ger': "Referenzmodell Dämpfung [dB]"}, 0.0, 5.0, 1.0, 0.1, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1435[0]', {'ger': "Referenzmodell Totzeit [ms]"}, 0.0, 3.0, 0.0, 0.1, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    ParamBitconfig('p1400[0]', {'ger': "Drehzahlregler Konfiguration"}, 0x8021, {'ger': [
                              "Automatische Kp/Tn-Adaption aktiv", # Bit 0
                              "Sensorlose Vektorregelung – I-Komponente einfrieren", # Bit 1
                              "Quelle des Beschleunigungsvorsteuerungssignals [0=extern (p1495), 1=intern(n_set)]", # Bit 2
                              "Referenzmodell – I-Komponente des Drehzahlsollwerts EIN", # Bit 3
                              "", # Bit 4
                              "Kp/Tn-Adaption aktiv", # Bit 5
                              "Freie Tn-Adaption aktiv", # Bit 6
                              "Interpolierte Drehzahlsollwert-Vorsteuerung", # Bit 7
                              "", # Bit 8
                              "", # Bit 9
                              "Drehzahlsollwert-Vorsteuerung aktiv", # Bit 10
                              "", "", "", # Bit 11, 12, 13
                              "Drehmomentvorsteuerung [1=immer aktiv, 0=nur bei n_ctrl Freigabe]", # Bit 14
                              "Sensorlose Vektorregelung – Drehzahlsollwert-Vorsteuerung", # Bit 15
                              "I-Komponente für Begrenzung aktiv", # Bit 16
                              "", # Bit 17
                              "Trägheitsmoment-Schätzer aktiv", # Bit 18
                              "Anti-Windup für Integralanteil aktiv", # Bit 19
                              "Beschleunigungsmodell EIN", # Bit 20
                              "", # Bit 21
                              "Trägheitsmoment-Schätzwert bei Pulsunterdrückung übernehmen", # Bit 22
                              "Beschleunigungsmodell (mit Drehzahlgeber) EIN", # Bit 23
                              "Trägheitsmoment-Schätzer – Schnellabschätzung aktiv", # Bit 24
                              "Momentane Beschleunigungsdrehmoment-Berechnung im I/f-Modus", # Bit 25
                              "", # Bit 26
                              "Getriebelastung – Drehmomentbegrenzung berücksichtigen", # Bit 27
                              "", "", "", "", "" # Bit 28, 29, 30, 31
                              ]}, default_lang=LANGUAGE),
    Parameter('p1464[0]', {'ger': "Drehzahl Adaptionsdrehzahl unten [m/min]"}, 0.0, 1000.0, 0.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1465[0]', {'ger': "Drehzahl Adaptionsdrehzahl oben [rpm]"}, 0.0, 210000.0, 210000.0, 10000.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1461[0]', {'ger': "Drehzahl Skalierung Kp oben [%]"}, 0.0, 200000.0, 100.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
    Parameter('p1463[0]', {'ger': "Drehzahl Skalierung Tn Adaption obere Skalierung [%]"}, 0.0, 200000.0, 100.0, 1.0, DECIMAL_DIGITS, "float32", default_lang=LANGUAGE),
]

speed_controller = ParameterContainer(
    {'ger': "Drehzahlregler"},
    speed_controller_param_list,
    default_lang=LANGUAGE
)

drive_controllers_list = [
    current_controller,
    speed_controller
]

# ===== Kinematic Tree =====

md_parameters = [
            ["N18880", "$MN_MM_MAXNUM_KIN_CHAIN_ELEM", False, "int", 0],
            ["N18882", "$MN_MM_MAX_NUM_KIN_SWITCHES", False, "int", 0],
            ["N16800", "$MN_ROOT_KIN_ELEM_NAME", False, "str", ""],
        ]

# Define KIN parameters
kin_parameters = [
    "$NK_NAME",
    "$NK_NEXT",
    "$NK_PARALLEL",
    "$NK_TYPE",
    "$NK_OFF_DIR",
    "$NK_AXIS",
    "$NK_A_OFF",
    "$NK_SWITCH_INDEX",
    "$NK_SWITCH_POS",
    "$NK_SWITCH"
]