#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pandorable problem set 3 for PSY 1210 - Fall 2019

@author: katherineduncan

In this problem set, you'll practice your new pandas data management skills, 
continuing to work with the 2018 IAT data used in class

Note that this is a group assignment. Please work in groups of ~4. You can divvy
up the questions between you, or better yet, work together on the questions to 
overcome potential hurdles 
"""

### This assignment is completed by An Qi Zhang, Rebekah Reuben, Laura Gravelsins, 
### and Xiao Min Chang.
#%% import packages 
import os
import numpy as np
import pandas as pd

#%%
# Question 1: reading and cleaning

# read in the included IAT_2018.csv file
Data_file = r'\Users\XiaoMin\Documents\GitHub\Lec3_Files\IAT_2018.csv'
IAT = pd.read_csv(Data_file)
# rename and reorder the variables to the following (original name->new name):
# session_id->id
# genderidentity->gender
# raceomb_002->race
# edu->edu
# politicalid_7->politic
# STATE -> state
# att_7->attitude 
# tblacks_0to10-> tblack
# twhites_0to10-> twhite
# labels->labels
# D_biep.White_Good_all->D_white_bias
# Mn_RT_all_3467->rt

IAT = IAT.rename(columns={'session_id': 'id',
                          'genderidentity': 'gender',
                          'raceomb_002':'race',
                          'edu':'edu',
                          'politicalid_7':'politic',
                          'STATE':'state',
                          'att_7':'attitude',
                          'tblacks_0to10':'tblack',
                          'twhites_0to10':'twhite',
                          'labels':'labels',
                          'D_biep.White_Good_all':'D_white_bias',
                          'Mn_RT_all_3467':'rt'
                          })
print(IAT)

# remove all participants that have at least one missing value
IAT_clean = IAT.dropna(axis=0,how='any')
IAT_clean.isnull().mean()

# check out the replace method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
# use this to recode gender so that 1=men and 2=women (instead of '[1]' and '[2]')
IAT_clean = IAT_clean.replace({'gender':{'[1]': 1, '[2]': 2}})
print(IAT_clean)

# use this cleaned dataframe to answer the following questions

#%%
# Question 2: sorting and indexing

# use sorting and indexing to print out the following information:

# the ids of the 5 participants with the fastest reaction times
IAT_clean = IAT_clean.sort_values(by='rt')
IAT_clean.head()

# the ids of the 5 men with the strongest white-good bias
IAT_clean = IAT_clean.sort_values(['gender', 'D_white_bias'], ascending = [True, False])
IAT_clean.head()

# the ids of the 5 women in new york with the strongest white-good bias
IAT_clean_NY_WOMEN = IAT_clean[(IAT_clean.state == 'NY') & (IAT_clean.gender == 2)]
IAT_clean_NY_WOMEN.sort_values(['D_white_bias'], ascending = [False])
IAT_clean_NY_WOMEN.head()



#%%
# Question 3: loops and pivots

# check out the unique method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.unique.html
# use it to get a list of states

states = pd.Series(pd.Categorical(IAT_clean.state)).unique()
print(states)

# write a loop that iterates over states to calculate the median white-good
# bias per state
# store the results in a dataframe with 2 columns: state & bias

state_bias_df = pd.DataFrame(columns=['state', 'bias'])
for state in states:
    median = IAT_clean[IAT_clean.state == state].D_white_bias.median()
    state_bias_df = state_bias_df.append({'state': state, 
                                    'bias': median}, ignore_index=True)
state_bias_df = state_bias_df.sort_values(by=['state'])
    


# now use the pivot_table function to calculate the same statistics
state_bias = pd.pivot_table(IAT_clean, values = 'D_white_bias',
                          index = ['state'],
                          aggfunc = np.median
                          )

# make another pivot_table that calculates median bias per state, separately 
# for each race (organized by columns)
state_race_bias= pd.pivot_table(IAT_clean, values = 'D_white_bias',
                                index = ['state'],
                                columns = ['race'],
                                aggfunc = np.median)

#%%
# Question 4: merging and more merging

# add a new variable that codes for whether or not a participant identifies as 
# black/African American
IAT_clean['is_black'] = 1*(IAT_clean.race==5)

# use your new variable along with the crosstab function to calculate the 
# proportion of each state's population that is black 
# *hint check out the normalization options
prop_black = (pd.crosstab(IAT_clean.state, IAT_clean.is_black, normalize='index'))

# state_pop.xlsx contains census data from 2000 taken from http://www.censusscope.org/us/rank_race_blackafricanamerican.html
# the last column contains the proportion of residents who identify as 
# black/African American 
# read in this file and merge its contents with your prop_black table
census =...
merged =...

# use the corr method to correlate the census proportions to the sample proportions

# now merge the census data with your state_race_bias pivot table

# use the corr method again to determine whether white_good biases is correlated 
# with the proportion of the population which is black across states
# calculate and print this correlation for white and black participants