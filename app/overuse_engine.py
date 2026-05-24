# app/overuse_engine.py
from config import THRESHOLDS, CHEMICAL_FERTILIZERS, NITROGEN_HEAVY

class OveruseEngine:
    """
    Analyzes soil and crop data to detect potential nutrient misuse patterns.
    Outputs are AI-assisted sustainability indicators, not definitive scientific diagnoses.
    """
    
    def __init__(self, data: dict):
        self.data = data
        self.warnings = []
        self.recommendations = []
        self.risk_flags = {}

    def _check_nitrogen_excess(self):
        """
        Rule: High N + repeated N-heavy fertilizer + poor yield indicates high overuse risk.
        """
        n_level = self.data.get('Nitrogen_Level', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        yield_val = self.data.get('Yield_Last_Season', 0)

        is_high_n = n_level > THRESHOLDS['N_HIGH']
        is_n_dependent = last_fert in NITROGEN_HEAVY
        is_poor_yield = yield_val < THRESHOLDS['YIELD_POOR']

        if is_high_n and is_n_dependent and is_poor_yield:
            self.risk_flags['NITROGEN_EXCESS'] = True
            self.warnings.append("High confidence: Potential nitrogen over-application pattern detected. Yield is not scaling with inputs.")
            self.recommendations.append("Reduce nitrogen-intensive fertilizers (e.g., Urea). Consider leguminous crop rotation.")
        elif is_high_n:
            self.risk_flags['NITROGEN_EXCESS'] = True
            self.warnings.append("Moderate confidence: Elevated residual nitrogen detected.")
            self.recommendations.append("Optimize nitrogen dosage based on precise soil testing.")

    def _check_salinity_risk(self):
        """
        Rule: High EC + high nutrients + chemical dependency strongly suggests salinity risk.
        """
        ec = self.data.get('Electrical_Conductivity', 0)
        last_fert = self.data.get('Fertilizer_Used_Last_Season', '')
        n_level = self.data.get('Nitrogen_Level', 0)
        
        is_high_ec = ec > THRESHOLDS['EC_HIGH']
        is_chem_dependent = last_fert in CHEMICAL_FERTILIZERS
        has_excess_nutrients = n_level > THRESHOLDS['N_HIGH']

        if is_high_ec and is_chem_dependent and has_excess_nutrients:
            self.risk_flags['SALINITY_RISK'] = True
            self.warnings.append("High confidence: Possible soil salinity risk observed due to chemical fertilizer accumulation.")
            self.recommendations.append("Flush soil with high-quality irrigation water and apply gypsum if sodic. Reduce chemical salt inputs.")
        elif is_high_ec:
            self.risk_flags['SALINITY_RISK'] = True
            self.warnings.append("Moderate confidence: Elevated electrical conductivity (EC) detected.")
            self.recommendations.append("Monitor soil salinity and ensure proper drainage.")

    def _check_soil_health(self):
        """
        Rule: Low organic carbon indicates poor soil structure, reducing fertilizer efficiency.
        """
        oc = self.data.get('Organic_Carbon', 1.0)
        
        if oc < THRESHOLDS['OC_LOW']:
            self.risk_flags['LOW_ORGANIC_CARBON'] = True
            self.warnings.append("Warning: Low soil organic carbon. This reduces nutrient retention and fertilizer efficiency.")
            self.recommendations.append("Introduce organic carbon enrichment (e.g., farmyard manure, vermicompost, or crop residue incorporation).")

    def analyze(self) -> dict:
        """Runs all heuristic checks and returns structured insights."""
        self._check_nitrogen_excess()
        self._check_salinity_risk()
        self._check_soil_health()
        
        # Risk level determination based on the number of flags
        flag_count = len(self.risk_flags)
        if flag_count >= 3:
            risk_level = "Critical"
        elif flag_count == 2:
            risk_level = "High"
        elif flag_count == 1:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        return {
            "risk_level": risk_level,
            "risk_flags": self.risk_flags,
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }