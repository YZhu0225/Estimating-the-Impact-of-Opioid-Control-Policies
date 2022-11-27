import pandas as pd
import datetime as dt

# dropbox links
fl_box = "https://www.dropbox.com/s/dgj6i7qpxae5rum/florida_shipment_data.csv?dl=1"
wa_box = "https://www.dropbox.com/s/0zxlngc2k2lhr2u/washington_shipment_data.csv?dl=1"

fl_df = pd.read_csv(fl_box)
wa_df = pd.read_csv(wa_box)


def clean_shipment(df, state_name):
    # convert TRANSACTION_DATE into datetime
    df["DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format="%m%d%Y")
    # extract year
    df["YEAR"] = df["DATE"].dt.year

    # make sure there are no missing opioid amounts
    assert df["CALC_BASE_WT_IN_GM"].isna().sum() == 0
    assert df["MME"].isna().sum() == 0

    # could not find an accurate way to impute missing counties, chose to drop
    clean_df = df.dropna(subset=["BUYER_STATE", "BUYER_COUNTY"])

    # group to find total opioids shipped per state-county-year
    grouped = clean_df.groupby(["BUYER_STATE", "BUYER_COUNTY", "YEAR"], as_index=False)[
        "MME"
    ].sum()

    grouped.to_csv(
        f"../20_intermediate_files/{state_name}_shipment_cleaned.csv",
        encoding="utf-8",
        index=False,
    )
    return None


if __name__ == "__main__":
    clean_shipment(fl_df, "florida")
    clean_shipment(wa_df, "washington")
