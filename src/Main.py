import services.transactions as tr
import services.charts as chr
def main():
    ch = int(input("Press 1 for transactions \n 2 for charts menu \n 3 to convert currency \n 4 to exit \n"))
    
    if(ch == 1):
        c1 = int(input("Press 1 to display transaction history \n 2 to make a new transaction \n 3 to exit \n"))
        if(c1 == 1):
            tr.displayhistory()
        if(c1 == 2):
            tr.makeTransaction()
        if(c1 == 3):
            return 0

    elif(ch == 2):
        print("Charts menu")
        c2 = int(input("Press \n 1 to generate pie chart for monthly expenses category wise \n 2 to generate bar graph for comparing expenses between months in a particular year \n 3 to generate line plot for daily expenses \n 4 to exit \n"))
        if(c2 == 1):
            target_month = input("Enter month in MM format: ")
            target_year = input("Enter year in YYYY format: ")
            chr.createPieChart_monthly(target_month, target_year)
        if(c2 == 2):
            target_year = input("Enter the year for which bar graph is to be made: ")
            chr.createBarGraph(target_year)
        
        if(c2 == 3):
            target_date = input("Enter month in YYYY-MM format: ")
            chr.createLinePlot(target_date)

        if(c2 == 4):
            return 0


    elif(ch == 3):
        print("Currency convertor")
    # TODO: Currency conversion code

    elif(ch == 4):
        return 0
    
    else:
        print("Wrong choice, please try again!")
    
    runChoice = input("Press 1 to continue using the app, and 2 to leave: ")
    if(runChoice == "2"):
        return 0
    elif(runChoice == "1"):
        main()
    else:
        print("Wrong choice, please try again!")
        return 0


main()
