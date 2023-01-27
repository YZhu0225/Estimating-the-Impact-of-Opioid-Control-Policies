# Estimating the Impact of Opioid Control Policies
IDS 720: Final project_Yellow Team - Suzy Anil, Sukhpreet Sahota, Xianchi Zhang, Yuanjing Zhu

## Purpose and Motivation

Prescription opioids were first introduced in 1990 to treat certain forms of cancer and aid post-surgery recovery. However, by 2007, an increase in advertisements for opioids by major pharmaceutical companies and over-prescribing led to patients with chronic illnesses taking opioids over longer periods of time, increasing their tolerance levels and raising the potential for opioid addiction. This also led to an increase in opioid imports and overdose deaths. To address this trend, states like Florida, Texas, and Washington implemented policies to limit the prescription of opioids in the hopes of reducing opioid abuse and overdose deaths. These policies included regulations on pain treatments, closing pain clinics that abuse their power, and introducing oversight on remaining clinics to monitor patient tolerances. Each state implemented different policies and their effectiveness was monitored through tracking opioid shipments and deaths due to opioid overdoses within each state. The purpose of this study is to understand the effectiveness of the various state-wide policy interventions during this time that were created to limit the prescription of opioids in the hopes of decreasing opioid deaths caused by overdoses.


## Methodology

We employed two strategies to gauge policy effectiveness: a pre-post comparison and a difference-in-difference comparison.

- **Pre-post comparison**: a method used to compare the periods before and after a specific policy was introduced to evaluate its effectiveness. It is used to inspect if there is a difference in observations that can be attributed to the policy. For example, in the case of Florida's policy, if the policy had an effect, there would be a downward trend in opioid shipments and overdose mortality after the policy was put in place. 

- **Difference-in-difference comparison**: a method of analysis that compares changes in a certain variable (in this case, opioid shipments and overdose deaths) between a group of states that have implemented policies (selected states) and a group of states that have not (reference states) over a certain period of time. This allows for a broader, nationwide view of changes in the variable and can help identify if a correlation exists between the policies and changes in trend within each selected state, while accounting for any outside factors that may have influenced the changes.

## Data source
- [Opioid Shipments](https://www.washingtonpost.com/graphics/2019/investigations/dea-pain-pill-database/) from *the Washington Post*
- [Opioid Mortality](https://github.com/YZhu0225/Estimating-the-Impact-of-Opioid-Control-Policies/tree/main/00_source_data/US_VitalStatistics) from *the US Vital Statistics*
- [County Population](https://github.com/YZhu0225/Estimating-the-Impact-of-Opioid-Control-Policies/tree/main/00_source_data/US_Population) from *the National Historical Geographic Information System*

## Conclusion
Based on our analysis, we found the following:
1. Florida had the highest increase in opioid shipments before regulations were put in place to limit prescriptions. Florida also had the most restrictive regulations among the three states studied, and as a result, both opioid shipments and overdose deaths decreased. 
2. In Texas, we saw a similar effect on overdose deaths, but no impact on opioid shipments. We concluded that the decrease in overdose deaths and opioid over-consumption in these states were directly caused by the policies put in place. 
3. However, in Washington, we did not see a significant impact on either opioid shipments or overdose deaths, indicating that the policies implemented there were not effective.

It's important to note whether the control states chosen for comparison with Florida, Texas, and Washington were selected appropriately. This is because it's difficult to infer if these control states had not implemented their own opioid regulation policies. If the control states truly had no policies in place, it would suggest that Washington's policy had no impact. However, if evidence later emerges that the control states did have policies in place prior to 2012, which resulted in stability of the mortality rate, it would be necessary to reexamine the impact by selecting new control states for all three states to further validate the conclusion of the analysis.

## Final report ([link](https://github.com/YZhu0225/Estimating-the-Impact-of-Opioid-Control-Policies/blob/main/40_docs/Final_Compiled_Version_Analysis_of_Opioid_Policies_Yellow_Team.pdf))

## Video presentation ([link](https://youtu.be/4tJa4STtUbQ))
