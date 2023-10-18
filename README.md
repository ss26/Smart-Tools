# Smart-Tools

# Data

Raw data from accelerometer, gyroscope, magnetometer, current sensor and microphone are collected using an arduino. 

## Raw data from human subjects

Source: [Drive link](https://drive.google.com/drive/folders/1gMgDPZyN0-7_UrQwlaAjl749x5vUcy1g?usp=share_link). 

The raw data is separated into 4 folders under each subject folder representing the four activities we predict. The files under human subjects are named `Subject_X_<task><10-digit-timestamp>`. Here, the \<task> represents the task: 

1. E = Engrave
2. C = Cut
3. S = Sand
4. R = Route

## Raw data from Yaskawa Robot

Source: [Drive Link](https://drive.google.com/drive/folders/1zDdbZgHg_TPNEmvVnSW1UaLOGJWqyEIY?usp=share_link). 

The Yaskawa robot had both an arduino and a raspberry pi connected to it for redundancy in data collection. Therefore, 2 folders `Arduino_Yaskawa` and `Raspberry_Yaskawa` are present. The files in each folder are named: `A_<task>_Main_Data_<run_number>`. As in the human data case, \<task> can be one of the four activities: "Engrave", "Cut", "Sand", or "Route". 

## Processed data

Once the data is collected and stored into separate `.csv` files, it is cleaned and processed. In both the drive folders, `Human` and `Yaskawa`, there is a `Processed Data` folder consisting of one parquet file that contains this processed data. Note that the files are stored in `.parquet` for memory efficiency over `.csv`. 

# TODO

- [X] Add data links
- [X] Rename Tree - Level 1 folders (anonymize subjects)
- [ ] Rename Tree - Level 2 folders (anonymize subjects)
- [ ] Add scripts to run each plot
- [ ] Write meaning of each column in the data in README
- [ ] Add comments in the code

 
