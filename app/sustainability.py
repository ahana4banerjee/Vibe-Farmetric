"""
app/sustainability.py

Calculates a baseline sustainability score by aggregating weighted penalties
derived from the OveruseEngine's heuristic analysis.
"""
from config import PENALTIES
from overuse_engine import OveruseEngine
import json

class SustainabilityEngine:
    def __init__(self, farm_data: dict):
        self.farm_data = farm_data
        self.base_score = 100
        self.penalties_applied = {}

    def _map_category(self, score: int) -> str:
        """Maps numerical score to a qualitative sustainability category."""
        if score >= 90: return "Excellent"
        if score >= 75: return "Good"
        if score >= 60: return "Moderate"
        if score >= 40: return "Poor"
        return "Critical"

    def evaluate(self) -> dict:
        """Runs the overuse analysis and compiles the final sustainability profile."""
        analyzer = OveruseEngine(self.farm_data)
        analysis = analyzer.analyze()
        
        score = self.base_score
        
        # Apply weighted penalties based on triggered flags
        for flag in analysis['risk_flags'].keys():
            if flag in PENALTIES:
                penalty = PENALTIES[flag]
                score -= penalty
                # Format flag name for clean UI display (e.g. "NITROGEN_EXCESS" -> "Nitrogen Excess")
                formatted_name = flag.replace('_', ' ').title()
                self.penalties_applied[formatted_name] = -penalty

        final_score = max(0, score)

        return {
            "sustainability_score": final_score,
            "category": self._map_category(final_score),
            "risk_score": analysis['risk_score'],
            "risk_level": analysis['risk_level'],
            "penalty_breakdown": self.penalties_applied,
            "triggered_rules": list(analysis['risk_flags'].keys()),
            "warnings": analysis['warnings'],
            "recommendations": analysis['recommendations'],
            "disclaimer": "AI-assisted sustainability indicator based on heuristic patterns. Not a certified agronomic diagnosis."
        }

# ==========================================
# ADVANCED TEST CASES
# ==========================================
if __name__ == "__main__":
    test_scenarios = {
        "1. Healthy Farm": {
            'Nitrogen_Level': 80, 'Phosphorus_Level': 30, 'Potassium_Level': 40,
            'Electrical_Conductivity': 0.8, 'Organic_Carbon': 1.2, 
            'Yield_Last_Season': 25, 'Fertilizer_Used_Last_Season': 'Compost'
        },
        "2. Nitrogen-Heavy Overuse": {
            'Nitrogen_Level': 140, 'Phosphorus_Level': 25, 'Potassium_Level': 30,
            'Electrical_Conductivity': 1.1, 'Organic_Carbon': 0.8, 
            'Yield_Last_Season': 12, 'Fertilizer_Used_Last_Season': 'Urea'
        },
        "3. Phosphorus-Heavy Imbalance": {
            'Nitrogen_Level': 90, 'Phosphorus_Level': 75, 'Potassium_Level': 20,
            'Electrical_Conductivity': 1.0, 'Organic_Carbon': 0.7, 
            'Yield_Last_Season': 14, 'Fertilizer_Used_Last_Season': 'DAP'
        },
        "4. Severe Salinity Stress": {
            'Nitrogen_Level': 130, 'Phosphorus_Level': 65, 'Potassium_Level': 85,
            'Electrical_Conductivity': 1.9, 'Organic_Carbon': 0.4, 
            'Yield_Last_Season': 10, 'Fertilizer_Used_Last_Season': '14-35-14'
        }
    }

    for scenario_name, data in test_scenarios.items():
        print(f"\n{'-'*50}")
        print(f"Executing Scenario: {scenario_name}")
        print(f"{'-'*50}")
        
        engine = SustainabilityEngine(data)
        result = engine.evaluate()
        
        # We selectively print the most important outputs for clarity
        print(f"Sustainability Score : {result['sustainability_score']} ({result['category']})")
        print(f"Risk Level           : {result['risk_level']} (Score: {result['risk_score']})")
        print(f"Penalty Breakdown    : {result['penalty_breakdown']}")
        print("\nWarnings:")
        for w in result['warnings']: print(f"  - {w}")
        print("\nRecommendations:")
        for r in result['recommendations']: print(f"  - {r}")