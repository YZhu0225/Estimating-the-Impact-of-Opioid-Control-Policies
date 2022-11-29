## Plot Pre-Post Graphs

## Import libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import altair as alt

## Load data from the three mortality rate cleansed files
death_data_load_FL = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/florida_death_cleaned.csv')
death_data_load_FL_copy = death_data_load_FL.copy()
death_data_FL = death_data_load_FL_copy.loc[death_data_load_FL_copy['STNAME']=='Florida']
death_data_FL_reference = death_data_load_FL_copy.loc[death_data_load_FL_copy['STNAME']!='Florida']

death_data_load_WA = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/washington_death_cleaned.csv')
death_data_load_WA_copy = death_data_load_WA.copy()
death_data_WA = death_data_load_WA_copy.loc[death_data_load_WA_copy['STNAME']=='Washington']
death_data_WA_reference = death_data_load_WA_copy.loc[death_data_load_WA_copy['STNAME']!='Washington']

death_data_load_TX = pd.read_csv('/Users/sukhpreetsahota/Desktop/Duke/Fall 2022/IDS 720.01.F22/Class Project/pds-2022-yellow-team/20_intermediate_files/texas_death_cleaned.csv')
death_data_load_TX_copy = death_data_load_TX.copy()
death_data_TX = death_data_load_TX_copy.loc[death_data_load_TX_copy['STNAME']=='Texas']
death_data_TX_reference = death_data_load_TX_copy.loc[death_data_load_TX_copy['STNAME']!='Texas']

## Check for years
print(death_data_load_FL_copy['YEAR'].unique())
print(death_data_load_WA_copy['YEAR'].unique())
print(death_data_load_TX_copy['YEAR'].unique())

## Split data by respective years to obtain pre-post dataframes
death_data_FL_pre = death_data_FL.loc[death_data_FL["YEAR"] < 2010]
death_data_FL_post = death_data_FL.loc[death_data_FL["YEAR"] >= 2010]
death_data_FL_pre['YEAR'].unique()
death_data_FL_post['YEAR'].unique()

death_data_WA_pre = death_data_WA.loc[death_data_WA["YEAR"] < 2012]
death_data_WA_post = death_data_WA.loc[death_data_FL["YEAR"] >= 2012]
death_data_WA_pre['YEAR'].unique()
death_data_WA_post['YEAR'].unique()

death_data_TX_pre = death_data_TX.loc[death_data_FL["YEAR"] < 2007]
death_data_TX_post = death_data_TX.loc[death_data_FL["YEAR"] >= 2007]
death_data_TX_pre['YEAR'].unique()
death_data_TX_post['YEAR'].unique()


## Function to create confidence interval
def get_reg_fit(data, yvar, xvar, legend, color, alpha):
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
    predictions['Indicator'] = f"{legend}"
    reg = alt.Chart(predictions).mark_line(color = "black").encode(
        x=xvar, y=yvar, color = alt.value(f"{color}"), opacity = alt.Opacity("Indicator"))
    ci = (
        alt.Chart(predictions)
        .mark_errorband()
        .encode(
            x=xvar,
            y=alt.Y("ci_low", title=yvar),
            y2="ci_high",
            color = alt.value(f"{color}")
        )
    )
    chart = ci + reg
    return predictions, chart

## Line graph/plot for pre-post analysis
def graph(year, color, data, yvar, xvar, legend):
    year = year
    yearList = []
    yearList.append(int(year))

    yearRange = list(np.arange(2003, 2016, 1))

    fit, reg_chart = get_reg_fit(data = data, yvar = yvar, xvar = xvar, legend = legend, color = color, alpha=0.05)

    yearDF = pd.DataFrame({"Year": year})

    rule = (
        alt.Chart(yearDF)
        .mark_rule(color="black")
        .encode(alt.X("Year:", title ="Year",axis=alt.Axis(values=yearRange)))
    )
    return (reg_chart + rule).properties(width=500, height=500)

## Combine fit and graph
# base = (
#     alt.Chart(
#         death_data_FL_pre, 
#         title="Mortality Analysis in Florida")
#     .mark_point()
#     .encode(
#         x=alt.X(
#             "YEAR", 
#             scale=alt.Scale(zero=False), 
#             axis = alt.Axis(format="T", 
#             title = "Year")), 
#         y = alt.Y("Death Rate (%)")
# ))
# fit = get_reg_fit(
#     base.transform_regression, 
#     yvar="Death Rate (%)", 
#     xvar="YEAR", 
#     alpha=0.05
# )
# base + fit


## Plotting pre-post for each state
pre_deaths_FL = graph(2010, 'blue', death_data_FL_pre, death_data_FL_pre['Death Rate (%)'], 'YEAR', 'STNAME')
post_deaths_FL = graph(2010, 'blue', death_data_FL_post, death_data_FL_post['Death Rate (%)'], 'YEAR', 'STNAME')
pre_post_FL = (pre_deaths_FL + post_deaths_FL)
pre_post_FL.properties(title = "Pre-Post Mortality Analysis for Florida")

pre_deaths_WA = graph(2011, 'purple', death_data_WA_pre, death_data_WA_pre['Death Rate (%)'], 'YEAR', 'STNAME')
post_deaths_WA = graph(2011, 'purple', death_data_WA_post, death_data_WA_post['Death Rate (%)'], 'YEAR', 'STNAME')
pre_post_WA = (pre_deaths_WA + post_deaths_WA)
pre_post_WA.properties(title = "Pre-Post Mortality Analysis for Washington")

pre_deaths_TX = graph(2007, 'orange', death_data_TX_pre, death_data_TX_pre['Death Rate (%)'], 'YEAR', 'STNAME')
post_deaths_TX = graph(2007, 'orange', death_data_TX_post, death_data_TX_post['Death Rate (%)'], 'YEAR', 'STNAME')
pre_post_TX = (pre_deaths_TX + post_deaths_TX)
pre_post_TX.properties(title = "Pre-Post Mortality Analysis for Texas")

