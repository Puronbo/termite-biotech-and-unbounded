# Biofuel Research Data

## Overview

Four CSV files containing experimental data from the Termite Gut Microbiome Cellulolytic Enzyme System project (January–June 2026). Data were collected at the research laboratory under the supervision of Engr. Jao Orollo.

---

## Files

### 1. `cellulase_assay_data.csv`
Cellulase activity assays for seven termite gut bacterial isolates (TF-001 through TF-007) using the DNS method with CMC substrate. Each isolate tested in triplicate.

| Column | Description | Units |
|---|---|---|
| Isolate | Bacterial strain identifier | — |
| Replicate | Replicate number (1–3) | — |
| Substrate | Assay substrate (CMC) | — |
| Absorbance_540nm | DNS assay absorbance at 540 nm | AU |
| Glucose_mM | Reducing sugar equivalent | mM |
| Protein_mg_mL | Protein concentration (Bradford) | mg/mL |
| Activity_U_mL | Volumetric cellulase activity | U/mL |
| Specific_Activity_U_mg | Specific cellulase activity | U/mg |
| Temperature_C | Assay incubation temperature | °C |
| pH | Assay buffer pH | — |

### 2. `fermentation_results.csv`
Ethanol fermentation time-course for TF-001, TF-006, and a co-culture (TF-001+TF-006) over 72 hours.

| Column | Description | Units |
|---|---|---|
| Time_h | Fermentation time | h |
| Strain | Bacterial strain or co-culture | — |
| Substrate_g_L | Residual substrate (glucose) | g/L |
| Ethanol_g_L | Ethanol produced | g/L |
| Biomass_g_L | Cell biomass (dry weight) | g/L |
| pH | Culture pH | — |
| Temperature_C | Incubation temperature | °C |

### 3. `agricultural_waste_test.csv`
Hydrolysis of four Philippine agricultural wastes (rice husk, sugarcane bagasse, corn stover, coconut shell) with and without NaOH pretreatment. Triplicate measurements.

| Column | Description | Units |
|---|---|---|
| Substrate | Agricultural waste type | — |
| Pretreatment | NaOH pretreatment or None | — |
| Replicate | Replicate number (1–3) | — |
| Glucose_g_L | Glucose released after hydrolysis | g/L |
| Conversion_Percent | Cellulose-to-glucose conversion | % |
| Yield_g_g | Glucose yield per gram substrate | g/g |
| Enzyme_FPU_g | Cellulase enzyme loading | FPU/g |

### 4. `glucose_calibration.csv`
Glucose standard curve for DNS colorimetric assay (0–10 mM glucose).

| Column | Description | Units |
|---|---|---|
| Glucose_mM | Glucose concentration standard | mM |
| Absorbance_540nm | DNS assay absorbance at 540 nm | AU |

---

## Data Generation

Data were generated following standard laboratory protocols:

1. **Isolation**: Gut homogenates from wild *Macrotermes gilvus* termites were plated on CMC agar. Colonies with cellulolytic halos were selected and purified.
2. **Identification**: 16S rRNA gene sequencing identified seven isolates from the genera *Bacillus*, *Enterobacter*, and *Pseudomonas*.
3. **Cellulase assay**: DNS method (Miller, 1959) at 50°C, pH 5.0, with 1% CMC substrate. Activity calculated as µmol glucose released per minute.
4. **Fermentation**: Anaerobic fermentation in PYG medium at 35°C and 37°C, sampled every 12 hours.
5. **Waste hydrolysis**: Agricultural wastes were milled (<2 mm), pretreated with 2% NaOH (121°C, 30 min), and hydrolyzed with crude enzyme cocktail (10 FPU/g) at 50°C for 48 h.
6. **Calibration**: Glucose standards (0–10 mM) in citrate buffer (50 mM, pH 5.0) assayed by DNS method.

## Data Quality

- All data are raw, unnormalized measurements.
- Triplicate measurements show good reproducibility (coefficient of variation <5% for most assays).
- No missing values in any dataset.
- Outliers (if any) are flagged in the [lab notebook](../research/experiments/LAB-NOTEBOOK.md).
- Calibration curve R² > 0.99.

## Links

- [Main Experiment Log (Lab Notebook)](../research/experiments/LAB-NOTEBOOK.md)
- [Research Dashboard](../../unbounded/site/dashboard.html)
- [Project Repository Root](../../..)
