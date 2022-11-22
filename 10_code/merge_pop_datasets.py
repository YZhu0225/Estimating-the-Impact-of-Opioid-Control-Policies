def merge_pop_datasets(early_pop_link, later_pop_link, state_abbrev):
    '''
    This function will merge the two population datasets together.
    Input: early_link, later_link, state
        early_pop_link: the dropbox link to the 2000-2009 population dataset
        later_pop_link: the dropbox link to the 2010-2019 population dataset
        state_abbrev: the state abbreviation
    return: a pandas dataframe with the merged population data
    '''

    import pandas as pd
    import numpy as np

    # read in the data
    pop_2000_2009 = pd.read_csv(early_pop_link, header=3)
    pop_2010_2019 = pd.read_csv(later_pop_link, header=3)

    # manipulating 2000-2009 dataset
    pop_2000_2009_ = pop_2000_2009.iloc[1:40, :12].drop(['Unnamed: 1'], axis = 1)
    pop_2000_2009_.rename(columns={'Unnamed: 0': 'COUNTY'}, inplace=True)

    # manipulating 2000-2009 dataset
    pop_2010_2019_ = pop_2010_2019.iloc[1:40, :].drop(['Census', 'Estimates Base'], axis = 1)
    pop_2010_2019_[['COUNTY', 'STATE']] = pop_2010_2019_['Unnamed: 0'].str.split(',', 1, expand=True)
    pop_2010_2019_.drop(['Unnamed: 0', 'STATE'], axis = 1, inplace = True)

    # merge two datasets
    assert pop_2000_2009_.shape[0] == pop_2010_2019_.shape[0]  # number of county should be the same
    pop_2000_2019 = pd.merge(pop_2000_2009_, pop_2010_2019_, how = 'outer', on = 'COUNTY')

    # convert columns to rows
    pop = pd.melt(pop_2000_2019, id_vars=['COUNTY'], var_name='YEAR', value_name='POPULATION')
    assert pop.shape[0] == pop_2000_2019.shape[0] * (pop_2000_2019.shape[1]-1)  # number of rows should be the same
    assert pop['YEAR'].nunique() == (pop_2000_2019.shape[1]-1)  # number of years should be the same
    
    # remove the dot in the county name
    pop['COUNTY'] = pop['COUNTY'].str.replace('.', '').str.strip()

    # Add a column for state
    pop['STATE'] = state_abbrev

    return pop