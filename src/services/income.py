from datetime import date
import csv

data = []

def displayhistory():
    print("Sources of income: ")
    with open("src/services/Income.csv", newline="") as csvfile:
        reader = csv.reader(csvfile) # Here, the reader variable stores the contents of the csv file
        next(reader)
        for row in csvfile:
            print(row)

def makeIncomeRecord(): # Function to make a transaction
    amt = input("Enter the amount of income: ")
    current_date = date.today()
    source = input("Enter the source of income: ")
    data = [amt, current_date, source]
    storeIncome(data)

def storeIncome(data): # Function to store the data in the list to a csv
    with open("src/services/Income.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)