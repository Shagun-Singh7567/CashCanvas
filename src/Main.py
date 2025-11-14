
def main():
    ch = int(input("Press 1 to see transaction history, 2 for charts menu, and 3 to convert currency: "))
    if(ch == 1):
        print("Let's review your transaction history")
    # TODO: Code for transaction menu
    elif(ch == 2):
        print("Charts menu")
    # TODO: Code for matplotlib
    elif(ch == 3):
        print("Currency convertor")
    # TODO: Currency conversion code
    else:
        print("Wrong choice, please try again!")
    
main()
