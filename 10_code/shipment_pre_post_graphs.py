## import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import altair as alt


## Load data from the FL shipment cleansed files
ship_data_load_FL = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/fl_ship_merge.csv')
ship_data_load_FL_copy = ship_data_load_FL.copy()
ship_data_load_FL_copy['Shipment_Rate_Percentage_MME_Rate'] = ship_data_load_FL_copy['MME']/ship_data_load_FL_copy['POPULATION']
ship_data_FL = ship_data_load_FL_copy.loc[ship_data_load_FL_copy['BUYER_STATE']=='FL']
ship_data_FL_reference = ship_data_load_FL_copy.loc[ship_data_load_FL_copy['BUYER_STATE']!='FL']
ship_data_FL


## Load data from the WA shipment cleansed files
ship_data_load_WA = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/wa_ship_merge.csv')
ship_data_load_WA_copy = ship_data_load_WA.copy()
ship_data_load_WA_copy['Shipment_Rate_Percentage_MME_Rate'] = ship_data_load_WA_copy['MME']/ship_data_load_WA_copy['POPULATION']
ship_data_WA = ship_data_load_WA_copy.loc[ship_data_load_WA_copy['BUYER_STATE']=='WA']
ship_data_WA_reference = ship_data_load_WA_copy.loc[ship_data_load_WA_copy['BUYER_STATE']!='WA']
ship_data_WA


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
            title = "Opioid Shipment Rate (per 100,000 people)")
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
            title = "Opioid Shipment Rate (per 100,000 people)")
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
line_2010 = alt.Chart(pd.DataFrame({'x': [2010]})).mark_rule(strokeDash=[5, 5]).encode(x='x')

## Generate final pre-post graph for FL
pre_post_FL = reg_chart_pre_FL + reg_chart_post_FL + line_2010
pre_post_FL.properties(title="Pre-Post Florida Shipment Rate Analysis")


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
line_2012 = alt.Chart(pd.DataFrame({'x': [2012]})).mark_rule(strokeDash=[5, 5]).encode(x='x')

## Generate final pre-post graph for WA
pre_post_WA = reg_chart_pre_WA + reg_chart_post_WA + line_2012
pre_post_WA.properties(title="Pre-Post Washington Shipment Rate Analysis")