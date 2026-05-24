# app/sustainability.py
from config import PENALTIES
from overuse_engine import OveruseEngine

class SustainabilityEngine:
    """
    Calculates a baseline sustainability score by aggregating weighted penalties
    derived from the OveruseEngine's heuristic analysis.
    """
    
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
        """
        Runs the overuse analysis, calculates the score, and formats the output.
        """
        # 1. Run the Overuse Engine
        analyzer = OveruseEngine(self.farm_data)
        overuse_results = analyzer.analyze()
        risk_flags = overuse_results['risk_flags']

        # 2. Calculate Penalties
        score = self.base_score
        
        for flag in risk_flags.keys():
            if flag in PENALTIES:
                penalty = PENALTIES[flag]
                score -= penalty
                # Record the breakdown (human readable)
                formatted_flag_name = flag.replace('_', ' ').title()
                self.penalties_applied[formatted_flag_name] = -penalty

        # Ensure score doesn't drop below 0
        final_score = max(0, score)

        # 3. Construct Final Output
        return {
            "sustainability_score": final_score,
            "category": self._map_category(final_score),
            "risk_level": overuse_results['risk_level'],
            "penalty_breakdown": self.penalties_applied,
            "warnings": overuse_results['warnings'],
            "recommendations": overuse_results['recommendations'],
            "disclaimer": "AI-assisted sustainability indicator based on heuristic patterns. Not a certified agronomic diagnosis."
        }

# ==========================================
# TEST BLOCK: Run this file directly to test
# ==========================================
if __name__ == "__main__":
    # Sample synthetic data representing a highly unsustainable farm
    sample_farm_data = {
        'Nitrogen_Level': 135,                  # High
        'Phosphorus_Level': 40,
        'Potassium_Level': 35,
        'Electrical_Conductivity': 1.8,         # High
        'Organic_Carbon': 0.3,                  # Low
        'Yield_Last_Season': 12,                # Poor Yield
        'Fertilizer_Used_Last_Season': 'Urea'   # Nitrogen Heavy / Chemical
    }

    print("Testing Sustainability Scoring Engine...\n")
    engine = SustainabilityEngine(sample_farm_data)
    result = engine.evaluate()
    
    import json
    print(json.dumps(result, indent=4))