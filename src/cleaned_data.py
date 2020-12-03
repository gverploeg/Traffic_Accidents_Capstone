import pandas as pd
import numpy as np

def merge_dataframes(df, df2):
    '''
    Two different datasets: 2009-2011 & 2012-2014

    ARGS:
        df - dataframe
        df2 - second dataframe to be added
    RETURN:
        New dataframe with prior two combined 
    '''
    joined_df = pd.concat([df, df2], axis=0)
    return joined_df

def display_row_nulls(df):
    '''
    Shows the rows with null values 
    
    ARGS: 
        df - dataframe
    RETURNS
        dataframe that has rows with null vals
    '''
    is_NaN = df.isnull()
    row_has_Nan = is_NaN.any(axis = 1)
    return df[row_has_Nan].head(15)

def drop_nulls_col(df, col):
    '''
    Drops null column with insignificant data

    ARGS: 
        df - dataframe
        col - column to be dropped
    RETURNS
        dataframe with removed null column
    '''
    return df.drop([col], axis=1, inplace= True)


def remove_null_rows(df, col):
    '''
    Takes the rows where the rows are not NAN

    ARGS: 
        df - dataframe
        col - column to be dropped
    RETURNS
        dataframe with removed null rows
    '''
    df = df[df[col].notna()]
    return df

def alter_target_feature(df, col):
    '''
    Creates Accident_Severity into Severe (1) or not (0)

    ARGS: 
        df - dataframe
        col - column to be dropped
    RETURNS
        dataframe with altered target  var
    '''
    return df[col].replace({2:1, 3:0}, inplace=True)

'''
Functions for Feature Engineering
'''

def new_col_slice(df, new_col, old_col, idx1, idx2):
    '''
    Creates new feature by slicing portion of old one

    ARGS: 
        df - dataframe
        new_col - column to be created
        old_col - column used 
        idx1 - index of slice
        idx2 - index of slice
    RETURNS
        dataframe with added features from slices as type int
    '''
    df[new_col] = df[old_col].str[idx1 : idx2]
    df[new_col] = df[new_col].astype(int)
    return df

def one_hot_encoding(df, categorical_feature):
    '''
    Converts categorical variables to numerical in an interpretable format
    ARGS: 
        df - dataframe
        categorical_feature 
    RETURNS
        dataframe with added features
    '''
    dummies = pd.get_dummies(df[[categorical_feature]])
    new_df = pd.concat([df, dummies], axis=1)
    return new_df


if __name__ == '__main__':

    # Read csv file into a pandas dataframe
    df1 = pd.read_csv('../data/accidents_2009_to_2011.csv')
    df2 = pd.read_csv('../data/accidents_2012_to_2014.csv')

    accident_df = merge_dataframes(df1, df2)
    drop_nulls_col(accident_df, 'Junction_Detail')
    accident_df = remove_null_rows(accident_df, 'Time')
    accident_df = remove_null_rows(accident_df, 'Weather_Conditions')
    accident_df = remove_null_rows(accident_df, 'Road_Surface_Conditions')
    alter_target_feature(accident_df, 'Accident_Severity')
    accident_df["Urban_or_Rural_Area"].replace({2:0}, inplace=True)

    # Create Hours_of_Day and Rush_Hour columns from the Accident Time & Months
    new_col_slice(accident_df, 'Months', 'Date', 3, 5)
    new_col_slice(accident_df, 'Hour_of_Day', 'Time', 0, 2)

    rush = []
    for row in accident_df['Hour_of_Day']:
        if row >= 0 and row <=6:        rush.append(0)
        elif row >= 7 and row <= 10:    rush.append(1)
        elif row > 10 and row <=15:     rush.append(0)
        elif row >15 and row <= 19:     rush.append(1)
        else:                           rush.append(0)
    accident_df['Rush Hour'] = rush

    # Create Weekday & Weekend Column
    weekend_or_not = []
    for row in accident_df['Day_of_Week']:
        if row == 1 or row ==7:     weekend_or_not.append(1)
        else:                       weekend_or_not.append(0)
    accident_df['Weekend'] =        weekend_or_not
        
    # One_Hot Features
    '''
    Dropped the original feature and dropped one of new data frames
    ''' 
    ac_df = one_hot_encoding(accident_df,'Road_Type')
    ac_df.drop(['Road_Type'],axis=1,inplace=True)
    ac_df.drop(['Road_Type_Single carriageway'],axis=1,inplace=True)

    ac_df = one_hot_encoding(ac_df,'Road_Surface_Conditions')
    ac_df.drop(['Road_Surface_Conditions'],axis=1,inplace=True)
    ac_df.drop(['Road_Surface_Conditions_Dry'],axis=1,inplace=True)

    ac_df = one_hot_encoding(ac_df,'Pedestrian_Crossing-Physical_Facilities')
    ac_df.drop(['Pedestrian_Crossing-Physical_Facilities'],axis=1,inplace=True)
    ac_df.drop(['Pedestrian_Crossing-Physical_Facilities_No physical crossing within 50 meters'],axis=1,inplace=True)

    ac_df = one_hot_encoding(ac_df,'Light_Conditions')
    ac_df.drop(['Light_Conditions'],axis=1,inplace=True)
    ac_df.drop(['Light_Conditions_Daylight: Street light present'],axis=1,inplace=True)

    ac_df = one_hot_encoding(ac_df,'Weather_Conditions')
    ac_df.drop(['Weather_Conditions'],axis=1,inplace=True)
    ac_df.drop(['Weather_Conditions_Fine without high winds'],axis=1,inplace=True)

    print(ac_df.groupby('Urban_or_Rural_Area').count()['Accident_Index'])

    # Save as CSV
    ac_df.to_csv('../data/cleaned_data.csv')

    # print(ac_df.head(5))

    # print(accident_df["Hour_of_Day"].head())
    # print(accident_df.head())

