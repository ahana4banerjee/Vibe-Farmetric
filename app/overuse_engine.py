"""
app/overuse_engine.py

Analyzes soil and crop data to detect potential nutrient misuse patterns.
Outputs are AI-assisted sustainability indicators, not definitive scientific diagnoses.
"""
from config import THRESHOLDS, FERTILIZER_GROUPS, RISK_WEIGHTS

class OveruseEngine:
    def __init__(self, data: dict):
        self.data = data
        self.warnings = []
        self.recommendations = []
        self.risk_flags = {}
        self.total_risk_score = 0

    def _add_risk(self, flag_name: str, warning: str, recommendation: str):
        """Helper method to register a risk flag, apply its weight, and log messages."""
        self.risk_flags[flag_name] = True
        self.total_risk_score += RISK_WEIGHTS.get(flag_name, 0)
        self.warnings.append(warning)
        if recommendation not in self.recommendations:
            self.recommendations.append(recommendation)

    def _check_nitrogen_excess(self):
        n_level = self.data.get('Nitrogen_Level', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        yield_val = self.data.get('Yield_Last_Season', 0)

        if n_level > THRESHOLDS['N_HIGH']:
            if last_fert in FERTILIZER_GROUPS['NITROGEN_HEAVY'] and yield_val < THRESHOLDS['YIELD_POOR']:
                self._add_risk('NITROGEN_EXCESS', 
                               "High confidence: Potential nitrogen over-application pattern detected. Yield response is low.", 
                               "Reduce nitrogen-intensive fertilizers and consider split applications.")
            else:
                self._add_risk('NITROGEN_EXCESS', 
                               "Moderate confidence: Elevated residual nitrogen detected.", 
                               "Optimize nitrogen dosage based on precise soil testing.")

    def _check_phosphorus_excess(self):
        p_level = self.data.get('Phosphorus_Level', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        yield_val = self.data.get('Yield_Last_Season', 0)

        if p_level > THRESHOLDS['P_HIGH']:
            if last_fert in FERTILIZER_GROUPS['PHOSPHORUS_HEAVY'] and yield_val < THRESHOLDS['YIELD_POOR']:
                self._add_risk('PHOSPHORUS_EXCESS', 
                               "High confidence: Potential phosphorus accumulation. Phosphorus may be fixing in the soil rather than reaching crops.", 
                               "Use biofertilizers (e.g., PSB) to solubilize existing soil phosphorus instead of adding more.")
            else:
                self._add_risk('PHOSPHORUS_EXCESS', 
                               "Moderate confidence: Elevated soil phosphorus observed.", 
                               "Reduce basal phosphorus application in the next cycle.")

    def _check_potassium_excess(self):
        k_level = self.data.get('Potassium_Level', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        yield_val = self.data.get('Yield_Last_Season', 0)

        if k_level > THRESHOLDS['K_HIGH']:
            if last_fert in FERTILIZER_GROUPS['POTASSIUM_HEAVY'] and yield_val < THRESHOLDS['YIELD_POOR']:
                self._add_risk('POTASSIUM_EXCESS', 
                               "High confidence: Potential potassium over-application pattern. Poor conversion to yield.", 
                               "Re-evaluate potassium needs and ensure balanced NPK ratios.")
            else:
                self._add_risk('POTASSIUM_EXCESS', 
                               "Moderate confidence: High residual potassium detected.", 
                               "Limit MOP or complex fertilizer applications temporarily.")

    def _check_nutrient_imbalance(self):
        n = self.data.get('Nitrogen_Level', 0)
        p = max(self.data.get('Phosphorus_Level', 0), 1) # Prevent division by zero
        k = max(self.data.get('Potassium_Level', 0), 1)

        # Heuristic: If Nitrogen is massively higher than P and K combined
        ratio = n / (p + k)
        if ratio > THRESHOLDS['N_PK_RATIO_MAX']:
            self._add_risk('NUTRIENT_IMBALANCE', 
                           "Potential nutrient imbalance detected. Excess nitrogen relative to phosphorus and potassium may reduce overall fertilizer efficiency.", 
                           "Adopt a balanced fertilization strategy. Focus on micronutrient balancing and crop rotation.")

    def _check_salinity_risk(self):
        ec = self.data.get('Electrical_Conductivity', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        n = self.data.get('Nitrogen_Level', 0)
        p = self.data.get('Phosphorus_Level', 0)
        k = self.data.get('Potassium_Level', 0)
        
        # Check total nutrient stress rather than just Nitrogen
        has_nutrient_stress = (n > THRESHOLDS['N_HIGH']) or (p > THRESHOLDS['P_HIGH']) or (k > THRESHOLDS['K_HIGH'])
        
        if ec > THRESHOLDS['EC_HIGH']:
            if last_fert in FERTILIZER_GROUPS['CHEMICAL'] and has_nutrient_stress:
                self._add_risk('SALINITY_RISK', 
                               "High confidence: Elevated soil salinity risk observed, likely exacerbated by cumulative chemical fertilizer stress.", 
                               "Flush soil with high-quality irrigation water. Limit heavy salt-index chemical fertilizers.")
            else:
                self._add_risk('SALINITY_RISK', 
                               "Moderate confidence: Elevated electrical conductivity (EC) detected.", 
                               "Monitor soil salinity trends and ensure proper field drainage.")

    def _check_soil_health(self):
        oc = self.data.get('Organic_Carbon', 1.0)
        if oc < THRESHOLDS['OC_LOW']:
            self._add_risk('LOW_ORGANIC_CARBON', 
                           "Possible soil structural weakness. Low organic carbon reduces nutrient retention.", 
                           "Introduce organic amendments (farmyard manure, vermicompost) to improve soil health.")

    def _calculate_risk_level(self) -> str:
        """Maps the numeric risk score to a categorical level."""
        score = self.total_risk_score
        if score <= 20: return "Low"
        if score <= 40: return "Moderate"
        if score <= 60: return "High"
        return "Critical"

    def analyze(self) -> dict:
        """Runs all heuristic modules and returns aggregated insights."""
        self._check_nitrogen_excess()
        self._check_phosphorus_excess()
        self._check_potassium_excess()
        self._check_nutrient_imbalance()
        self._check_salinity_risk()
        self._check_soil_health()

        return {
            "risk_score": self.total_risk_score,
            "risk_level": self._calculate_risk_level(),
            "risk_flags": self.risk_flags,
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }