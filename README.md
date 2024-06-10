# DALTON-Dataset
We present spatiotemporal measurements of air quality from 30 indoor sites over six months during summer and winter seasons (**89.1M samples, totalling 13646 hours of air quality data from all sites**). The sites are geographically located across four regions of type: rural, suburban, and urban, covering the typical low to middle-income population in India. The dataset contains various types of indoor environments (e.g., studio apartments, classrooms, research laboratories, food canteens, and residential households). Fig. 1 shows the overview of the data collection setup in a typical indoor environment. Our dataset provides the basis for data-driven learning model research aimed at coping with unique pollution patterns in developing countries.

<p align="center">
      <img src="./Assets/system_diagram.png" width="90%"/><br><strong>Fig.1:</strong> Overview of the field study and data collection with multiple air quality monitors in a typical indoor setup.
</p>

# Installation
To install the required packages in your python(>=3.11) environment you need to run the below commands:
```bash
git clone https://github.com/prasenjit52282/dalton-dataset.git
sudo apt-get update
sudo apt-get install make
cd dalton-dataset
pip install -r requirements.txt
```

# Attributes
We have given comprehensive metadata for all the sensors and their placemant in [Metadata](https://github.com/prasenjit52282/dalton-dataset/tree/main/Metadata) folder. The collected air quality and other necessary attributes from each sensor is as shown below.

| Parameters | Description                                                                                |
|------------|--------------------------------------------------------------------------------------------|
| <tt>ts</tt>         | Timestamp `yyyy/mm/dd HH:MM:SS` from the ESP32 MCU after reading sensor values             |
| <tt>T</tt>          | Temperature reading of the indoor environment in celsius at time ts                        |
| <tt>H</tt>          | Humidity reading of the indoor environment in percentage at time ts                        |
| <tt>PMS1</tt>       | Less than 1 micron dust particle readings in parts per million (ppm) at time ts            |
| <tt>PMS2_5</tt>     | Less than 2.5 micron dust particle readings in ppm at time ts                              |
| <tt>PMS10</tt>      | Less than 10 micron dust particle readings in ppm at time ts                               |
| <tt>CO2</tt>        | Carbon dioxide concentration in ppm at time ts                                             |
| <tt>NO2</tt>        | Nitrogen dioxide concentration in ppm at time ts                                           |
| <tt>CO</tt>         | Carbon monoxide concentration in ppm at time ts                                            |
| <tt>VoC</tt>        | Volatile organic compounds concentration in parts per billion (ppb) at time ts             |
| <tt>C2H5OH</tt>     | Ethyl alcohol concentration in ppb at time ts                                              |
| <tt>ID</tt>         | Unique identifier of the deployed sensor                                      |
| <tt>Loc</tt>        | Location of DALTON sensor in the indoor environment                                        |
| <tt>Customer</tt>   | Participant name of the measurement site. Replace with `SiteID` to preserve privacy (`H1` - `H13`,`A1` - `A8`,`R1` - `R5`,`F1` - `F2`,`C1` - `C2`,) |
| <tt>Ph</tt>         | Phone number of the customer for urgent contact. Replaced with `XXXX` to preserve privacy    |

The activity and event annotations are stored in the `Annotations.csv` file in [Metadata](https://github.com/prasenjit52282/dalton-dataset/tree/main/Metadata) folder. As annotation may come from different occupants from the same site, we have given unique identifier to each participant (`P1` - `P46`). Each annotation is comprised of the following values.

| Parameters | Description                                                                                |
|------------|--------------------------------------------------------------------------------------------|
| <tt>ts</tt>         | Starting timestamp `yyyy/mm/dd HH:MM:SS` of the indoor event or activity             |
| <tt>Label</tt>          | Activity or event label with detailed description (if possible) |
| <tt>Site</tt>          | `SiteID` of the measurement site. Match with `Customer` in the sensor attributed table  |
| <tt>Customer</tt>       | Unique participant identifier (`P1` - `P46`) |

The annotations can be associated with the sensor readings of any site to analyse the impact of indoor events and activities on the air pollution dynamics.

# Dataset Preparation

## Python scripts
Execute the following commands to preprocess the air quality measurements from RAW csv files to the organised and cleaned dataset:

* Merge Replicas for a Measurement Site 
    > ```python merge_replicas.py --customer {SiteID}```
* Clean and Preprocess for a Measurement Site 
    > ```python preprocess_data.py --customer {SiteID} --workers #cpus```
* Mark BreakPoints in the Data for a Measurement Site
    > ```python mark_breakpoints.py --customer {SiteID} --workers #cpus  [--plot]```
* Compute Satistical Features from the Cleaned Dataset
    > ```python compute_feat.py --customer {SiteID} --workers #cpus```

For convinence, we have provided the Makefile with the below commands to process the dataset from raw csvs (`./Data` folder) to processed csvs (`./Processed` folder). The repository contains all the processed files. However, the raw csvs can be downloaded and placed in the `./Data` folder from [Raw Dataset Files](https://iitkgpacin-my.sharepoint.com/:u:/g/personal/pkarmakar_kgpian_iitkgp_ac_in/EUJjN1c_gU9Jjh2Rj7ghDx8BZ0QWS42mP7gHXU80lHlmjg?e=nzshah) if needed.
```bash
make preprocess
```

## Preprocessing & Cleaning Steps

# File Structure
```
.
├── ./Assets
│   └── ./Assets/system_diagram.png
├── ./Data                                 /* Raw Dataset
│   ├── ./Data/A1
│   │   └── ./Data/A1/101_Study_Desk.csv
│   ├── ./Data/H1
│   │   ├── ./Data/H1/41_Kitchen.csv
│   │   ├── ./Data/H1/[ID_Loc].csv         /* Files
│   │   └── ./Data/H1/45_Parent_room.csv
│   └── ./Data/[Site]                      /* Directories
│       └── ./Data/[Site]/[ID_Loc].csv
├── ./Merged
│   ├── ./Merged/data_A1.csv
│   └── ./Merged/data_[Site].csv           /* Files
├── ./Processed                            /* Processed Dataset
│   ├── ./Processed/A1
│   │   ├── ./Processed/A1/2023_06_10
│   │   │   └── ./Processed/A1/2023_06_10/101_Study_Desk.csv
│   │   ├── ./Processed/A1/[Date]
│   │   │   └── ./Processed/A1/[Date]/[ID_Loc].csv  /* Files
│   │   └── ./Processed/A1/2023_06_16
│   │       └── ./Processed/A1/2023_06_16/101_Study_Desk.csv
│   └── ./Processed/[Site]                 /* Directories
│       └── ./Processed/[Site]/[Date]
│           └── ./Processed/[Site]/[Date]/[ID_Loc].csv
├── ./Features
│   ├── ./Features/A1
│   │   ├── ./Features/A1/2023_06_10_101_Study_Desk.csv
│   │   ├── ./Features/A1/[Date_ID_Loc].csv         /* Files
│   │   └── ./Features/A1/2023_06_16_101_Study_Desk.csv
│   └── ./Features/[Site]                  /* Directories
│       └── ./Features/A2/[Date_ID_Loc].csv
├── ./Metadata
│   ├── ./Metadata/An:x:tations.csv
│   ├── ./Metadata/Occupants.csv
│   └── ./Metadata/Site_wise_details.csv
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


# Dataset Details
|Site ID|#Dev|Site Area (sqft)|Floor Plan|#F/ #M|Duration (Hrs)|#Samples|Annot|Participants|
|-------|--------|----------------|----------|--------------|-------------------|--------|-----------|-------|
|H1     |5       |1100            |:heavy_check_mark:       |1/1           |772                |11402870|:heavy_check_mark:        |P1 P2                      |
|H2     |7       |1100            |:heavy_check_mark:       |2/2           |469                |8333689 |:heavy_check_mark:        |P3 P4 P5 P6                |
|H3     |3       |1000            |:heavy_check_mark:       |1/1           |463                |4041058 |:heavy_check_mark:        |P7 P8                      |
|H4     |5       |1200            |:heavy_check_mark:       |1/1           |2635               |24021924|:x:         |P9 P10                     |
|H5     |2       |1200            |:heavy_check_mark:       |1/1           |2634               |7395189 |:x:         |P11 P12                    |
|H6     |5       |400             |:heavy_check_mark:       |1/1           |218                |3188644 |:heavy_check_mark:        |P13 P14                    |
|H7     |2       |400             |:x:        |1/1           |366                |2306882 |:heavy_check_mark:        |P15 P16                    |
|H8     |5       |1100            |:x:        |2/1           |570                |8676832 |:heavy_check_mark:        |P1 P17 P18                 |
|H9     |2       |300             |:x:        |1/1           |768                |3894082 |:heavy_check_mark:        |P19 P20                    |
|H10    |2       |600             |:x:        |2/2           |25                 |70554   |:x:         |P21 P22 P23 P24            |
|H11    |2       |600             |:x:        |1/2           |86                 |60098   |:x:         |P25 P26 P27                |
|H12    |2       |216             |:x:        |1/1           |178                |1054696 |:heavy_check_mark:        |P19 P20                    |
|H13    |2       |216             |:x:        |1/1           |127                |269824  |:heavy_check_mark:        |P19 P20                    |
|A1     |1       |150             |:x:        |1/0           |146                |226888  |:heavy_check_mark:        |P28                        |
|A2     |1       |150             |:x:        |0/1           |289                |193557  |:x:         |P29                        |
|A3     |1       |180             |:x:        |0/1           |344                |1098827 |:heavy_check_mark:        |P30                        |
|A4     |1       |150             |:x:        |1/0           |125                |384975  |:x:         |P31                        |
|A5     |1       |150             |:x:        |1/0           |1                  |77      |:heavy_check_mark:        |P32                        |
|A6     |1       |100             |:x:        |0/1           |51                 |154398  |:heavy_check_mark:        |P33                        |
|A7     |1       |150             |:x:        |0/1           |55                 |54741   |:heavy_check_mark:        |P34                        |
|A8     |1       |150             |:x:        |0/1           |60                 |189141  |:x:         |P35                        |
|R1     |4       |522             |:heavy_check_mark:       |1/6           |834                |6203065 |:heavy_check_mark:        |P36 P37 P38 P39 P40 P41 P42|
|R2     |1       |320             |:heavy_check_mark:       |2/2           |367                |1161570 |:heavy_check_mark:        |P43                        |
|R3     |1       |616             |:heavy_check_mark:       |0/1           |243                |750745  |:heavy_check_mark:        |P44                        |
|R4     |4       |522             |:heavy_check_mark:       |:heavy_minus_sign:             |371                |387195  |:x:         |:heavy_minus_sign:                          |
|R5     |3       |600             |:heavy_check_mark:       |:heavy_minus_sign:             |179                |1583750 |:x:         |:heavy_minus_sign:                          |
|F1     |1       |150             |:heavy_check_mark:       |2/0           |450                |631193  |:x:         |P46                        |
|F2     |1       |150             |:heavy_check_mark:       |:heavy_minus_sign:             |450                |631193  |:x:         |:heavy_minus_sign:                          |
|C1     |1       |500             |:x:        |:heavy_minus_sign:             |333                |590272  |:x:         |:heavy_minus_sign:                          |
|C2     |1       |500             |:x:        |:heavy_minus_sign:             |53                 |158256  |:x:         |:heavy_minus_sign:                          |


# Reference
To refer the DALTON-dataset, please cite the following work.

BibTex Reference:
```
Coming Soon!
```
For questions and general feedback, contact [Prasenjit Karmakar](https://prasenjit52282.github.io/).

<!-- @article{karmakar2024communities,
  title={Indoor Air Quality Dataset with Activities of Daily Living in Low to Middle-income Communities},
  author={Karmakar, Prasenjit and Pradhan, Swadhin and Chakraborty, Sandip},
  year={2024}
} -->
