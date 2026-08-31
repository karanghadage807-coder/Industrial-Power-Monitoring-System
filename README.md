# Industrial Power Monitoring System

A Python-based industrial electrical power monitoring and analysis system designed to evaluate electrical loads, power factor, transformer loading, energy consumption, and electrical losses.

The project combines electrical engineering calculations with Python, Pandas, and Streamlit to provide an interactive monitoring and decision-support dashboard.

---

## Project Overview

Industrial electrical systems contain multiple loads such as motors, pumps, and compressors. Poor power factor and high reactive power increase current, transformer loading, and electrical losses.

This project analyzes a modeled industrial electrical system and provides:

- Load-wise electrical analysis
- Power factor evaluation
- Load priority ranking
- Power factor correction
- Capacitor-bank selection
- Power factor sensitivity analysis
- Transformer loading analysis
- Energy consumption estimation
- Copper-loss analysis
- Loss-energy savings analysis
- Automated engineering recommendations
- Interactive Streamlit dashboard

---

## Key Features

### 1. Load Analysis

Analyzes individual industrial loads using:

- Active Power (kW)
- Reactive Power (kVAR)
- Power Factor (PF)

The system identifies loads with high power consumption, high reactive power, and poor power factor.

### 2. Load Priority Analysis

Loads are ranked according to their electrical impact using a priority score.

This helps identify loads that should receive higher priority for power factor correction and electrical improvement.

### 3. Power Factor Correction

The system calculates the capacitor requirement for a selected target power factor and selects a practical capacitor-bank size based on the configured capacitor step.

The effect of power factor correction on:

- Reactive power
- Apparent power
- Power factor
- Line current
- Transformer loading

is evaluated.

### 4. Power Factor Sensitivity Analysis

Multiple target power factors are evaluated to understand the relationship between:

- Target PF
- Required capacitor size
- Selected capacitor size
- Achieved PF
- LV current
- Transformer loading

### 5. Transformer Analysis

The system evaluates:

- Transformer loading
- LV full-load current
- HV full-load current
- Actual LV load current
- Copper loss
- Core loss
- Total transformer loss
- Transformer efficiency

### 6. Energy Analysis

Estimated energy consumption is calculated using:

- Load power
- Load factor
- Operating hours

Daily and monthly energy consumption are calculated for individual industrial loads and for the complete system.

### 7. Loss Analysis

Three-phase copper losses are estimated using:

P_loss = 3 x I^2 x R

The system compares electrical losses before and after power factor correction.

### 8. Engineering Recommendations

Automatic recommendations are generated using:

- Power factor
- Reactive power
- Load priority

---

## Key Results

The developed system produced the following results for the modeled industrial load system:

| Parameter | Result |
|---|---:|
| Total Active Power | 650.00 kW |
| Total Reactive Power | 380.12 kVAR |
| Original Apparent Power | 752.99 kVA |
| Original Power Factor | 0.863 |
| Target Power Factor | 0.95 |
| Selected Capacitor Bank | 175 kVAR |
| Achieved Power Factor | 0.954 |
| Current Before Correction | 1047.56 A |
| Current After Correction | 948.24 A |
| Current Reduction | ~9.5% |
| Transformer Loading Before | 75.30% |
| Transformer Loading After | 68.16% |
| Copper Loss Before | 65.84 kW |
| Copper Loss After | 53.95 kW |
| Copper Loss Reduction | 18.06% |
| Daily Energy Consumption | 6643 kWh |
| Monthly Energy Consumption | 199290 kWh |

### Highest Priority Load

**Motor_2**

- Power Factor: 0.82
- Reactive Power: 104.70 kVAR
- Priority Score: 18.846
- Recommendation: High priority for power factor correction

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard with six sections:

1. Dashboard
2. Load Analysis
3. Power Factor Correction
4. Energy Analysis
5. Loss Analysis
6. Recommendations

The dashboard provides:

- KPI cards
- Electrical load tables
- Bar charts
- Sensitivity analysis
- Before/after correction comparison
- Transformer loading information
- Loss analysis
- Automated recommendations

---

## Project Structure

```text
Industrial-Power-Monitoring-System/
|
+-- dashboard/
|   +-- app.py
|
+-- data/
|   +-- loads.csv
|   +-- load_analysis_results.csv
|   +-- load_priority_results.csv
|   +-- load_recommendations.csv
|   +-- pf_correction_results.csv
|   +-- pf_sensitivity_results.csv
|   +-- energy_analysis_results.csv
|   +-- loss_analysis_results.csv
|   +-- loss_energy_analysis_results.csv
|   +-- capacitor_bank.csv
|   +-- transformer.csv
|
+-- docs/
|
+-- matlab/
|
+-- results/
|
+-- src/
|   +-- load_analysis.py
|   +-- load_priority.py
|   +-- load_recommendation.py
|   +-- pf_sensitivity.py
|   +-- transformer_analysis.py
|   +-- energy_analysis.py
|   +-- loss_analysis.py
|   +-- loss_energy_analysis.py
|
+-- .gitignore
+-- README.md
+-- requirements.txt