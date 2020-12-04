import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from cleaned_data import *

def geographic_plot(conditon, color, title, facecolor, save_loc):
    ''' Create Latitude Longitude plot of specific features'''
    fig, ax = plt.subplots(1, figsize=(10,15))
    conditon.plot(kind='scatter', x='Longitude',y ='Latitude',
                color=color, 
                s=.1, alpha=.9, subplots=True, ax=ax)
    ax.set_title(title, fontsize=22)
    ax.set_facecolor(facecolor)
    ax.yaxis.label.set_size(20)
    ax.xaxis.label.set_size(20)
    plt.savefig(save_loc, dpi=150, bbox_inches = 'tight')

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

def plots_with_severity_groups(df1, df2, ylab, title, save_loc):
    # save_loc
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(15, 6))
    bar_width = 0.4
    x1 = df1.iloc[:,0]
    x2 = df2.iloc[:,0]
    y1 = df1.iloc[:,1]
    y2 = df2.iloc[:,1]
    ax.bar(x1, y1, color='royalblue', width=bar_width, align='edge', label='Minor')
    ax.bar(x2, y2, color='tomato', width=-bar_width, align='edge', label='Severe')
    plt.xticks(rotation=45, fontsize=20, horizontalalignment='center')
    ax.set_ylabel(ylab, fontsize=20)
    ax.set_title(title, fontsize=22)
    fig.tight_layout()
    ax.legend(fontsize= 14)
    plt.savefig(save_loc, dpi=150, bbox_inches = 'tight')

def plots_with_severity_groups_ratios(df1, df2, ylab, title, save_loc):
    # save_loc
    plt.style.use('ggplot')
    fig, ax = plt.subplots(1, figsize=(15, 6))
    bar_width = 0.4
    x1 = df1.iloc[:,0]
    x2 = df2.iloc[:,0]
    y1 = df1.iloc[:,1]
    y2 = df2.iloc[:,1]
    ax.bar(x1, (y1/(y1+y2)), color='royalblue', width=bar_width, align='edge', label='Minor')
    ax.bar(x2, (y2/(y1+y2)), color='tomato', width=-bar_width, align='edge', label='Severe')
    plt.xticks(rotation=45, fontsize=20, horizontalalignment='center')
    ax.set_ylabel(ylab, fontsize=20)
    ax.set_title(title, fontsize=22)
    fig.tight_layout()
    ax.legend()
    plt.savefig(save_loc, dpi=150, bbox_inches = 'tight')


if __name__ == '__main__':

    # Read csv file into a pandas dataframe
    acc_df = pd.read_csv('../data/cleaned_data.csv')

    # Map plot showing lat and long of speed limit of Severe Accidents
    condition = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Speed_limit'] >= 60)]
    # geographic_plot(condition, 'yellow', 'Severity of High Speed Limits', 'Black')

    condition2 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Speed_limit'] < 60)]
    # geographic_plot(condition2, 'yellow', 'Severity of Low Speed Limits', 'Black')

    condition3 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Urban_or_Rural_Area'] == 0)]
    geographic_plot(condition3, 'red', 'Severity of Rural Areas', 'Black', '../images/rural_map.png')

    condition4 = acc_df[(acc_df['Accident_Severity'] == 1) & (acc_df['Urban_or_Rural_Area'] == 1)]
    geographic_plot(condition4, 'red', 'Severity of Urban Areas', 'Black', '../images/urban_map.png')

    # Plot Severe/ Non Severe Ratios with regards to feature
    not_severe = acc_df[(acc_df['Accident_Severity'] == 0)]
    is_severe = acc_df[(acc_df['Accident_Severity'] == 1)]

    # Plot Time of Day Counts and Percentages
    tm_0 = not_severe.groupby(['Hour_of_Day'])['Accident_Index'].count().reset_index()
    tm_1 = is_severe.groupby(['Hour_of_Day'])['Accident_Index'].count().reset_index()

    plots_with_severity_groups(tm_0, tm_1, "Number of Accidents", 'Accidents By Hour', '../images/hour_count.png')
    plots_with_severity_groups_ratios(tm_0, tm_1, "Percent of Accidents", 'Percentage of Accidents By Hour', '../images/hour_pt.png')


    # Plot Time of Day Counts and Percentages



    
    plt.show()