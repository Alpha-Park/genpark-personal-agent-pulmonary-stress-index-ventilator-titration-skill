"""
Example usage for Pulmonary Stress Index (SI) Skill.
"""

from client import PulmonaryStressIndexClient


def main():
    client = PulmonaryStressIndexClient()

    print("--- Case 1: Optimal Linear Compliance (Protective Ventilation) ---")
    optimal_case = client.calculate_stress_index(
        stress_index_b=1.01,
        peep_cmh2o=10.0,
        plateau_pressure_cmh2o=22.0,
        tidal_volume_ml=420.0
    )
    print("Stress Index (b):", optimal_case["stress_index_metrics"]["stress_index_b"])
    print("Ventilation Phenotype:", optimal_case["clinical_titration"]["ventilation_phenotype"])
    print("Titration Guidance:", optimal_case["clinical_titration"]["titration_guidance"])
    print()

    print("--- Case 2: Tidal Recruitment / Atelectotrauma (Insufficient PEEP) ---")
    recruitment_case = client.calculate_stress_index(
        stress_index_b=0.88,
        peep_cmh2o=6.0,
        plateau_pressure_cmh2o=20.0,
        tidal_volume_ml=450.0
    )
    print("Stress Index (b):", recruitment_case["stress_index_metrics"]["stress_index_b"])
    print("Ventilation Phenotype:", recruitment_case["clinical_titration"]["ventilation_phenotype"])
    print("Titration Guidance:", recruitment_case["clinical_titration"]["titration_guidance"])
    print("Lung Injury Risk:", recruitment_case["clinical_titration"]["lung_injury_risk"])
    print()

    print("--- Case 3: Tidal Hyperinflation / Overdistension (Excessive PEEP/Vt) ---")
    hyperinflation_case = client.calculate_stress_index(
        stress_index_b=1.14,
        peep_cmh2o=16.0,
        plateau_pressure_cmh2o=32.0,
        tidal_volume_ml=500.0
    )
    print("Stress Index (b):", hyperinflation_case["stress_index_metrics"]["stress_index_b"])
    print("Ventilation Phenotype:", hyperinflation_case["clinical_titration"]["ventilation_phenotype"])
    print("Titration Guidance:", hyperinflation_case["clinical_titration"]["titration_guidance"])


if __name__ == "__main__":
    main()
