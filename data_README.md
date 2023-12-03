# Data

## Source 

Raw data from accelerometer, gyroscope, magnetometer, current sensor and microphone are collected using an arduino. 

Here's the link for both human and robot data. 

Source: [Box link](https://utexas.box.com/s/ail8mdlvn97gygzu6eefn3nr0un53v46).

## File structure

Download the data from the link provided and place it in a folder called 'data'. The file tree should then look like:

```
.
├── data
│   ├── Human
│   │   ├── Processed Data
│   │   ├── Run_1_Samples
│   │   ├── Run_2_Samples
│   │   ├── Run_3_Samples
│   │   ├── Run_4_Samples
│   │   ├── Run_5_Samples
│   │   ├── Run_6_Samples
│   │   ├── Run_7_Samples
│   │   ├── Run_8_Samples
│   │   ├── Run_9_Samples
│   │   └── Subject_5_different_tool
│   ├── No Pretraining vs. Pretraining
│   │   ├── Human trained + no pretraining (Seed: 42).csv
│   │   ├── Human trained + no pretraining (Seed: 43).csv
│   │   ├── Human trained + no pretraining (Seed: 44).csv
│   │   ├── Human trained + no pretraining (Seed: 45).csv
│   │   ├── Human trained + no pretraining (Seed: 46).csv
│   │   ├── Human trained + Yaskawa pretraining (Seed: 42).csv
│   │   ├── Human trained + Yaskawa pretraining (Seed: 43).csv
│   │   ├── Human trained + Yaskawa pretraining (Seed: 44).csv
│   │   ├── Human trained + Yaskawa pretraining (Seed: 45).csv
│   │   └── Human trained + Yaskawa pretraining (Seed: 46).csv
|   └── Yaskawa
│       ├── Arduino_Yaskawa
│       ├── Processed Data
│       └── Raspberry_Yaskawa
```

## Raw data

The raw data consists of the following nine sensor readings from the accelerometer, gyroscope, magnetometer, current (I) sensor, and microphone RESPECTIVELY:

| acc_x | acc_y | acc_z | w_x | w_y | w_z | b_x | b_y | b_z | I_sens | S_rms |
|:-----:|:-----:|-------|-----|-----|-----|-----|-----|-----|--------|-------|

### Human

The raw data is separated into 4 folders under each subject folder representing the four activities we predict. The files under human subjects are named `Subject_X_<task><10-digit-timestamp>`. Here, the \<task> represents the task: 

1. E = Engrave
2. C = Cut
3. S = Sand
4. R = Route

### Yaskawa 

The Yaskawa robot had both an arduino and a raspberry pi connected to it for redundancy in data collection. Therefore, 2 folders `Arduino_Yaskawa` and `Raspberry_Yaskawa` are present. The files in each folder are named: `A_<task>_Main_Data_<run_number>`. As in the human data case, \<task> can be one of the four activities: "Engrave", "Cut", "Sand", or "Route".

## Processed data

The processing of data took place in three steps:
1. Smoothening: 
   - A simple rolling window operation was performed to remove the noise in the data's variance. Refer to [panda's dataframe rolling](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html) API. 
2. Cleaning:
   - We then manually cleaned the data by truncating each sensor's range of values (set y-limit)
3. Pre-processing / feature extraction:
   - We finally calculate ten statistics for each of the 11 sensors: [min](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.min.html), [max](https://pandas.pydata.org/docs/reference/api/pandas.Series.max.html), [mean](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.mean.html), [kurtosis](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.kurtosis.html), [sem](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sem.html), [standard deviation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.std.html), [variance](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.var.html), [skew](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.skew.html), [mad](https://www.wikiwand.com/en/Average_absolute_deviation), [sum](https://pandas.pydata.org/docs/reference/api/pandas.Series.sum.html). 
   - This results in `11 sensors` $\times$ `10 statistics` = `110` columns of data, as seen in the processed data files. 


In the drive folders `Human` and `Yaskawa`, there are `Processed Data` folders consisting of `.parquet` files of this processed data:

 1. `data/Human/Processed Data/F2021_Human_Smoothened_Cleaned_Processed.parquet`
 2. `data/Robot/Processed Data/S2023_Yaskawa_Smoothened_Cleaned_Processed.parquet`


> **Note:** The files are stored in `.parquet` for memory efficiency over `.csv`. For details on why, read [this](https://www.databricks.com/glossary/what-is-parquet) blog post!
