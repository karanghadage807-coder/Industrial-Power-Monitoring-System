import pandas as pd
import math

# -----------------------------------
# 1. Read load data
# -----------------------------------

loads = pd.read_csv("data/loads.csv")


# -----------------------------------
# 2. Calculate electrical parameters
# -----------------------------------

results = []

for _, row in loads.iterrows():

    load_name = row["load_name"]

    p_kw = row["p_kw"]

    pf = row["pf"]

    voltage_v = row["voltage_v"]

    # Phase angle
    phi = math.acos(pf)

    # Reactive power
    q_kvar = p_kw * math.tan(phi)

    # Apparent power
    s_kva = math.sqrt(
        p_kw**2 +
        q_kvar**2
    )

    # Three-phase current
    current_a = (
        p_kw * 1000 /
        (
            math.sqrt(3) *
            voltage_v *
            pf
        )
    )

    results.append({
        "Load": load_name,
        "P_kW": p_kw,
        "Q_kVAR": q_kvar,
        "S_kVA": s_kva,
        "PF": pf,
        "Current_A": current_a
    })


# -----------------------------------
# 3. Create result table
# -----------------------------------

results_df = pd.DataFrame(results)


# -----------------------------------
# 4. Display results
# -----------------------------------

print("\nINDUSTRIAL LOAD ANALYSIS")
print("========================")

print(
    results_df.to_string(
        index=False
    )
)


# -----------------------------------
# 5. Total system quantities
# -----------------------------------

total_p = results_df["P_kW"].sum()

total_q = results_df["Q_kVAR"].sum()

total_s = math.sqrt(
    total_p**2 +
    total_q**2
)

overall_pf = total_p / total_s


print("\nSYSTEM TOTALS")
print("=============")

print(f"Total Active Power : {total_p:.2f} kW")

print(f"Total Reactive Power : {total_q:.2f} kVAR")

print(f"Total Apparent Power : {total_s:.2f} kVA")

print(f"Overall Power Factor : {overall_pf:.3f}")