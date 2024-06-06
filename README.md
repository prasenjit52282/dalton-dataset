# DALTON-Dataset

<p align="center">
      <img src="./Assets/system_diagram.png" width="90%"/><br><strong>Fig.1:</strong> Overview of our extensive field study and data collection with multiple air quality monitors in a typical indoor environment.
</p>

We present spatiotemporal measurements of air quality from 30 indoor sites over six months during summer and winter seasons. The sites are geographically located across four regions of type: rural, suburban, and urban, covering the typical low to middle-income population in India. The dataset contains various types of indoor environments (e.g., studio apartments, classrooms, research laboratories, food canteens, and residential households), and can provide the basis for data-driven learning model research aimed at coping with unique pollution patterns in developing countries.
<br/>

# Prerequisite
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
Assets
Data
    └── {file}.py
library
    └── __init__.py
    └── base_metrics.py
    └── breakpoints.py
    └── constants.py
    └── feat.py
    └── preprocess.py

merge_replicas.py
preprocess_data.py
mark_breakpoints.py
compute_feat.py
requirements.txt
.gitignore
LICENSE
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