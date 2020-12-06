'''Stock Association Rule Mining by William Brown'''

#Imports
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from apyori import apriori

#Parameters
period = '1460d'    #4 years
min_support = 0.005
min_confidence = 0.15
min_lift = 1.5

#Functions
def transCalc(itemList, item):
    result = []
    for i in itemList:
        if i == item:
            result.append(item)
        else:
            result.append(0)
    return result

running = True
while running:
    #User Input
    stockTicker = input('Please enter a stock symbol or 0 to exit:')
    if stockTicker == '0':
        break

    #Read Data
    msft = yf.Ticker(stockTicker)
    #choose how far back to go
    df = msft.history(period=period)
    if len(df.index) == 0:
        continue
    print(df)

    #Columns Avalible: 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'
    #Index = Date

    #Creating Categorical DataFrame
    cat_df = pd.DataFrame()
    #Gain Percentage Calculation
    #Gain % = ((Close-Open)/Close) * 100
    gainPercentage = []
    for i in range(len(df['Open'])):
        gainPerVal = ((df['Close'][i] - df['Open'][i])/df['Close'][i]) * 100
        gainPercentage.append(gainPerVal)

    #Gain Grade Calculation
    #Gain Grade = (A > 2, B > 1, C > 0, D > -1, F <= -1)
    buyGrade = []
    #Frequencies for chi square
    for i in range(len(gainPercentage)):
        if gainPercentage[i] > 2:
            grade = 'A'
        elif gainPercentage[i] > 1:
            grade = 'B'
        elif gainPercentage[i] > 0:
            grade = 'C'
        else:
            grade = 'F'
        buyGrade.append(grade)
    cat_df['Buy Grade'] = buyGrade

    #Month Calculation
    months = []
    for i in range(len(df.index)):
        monthNum = str(df.index[i])[5:7]
        if monthNum == '01':
            month = 'January'
        elif monthNum == '02':
            month = 'February'
        elif monthNum == '03':
            month = 'March'
        elif monthNum == '04':
            month = 'April'
        elif monthNum == '05':
            month = 'May'
        elif monthNum == '06':
            month = 'June'
        elif monthNum == '07':
            month = 'July'
        elif monthNum == '08':
            month = 'August'
        elif monthNum == '09':
            month = 'September'
        elif monthNum == '10':
            month = 'October'
        elif monthNum == '11':
            month = 'November'
        else:
            month = 'December'
        months.append(month)
    cat_df['Month'] = months

    print(cat_df)

    #Plotting Histograms of Features
    fig, axs = plt.subplots(2, tight_layout=True, figsize=(10,10))
    #Buy Grade
    axs[0].hist(cat_df['Buy Grade'], bins=4)
    axs[0].set_title('Buy Grade')

    #Season
    axs[1].hist(cat_df['Month'], bins=12, color='green')
    axs[1].set_title('Month')

    plt.show()

    #Creating Transactional DataFrame
    trans_df = pd.DataFrame()

    for j in ['A', 'B', 'C', 'F']:
        trans_df['{}'.format(j)] = transCalc(cat_df['Buy Grade'], j)
    for k in ['January', 'February', 'March', 'April', 'May', 'June',\
              'July', 'August', 'September', 'October', 'November', 'December']:
        trans_df['{}'.format(k)] = transCalc(cat_df['Month'], k)
    
    print(trans_df)

    #Generating Rules
    #generating list of lists
    transRecords = []
    for i in range(0, len(trans_df.index)):
        trans = []
        for j in trans_df.iloc[i]:
            if j != 0:
                trans.append(j)
        transRecords.append(trans)

    #generating rules
    #Support = frequency of items together/total
    #Confidence = frequency of item 2 in transactions that contain item 1
    #Lift = How much our confidence has increased that item 2 will be purchased given that item 1 was purchased
    association_rules = apriori(transRecords, min_support=min_support, min_confidence=min_confidence, min_lift=min_lift)
    association_results = list(association_rules)

    #eliminating rules < 1 item
    rules = []
    for i in association_results:
        if len(i[0]) >= 2:
            rules.append(i)
        
    print('{} Rules Generated!'.format(len(rules)))

    #Printing Rules
    for item in rules:
        # first index of the inner list
        # Contains base item and add item
        pair = item[0]
        items = [x for x in pair]
        print("Rule: " + items[0] + " -> " + items[1])

        #second index of the inner list
        print("Support: " + str(item[1]))

        #third index of the list located at 0th
        #of the third index of the inner list

        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")

print('Done!')