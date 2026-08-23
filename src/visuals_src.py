import matplotlib.pyplot as plt
import numpy as np

#1st chart: Churners in each category of risk
plt.figure()
categories = np.array(["Low risk", "Medium risk", "High risk"])
scores = np.array([3.0, 13.42, 52.45])

plt.title("% of Churners in each category")
plt.xlabel("Risk categories")
plt.ylabel("Churners in %")
plt.ylim(0, 100)

for i, score in enumerate(scores):
    plt.text(i, score + 1, f"{score}%", ha="center")

plt.bar(categories, scores, color=["green", "orange", "red"],
                            edgecolor="black")
plt.savefig("../Visualizations/churn_by_risk_tier.png")

#2nd graph: Churn rate by # of products
plt.figure()
product_num = np.array(["One", "Two", "Three", "Four"])
churn_rate = np.array([28, 8, 83, 100])

plt.title("Churn rate by # of products")
plt.xlabel("# of products")
plt.ylabel("churners in %")
plt.ylim(0, 100)

for i, rate in enumerate(churn_rate):
    plt.text(i, rate + 1, f"{rate}%", ha="center")

plt.bar(product_num, churn_rate, color=["yellow", "green", "orange", "red"],
                                 edgecolor="black")
plt.savefig("../Visualizations/churn_by_products.png")

#3rd graph: Churn rate by Age
plt.figure()
age_range = np.array(["18-32", "32-37", "37-44", "44-92"])
churn_rate = np.array([8, 10, 19, 43])

plt.title("Churn rate by Age")
plt.xlabel("Age range by spread")
plt.ylabel("Churners in %")
plt.ylim(0, 100)

for i, score in enumerate(churn_rate):
    plt.text(i, score + 1, f"{score}%", ha="center")

plt.bar(age_range, churn_rate, color=["green", "yellow", "orange", "red"],
                               edgecolor="black")
plt.savefig("../Visualizations/churn_by_age.png")

#4th graph: Churn rate by Country
plt.figure()
country = np.array(["France", "Germany", "Spain"])
churn_rate = np.array([16, 32, 17])

plt.title("Churn rate by Country")
plt.xlabel("Countries")
plt.ylabel("Churners in %")
plt.ylim(0, 100)

for i, score in enumerate(churn_rate):
    plt.text(i, score + 1, f"{score}%", ha="center")

plt.bar(country, churn_rate, color=["green", "red", "yellow"],
                             edgecolor="black")
plt.savefig("../Visualizations/churn_by_country.png")