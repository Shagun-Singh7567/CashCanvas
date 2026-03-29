# CashCanvas
## Overview
CashCanvas is a simple budget tracker CLI app which helps users store and view transactions and income in csv files, and view their spending habits as well as gain AI insights on it.
Built using Python, CashCanvas focuses on simplicity, speed, and zero-stress budgeting.

## Features
Add, Edit & Delete Transactions – Keep your money flow clean and aesthetic.

Automatic Category Suggestion - Instead of selecting manually, ask AI to suggest you what the category should be.

Category-wise Expense Tracking – Transactions are stored category wise, so the 

Monthly & Weekly Summaries – See spending patterns as charts.

Beautiful Matplotlib Charts – Visualize your finances like a pro.

CSV Persistence – Your data stays safe between sessions.

AI Assistant - Suggests budgeting tips and gives spending insights based on the data.

## Technologies & Tools Used
Python 3.13.7

Matplotlib – For plotting the transactions.

CSV File Storage – Lightweight local database.

CustomTkinter - For UI

LiquidAI: LFM2.5-1.2B-Instruct - API Key for AI models

## Steps to Install & Run
1. Clone the Repository
Run the following commands on the git bash terminal:<br>
    git clone https://github.com/Shagun-Singh7567/CashCanvas
2. Install dependancies
On the terminal, run the following commands to install the required libraries:<br>
    pip install matplotlib<br>
    pip install rich <br>
    pin install customtkinter
3. Run the App<br>
    python cashcnvas_app.py


## Instructions for Testing
Make sure you have test data or sample CSVs in the /data folder.

Test manually by:

1. Adding sample transactions and income records

2. Viewing transactions and income records

3. Opening charts

4. Checking if data persists after restart

5. Check if AI outputs are proper

## Screenshots
![Dashboard](/assets/Dashboard.png)
![Create Transaction](/assets/Transaction-Made.png)
![View Transactions](/assets/Transaction-View.png)
![Bar Graph](/assets/BarGraph-Visual.png)
![Pie Chart](/assets/PieChart-Visual.png)
![Line Plot](/assets/LinePlot-Visual.png)
![Create Income Record](/assets/Income-Made.png)
![View Income](/assets/Income-View.png)
![Budget Tips](/assets/Budget%20Tips.png)
![Spending Insights](/assets/Spending%20Insights.png)


