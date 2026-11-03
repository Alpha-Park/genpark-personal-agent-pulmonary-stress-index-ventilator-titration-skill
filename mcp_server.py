"""
MCP Server implementation for Pulmonary Stress Index (SI) Skill.
Exposes standard FastMCP-compatible tools for ventilator pressure profile analysis and PEEP titration.
"""

import sys
import json
from typing import Dict, Any, Optional, List, Tuple
from client import PulmonaryStressIndexClient


def evaluate_stress_index(
    stress_index_b: Optional[float] = None,
    time_pressure_samples: Optional[List[Tuple[float, float]]] = None,
    peep_cmh2o: Optional[float] = 10.0,
    plateau_pressure_cmh2o: Optional[float] = 24.0,
    tidal_volume_ml: Optional[float] = 420.0
) -> str:
    """
    Evaluates mechanical ventilation Stress Index (SI) from airway pressure profile.
    Returns structured recommendations for PEEP and tidal volume titration.
    """
    client = PulmonaryStressIndexClient()
    result = client.calculate_stress_index(
        time_pressure_samples=time_pressure_samples,
        stress_index_b=stress_index_b,
        peep_cmh2o=peep_cmh2o,
        plateau_pressure_cmh2o=plateau_pressure_cmh2o,
        tidal_volume_ml=tidal_volume_ml
    )
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--tools":
        tools = [
            {
                "name": "evaluate_stress_index",
                "description": "Calculates or stratifies mechanical ventilation Stress Index (Paw = a * t^b + c) to distinguish alveolar recruitment (b < 0.95), linear compliance (0.95-1.05), and tidal overdistension (b > 1.05).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "stress_index_b": {"type": "number", "description": "Pre-fitted Stress Index exponent 'b'"},
                        "peep_cmh2o": {"type": "number", "description": "Positive end-expiratory pressure in cmH2O (default: 10.0 cmH2O)"},
                        "plateau_pressure_cmh2o": {"type": "number", "description": "End-inspiratory plateau airway pressure in cmH2O (default: 24.0 cmH2O)"},
                        "tidal_volume_ml": {"type": "number", "description": "Delivered tidal volume in mL (default: 420.0 mL)"}
                    }
                }
            }
        ]
        print(json.dumps(tools, indent=2))
    else:
        # Simple self-test
        client = PulmonaryStressIndexClient()
        test_res = client.calculate_stress_index(
            stress_index_b=1.02,
            peep_cmh2o=10.0,
            plateau_pressure_cmh2o=24.0
        )
        print("Self-test passed:")
        print(json.dumps(test_res, indent=2))
