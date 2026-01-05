import pandas as pd
import numpy as np

np.random.seed(42)

rows = 1000

data = {
    "magnitude": np.round(np.random.uniform(4.0, 9.2, rows), 2),
    "depth": np.round(np.random.uniform(5, 700, rows), 1),
    "cdi": np.round(np.random.uniform(0, 10, rows), 2),
    "mmi": np.round(np.random.uniform(1, 10, rows), 2),
    "sig": np.round(np.random.uniform(0, 1800, rows), 1),
}

df = pd.DataFrame(data)

# REALISTIC ALERT LOGIC
def assign_alert(row):
    if row["magnitude"] >= 7.5 or row["mmi"] >= 8:
        return "red"
    elif row["magnitude"] >= 6.5 or row["mmi"] >= 6:
        return "orange"
    elif row["magnitude"] >= 5.5 or row["mmi"] >= 4:
        return "yellow"
    else:
        return "green"

df["alert"] = df.apply(assign_alert, axis=1)

df.to_csv("usgs_earthquake_realistic_1000.csv", index=False)

print("✅ Realistic USGS-style dataset generated (1000 rows)")
