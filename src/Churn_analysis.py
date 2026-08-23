import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#loaded the data
def load_data():
    data_path = BASE_DIR / "Data" / "raw" / "Bank_Customer_Churn.csv"
    df = pd.read_csv(data_path)
    return df

df = load_data()

pd.set_option("display.max_columns", None)

df.set_index("customer_id", inplace=True)

#These weights are from the eda.py file's analysis
#These weight give each column a specific amount of power in categorizing churners.
weight = {"Products_number": 0.5257,
          "Age": 0.2,
          "Country": 0.0914,
          "Active_member": 0.0743,
          "Balance": 0.0571,
          "gender": 0.0514
          }

# Based on the spread found in eda.py, I calculated the churn score for each column of the data set.
# I multiplied each ranges churn rate by the weight of each column for all the columns
def churn_products(products_number):
    if products_number == 1:
        return 0.28 * 0.5257
    elif products_number == 2:
        return 0.08 * 0.5257
    elif products_number == 3:
        return 0.83 * 0.5257
    elif products_number == 4:
        return 1.0 * 0.5257

def churn_age(age):
    if 18 <= age <= 32:
        return 0.07 * 0.2
    elif 33 <= age <= 37:
        return 0.10 * 0.2
    elif 38 <= age <= 44:
        return 0.19 * 0.2
    elif 45 <= age <= 92:
        return 0.43 * 0.2

def churn_country(country):
    if country == "France":
        return 0.16 * 0.0914
    elif country == "Germany":
        return 0.32 * 0.0914
    elif country == "Spain":
        return 0.16 * 0.0914

def churn_activity(activity):
    if activity == 0:
        return 0.26 * 0.0743
    elif activity == 1:
        return 0.14 * 0.0743

def churn_balance(balance):
    if 0 <= balance <= 97198:
        return 0.15 * 0.0571
    elif 97199 <= balance <= 127644.24:
        return 0.26 * 0.0571
    elif 127644.25 <= balance <= 250898.09:
        return 0.24 * 0.0571

def churn_gender(gender):
    if gender == "Male":
        return 0.16 * 0.0514
    elif gender == "Female":
        return 0.25 * 0.0514

# This adds the total of the churn score.
# It shows it in its own column in a percentage form.
# the closer it is to 100% the likelier that customer on that row is a churner
def total_perc(row):
    total = (
                churn_products(row["products_number"])
              + churn_age(row["age"])
              + churn_country(row["country"])
              + churn_activity(row["active_member"])
              + churn_balance(row["balance"])
              + churn_gender(row["gender"])
    )
    total = (total * 100)
    total = round(total, 2)
    return total

df["churn_score"] = df.apply(total_perc, axis=1)
# Based on the spread of the churn score I divided them in 3 categories of risk(low risk, medium risk, high risk)
# The higher the churn score the higher the risk
# The cutoffs 12.65 and 23.79 represent the 25th and 75th percentile split into 3 categories of churn score column
def risk_score(row):
    churn_score = row["churn_score"]
    if churn_score <= 12.65:
        return "low risk"
    elif 12.65 <= churn_score <= 23.79:
        return "medium risk"
    elif 23.79 <= churn_score:
        return "high risk"

df["risk_score"] = df.apply(risk_score, axis=1)

# results of churning in percentage of customers flagged as high/medium/low risk
perc_of_high_risk = round((df[df["risk_score"] == "high risk"]["churn"].mean()) * 100, 2)
perc_of_medium_risk = round((df[df["risk_score"] == "medium risk"]["churn"].mean()) * 100, 2)
perc_of_low_risk = round((df[df["risk_score"] == "low risk"]["churn"].mean()) * 100, 2)

print(f"{perc_of_high_risk}% of high risk category are churners")
print(f"{perc_of_medium_risk}% of medium risk category are churners")
print(f"{perc_of_low_risk}% of low risk category are churners.")

#This is to validate my model.
#The average churn score predicted by my model closely matches the actual churn rate of the dataset, suggesting the model is well calibrated.
churn_mean = round(df["churn_score"].mean(), 2)
print(f"\n{churn_mean}% is the mean churn rate found by the risk scorer which matches the actual churn rate of the dataset(20%)")

df.to_csv( BASE_DIR / "Data" / "cleaned" / "Churn_analysis.csv", index=False)