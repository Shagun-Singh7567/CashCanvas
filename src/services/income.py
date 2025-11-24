from datetime import date
import csv
from rich.console import Console
from rich.table import Table

data = []

def displayhistory():
    table = Table(title="Transactions made")
    table.add_column("Amount", style="green")
    table.add_column("Date")
    table.add_column("Source")
    with open("src/data/Income.csv", newline="") as csvfile:
        reader = csv.reader(csvfile) # Here, the reader variable stores the contents of the csv file
        next(reader)
        for row in csvfile:
            values = row.split(",")
            table.add_row(*values)
    
    console = Console()
    console.print(table)


def makeIncomeRecord(): # Function to make a transaction
    amt = input("Enter the amount of income: ")
    current_date = date.today()
    source = input("Enter the source of income: ")
    data = [amt, current_date, source]
    storeIncome(data)

def storeIncome(data): # Function to store the data in the list to a csv
    with open("src/data/Income.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)