import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT_FOLDER = os.path.abspath(os.curdir)
filename = "id_ood_barplot.png"

# data obtained from multiple csv files
# hard to read so typing out the accuracies below for easy plotting
subjects_df = pd.DataFrame()
subjects = [0, 1, 2, 3, 4, 5, 6]
subjects_df['subject'] = subjects * 4
subjects_df['method'] = ['(OoD) Zero-Shot Training']*7 + ['(OoD) Pre-trained Fine-tuning'] * \
    7 + ['(ID) Zero-Shot Training']*7 + ['(ID) Pre-trained Fine-tuning']*7
subjects_df['accuracy'] = (0.729, 0.613, 0.801, 0.761, 0.936, 0.681, 0.728)
+ (0.738, 0.677, 0.877, 0.755, 0.956, 0.693, 0.723)
+ (0.769, 0.631, 0.814, 0.739, 0.935, 0.832, 0.732)
+ (0.80, 0.832, 0.873, 0.841, 0.963, 0.742, 0.735)

subjects_df['accuracy'] *= 100
subjects_df['hatch pattern'] = ['']*14 + ['/']*14

palette = {
    "(OoD) Zero-Shot Training": "#ff4d4d",
    "(OoD) Pre-trained Fine-tuning": "#b30000",
    "(ID) Zero-Shot Training": "#90ee90",
    "(ID) Pre-trained Fine-tuning": "#009a00"
}

g = sns.catplot(
    data=subjects_df, kind="bar",
    x="subject", y="accuracy", hue="method", palette=palette, hatch="hatch pattern", height=8, aspect=1, legend=False)
g.despine(left=True)

hatches = [''] * 7 + [''] * 7 + ['..'] * 7 + ['..'] * 7

print(g.axes[0, 0].patches)
for i, bar in enumerate(g.axes[0, 0].patches):
    bar.set_hatch(hatches[i])
l = plt.legend(bbox_to_anchor=(1.05, 1.05), ncol=2,
               loc='lower right', prop={'size': 14})
for lp, hatch in zip(l.get_patches(), ['', '', '..', '..']):
    lp.set_hatch(hatch)
    lp.set_edgecolor('k')

plt.grid()
plt.xlabel("Subjects", fontsize=22)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.ylabel("Test Accuracies (in %)", fontsize=22)
plt.title("Model comparison on ID and OoD Distributions", fontsize=24)

plt.savefig(ROOT_FOLDER + f"/plots/" + filename, bbox_inches='tight', dpi=600)
