# app/config.py

"""
Configuration file for Vibe-FrameTric Agronomy Engine.
These thresholds are heuristic approximations for the AI prototype 
and should be tuned based on regional soil testing standards.
"""

THRESHOLDS = {
    'N_HIGH': 120,         # mg/kg or ppm
    'P_HIGH': 60,          # mg/kg or ppm
    'K_HIGH': 80,          # mg/kg or ppm
    'EC_HIGH': 1.5,        # ds/m (Electrical Conductivity indicating potential salinity)
    'OC_LOW': 0.5,         # % (Organic Carbon)
    'YIELD_POOR': 15       # Baseline yield threshold indicating poor fertilizer efficiency
}

# Fertilizers typically heavy in specific chemicals
CHEMICAL_FERTILIZERS = ['Urea', 'DAP', 'MOP', '14-35-14', '28-28', '10-26-26']
NITROGEN_HEAVY = ['Urea', 'DAP', '28-28']
PHOSPHORUS_HEAVY = ['DAP', 'SSP', '14-35-14', '10-26-26']

PENALTIES = {
    'NITROGEN_EXCESS': 15,
    'PHOSPHORUS_EXCESS': 12,
    'POTASSIUM_EXCESS': 10,
    'SALINITY_RISK': 18,
    'LOW_ORGANIC_CARBON': 15,
    'NUTRIENT_IMBALANCE': 10,
    'REPEATED_DEPENDENCY': 10,
    'LOW_EFFICIENCY': 10
}