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

# Calculate the death rate
fl_death_pop['Death Rate (%)'] = 100 * fl_death_pop['Deaths'] / fl_death_pop['POPULATION']

# missing values
fl_death_pop.isna().sum()
## We only have missing values for deaths

## Use KNN to impute the missing values
from sklearn.impute import KNNImputer

imputed_fl_death_pop = pd.DataFrame(columns=['YEAR', 'Death Rate (%)', 'POPULATION', 'STNAME'])
impute_df = fl_death_pop.loc[:, ['YEAR', 'STNAME', 'Death Rate (%)', 'POPULATION']]

for state in fl_death_pop['STNAME'].unique():
    X = impute_df.loc[impute_df['STNAME'] == state, ['YEAR', 'Death Rate (%)', 'POPULATION']]
    imputer = KNNImputer(n_neighbors=3)
    imputer.fit(X)
    X_imputed = imputer.transform(X)
    X_imputed = pd.DataFrame(X_imputed, columns=['YEAR', 'Death Rate (%)', 'POPULATION'])
    X_imputed['STNAME'] = state
    imputed_fl_death_pop = pd.concat([imputed_fl_death_pop, X_imputed])

imputed_fl_death_pop = imputed_fl_death_pop.reset_index(drop=True)
imputed_fl_death_pop = pd.concat([imputed_fl_death_pop, fl_death_pop.loc[:, ['CTYNAME']]], axis=1)

# check if the number of rows is correct
assert imputed_fl_death_pop.shape[0] == fl_death_pop.shape[0]
# check whether there is any missing value
assert imputed_fl_death_pop.isna().sum().sum() == 0

# Add indicator for treatment and control group
fl_death_pop['Indicator'] = fl_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Florida' else "Control")



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

# Calculate the death rate
tx_death_pop['Death Rate (%)'] = 100 * tx_death_pop['Deaths'] / tx_death_pop['POPULATION']


# Add indicator for treatment and control group
tx_death_pop['Indicator'] = tx_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Texas' else "Control")

# missing values
tx_death_pop.isna().sum()
## We only have missing values for deaths

## Use KNN to impute the missing values
imputed_tx_death_pop = pd.DataFrame(columns=['YEAR', 'Death Rate (%)', 'POPULATION', 'STNAME'])
impute_df = tx_death_pop.loc[:, ['YEAR', 'STNAME', 'Death Rate (%)', 'POPULATION']]

for state in tx_death_pop['STNAME'].unique():
    X = impute_df.loc[impute_df['STNAME'] == state, ['YEAR', 'Death Rate (%)', 'POPULATION']]
    imputer = KNNImputer(n_neighbors=3)
    imputer.fit(X)
    X_imputed = imputer.transform(X)
    X_imputed = pd.DataFrame(X_imputed, columns=['YEAR', 'Death Rate (%)', 'POPULATION'])
    X_imputed['STNAME'] = state
    imputed_tx_death_pop = pd.concat([imputed_tx_death_pop, X_imputed])

imputed_tx_death_pop = imputed_tx_death_pop.reset_index(drop=True)
imputed_tx_death_pop = pd.concat([imputed_tx_death_pop, tx_death_pop.loc[:, ['CTYNAME']]], axis=1)

# check if the number of rows is correct
assert imputed_tx_death_pop.shape[0] == tx_death_pop.shape[0]
# check whether there is any missing value
assert imputed_tx_death_pop.isna().sum().sum() == 0

# Add indicator for treatment and control group
imputed_tx_death_pop['Indicator'] = imputed_tx_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Texas' else "Control")



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

# Calculate the death rate
wa_death_pop['Death Rate (%)'] = 100 * wa_death_pop['Deaths'] / wa_death_pop['POPULATION']

# missing values
wa_death_pop.isna().sum()

## We only have missing values for deaths

## Use KNN to impute the missing values
imputed_wa_death_pop = pd.DataFrame(columns=['YEAR', 'Death Rate (%)', 'POPULATION', 'STNAME'])
impute_df = wa_death_pop.loc[:, ['YEAR', 'STNAME', 'Death Rate (%)', 'POPULATION']]

for state in wa_death_pop['STNAME'].unique():
    X = impute_df.loc[impute_df['STNAME'] == state, ['YEAR', 'Death Rate (%)', 'POPULATION']]
    imputer = KNNImputer(n_neighbors=3)
    imputer.fit(X)
    X_imputed = imputer.transform(X)
    X_imputed = pd.DataFrame(X_imputed, columns=['YEAR', 'Death Rate (%)', 'POPULATION'])
    X_imputed['STNAME'] = state
    imputed_wa_death_pop = pd.concat([imputed_wa_death_pop, X_imputed])

imputed_wa_death_pop = imputed_wa_death_pop.reset_index(drop=True)
imputed_wa_death_pop = pd.concat([imputed_wa_death_pop, wa_death_pop.loc[:, ['CTYNAME']]], axis=1)

# check if the number of rows is correct
assert imputed_wa_death_pop.shape[0] == wa_death_pop.shape[0]
# check whether there is any missing value
assert imputed_wa_death_pop.isna().sum().sum() == 0

# Add indicator for treatment and control group
wa_death_pop['Indicator'] = wa_death_pop['STNAME'].apply(lambda x: "Treatment" if x == 'Washington' else "Control")
