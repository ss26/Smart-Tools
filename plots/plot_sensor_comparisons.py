import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT_FOLDER = os.path.abspath(os.curdir)
filename = "sensor_comparisons.png"

def transformer(df1, df2):
    df1_modified = pd.DataFrame()
    quantile_ranges = list(np.arange(0, 1, 0.01))
    
    def quantile_vals(df, quantile_ranges):
        return [df.quantile(q) for q in quantile_ranges] 

    df1_modified['values'] = pd.concat(quantile_vals(df1, quantile_ranges), ignore_index=False)
    df1_modified['category'] = df1_modified.index
    df1_modified['type'] = 'human'

    df2_modified = pd.DataFrame()
    df2_modified['values'] = pd.concat(quantile_vals(df2, quantile_ranges), ignore_index=False)
    df2_modified['category'] = df2_modified.index
    df2_modified['type'] = 'robot'

    df_proc = pd.concat([df1_modified, df2_modified])
    return df_proc

df_robot = pd.read_parquet(ROOT_FOLDER + f"/data/Yaskawa/Processed Data/S2023_Yaskawa_Smoothened_Cleaned.parquet")
df_human = pd.read_parquet(ROOT_FOLDER + f"/data/Human/Processed Data/F2021_Human_Smoothened_Cleaned.parquet")

df_robot = df_robot.iloc[:, :-1]
df_human = df_human.iloc[:, :-1]
for column in df_robot.columns:
    df_robot[column] = df_robot[column] / df_robot[column].abs().max()

for column in df_human.columns:
    df_human[column] = df_human[column] / df_human[column].abs().max()

raw_df_boxplot = transformer(df_human, df_robot)

ax = sns.boxplot(x='category', y='values',
            hue='type', palette=["m", "g"],
            data=raw_df_boxplot)
ax.set_xticklabels(ax.get_xticklabels(),rotation=30, fontsize=18)
ax.set_title("Raw Sensor Reading Comparison", fontsize=18)
ax.set_xlabel("Sensor", fontsize=18)
ax.set_ylabel("Sensor Values", fontsize=18)
ax.legend(fontsize=18)
plt.tight_layout()
# plt.show()

plt.savefig(ROOT_FOLDER + f"/plots/" + filename, dpi=600)

print(f"Saved plot: {filename}!")