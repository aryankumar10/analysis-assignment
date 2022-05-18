import pandas as pd
import warnings
from pandas.core.common import SettingWithCopyWarning
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default='browser'
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

# Declaring functions ------------------------------------
def buy(amount, buyAmount, stocks):
    value = 0
    while (value <= (amount-buyAmount)):
        value += buyAmount
        stocks += 1
    amount -= value
    return amount, stocks

def sell(amount, sellAmount, stocks):
    amount += sellAmount*stocks
    stocks = 0
    return amount, stocks

def profit_loss(startMoney, endMoney):
    if endMoney < startMoney:
        return ("Loss : " + str(endMoney - startMoney))
    else:
        return ("Profit : " + str(endMoney - startMoney))


# Importing file ----------------------------------------
exFile = pd.ExcelFile(r"sample_data.xls")
df = exFile.parse()
df.drop("Unnamed: 0", axis=1, inplace=True)


# Creating custom fields --------------------------------
d = []      # Storing date
t = []      # Storing time
r = []      # Storing profit/loss
s = []      # Storing number of stocks currently holding
ca = []     # Storing current amount
for i in range(len(df)):
    d.append((df['date'][i])[:10])
    t.append((df['date'][i])[11:])
    r.append('')
    s.append('')
    ca.append('')
df['date'] = d
df['time'] = t
df['p/f'] = r
df['stocks'] = s
df['current_amount'] = ca


# Start of analysis -------------------------------------
currentAmount = 100000
stocks = 0
i = 0
count = 0
while (i < len(df)):
    currentDate = df['date'][i]
    dayAmount = currentAmount
    
    buyTime = df['time'][i+1]
    buyAmount = df['low'][i+1]
    currentAmount, stocks = buy(currentAmount, buyAmount, stocks)
    df['stocks'][i+1] = stocks
    df['current_amount'][i+1] = currentAmount
    
    sellTime = df['time'][i+23]
    sellAmount = df['high'][i+23]
    currentAmount, stocks = sell(currentAmount, sellAmount, stocks)
    
    pf_res = profit_loss(dayAmount, currentAmount)
    df['p/f'][i+23] = pf_res
    df['stocks'][i+23] = stocks
    df['current_amount'][i+23] = currentAmount
    
    i += 25
    count += 1


# Creating result dataframe to store in result excel file ----
result = pd.DataFrame()
result.index = [i for i in range(count)]
r_d = []
r_r = []

for i in range (23, len(df), 25):
    r_d.append(df['date'][i])
    r_r.append(df['p/f'][i])

result['date'] = r_d
result['result'] = r_r

result.to_excel('result.xlsx')

# Finding maximum profit and loss -----------------------------
findMaxMin = []
for i in range(len(r_r)):
    ele = r_r[i].split(' ')
    findMaxMin.append(float(ele[2]))

print("Max profit = {}\nMax loss = {}\nTotal capital in the end = {}".format(max(findMaxMin), min(findMaxMin), currentAmount))

# Plotting graph for overall data ------------------------------
df_graph = pd.DataFrame()
df_graph['date'] = r_d
df_graph['open'] = ['' for i in range(count)]
df_graph['close'] = ['' for i in range(count)]
df_graph['high'] = ['' for i in range(count)]
df_graph['low'] = ['' for i in range(count)]
i = 0
k = 0
while (i < len(df)):
    df_h = []
    df_l = []
    for j in range(i, i+25):
        df_h.append(df['high'][j])
        df_l.append(df['low'][j])
    df_graph['open'][k] = df['open'][i]
    df_graph['close'][k] = df['close'][i+24]
    df_graph['high'][k] = max(df_h)
    df_graph['low'][k] = min(df_l)
    i += 25
    k += 1
    
fig1 = go.Figure(data=[go.Candlestick(x = df_graph['date'],
                open = df_graph['open'],
                high = df_graph['high'],
                low = df_graph['low'],
                close = df_graph['close'])])
fig1.update_layout(xaxis_rangeslider_visible=False)
fig1.show()
