import matplotlib.pyplot as plt
import numpy as np
import csv
def createPieChart_monthly(target_month, target_year):
    categorytotals = {}

    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date_str = row[1]
            amount = row[0]
            category = row[3]
            
            month = date_str[5:7]
            year = date_str[:4]

            if month == target_month and year == target_year:
                if category not in categorytotals:
                    categorytotals[category] = 0

                categorytotals[category] += float(amount)
        labels = list(categorytotals.keys())
        values = list(categorytotals.values())
        plt.pie(values, labels = labels, autopct="%1.1f%%")
        plt.title("Monthly savings")
        plt.show()
    

def createBarGraph():
    x = {}
    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date = row[1]
            amount = row[0]

            date = date[:7]
            
            if date not in x:
                x[date] = 0
            x[date] += float(amount)

    months = list(x.keys())
    amounts = list(x.values())
    plt.bar(months,amounts)
    plt.show()

def createLinePlot(target_month):
    monthtotals = {}

    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            date_str = row[1]
            amount = row[0]

            month_date_str = date_str[:7]

            if(month_date_str == target_month):
                if date_str not in monthtotals:
                    monthtotals[date_str] = 0

                monthtotals[date_str] += float(amount)

        
        labels = list(monthtotals.keys())
        values = list(monthtotals.values())
        plt.scatter(labels,values)
        plt.plot(labels, values, linestyle= "dashed")
        plt.title("Monthly savings")
        plt.show()
createLinePlot("2024-09")



            