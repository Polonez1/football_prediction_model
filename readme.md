# Football matches prediction

We use Machine learning and historical data to predict EPL football matches

# Project structure

- **data/downloaded_data**: Data Folder
  - `EPL_22_23.xlsx`: Hisrorical EPL data for 2020-2023 season
  - `epl_to_prediction.xlsx`: fixtures data with stats
  - `matches.xlsx`: ELO data to test model which based on ELO stats

- **data_processing/**: The folder where the data processing module is located

- **deployment/**: Folder containing app deployment scripts

- **machine_learning/**: Folder containing machine learning scripts

- **scraping**: Folder containing data scraping scripts from ELO

- **wsc_scraping/**: Folder containing whoscored.com scraping scripts

- **README.md**: information about project

- **requirements.txt**: pip install requirements

## Instalation
Download project to your local repository.
- open cmd or powershell in you folder
- enter this command in cmd or powershell
```git clone https://github.com/Polonez1/football_prediction_model```

install all requirements
```pip install -r requirements.txt```

- enable app in cmd or powershell
```python -m uvicorn main:app --reload```

- open new powershell or cmd window and change to project directody
```cd \project_directory\```

The app is running in one window and the project is running in the other, which will make requests to the app.

## Commands

Get all matches fixtures
```python run.py --get_fixtures```

Get one match prediction
```python run.py --predict --match "{match_name}"```

Get all incomming matches predictions
```python run.py --predict_all```

## Goals and conclusions

# Goals

- Based on statistics and historical data, make predictions: win, draw, away win using Machine Learning (random fores classifier)
- have a score of ~55%

# Conclusions

- The model shows well in some cases
- In some cases this produced a good result, while potentially most would have chosen the opposite result
- Data set too small
- Model can't cope with a draw
- Needs better data parsing

