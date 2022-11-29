## import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import altair as alt

## Load data from the FL mortality cleansed files
death_data_load_FL = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/florida_death_cleaned.csv')
death_data_load_FL_copy = death_data_load_FL.copy()
death_data_load_FL_copy['Death_Rate_Percentage'] = death_data_load_FL_copy['Death Rate (%)'] * 1000
death_data_FL = death_data_load_FL_copy.loc[death_data_load_FL_copy['STNAME']=='Florida']
death_data_FL_reference = death_data_load_FL_copy.loc[death_data_load_FL_copy['STNAME']!='Florida']
death_data_FL


## Transform and Groupby Death Rate by State and Year for FL
death_data_FL[
    "average_deaths_state"
] = death_data_FL.groupby(["STNAME", "YEAR"])[
    "Death_Rate_Percentage"
].transform(
    "mean"
)
death_data_FL_subset = death_data_FL[["STNAME", "YEAR", "average_deaths_state"]]
death_data_FL_subset_grouped = death_data_FL_subset.groupby(["STNAME", "YEAR"], as_index = False).mean()
death_data_FL_subset_grouped_pre = death_data_FL_subset_grouped.loc[death_data_FL_subset_grouped["YEAR"] < 2010]
death_data_FL_subset_grouped_post = death_data_FL_subset_grouped.loc[death_data_FL_subset_grouped["YEAR"] >= 2010]


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
            title = "Mortality Rate (per 100,000 people)")
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
    death_data_FL_subset_grouped_pre, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)
reg_chart_pre_FL

fit, reg_chart_post_FL = get_reg_fit_FL(
    death_data_FL_subset_grouped_post, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2010 = alt.Chart(pd.DataFrame({'x': [2010]})).mark_rule(strokeDash=[5, 5]).encode(x='x')

## Generate final pre-post graph for FL
pre_post_FL = reg_chart_pre_FL + reg_chart_post_FL + line_2010
pre_post_FL.properties(title="Pre-Post Florida Mortality Rate Analysis")


## Load data from the WA and TX deaths cleansed files
death_data_load_WA = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/washington_death_cleaned.csv')
death_data_load_WA_copy = death_data_load_WA.copy()
death_data_load_WA_copy['Death_Rate_Percentage'] = death_data_load_WA_copy['Death Rate (%)'] * 1000
death_data_WA = death_data_load_WA_copy.loc[death_data_load_WA_copy['STNAME']=='Washington']
death_data_WA_reference = death_data_load_WA_copy.loc[death_data_load_WA_copy['STNAME']!='Washington']

death_data_load_TX = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/texas_death_cleaned.csv')
death_data_load_TX_copy = death_data_load_TX.copy()
death_data_load_TX_copy['Death_Rate_Percentage'] = death_data_load_TX_copy['Death Rate (%)'] * 1000
death_data_TX = death_data_load_TX_copy.loc[death_data_load_TX_copy['STNAME']=='Texas']
death_data_TX_reference = death_data_load_TX_copy.loc[death_data_load_TX_copy['STNAME']!='Texas']


## Transform and Groupby Death Rate by State and Year for WA
death_data_WA[
    "average_deaths_state"
] = death_data_WA.groupby(["STNAME", "YEAR"])[
    "Death_Rate_Percentage"
].transform(
    "mean"
)
death_data_WA_subset = death_data_WA[["STNAME", "YEAR", "average_deaths_state"]]
death_data_WA_subset_grouped = death_data_WA_subset.groupby(["STNAME", "YEAR"], as_index = False).mean()
death_data_WA_subset_grouped_pre = death_data_WA_subset_grouped.loc[death_data_WA_subset_grouped["YEAR"] < 2012]
death_data_WA_subset_grouped_post = death_data_WA_subset_grouped.loc[death_data_WA_subset_grouped["YEAR"] >= 2012]


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
            title = "Mortality Rate (per 100,000 people)")
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
    death_data_WA_subset_grouped_pre, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_WA = get_reg_fit_WA(
    death_data_WA_subset_grouped_post, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2012 = alt.Chart(pd.DataFrame({'x': [2012]})).mark_rule(strokeDash=[5, 5]).encode(x='x')

## Generate final pre-post graph for WA
pre_post_WA = reg_chart_pre_WA + reg_chart_post_WA + line_2012
pre_post_WA.properties(title="Pre-Post Washington Mortality Rate Analysis")


## Transform and Groupby Death Rate by State and Year for TX
death_data_TX[
    "average_deaths_state"
] = death_data_TX.groupby(["STNAME", "YEAR"])[
    "Death_Rate_Percentage"
].transform(
    "mean"
)
death_data_TX_subset = death_data_TX[["STNAME", "YEAR", "average_deaths_state"]]
death_data_TX_subset_grouped = death_data_TX_subset.groupby(["STNAME", "YEAR"], as_index = False).mean()
death_data_TX_subset_grouped_pre = death_data_TX_subset_grouped.loc[death_data_TX_subset_grouped["YEAR"] < 2007]
death_data_TX_subset_grouped_post = death_data_TX_subset_grouped.loc[death_data_TX_subset_grouped["YEAR"] >= 2007]


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
            title = "Mortality Rate (per 100,000 people)")
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
    death_data_TX_subset_grouped_pre, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)

fit, reg_chart_post_TX = get_reg_fit_TX(
    death_data_TX_subset_grouped_post, 
    yvar="average_deaths_state", 
    xvar="YEAR", 
    alpha=0.05
)

## Create line post-policy implementation
line_2007 = alt.Chart(pd.DataFrame({'x': [2007]})).mark_rule(strokeDash=[5, 5]).encode(x='x')

## Generate final pre-post graph for TX
pre_post_TX = reg_chart_pre_TX + reg_chart_post_TX + line_2007
pre_post_TX.properties(title="Pre-Post Texas Mortality Rate Analysis")