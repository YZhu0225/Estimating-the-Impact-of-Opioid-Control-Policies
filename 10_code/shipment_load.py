import pandas as pd

box_link = "https://www.dropbox.com/s/95ujsl5fa1r4ko2/prescription_data.zip?dl=1"
states = ["SC", "LA", "AZ", "CO", "NY", "FL", "WA"]
cols_needed = [
    "BUYER_STATE",
    "BUYER_COUNTY",
    "TRANSACTION_DATE",
    "CALC_BASE_WT_IN_GM",
    "MME_Conversion_Factor",
    "MME",
]

data = []
# read in full shipment data
ship_iter = pd.read_csv(
    box_link, compression="zip", iterator=True, chunksize=1000000, usecols=cols_needed
)

# process chunks for required ref states
for ship_chunk in ship_iter:
    chunk = ship_chunk[ship_chunk["BUYER_STATE"].isin(states)]
    data.append(chunk)
ship_df = pd.concat(data)

# reference states for shipment analysis
florida_ref = ["FL", "SC", "LA", "AZ"]
washington_ref = ["WA", "CO", "AZ", "NY"]

# dataframes for FL, WA with reference states
florida_ship_df = ship_df[ship_df["BUYER_COUNTY"].isin(florida_ref)]
washington_ship_df = ship_df[ship_df["BUYER_COUNTY"].isin(washington_ref)]

# output to csv for cleaning
florida_ship_df.to_csv(
    "../20_intermediate_files/florida_shipment_data.csv", encoding="utf-8", index=False
)
washington_ship_df.to_csv(
    "../20_intermediate_files/washington_shipment_data.csv",
    encoding="utf-8",
    index=False,
)
