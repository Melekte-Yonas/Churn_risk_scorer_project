# EDA Goal: Identify meaningful predictors of customer churn
# Dataset: Bank_Customer_Churn.csv(10k customers)

#1. I first imported the data and made it easier to see.
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

df = df.drop(columns= ["customer_id"])


#2. I then went through each column to see meaningful differences between churners and non churners that might suggest likeliness of churning.

#I. COLUMN NAME: "active_member"
print(df.groupby("active_member")["churn"].mean())
print()
# this gives me the likeliness for a non-active member and an active member to churn.
#results: active_member
#         0    0.268509 non-active members are 26% likely to churn
#         1    0.142691 active members are 14% likely to churn.
# The result showed that non-active members were more likely to churn


#II. COLUMN NAME: "balance"
print(df["balance"].describe())
print()
#then I chose the ranges based on the spread:
filtered_df = df[df["balance"].between(0, 97198)]["churn"].mean()
print(f"1st Range: {(filtered_df * 100):.2f}%")
filtered_df = df[df["balance"].between(97198, 127644.24)]["churn"].mean()
print(f"2nd Range: {(filtered_df * 100):.2f}%")
filtered_df = df[df["balance"].between(127644.24, 250898.09)]["churn"].mean()
print(f"3rd Range: {(filtered_df * 100):.2f}%")
print()
# I used this code for each range of balance in this dataset and found this:
# 1st range: 0 - 97,198, chance of churning: 16%
# 2nd range: 97,198 - 127,644.24, chance of churning: 26%
# 3rd range: 127,644.24 - 250,898.09, chance of churning: 24%
# The results showed that people with higher balance were more likely to churn


#III. COLUMN NAME: "age"
print(df["age"].describe())
print()
# I found the spread just like the balance column:
filtered_df1 = df[df["age"].between(18, 32)]["churn"].mean()
print(f"1st Range: {filtered_df1 * 100:.2f}%")
filtered_df1 = df[df["age"].between(32, 37)]["churn"].mean()
print(f"2nd Range: {filtered_df1 * 100:.2f}%")
filtered_df1 = df[df["age"].between(37, 44)]["churn"].mean()
print(f"3rd Range: {filtered_df1 * 100:.2f}%")
filtered_df1 = df[df["age"].between(44, 92)]["churn"].mean()
print(f"4th Range: {filtered_df1 * 100:.2f}%")
print()
# I used the same code as the balance column to find the likeliness of churning in each range of age:
# results:
#         1st range: 18 - 32, likeliness of churning: 7%
#         2nd range: 33 - 37, likeliness of churning: 10%
#         3rd range: 38 - 44, likeliness of churning: 19%
#         4th range: 44 - 92, likeliness of churning: 43%
# The results showed that older people where more likely to churn


#IV. COLUMN NAME: "product number":
# this column showed how many products/accounts/credit cards each person had in this bank:
total_pd = df["products_number"].value_counts()
churn_pd = df[df["churn"] == 1]["products_number"].value_counts()
percentage_of_churners = (churn_pd / total_pd) * 100
print(percentage_of_churners)
print()
# This code finds the percentage of churners based on each product number ranging from 1 product to 4 products
#      1 product: 28% churners
#      2 products: 8% churners
#      3 products: 83% churners
#      4 products: 100% churners
# This the biggest indicator of churning so far.
#


#V. COLUMN NAME: "country":
#There are 3 countries listed in this column(France, Germany, and spain)
total_countries = df["country"].value_counts()
churn_countries = df[df["churn"] == 1]["country"].value_counts()
perc_of_churners = (churn_countries / total_countries) * 100
print(perc_of_churners)
print()
#similarly to the previous column, I found the percentage of churners in each country
#     France: 16%
#     Germany: 32%
#     Spain: 17%
# This showed me that Germany is more likely to churn than all the other countries


#VI. COLUMN NAME: "gender":
total = df["gender"].value_counts()
churn_total = df[df["churn"] == 1]["gender"].value_counts()
perc_of_churners1 = (churn_total / total) * 100
print(perc_of_churners1)
print()
#again I used a similar code to find the percentage of churners for male and female:
#     Male: 16% churn
#     Female: 25% churn


#3. After I found the percentages, I created the weight each column had in determining the likeliness of churning for all the accounts.

#I. FINDING GAPS:
# I first found the gap between the most likely value and the least likely value for each column:
#      Active_member: 13% = 27% - 14%
#      balance: 10% = 26% - 16%
#      age: 35% = 43% - 8%
#      product_number: 92% = 100% - 8%
#      country: 16% = 32% - 16%
#      gender: 9% = 25% - 16%

#II. FINDING THE WEIGHT:
# I put the gaps from highest to lowest in a dictionary
gaps = {"Age": 0.35,
        "country": 0.16,
        "Active member": 0.13,
        "balance": 0.10,
        "products_number": 0.92,
        "gender": 0.09}

sum1 = sum(gaps.values())
weight_list = {}

for name, value in gaps.items():
    weight = value / sum1
    weight = round(weight, 4)
    weight_list[name] = weight
# for each column, I divided the sum of the gaps from each columns gap to determine weight.

print(weight_list)
print(sum(weight_list.values()))
# results:
#        Age: 0.2
#        Country: 0.0914
#        Active_member: 0.0743
#        Balance: 0.0571
#        Products_number: 0.5257
#        gender: 0.0514

#now I will use these weights to create my risk scorer in the churn_analysis.py file.
