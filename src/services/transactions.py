from datetime import date
import csv
from rich.console import Console
from rich.table import Table

data = []

def displayhistory(): # Displaying transaction history
    table = Table(title="Transactions made")
    table.add_column("Amount", style="green")
    table.add_column("Date")
    table.add_column("Description")
    table.add_column("Category")

    with open("src/services/Transactions.csv", newline="") as csvfile:
        reader = csv.reader(csvfile) # Here, the reader variable stores the contents of the csv file
        next(reader)
        for row in csvfile:
            values = row.split(",")
            table.add_row(*values)
    
    console = Console()
    console.print(table)

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




