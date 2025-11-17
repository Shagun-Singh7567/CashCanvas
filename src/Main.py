import services.transactions as tr
def main():
    ch = int(input("Press 1 for transactions, 2 for charts menu, 3 to convert currency and 4 to exit: "))
    
    if(ch == 1):
        c1 = int(input("Press 1 to display transaction history, 2 to make a new transaction, and 3 to exit"))
        if(c1 == 1):
            tr.displayhistory()
        if(c1 == 2):
            tr.makeTransaction()
        if(c1 == 3):
            return 0

    elif(ch == 2):
        print("Charts menu")
    # TODO: Code for matplotlib
    elif(ch == 3):
        print("Currency convertor")
    # TODO: Currency conversion code

    elif(ch == 4):
        return 0
    
    else:
        print("Wrong choice, please try again!")
    
main()
