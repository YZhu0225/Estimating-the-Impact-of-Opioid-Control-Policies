import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

csvdir = "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics"

dataframes = []
for csv in os.listdir(csvdir):
    fullpath = os.path.join(csvdir, csv)
    print(fullpath)
    if os.path.isfile(fullpath):
        # Read a csv into a dataframe and append to a list of dataframes
        dataframe = pd.read_table(fullpath)
        dataframes.append(dataframe)

# Concatenate all created dataframes into one
df = pd.concat(dataframes)

# read all original txt files
txt1 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2003.txt"
)
txt2 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2004.txt"
)
txt3 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2005.txt"
)
txt4 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2006.txt"
)
txt5 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2007.txt"
)
txt6 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2008.txt"
)
txt7 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2009.txt"
)
txt8 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2010.txt"
)
txt9 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2011.txt"
)
txt10 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2012.txt"
)
txt11 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2013.txt"
)
txt12 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2014.txt"
)
txt13 = pd.read_table(
    "/workspaces/pds-2022-yellow-team/00_source_data/US_VitalStatistics/Underlying Cause of Death, 2015.txt"
)

# calculate the total rows of all original txt files
num_rows = 0
for i in range(1, 14):
    num_rows += eval(f"txt{i}").shape[0]

# make sure the number of rows in concatenated dataframe is equal to the total rows of all original txt files
assert df.shape[0] == num_rows

# drop unnecessary column
temp = df.copy()
temp.drop("Notes", axis=1, inplace=True)

# fill missing values with 0
temp.dropna(how="all", inplace=True)
assert temp.isna().sum().sum() == 0

# select cause of death containing drug poisoning
only_od_all_years = temp[
    temp["Drug/Alcohol Induced Cause"].str.contains("Drug poisonings")
]

# split county and state
only_od_all_years[["CTYNAME", "STNAME"]] = only_od_all_years["County"].str.split(
    ",", 1, expand=True
)

# remove the space in front of state
only_od_all_years["STNAME"] = only_od_all_years["STNAME"].str.strip()
assert len(only_od_all_years.columns) - len(temp.columns) == 2

# select the states we are interested in
states = ["AZ", "CO", "FL", "HI", "LA", "NV", "NY", "OK", "OR", "SC", "TX", "WA", "WI"]
only_od_all_years = only_od_all_years[only_od_all_years["STNAME"].isin(states)]

# write only_od to csv
only_od_all_years.to_csv(
    "/workspaces/pds-2022-yellow-team/20_intermediate_files/only_od_all_years.csv",
    index=False,
)
