"""
Pulmonary Stress Index (SI) & Ventilator PEEP/Tidal Volume Titration Client.
Zero-mock pure Python standard library implementation.
Fits the dynamic constant-flow airway pressure equation Paw(t) = a * t^b + c,
calculates Stress Index (b), and classifies cyclic alveolar recruitment (b < 0.95),
optimal linear compliance (0.95 <= b <= 1.05), and tidal hyperinflation/overdistension (b > 1.05).
"""

import math
from typing import Dict, Any, Optional, List, Tuple


class PulmonaryStressIndexClient:
    """
    Evaluates dynamic airway pressure trajectory during constant-flow mechanical ventilation:
    - Paw(t) = a * t^b + c (Ranieri model)
    - Stress Index (b):
        * b < 0.95: Tidal recruitment / cyclic atelectotrauma (insufficient PEEP)
        * 0.95 <= b <= 1.05: Linear compliance (optimal lung-protective ventilation)
        * b > 1.05: Tidal hyperinflation / overdistension (excessive PEEP / Vt)
    - Prevents Ventilator-Induced Lung Injury (VILI) in Acute Respiratory Distress Syndrome (ARDS).
    """

    def __init__(self):
        pass

    def calculate_stress_index(
        self,
        time_pressure_samples: Optional[List[Tuple[float, float]]] = None,
        stress_index_b: Optional[float] = None,
        peep_cmh2o: Optional[float] = 10.0,
        plateau_pressure_cmh2o: Optional[float] = 24.0,
        tidal_volume_ml: Optional[float] = 420.0
    ) -> Dict[str, Any]:
        """
        Calculates or stratifies the Stress Index (SI).
        time_pressure_samples: list of (time_sec, pressure_cmh2o) tuples during constant inspiratory flow.
        stress_index_b: directly provided Stress Index coefficient if already pre-fitted.
        """
        if stress_index_b is None and (not time_pressure_samples or len(time_pressure_samples) < 3):
            raise ValueError("Either stress_index_b or at least 3 (time, pressure) samples must be provided.")

        fitted_a = None
        c_baseline = peep_cmh2o if peep_cmh2o is not None else 0.0

        if stress_index_b is None and time_pressure_samples:
            # Perform log-linear regression: ln(Paw - c) = ln(a) + b * ln(t)
            valid_pts = []
            for t, p in time_pressure_samples:
                if t > 0 and (p - c_baseline) > 0.1:
                    valid_pts.append((math.log(t), math.log(p - c_baseline)))

            if len(valid_pts) < 3:
                raise ValueError("Insufficient points where (Paw - PEEP) > 0 for reliable curve fitting.")

            n = len(valid_pts)
            sum_x = sum(x for x, y in valid_pts)
            sum_y = sum(y for x, y in valid_pts)
            sum_xx = sum(x * x for x, y in valid_pts)
            sum_xy = sum(x * y for x, y in valid_pts)

            denominator = (n * sum_xx - sum_x * sum_x)
            if abs(denominator) < 1e-9:
                b_val = 1.0
                fitted_a = 1.0
            else:
                b_val = (n * sum_xy - sum_x * sum_y) / denominator
                ln_a = (sum_y - b_val * sum_x) / n
                fitted_a = math.exp(ln_a)
            stress_index_b = b_val

        # Clinical Classification based on Ranieri NEJM standards:
        if stress_index_b < 0.95:
            ventilation_phenotype = "Tidal Recruitment / Cyclic Atelectasis (SI < 0.95)"
            actionable_titration = "PEEP is insufficient; compliance improves during inspiration as collapsed lung units are recruited. Titrate PEEP upward to prevent repeated cyclical opening/closing injury."
            lung_injury_risk = "High risk of cyclic shear stress and atelectotrauma."
        elif stress_index_b > 1.05:
            ventilation_phenotype = "Tidal Hyperinflation / Parenchymal Overdistension (SI > 1.05)"
            actionable_titration = "End-inspiratory elastance increases as lungs are stretched onto the flat upper portion of the P-V curve. Decrease PEEP or down-titrate tidal volume toward 4-6 mL/kg PBW."
            lung_injury_risk = "High risk of alveolar rupture, barotrauma, volutrauma, and right ventricular afterload impediment."
        else:
            ventilation_phenotype = "Linear Compliance / Optimal Lung-Protective Zone (0.95 <= SI <= 1.05)"
            actionable_titration = "Current PEEP and tidal volume maintain ventilation within the safe, linear compliance range. Maintain lung-protective settings."
            lung_injury_risk = "Low / minimal risk of cyclic mechanical injury."

        # Driving pressure context
        driving_pressure_cmh2o = None
        if plateau_pressure_cmh2o and peep_cmh2o:
            driving_pressure_cmh2o = round(plateau_pressure_cmh2o - peep_cmh2o, 1)

        return {
            "status": "success",
            "stress_index_metrics": {
                "stress_index_b": round(stress_index_b, 3),
                "curve_scaling_factor_a": round(fitted_a, 3) if fitted_a is not None else None,
                "baseline_pressure_c_cmh2o": round(c_baseline, 1),
                "driving_pressure_cmh2o": driving_pressure_cmh2o,
                "plateau_pressure_cmh2o": plateau_pressure_cmh2o,
                "peep_cmh2o": peep_cmh2o,
                "tidal_volume_ml": tidal_volume_ml
            },
            "clinical_titration": {
                "ventilation_phenotype": ventilation_phenotype,
                "titration_guidance": actionable_titration,
                "lung_injury_risk": lung_injury_risk
            }
        }
