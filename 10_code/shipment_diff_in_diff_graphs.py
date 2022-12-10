## import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import altair as alt

## Load data from the FL shipment cleansed files
ship_data_load_FL = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/fl_ship_merge.csv')
ship_data_load_FL_copy = ship_data_load_FL.copy()
ship_data_load_FL_copy = ship_data_load_FL_copy[["BUYER_STATE_x", "BUYER_COUNTY_x", "YEAR", "MME", "FIPS Code", "State_x", "STNAME", "CTYNAME", "POPULATION"]]
ship_data_load_FL_copy = ship_data_load_FL_copy.rename(columns={"BUYER_STATE_x": "BUYER_STATE", "BUYER_COUNTY_x": "BUYER_COUNTY", "State_x": "State"})
ship_data_load_FL_copy['Shipment_Rate_Percentage_MME_Rate'] = ship_data_load_FL_copy['MME']/ship_data_load_FL_copy['POPULATION']
ship_data_FL = ship_data_load_FL_copy.loc[ship_data_load_FL_copy['BUYER_STATE']=='FL']
ship_data_FL_reference = ship_data_load_FL_copy.loc[ship_data_load_FL_copy['BUYER_STATE']!='FL']
ship_data_FL


## Transform and Groupby MME Rate by State and Year for FL
ship_data_FL[
    "MME_Rate"
] = ship_data_FL.groupby(["BUYER_STATE", "YEAR"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_FL_subset = ship_data_FL[["BUYER_STATE", "YEAR", "MME_Rate"]]
ship_data_FL_subset_grouped = ship_data_FL_subset.groupby(["BUYER_STATE", "YEAR"], as_index = False).mean()
ship_data_FL_subset_grouped_pre = ship_data_FL_subset_grouped.loc[ship_data_FL_subset_grouped["YEAR"] < 2010]
ship_data_FL_subset_grouped_post = ship_data_FL_subset_grouped.loc[ship_data_FL_subset_grouped["YEAR"] >= 2010]


## Function to create confidence interval for FL
def get_reg_fit_FL(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "teal").encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "teal")
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for FL
fit, reg_chart_pre_FL = get_reg_fit_FL(
    ship_data_FL_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_FL = get_reg_fit_FL(
    ship_data_FL_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2010 = alt.Chart(pd.DataFrame({'x': [2010]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for FL
pre_post_FL = reg_chart_pre_FL + reg_chart_post_FL + line_2010
pre_post_FL.properties(title="Pre-Post Shipment Rate Analysis of Florida")


## Include indicator for reference states for aggregation
ship_data_FL_reference["Reference_State_Indicator"] = 1
ship_data_FL_reference


## Transform and Groupby MME Rate by State and Year for FL Reference states
ship_data_FL_reference[
    "MME_Rate"
] = ship_data_FL_reference.groupby(["Reference_State_Indicator", "YEAR"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_FL_ref_subset = ship_data_FL_reference[["YEAR", "MME_Rate"]]
ship_data_FL_ref_subset_grouped = ship_data_FL_ref_subset.groupby(["YEAR"], as_index = False).mean()
ship_data_FL_ref_subset_grouped_pre = ship_data_FL_ref_subset_grouped.loc[ship_data_FL_ref_subset_grouped["YEAR"] < 2010]
ship_data_FL_ref_subset_grouped_post = ship_data_FL_ref_subset_grouped.loc[ship_data_FL_ref_subset_grouped["YEAR"] >= 2010]


## Function to create confidence interval for FL reference states
def get_reg_fit_FL_ref(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "grey", opacity=0.3).encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "grey", opacity=0.3)
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for FL reference states
fit, reg_chart_pre_FL_ref = get_reg_fit_FL_ref(
    ship_data_FL_ref_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_FL_ref = get_reg_fit_FL_ref(
    ship_data_FL_ref_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2010 = alt.Chart(pd.DataFrame({'x': [2010]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for FL reference states
pre_post_FL_ref = reg_chart_pre_FL_ref + reg_chart_post_FL_ref + line_2010
pre_post_FL_ref.properties(title="Pre-Post Shipment Rate Analysis of Florida Reference States")


## Combine pre-post graphs to create diff-in-diff graph for FL and FL reference states
diff_in_diff_FL = pre_post_FL + pre_post_FL_ref
diff_in_diff_FL.properties(title="Diff-in-Diff Shipment Rate Analysis of Florida vs Reference States")


## Load data from the WA shipment cleansed files
ship_data_load_WA = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/wa_ship_merge.csv')
ship_data_load_WA_copy = ship_data_load_WA.copy()
ship_data_load_WA_copy['Shipment_Rate_Percentage_MME_Rate'] = ship_data_load_WA_copy['MME']/ship_data_load_WA_copy['POPULATION']
ship_data_WA = ship_data_load_WA_copy.loc[ship_data_load_WA_copy['BUYER_STATE']=='WA']
ship_data_WA_reference = ship_data_load_WA_copy.loc[ship_data_load_WA_copy['BUYER_STATE']!='WA']
ship_data_WA


## Transform and Groupby MME Rate by State and Year for WA
ship_data_WA[
    "MME_Rate"
] = ship_data_WA.groupby(["BUYER_STATE", "YEAR"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_WA_subset = ship_data_WA[["BUYER_STATE", "YEAR", "MME_Rate"]]
ship_data_WA_subset_grouped = ship_data_WA_subset.groupby(["BUYER_STATE", "YEAR"], as_index = False).mean()
ship_data_WA_subset_grouped_pre = ship_data_WA_subset_grouped.loc[ship_data_WA_subset_grouped["YEAR"] < 2012]
ship_data_WA_subset_grouped_post = ship_data_WA_subset_grouped.loc[ship_data_WA_subset_grouped["YEAR"] >= 2012]


## Function to create confidence interval for WA
def get_reg_fit_WA(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "purple").encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "purple")
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for WA
fit, reg_chart_pre_WA = get_reg_fit_WA(
    ship_data_WA_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_WA = get_reg_fit_WA(
    ship_data_WA_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2012 = alt.Chart(pd.DataFrame({'x': [2012]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for WA
pre_post_WA = reg_chart_pre_WA + reg_chart_post_WA + line_2012
pre_post_WA.properties(title="Pre-Post Shipment Rate Analysis of Washington")


## Include indicator for reference states for aggregation
ship_data_WA_reference["Reference_State_Indicator"] = 1
ship_data_WA_reference["BUYER_STATE"].unique()


## Transform and Groupby MME Rate by State and Year for WA reference states
ship_data_WA_reference[
    "MME_Rate"
] = ship_data_WA_reference.groupby(["Reference_State_Indicator", "YEAR"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_WA_ref_subset = ship_data_WA_reference[["YEAR", "MME_Rate"]]
ship_data_WA_ref_subset_grouped = ship_data_WA_ref_subset.groupby(["YEAR"], as_index = False).mean()
ship_data_WA_ref_subset_grouped_pre = ship_data_WA_ref_subset_grouped.loc[ship_data_WA_ref_subset_grouped["YEAR"] < 2012]
ship_data_WA_ref_subset_grouped_post = ship_data_WA_ref_subset_grouped.loc[ship_data_WA_ref_subset_grouped["YEAR"] >= 2012]


## Function to create confidence interval for WA reference states
def get_reg_fit_WA_ref(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "red", opacity=0.2).encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "red", opacity=0.2)
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for WA reference states
fit, reg_chart_pre_WA_ref = get_reg_fit_WA_ref(
    ship_data_WA_ref_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_WA_ref = get_reg_fit_WA_ref(
    ship_data_WA_ref_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2012 = alt.Chart(pd.DataFrame({'x': [2012]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for WA reference states
pre_post_WA_ref = reg_chart_pre_WA_ref + reg_chart_post_WA_ref + line_2012
pre_post_WA_ref.properties(title="Pre-Post Shipment Rate Analysis of Washington Reference States")


## Combine pre-post graphs to create diff-in-diff graph for WA and WA reference states
diff_in_diff_WA = pre_post_WA + pre_post_WA_ref
diff_in_diff_WA.properties(title="Diff-in-Diff Shipment Rate Analysis of Washington vs Reference States")


## Load data from the TX shipment cleansed files
ship_data_load_TX = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/tx_ship_merge.csv')
ship_data_load_TX_copy = ship_data_load_TX.copy()
ship_data_load_TX_copy = ship_data_load_TX_copy[["BUYER_STATE", "BUYER_COUNTY", "YEAR", "MONTH", "MME", "FIPS Code", "State_x", "STNAME", "CTYNAME", "POPULATION"]]
ship_data_load_TX_copy = ship_data_load_TX_copy.rename(columns={"State_x": "State"})
ship_data_load_TX_copy["YEAR_AND_MONTH_DATE"] = ship_data_load_TX_copy["YEAR"] + (
    (ship_data_load_TX_copy["MONTH"] - 1)/12)
ship_data_load_TX_copy['Shipment_Rate_Percentage_MME_Rate'] = ship_data_load_TX_copy['MME']/ship_data_load_TX_copy['POPULATION']
ship_data_TX = ship_data_load_TX_copy.loc[ship_data_load_TX_copy['BUYER_STATE']=='TX']
ship_data_TX_reference = ship_data_load_TX_copy.loc[ship_data_load_TX_copy['BUYER_STATE']!='TX']
ship_data_TX


## Transform and Groupby MME Rate by State and Year for TX
ship_data_TX[
    "MME_Rate"
] = ship_data_TX.groupby(["BUYER_STATE", "YEAR_AND_MONTH_DATE"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_TX_subset = ship_data_TX[["BUYER_STATE", "YEAR_AND_MONTH_DATE", "MME_Rate"]]
ship_data_TX_subset_grouped = ship_data_TX_subset.groupby(["BUYER_STATE", "YEAR_AND_MONTH_DATE"], as_index = False).mean()
ship_data_TX_subset_grouped_pre = ship_data_TX_subset_grouped.loc[ship_data_TX_subset_grouped["YEAR_AND_MONTH_DATE"] < 2007]
ship_data_TX_subset_grouped_post = ship_data_TX_subset_grouped.loc[ship_data_TX_subset_grouped["YEAR_AND_MONTH_DATE"] >= 2007]


## Function to create confidence interval for TX
def get_reg_fit_TX(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "orange").encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "orange")
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for TX
fit, reg_chart_pre_TX = get_reg_fit_TX(
    ship_data_TX_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR_AND_MONTH_DATE", 
    alpha=0.05
)

fit, reg_chart_post_TX = get_reg_fit_TX(
    ship_data_TX_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR_AND_MONTH_DATE", 
    alpha=0.05
)

## Create line post-policy implementation
line_2007 = alt.Chart(pd.DataFrame({'x': [2007]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for TX
pre_post_TX = reg_chart_pre_TX + reg_chart_post_TX + line_2007
pre_post_TX.properties(title="Pre-Post Shipment Rate Analysis of Texas")


## Include indicator for reference states for aggregation
ship_data_TX_reference["Reference_State_Indicator"] = 1
ship_data_TX_reference["BUYER_STATE"].unique()


## Transform and Groupby MME Rate by State and Year for WA reference states
ship_data_TX_reference[
    "MME_Rate"
] = ship_data_TX_reference.groupby(["Reference_State_Indicator", "YEAR_AND_MONTH_DATE"])[
    "Shipment_Rate_Percentage_MME_Rate"
].transform(
    "mean"
)
ship_data_TX_ref_subset = ship_data_TX_reference[["YEAR_AND_MONTH_DATE", "MME_Rate"]]
ship_data_TX_ref_subset_grouped = ship_data_TX_ref_subset.groupby(["YEAR_AND_MONTH_DATE"], as_index = False).mean()
ship_data_TX_ref_subset_grouped_pre = ship_data_TX_ref_subset_grouped.loc[ship_data_TX_ref_subset_grouped["YEAR_AND_MONTH_DATE"] < 2007]
ship_data_TX_ref_subset_grouped_post = ship_data_TX_ref_subset_grouped.loc[ship_data_TX_ref_subset_grouped["YEAR_AND_MONTH_DATE"] >= 2007]


## Function to create confidence interval for TX reference states
def get_reg_fit_TX_ref(data, yvar, xvar, alpha):
    # Grid for predicted values
    x = data.loc[pd.notnull(data[yvar]), xvar]
    xmin = x.min()
    xmax = x.max()
    step = (xmax - xmin) / 100
    grid = np.arange(xmin, xmax + step, step)
    predictions = pd.DataFrame({xvar: grid})

    # Fit model, get predictions
    model = smf.ols(f"{yvar} ~ {xvar}", data=data).fit()
    model_predict = model.get_prediction(predictions[xvar])
    predictions[yvar] = model_predict.summary_frame()["mean"]
    predictions[["ci_low", "ci_high"]] = model_predict.conf_int(alpha=alpha)

    # Build chart
    reg = alt.Chart(predictions).mark_line(color = "blue", opacity=0.2).encode(
        x=alt.X(
            xvar, 
            scale=alt.Scale(zero=False), 
            axis = alt.Axis(format="T", 
            title = "Year")), 
        y = alt.Y(
            yvar, 
            scale=alt.Scale(zero=False),
            title = "Opioid Shipments per 100,000 people in Milligrams (MME)")
    )
    ci = (
        alt.Chart(predictions)
        .mark_errorband(color = "blue", opacity=0.2)
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=""),
            y2="ci_high",
        )
    )
    chart = ci + reg
    return predictions, chart


## Generate Pre-Post Graphs for WA reference states
fit, reg_chart_pre_TX_ref = get_reg_fit_TX_ref(
    ship_data_TX_ref_subset_grouped_pre, 
    yvar="MME_Rate", 
    xvar="YEAR_AND_MONTH_DATE", 
    alpha=0.05
)

fit, reg_chart_post_TX_ref = get_reg_fit_TX_ref(
    ship_data_TX_ref_subset_grouped_post, 
    yvar="MME_Rate", 
    xvar="YEAR_AND_MONTH_DATE", 
    alpha=0.05
)

## Create line post-policy implementation
line_2007 = alt.Chart(pd.DataFrame({'x': [2007]})).mark_rule(strokeDash=[10, 7], color = "red", strokeWidth=3).encode(x='x')

## Generate final pre-post graph for WA reference states
pre_post_TX_ref = reg_chart_pre_TX_ref + reg_chart_post_TX_ref + line_2007
pre_post_TX_ref.properties(title="Pre-Post Shipment Rate Analysis of Texas Reference States")


## Combine pre-post graphs to create diff-in-diff graph for WA and WA reference states
diff_in_diff_TX = pre_post_TX + pre_post_TX_ref
diff_in_diff_TX.properties(title="Diff-in-Diff Shipment Rate Analysis of Texas vs Reference States")