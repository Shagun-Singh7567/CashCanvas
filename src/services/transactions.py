from datetime import date
import csv

data = []

def displayhistory(): # Displaying transaction history
    print("Transactions made: ")
    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile) # Here, the reader variable stores the contents of the csv file
        next(reader)
        for row in csvfile:
            print(row)

def makeTransaction(): # Function to make a transaction
    amt = int(input("Enter the amount withdrawn: "))
    current_date = date.today()
    print(current_date)
    reason = input("Enter the purpose of making the transaction: ")
    category = input("Enter the category of the transaction: ")
    data = [amt, current_date, reason, category]

    storeTransaction(data)

def storeTransaction(data): # Function to store the data in the list to a csv
    with open("src/services/Transactions.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)




