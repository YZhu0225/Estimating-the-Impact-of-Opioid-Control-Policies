import pandas as pd

# merge FIPS code to include state, state abreviation, and fips code
fips_url_full = "https://www.dropbox.com/s/04eu0q6sgph8wto/US_FIPS_Codes.xls?dl=1"
fips_url_abv = "https://www.dropbox.com/s/d503mesxlsc1yfa/county_fips.csv?dl=1"

fl_path = "../20_intermediate_files/florida_shipment_cleaned.csv"
fl_pop_path = "../20_intermediate_files/fl_shipment_pop.csv"

wa_path = "../20_intermediate_files/washington_shipment_cleaned.csv"
wa_pop_path = "../20_intermediate_files/wa_shipment_pop.csv"

# clean FIPS with full state name
fips_full = pd.read_excel(
    fips_url_full,
    header=1,
    dtype={"State": str, "County Name": str, "FIPS State": str, "FIPS County": str},
)
fips_full["FIPS Code"] = fips_full["FIPS State"] + fips_full["FIPS County"]
fips_full["FIPS Code"] = fips_full["FIPS Code"].str.lstrip("0")
fips_full.drop(columns=["FIPS State", "FIPS County"], inplace=True)
fips_full["FIPS Code"] = fips_full["FIPS Code"].astype(int)

# clean FIPS with state abv.
fips_abv = pd.read_csv(fips_url_abv)
fips_abv.rename(columns={"countyfips": "FIPS Code"}, inplace=True)

# merge two FIPS df
fips = fips_abv.merge(fips_full, how="left", on=["FIPS Code"], validate="1:1")
fips.drop(columns=["County Name"], inplace=True)

# Arkansas missing from fips_full, impute missing rows
missing_state = fips["State"].isna()
impute_dict = dict({"AK": "Arkansas"})
fips.loc[missing_state, "State"] = fips.loc[missing_state, "BUYER_STATE"].map(
    impute_dict
)

# merge FIPS with shipment data
fl_df = pd.read_csv(fl_path)
fl_ship_fips = fl_df.merge(
    fips, how="left", on=["BUYER_STATE", "BUYER_COUNTY"], validate="m:1"
)

wa_df = pd.read_csv(wa_path)
wa_ship_fips = wa_df.merge(
    fips, how="left", on=["BUYER_STATE", "BUYER_COUNTY"], validate="m:1"
)

# clean and standardize population data to merge with shipment
fl_df_pop = pd.read_csv(fl_pop_path)
fl_df_pop["CTYNAME"] = fl_df_pop["CTYNAME"].str.replace(" County", "")
fl_df_pop["CTYNAME"] = fl_df_pop["CTYNAME"].str.upper()

wa_df_pop = pd.read_csv(wa_pop_path)
wa_df_pop["CTYNAME"] = wa_df_pop["CTYNAME"].str.replace(" County", "")
wa_df_pop["CTYNAME"] = wa_df_pop["CTYNAME"].str.upper()

# merge shipment and population data
fl_ship_pop = fl_ship_fips.merge(
    fl_df_pop,
    how="left",
    left_on=["State", "BUYER_COUNTY", "YEAR"],
    right_on=["STNAME", "CTYNAME", "YEAR"],
    validate="1:1",
)
wa_ship_pop = wa_ship_fips.merge(
    wa_df_pop,
    how="left",
    left_on=["State", "BUYER_COUNTY", "YEAR"],
    right_on=["STNAME", "CTYNAME", "YEAR"],
    validate="1:1",
)

fl_ship_pop.to_csv(
    f"../20_intermediate_files/fl_ship_merge.csv",
    encoding="utf-8",
    index=False,
)
wa_ship_pop.to_csv(
    f"../20_intermediate_files/wa_ship_merge.csv",
    encoding="utf-8",
    index=False,
)
