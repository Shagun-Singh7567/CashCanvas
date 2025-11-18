import matplotlib.pyplot as plt
import csv
def createPieChart_monthly(target_month, target_year):
    categorytotals = {}

    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date_str = row[1].strip()
            amount = row[0]
            category = row[3]

            month = date_str[5:7].strip()
            year = date_str[:4].strip()

            if month == target_month and year == target_year:
                if category not in categorytotals:
                    categorytotals[category] = 0

                categorytotals[category] += float(amount)
        labels = list(categorytotals.keys())
        values = list(categorytotals.values())
        plt.pie(values, labels = labels, autopct="%1.1f%%")
        plt.title("Monthly savings")
        plt.show()



            