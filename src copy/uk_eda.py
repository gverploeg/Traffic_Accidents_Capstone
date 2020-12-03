import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from cleaned_data import *

def geographic_plot(conditon, color, title, facecolor):
    ''' Create Latitude Longitude plot of specific features'''
    fig, ax = plt.subplots(1, figsize=(10,15))
    conditon.plot(kind='scatter', x='Longitude',y ='Latitude',
                color=color, 
                s=.1, alpha=.9, subplots=True, ax=ax)
    ax.set_title(title)
    ax.set_facecolor(facecolor)
    fig.tight_layout()

def groupby_func(df, group, agg_column, modifier = 'count'):
    '''
    Create different groupby dataframes with different aggregate functions
    '''
    if modifier == 'sum':
        return df.groupby(group)[agg_column].sum().reset_index()
    elif modifier == 'max':
        return df.groupby(group)[agg_column].max().reset_index()
    elif modifier == 'min':
        return df.groupby(group)[agg_column].min().reset_index()
    elif modifier == 'count':
        return df.groupby(group)[agg_column].count().reset_index()

def plots_with_severity_groups(df1, df2, title, save_loc):
    # save_loc
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(15, 6))
    bar_width = 0.8
    x1 = df1.iloc[:,0]
    x2 = df2.iloc[:,0]
    y1 = df1.iloc[:,1]
    y2 = df2.iloc[:,1]
    ax.bar(x1, y1, color='royalblue', width=bar_width, align='edge', label='Minor')
    ax.bar(x2, y2, color='tomato', width=-bar_width, align='edge', label='Severe')
    plt.xticks(rotation=45, fontsize=14, horizontalalignment='center')
    ax.set_ylabel("Ratio of Attacks", fontsize=15)
    ax.set_title(title, fontsize=18)
    fig.tight_layout()
    ax.legend()
    plt.savefig(save_loc, bbox_inches = 'tight')


if __name__ == '__main__':

    # Read csv file into a pandas dataframe
    acc_df = pd.read_csv('../data/cleaned_data.csv')

    # Map plot showing lat and long of speed limit of Severe Accidents
    # condition = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Speed_limit'] >= 60)]
    # geographic_plot(condition, 'yellow', 'Severity of High Speed Limits', 'Black')

    # condition2 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Speed_limit'] < 60)]
    # geographic_plot(condition2, 'yellow', 'Severity of Low Speed Limits', 'Black')

    condition3 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Urban_or_Rural_Area'] == 2)]
    geographic_plot(condition3, 'red', 'Severity of Rural Areas', 'Black')

    condition4 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Urban_or_Rural_Area'] == 1)]
    geographic_plot(condition4, 'red', 'Severity of Urban Areas', 'Black')

    # Plot Severe/ Non Severe Ratios with regards to feature
    not_severe = accident_df[(accident_df['Accident_Severity'] == 0)]
    is_severe = accident_df[(accident_df['Accident_Severity'] == 1)]

    
    plt.show()