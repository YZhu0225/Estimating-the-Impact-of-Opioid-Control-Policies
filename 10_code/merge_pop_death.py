import numpy as np
import pandas as pd

### Death: Florida and its reference states
all_death = pd.read_csv('../20_intermediate_files/only_od_all_years.csv')
fl_pop = pd.read_csv('../20_intermediate_files/fl_death_pop.csv')

# select only florida and its reference states
fl_ref_states = ['LA', 'NV', 'CO', 'FL']
fl_death = all_death[all_death['STNAME'].isin(fl_ref_states)]

# rename the abbrevation state name to its full name
fl_death_ = fl_death.replace({'NV': 'Nevada', 'FL': 'Florida', 'LA': 'Louisiana', 'CO': 'Colorado'})

# make sure the state names are the same
assert (fl_death_['STNAME'].unique() == fl_pop['STNAME'].unique()).all()

# rename year
fl_death_ = fl_death_.rename(columns={'Year': 'YEAR'})

# remove useless columns: County, Year Code
fl_death_ = fl_death_.loc[:, [ 'YEAR', 'STNAME', 'CTYNAME','Deaths']]

# Collapsing the dataset to get total number of deaths per county per year
fl_agg_death = fl_death_.groupby(['YEAR', 'STNAME', 'CTYNAME'], as_index=False)['Deaths'].sum()

# merge the two dataframes
fl_death_pop = pd.merge(fl_pop, fl_agg_death, how='outer', on = ['STNAME', 'CTYNAME', 'YEAR'], indicator=True)

# make sure the number of rows is correct
assert fl_death_pop.shape[0] == fl_pop.shape[0]
assert fl_death_pop[fl_death_pop["_merge"] == 'both'].shape[0] == fl_agg_death.shape[0]

# remove the year where we don't have the opoid death data
min_year = fl_death_['YEAR'].min()
max_year = fl_death_['YEAR'].max()
fl_death_pop = fl_death_pop[(fl_death_pop['YEAR'] >= min_year) & (fl_death_pop['YEAR'] <= max_year)].reset_index(drop=True)

## We only have missing values for deaths

# use random number 1-10 to fill the missing values
fl_death_pop['Deaths'] = fl_death_pop['Deaths'].apply(lambda x: np.random.randint(0, 10) if np.isnan(x) else x)

# check whether there is any missing value
assert fl_death_pop.isna().sum().sum() == 0

# drop useless column
fl_death_pop = fl_death_pop.drop(columns=['_merge'])

# Calculate the death rate
fl_death_pop['Death Rate (%)'] = 100 * fl_death_pop['Deaths'] / fl_death_pop['POPULATION']

# Add indicator for treatment and control group
fl_death_pop['Indicator'] = fl_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Florida' else "Control")

# write to csv
fl_death_pop.to_csv('../20_intermediate_files/florida_death_cleaned.csv', index=False)



### Death: Texas and its reference states
tx_pop = pd.read_csv('../20_intermediate_files/tx_death_pop.csv')

# select only texas and its reference states
tx_ref_states = ['NY', 'OR', 'TX', 'WI']
tx_death = all_death[all_death['STNAME'].isin(tx_ref_states)]

# rename the abbrevation state name to its full name
tx_death_ = tx_death.replace({'NY': 'New York', 'OR': 'Oregon', 'TX': 'Texas', 'WI': 'Wisconsin'})

# make sure the state names are the same
assert (tx_death_['STNAME'].unique() == tx_pop['STNAME'].unique()).all()

# rename year
tx_death_ = tx_death_.rename(columns={'Year': 'YEAR'})

# remove useless columns: County, Year Code
tx_death_ = tx_death_.loc[:, [ 'YEAR', 'STNAME', 'CTYNAME','Deaths']]

# Collapsing the dataset to get total number of deaths per county per year
tx_agg_death = tx_death_.groupby(['YEAR', 'STNAME', 'CTYNAME'], as_index=False)['Deaths'].sum()

# merge the two dataframes
tx_death_pop = pd.merge(tx_pop, tx_agg_death, how='outer', on = ['STNAME', 'CTYNAME', 'YEAR'], indicator=True)

# make sure the number of rows is correct
assert tx_death_pop.shape[0] == tx_pop.shape[0]
assert tx_death_pop[tx_death_pop["_merge"] == 'both'].shape[0] == tx_agg_death.shape[0]

# remove the year where we don't have the opoid death data
min_year = tx_death_['YEAR'].min()
max_year = tx_death_['YEAR'].max()
tx_death_pop = tx_death_pop[(tx_death_pop['YEAR'] >= min_year) & (tx_death_pop['YEAR'] <= max_year)].reset_index(drop=True)

# use random number 1-10 to fill the missing values
tx_death_pop['Deaths'] = tx_death_pop['Deaths'].apply(lambda x: np.random.randint(0, 10) if np.isnan(x) else x)

# check whether there is any missing value
assert tx_death_pop.isna().sum().sum() == 0

# drop useless column
tx_death_pop = tx_death_pop.drop(columns=['_merge'])

# Calculate the death rate
tx_death_pop['Death Rate (%)'] = 100 * tx_death_pop['Deaths'] / tx_death_pop['POPULATION']

# Add indicator for treatment and control group
tx_death_pop['Indicator'] = tx_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Texas' else "Control")

# write to csv
tx_death_pop.to_csv('../20_intermediate_files/texas_death_cleaned.csv', index=False)



### Death: Washington and its reference states
wa_pop = pd.read_csv('../20_intermediate_files/wa_death_pop.csv')

# select only washington and its reference states
wa_ref_states = ['HI', 'OK', 'OR', 'WA']
wa_death = all_death[all_death['STNAME'].isin(wa_ref_states)]

# rename the abbrevation state name to its full name
wa_death_ = wa_death.replace({'HI': 'Hawaii', 'OK': 'Oklahoma', 'OR': 'Oregon', 'WA': 'Washington'})

# make sure the state names are the same
assert (wa_death_['STNAME'].unique() == wa_pop['STNAME'].unique()).all()

# rename year
wa_death_ = wa_death_.rename(columns={'Year': 'YEAR'})

# remove useless columns: County, Year Code
wa_death_ = wa_death_.loc[:, [ 'YEAR', 'STNAME', 'CTYNAME','Deaths']]

# Collapsing the dataset to get total number of deaths per county per year
wa_agg_death = wa_death_.groupby(['YEAR', 'STNAME', 'CTYNAME'], as_index=False)['Deaths'].sum()

# merge the two dataframes
wa_death_pop = pd.merge(wa_pop, wa_agg_death, how='outer', on = ['STNAME', 'CTYNAME', 'YEAR'], indicator=True)

# make sure the number of rows is correct
assert wa_death_pop.shape[0] == wa_pop.shape[0]
assert wa_death_pop[wa_death_pop["_merge"] == 'both'].shape[0] == wa_agg_death.shape[0]

# remove the year where we don't have the opoid death data
min_year = wa_death_['YEAR'].min()
max_year = wa_death_['YEAR'].max()
wa_death_pop = wa_death_pop[(wa_death_pop['YEAR'] >= min_year) & (wa_death_pop['YEAR'] <= max_year)].reset_index(drop=True)

# use random number 1-10 to fill the missing values
wa_death_pop['Deaths'] = wa_death_pop['Deaths'].apply(lambda x: np.random.randint(0, 10) if np.isnan(x) else x)

# check whether there is any missing value
assert wa_death_pop.isna().sum().sum() == 0

# drop useless column
wa_death_pop = wa_death_pop.drop(columns=['_merge'])

# Calculate the death rate
wa_death_pop['Death Rate (%)'] = 100 * wa_death_pop['Deaths'] / wa_death_pop['POPULATION']

# Add indicator for treatment and control group
wa_death_pop['Indicator'] = wa_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Washington' else "Control")

# write to csv
wa_death_pop.to_csv('../20_intermediate_files/washington_death_cleaned.csv', index=False)