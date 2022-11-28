import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def merge_pop_data(state_name):
    """
    This function will merge the two population datasets together.
    Input: state_name
        state_name: the state name
    return: a pandas dataframe with the merged population data
    """
    # read in the data
    all_2000_2009 = pd.read_csv(
        "../00_source_data/US_Population/start_2000.csv", encoding="latin-1"
    )
    all_2010_2019 = pd.read_csv(
        "../00_source_data/US_Population/start_2010.csv", encoding="latin-1"
    )

    # columns to keep
    pop_col_2000_2009 = [
        "STNAME",
        "CTYNAME",
        "POPESTIMATE2000",
        "POPESTIMATE2001",
        "POPESTIMATE2002",
        "POPESTIMATE2003",
        "POPESTIMATE2004",
        "POPESTIMATE2005",
        "POPESTIMATE2006",
        "POPESTIMATE2007",
        "POPESTIMATE2008",
        "POPESTIMATE2009",
    ]
    pop_col_2010_2019 = [
        "STNAME",
        "CTYNAME",
        "POPESTIMATE2010",
        "POPESTIMATE2011",
        "POPESTIMATE2012",
        "POPESTIMATE2013",
        "POPESTIMATE2014",
        "POPESTIMATE2015",
        "POPESTIMATE2016",
        "POPESTIMATE2017",
        "POPESTIMATE2018",
        "POPESTIMATE2019",
    ]

    # filter the data
    pop_2000_2009 = all_2000_2009[all_2000_2009["STNAME"] == state_name][
        pop_col_2000_2009
    ]
    pop_2010_2019 = all_2010_2019[all_2010_2019["STNAME"] == state_name][
        pop_col_2010_2019
    ]

    # rename the columns
    pop_2000_2009.columns = [
        "STNAME",
        "CTYNAME",
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
    ]
    pop_2010_2019.columns = [
        "STNAME",
        "CTYNAME",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
    ]

    assert (
        pop_2000_2009.shape[0] == pop_2010_2019.shape[0]
    )  # number of county should be the same
    # merge two datasets
    pop_2000_2019 = pd.merge(
        pop_2000_2009, pop_2010_2019, how="outer", on=["STNAME", "CTYNAME"]
    )

    # remove the aggregate population of the state
    pop_2000_2019 = pop_2000_2019[pop_2000_2019["CTYNAME"] != state_name]

    # convert columns to rows
    pop = pd.melt(
        pop_2000_2019,
        id_vars=["STNAME", "CTYNAME"],
        var_name="YEAR",
        value_name="POPULATION",
    )
    assert pop.shape[0] == pop_2000_2019.shape[0] * (
        pop_2000_2019.shape[1] - 2
    )  # number of rows should be the same
    assert pop["YEAR"].nunique() == (
        pop_2000_2019.shape[1] - 2
    )  # number of years should be the same

    return pop


### Florida and its reference states: AZ, CO, FL, LA, NV, SC
pop_az = merge_pop_data("Arizona")
pop_co = merge_pop_data("Colorado")
pop_fl = merge_pop_data("Florida")
pop_la = merge_pop_data("Louisiana")
pop_nv = merge_pop_data("Nevada")
pop_sc = merge_pop_data("South Carolina")

# check missing values
for i in [pop_az, pop_co, pop_fl, pop_la, pop_nv, pop_sc]:
    print(f"Population dataframe has {i.isna().sum().sum()} missing values")

# Manipulate missing values in Louisiana
pop_la[pop_la["POPULATION"].isna()]
all_2000_2009 = pd.read_csv(
    "../00_source_data/US_Population/start_2000.csv", encoding="latin-1"
)
all_2010_2019 = pd.read_csv(
    "../00_source_data/US_Population/start_2010.csv", encoding="latin-1"
)

# columns to keep
pop_col_2000_2009 = [
    "STNAME",
    "CTYNAME",
    "POPESTIMATE2000",
    "POPESTIMATE2001",
    "POPESTIMATE2002",
    "POPESTIMATE2003",
    "POPESTIMATE2004",
    "POPESTIMATE2005",
    "POPESTIMATE2006",
    "POPESTIMATE2007",
    "POPESTIMATE2008",
    "POPESTIMATE2009",
]
pop_col_2010_2019 = [
    "STNAME",
    "CTYNAME",
    "POPESTIMATE2010",
    "POPESTIMATE2011",
    "POPESTIMATE2012",
    "POPESTIMATE2013",
    "POPESTIMATE2014",
    "POPESTIMATE2015",
    "POPESTIMATE2016",
    "POPESTIMATE2017",
    "POPESTIMATE2018",
    "POPESTIMATE2019",
]

# filter the data
pop_2000_2009 = all_2000_2009[all_2000_2009["STNAME"] == "Louisiana"][pop_col_2000_2009]
pop_2010_2019 = all_2010_2019[all_2010_2019["STNAME"] == "Louisiana"][pop_col_2010_2019]

# rename the columns
pop_2000_2009.columns = [
    "STNAME",
    "CTYNAME",
    "2000",
    "2001",
    "2002",
    "2003",
    "2004",
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
]
pop_2010_2019.columns = [
    "STNAME",
    "CTYNAME",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
]

pop_2010_2019[pop_2010_2019["CTYNAME"] == "LaSalle Parish"]
pop_2000_2009[pop_2000_2009["CTYNAME"] == "LaSalle Parish"]

pop_2000_2009["CTYNAME"].unique()
# County "LaSalle Parish" in population_2010_2019 is spelled as "La Salle Parish" in population_2000_2009

# replace La Salle Parish with LaSalle Parish
pop_2000_2009["CTYNAME"] = pop_2000_2009["CTYNAME"].replace(
    "La Salle Parish", "LaSalle Parish"
)

# merge two datasets
pop_2000_2019 = pd.merge(
    pop_2000_2009, pop_2010_2019, how="outer", on=["STNAME", "CTYNAME"]
)
assert pop_2000_2019.isna().sum().sum() == 0  # make sure there is no missing value

# remove the aggregate population of the state
pop_2000_2019 = pop_2000_2019[pop_2000_2019["CTYNAME"] != "Louisiana"]

# convert columns to rows
pop_la = pd.melt(
    pop_2000_2019,
    id_vars=["STNAME", "CTYNAME"],
    var_name="YEAR",
    value_name="POPULATION",
)

fl_shipment_pop = pd.concat([pop_az, pop_fl, pop_la, pop_sc])
assert (
    fl_shipment_pop.shape[0]
    == pop_az.shape[0] + pop_fl.shape[0] + pop_la.shape[0] + pop_sc.shape[0]
)  # make sure the number of rows is the same
# write the data to csv
fl_shipment_pop.to_csv("../20_intermediate_files/fl_shipment_pop.csv", index=False)

fl_death_pop = pd.concat([pop_co, pop_fl, pop_la, pop_nv])
assert (
    fl_death_pop.shape[0]
    == pop_co.shape[0] + pop_fl.shape[0] + pop_la.shape[0] + pop_nv.shape[0]
)  # make sure the number of rows is the same
# write the data to csv
fl_death_pop.to_csv("../20_intermediate_files/fl_death_pop.csv", index=False)


### Texas and its reference states: NY, OR, TX, WI
pop_ny = merge_pop_data("New York")
pop_or = merge_pop_data("Oregon")
pop_tx = merge_pop_data("Texas")
pop_wi = merge_pop_data("Wisconsin")

# check missing values
for i in [pop_ny, pop_or, pop_tx, pop_wi]:
    print(f"Population dataframe has {i.isna().sum().sum()} missing values")

tx_death_pop = pd.concat([pop_ny, pop_or, pop_tx, pop_wi])
assert (
    tx_death_pop.shape[0]
    == pop_ny.shape[0] + pop_or.shape[0] + pop_tx.shape[0] + pop_wi.shape[0]
)  # make sure the number of rows is the same
# write the data to csv
tx_death_pop.to_csv("../20_intermediate_files/tx_death_pop.csv", index=False)


### Washington and its reference states: AZ, CO, HI, NY, OK, OR, WA
pop_az = merge_pop_data("Arizona")
pop_co = merge_pop_data("Colorado")
pop_hi = merge_pop_data("Hawaii")
pop_ny = merge_pop_data("New York")
pop_ok = merge_pop_data("Oklahoma")
pop_or = merge_pop_data("Oregon")
pop_wa = merge_pop_data("Washington")

# check missing values
for i in [pop_az, pop_co, pop_hi, pop_ny, pop_ok, pop_or, pop_wa]:
    print(f"Population dataframe has {i.isna().sum().sum()} missing values")

wa_shipment_pop = pd.concat([pop_az, pop_co, pop_ny, pop_wa])
assert (
    wa_shipment_pop.shape[0]
    == pop_az.shape[0] + pop_co.shape[0] + pop_ny.shape[0] + pop_wa.shape[0]
)  # make sure the number of rows is the same
# write the data to csv
wa_shipment_pop.to_csv("../20_intermediate_files/wa_shipment_pop.csv", index=False)

wa_death_pop = pd.concat([pop_hi, pop_ok, pop_or, pop_wa])
assert (
    wa_death_pop.shape[0]
    == pop_hi.shape[0] + pop_ok.shape[0] + pop_or.shape[0] + pop_wa.shape[0]
)  # make sure the number of rows is the same
# write the data to csv
wa_death_pop.to_csv("../20_intermediate_files/wa_death_pop.csv", index=False)
