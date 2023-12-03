import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats
import os

# set up constants, change filename if you like
SEEDS = [42, 43, 44, 45, 46]
ROOT_FOLDER = os.path.abspath(os.curdir)
filename = "test_accuracy_all_humans_zero_shot_vs_pretrained.png"

# set up necessary variables
percents = []
df_accs_no_pretrain, df_lls_no_pretrain = pd.DataFrame(), pd.DataFrame()
df_accs_pretrain, df_lls_pretrain = pd.DataFrame(), pd.DataFrame()
accs_no_pretrain_mean, accs_no_pretrain_std, lls_no_pretrain_mean, lls_no_pretrain_std = [], [], [], []
accs_pretrain_mean, accs_pretrain_std, lls_pretrain_mean, lls_pretrain_std = [], [], [], []

# read csv files
for SEED in SEEDS:
    df_no_pretrain = pd.read_csv(ROOT_FOLDER + f"/data/No Pretraining vs. Pretraining/Human trained + no pretraining (Seed: {SEED}).csv").drop(columns=["Unnamed: 0"])    
    df_accs_no_pretrain[f'Seed: {SEED}'] = df_no_pretrain['accuracy']
    df_lls_no_pretrain[f'Seed: {SEED}'] = df_no_pretrain['logloss']

    df_pretrain = pd.read_csv(ROOT_FOLDER + f"/data/No Pretraining vs. Pretraining/Human trained + Yaskawa pretraining (Seed: {SEED}).csv").drop(columns=["Unnamed: 0"])
    df_accs_pretrain[f'Seed: {SEED}'] = df_pretrain['accuracy']
    df_lls_pretrain[f'Seed: {SEED}'] = df_pretrain['logloss']

    percents += [df_no_pretrain['percent']]

percents = list(df_no_pretrain['percent'])

# calculate mean and standard deviation of the 5 seeded runs
for i in range(len(percents)):
    accs_no_pretrain_mean += [stats.mean([
        df_accs_no_pretrain['Seed: 42'][i], 
        df_accs_no_pretrain['Seed: 43'][i], 
        df_accs_no_pretrain['Seed: 44'][i], 
        df_accs_no_pretrain['Seed: 45'][i], 
        df_accs_no_pretrain['Seed: 46'][i]]
        )]
    
    accs_no_pretrain_std += [stats.stdev([
        df_accs_no_pretrain['Seed: 42'][i], 
        df_accs_no_pretrain['Seed: 43'][i], 
        df_accs_no_pretrain['Seed: 44'][i], 
        df_accs_no_pretrain['Seed: 45'][i], 
        df_accs_no_pretrain['Seed: 46'][i]]
        )]
    
    accs_pretrain_mean += [stats.mean([
        df_accs_pretrain['Seed: 42'][i], 
        df_accs_pretrain['Seed: 43'][i], 
        df_accs_pretrain['Seed: 44'][i], 
        df_accs_pretrain['Seed: 45'][i], 
        df_accs_pretrain['Seed: 46'][i]]
        )]
    
    accs_pretrain_std += [stats.stdev([
        df_accs_pretrain['Seed: 42'][i], 
        df_accs_pretrain['Seed: 43'][i], 
        df_accs_pretrain['Seed: 44'][i], 
        df_accs_pretrain['Seed: 45'][i], 
        df_accs_pretrain['Seed: 46'][i]]
        )]

# adjust percentages
percents_x_100 = [percent*100 for percent in percents]

accs_no_pretrain_stds_plus = [first + second for first, second in zip([acc*100 for acc in accs_no_pretrain_mean], [std for std in accs_no_pretrain_std])]
accs_no_pretrain_stds_minus = [first - second for first, second in zip([acc*100 for acc in accs_no_pretrain_mean], [std for std in accs_no_pretrain_std])]

accs_pretrain_stds_plus = [first + second for first, second in zip([acc*100 for acc in accs_pretrain_mean], [std for std in accs_pretrain_std])]
accs_pretrain_stds_minus = [first - second for first, second in zip([acc*100 for acc in accs_pretrain_mean], [std for std in accs_pretrain_std])]

# plot test accuracy of zero shot training vs fine tuning pretrained model
plt.cla()
fig, ax = plt.subplots()
ax.plot(percents_x_100, [acc*100 for acc in accs_no_pretrain_mean], '.r--', linewidth=3, markersize=10, alpha=1)
ax.fill_between(percents_x_100, accs_no_pretrain_stds_plus, accs_no_pretrain_stds_minus, color='#ff8080', alpha=0.4)
ax.plot([percent*100 for percent in percents], [acc*100 for acc in accs_pretrain_mean], '.g-', linewidth=3, markersize=10, alpha=1)
ax.fill_between(percents_x_100, accs_pretrain_stds_plus, accs_pretrain_stds_minus, color='#90ee90', alpha=0.4)
ax.set_title(f"Test Accuracy vs Dataset volume", fontsize=18)
ax.set_xlabel("Percentage of Data (in %)", fontsize=18)
ax.set_ylabel("Test Accuracy (in %)", fontsize=18)
ax.legend(["Zero-Shot Training", "Pre-trained Fine-Tuning"], fontsize=18)
ax.grid(visible=1)
# fig.show()

# save figure and exit
if filename is None:
    plt.savefig(ROOT_FOLDER + f"/plots/" + "test_accuracy_all_humans_zero_shot_vs_pretrained.png", dpi=600)
else:
    plt.savefig(ROOT_FOLDER + f"/plots/" + filename, dpi=600)

print(f"Saved plot: {filename}!")


