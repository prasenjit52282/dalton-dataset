# DALTON-Dataset
We present spatiotemporal measurements of air quality from 30 indoor sites over six months during summer and winter seasons. The sites are geographically located across four regions of type: rural, suburban, and urban, covering the typical low to middle-income population in India. The dataset contains various types of indoor environments (e.g., studio apartments, classrooms, research laboratories, food canteens, and residential households), and can provide the basis for data-driven learning model research aimed at coping with unique pollution patterns in developing countries.

<p align="center">
      <img src="./Assets/system_diagram.png" width="90%"/><br><strong>Fig.1:</strong> Overview of our extensive field study and data collection with multiple air quality monitors in a typical indoor environment.
</p>
In the dataset we have given comprehensive metadata for all the sensors and their placemant. The collected attributes from each sensor is as shown below.

| `Parameters` | `Description`                                                                                |
|------------|--------------------------------------------------------------------------------------------|
| ts         | Timestamp (yyyy/mm/dd HH:MM:SS) from the ESP32 MCU after reading sensor values             |
| T          | Temperature reading of the indoor environment in celsius at time ts                        |
| H          | Humidity reading of the indoor environment in percentage at time ts                        |
| PMS1       | Less than 1 micron dust particle readings in parts per million (ppm) at time ts            |
| PMS2_5     | Less than 2.5 micron dust particle readings in ppm at time ts                              |
| PMS10      | Less than 10 micron dust particle readings in ppm at time ts                               |
| CO2        | Carbon dioxide concentration in ppm at time ts                                             |
| NO2        | Nitrogen dioxide concentration in ppm at time ts                                           |
| CO         | Carbon monoxide concentration in ppm at time ts                                            |
| VoC        | Volatile organic compounds concentration in parts per billion (ppb) at time ts             |
| C2H5OH     | Ethyl alcohol concentration in ppb at time ts                                              |
| ID         | Unique identifier of the deployed \ourmethod{} sensor                                      |
| Loc        | Location of DALTON sensor in the indoor environment                                        |
| Customer   | The name of the occupant who participated during the sensor deployment in his indoor space |
| Ph         | Phone number of the customer for urgent contact. Replaced with XXXX to preserve privacy    |

# Installation
To install the required packages in your python(>=3.11) environment you need to run the below commands:
```bash
git clone https://github.com/prasenjit52282/dalton-dataset.git
cd dalton-dataset
pip install -r requirements.txt
```

# Data Preprocessing
Execute the following commands to preprocess the air quality measurements from RAW csv files to the organised and cleaned dataset:

* Merge Replicas for a Measurement Site 
    > ```python merge_replicas.py --customer NAME```
* Clean and Preprocess for a Measurement Site 
    > ```python preprocess_data.py --customer NAME --workers #cpus```
* Mark BreakPoints in the Data for a Measurement Site
    > ```python mark_breakpoints.py --customer NAME --workers #cpus  [--plot]```
* Compute Satistical Features from the Cleaned Dataset
    > ```python compute_feat.py --customer NAME --workers #cpus```


# File Structure
```
.
├── ./Assets
│   └── ./Assets/system_diagram.png
├── ./Data
│   ├── ./Data/A1
│   │   └── ./Data/A1/101_Study_Desk.csv
│   ├── ./Data/H1
│   │   ├── ./Data/H1/41_Kitchen.csv
│   │   ├── ./Data/H1/42_Bedroom_beside.csv
│   │   ├── ./Data/H1/43_Dining_left.csv
│   │   ├── ./Data/H1/44_Dining_right.csv
│   │   └── ./Data/H1/45_Parent_room.csv
│   └── ./Data/[Site]                      /* Directories
│       └── ./Data/[Site]/[ID_Loc].csv
├── ./Merged
│   ├── ./Merged/data_A1.csv
│   └── ./Merged/data_[Site].csv           /* Files
├── ./Processed
│   ├── ./Processed/A1
│   │   ├── ./Processed/A1/2023_06_10
│   │   │   └── ./Processed/A1/2023_06_10/101_Study_Desk.csv
│   │   ├── ./Processed/A1/2023_06_11
│   │   │   └── ./Processed/A1/2023_06_11/101_Study_Desk.csv
│   │   ├── ./Processed/A1/2023_06_12
│   │   │   └── ./Processed/A1/2023_06_12/101_Study_Desk.csv
│   │   ├── ./Processed/A1/2023_06_13
│   │   │   └── ./Processed/A1/2023_06_13/101_Study_Desk.csv
│   │   ├── ./Processed/A1/2023_06_14
│   │   │   └── ./Processed/A1/2023_06_14/101_Study_Desk.csv
│   │   └── ./Processed/A1/2023_06_16
│   │       └── ./Processed/A1/2023_06_16/101_Study_Desk.csv
│   └── ./Processed/[Site]                 /* Directories
│       └── ./Processed/[Site]/[Date]
│           └── ./Processed/[Site]/[Date]/[ID_Loc].csv
├── ./library
│   ├── ./library/base_metrics.py
│   ├── ./library/breakpoints.py
│   ├── ./library/constants.py
│   ├── ./library/feat.py
│   ├── ./library/__init__.py
│   └── ./library/preprocess.py
├── ./merge_replicas.py
├── ./preprocess_data.py
├── ./mark_breakpoints.py
├── ./compute_feat.py
├── ./file_structure.txt
├── ./merge.sh
├── ./preprocess.sh
├── ./breakpoint.sh
├── ./features.sh
├── ./Makefile
├── ./LICENSE
├── ./README.md
└── ./requirements.txt

564 directories, 1454 files
```

# Reference
To refer the DALTON-dataset, please cite the following work.

BibTex Reference:
```
@article{karmakar2024communities,
  title={Indoor Air Quality Dataset with Activities of Daily Living in Low to Middle-income Communities},
  author={Karmakar, Prasenjit and Pradhan, Swadhin and Chakraborty, Sandip},
  year={2024}
}
```
For questions and general feedback, contact [Prasenjit Karmakar](https://prasenjit52282.github.io/).