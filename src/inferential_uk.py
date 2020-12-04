import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from statsmodels.tools import add_constant
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor 

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler

def balance_data(df1, df2):
    '''
    Large imbalance between Severe and Minor Accidents - severe accidents only account for 17% of total data
    '''
    sev_0_samp = df1.sample(n=len(df2))
    new_df = pd.concat([df2, sev_0_samp], axis=0)
    return new_df

def vif(specif_cols):
    '''
    Calculating VIF for each feature 
    '''
    vif_data = pd.DataFrame() 
    vif_data["Feature"] = specif_cols.columns

    vif_data["VIF"] = [variance_inflation_factor(specif_cols.values, i) 
                          for i in range(len(specif_cols.columns))]
    return vif_data

def standardize(col, feature_df):
    '''
    Create new df that is standardized
    '''
    scaler = StandardScaler()
    col_to_stan = feature_df[col].to_frame()
    col_to_stan = scaler.fit_transform(col_to_stan)

    stand_df = feature_df.copy()
    stand_df.drop(col, axis=1, inplace=True)
    stand_df[col] = col_to_stan

    return stand_df

def logit_mod(features, df):
    '''
    make logit model of features
    '''
    X = features.values
    y = df['Accident_Severity'].values
    logit_model = Logit(y, X).fit()
    return logit_model.summary2()


if __name__ == '__main__':
    # Read cleaned csv file into a pandas dataframe
    acc_df = pd.read_csv('../data/cleaned_data.csv')

    # Severe/ Non Severe Ratios with regards to feature
    not_severe = acc_df[(acc_df['Accident_Severity'] == 0)]
    is_severe = acc_df[(acc_df['Accident_Severity'] == 1)]

    # Balance the Data
    accident_df = balance_data(not_severe, is_severe)

    # Determine your Features
    imp_features= accident_df[['Weekend','Urban_or_Rural_Area', 'Rush Hour', 'Speed_limit' ,
       'Road_Type_Dual carriageway', 'Road_Type_One way street',
       'Road_Type_Roundabout', 'Road_Type_Slip road', 'Road_Type_Unknown',
       'Road_Surface_Conditions_Flood (Over 3cm of water)',
       'Road_Surface_Conditions_Frost/Ice', 'Road_Surface_Conditions_Snow',
       'Road_Surface_Conditions_Wet/Damp',
       'Pedestrian_Crossing-Physical_Facilities_Central refuge',
       'Pedestrian_Crossing-Physical_Facilities_Footbridge or subway',
       'Pedestrian_Crossing-Physical_Facilities_Pedestrian phase at traffic signal junction',
       'Pedestrian_Crossing-Physical_Facilities_Zebra crossing',
       'Pedestrian_Crossing-Physical_Facilities_non-junction pedestrian crossing',
       'Light_Conditions_Darkeness: No street lighting',
       'Light_Conditions_Darkness: Street lighting unknown',
       'Light_Conditions_Darkness: Street lights present and lit',
       'Light_Conditions_Darkness: Street lights present but unlit',
       'Weather_Conditions_Fine with high winds',
       'Weather_Conditions_Fog or mist', 'Weather_Conditions_Other',
       'Weather_Conditions_Raining with high winds',
       'Weather_Conditions_Raining without high winds',
       'Weather_Conditions_Snowing with high winds',
       'Weather_Conditions_Snowing without high winds',
       'Weather_Conditions_Unknown']]

    # Standardize - in this case Speed_limit
    new_features_stand = standardize('Speed_limit', imp_features)

    # Test
    # print(logit_mod(new_features_stand, accident_df))