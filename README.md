# Smart-Tools

This is the code repository of our paper titled "Using human and robot synthetic data for training smart hand tools", in press at ICRA 2024. 


# Table of Contents

- [Smart-Tools](#smart-tools)
- [Table of Contents](#table-of-contents)
- [TLDR](#tldr)
- [Usage](#usage)
  - [1. Packages](#1-packages)
  - [2. Data](#2-data)
  - [3. Code](#3-code)


# TLDR

We introduce a data collection and training pipeline for everyday mechanical engineering tasks (cutting, sanding, routing, engraving) performed by hand tools. The paper discusses data trends and establishes a roadmap for model deployment on edge devices.

# Usage

## 1. Packages
Install Poetry if you don't have it already:

  ```
  pipx install poetry
  ```

## 2. Data

Refer [data_README.md](data_README.md).

## 3. Code

1. Clone the repository and change directory, 
  ```
  git clone git@github.com:UTAustin-SwarmLab/Smart-Tools.git
  ```

2. Install dependencies using Poetry: 
  ```
  poetry install
  ```

3. Make sure you choose the virtual environment created by Poetry as the Python interpreter for running the project's code!



 
