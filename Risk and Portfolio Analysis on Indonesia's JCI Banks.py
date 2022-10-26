#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import date
from nsepy import get_history as gh
import googlefinance as gfc
plt.style.use('fivethirtyeight')
import plotly.graph_objs as go
get_ipython().run_line_magic('matplotlib', 'inline')

from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import yfinance as yf


# Defining the companies and other parameters

# In[2]:


stocksymbols=['BBCA.JK', 'BBRI.JK', 'BMRI.JK', 'BBNI.JK', 'BDMN.JK', 'MAYA.JK']
start_date = date(2017,10,14)
end_date = date.today()
print(end_date)
print(f"You have {len(stocksymbols)} assets in your porfolio" )


# ## Fething the Data

# In[3]:


data=yf.download(stocksymbols, start_date, end_date)['Adj Close']


# Principles:
# 1. Maximize return for a given level of risk.
# 2. Minimize risk for a given level of return.

# ## Analysis 

# Plotting the adjusted close price as the closing price has been adjusted to reflect the stock's value after taking account any corporate actions.

# In[4]:


data.plot(figsize=(10,7))
plt.legend()
plt.title("Adjusted Close Price of Top Tier JCI Banks", fontsize=16)
plt.ylabel('Price', fontsize=12)
plt.xlabel('Year', fontsize=12)
plt.grid(which="major", color='k', linestyle='-.', linewidth=0.01)
plt.show()


# In terms of asset, the biggest bank in Indonesia as follows:
# 1. BMRI
# 2. BMRI
# 3. BBCA
# 4. BBNI
# .....
# 
# It is interesting to note here that the highest to lowest adjusted stock price of the banks:
# 1. BMRI
# 2. BBNI
# 3. BBCA
# 4. BBRI
# ....

# ### Correlation Matrix

# Correlation matrix to see the relationship amongst banks

# In[5]:


correlation_matrix=data.corr(method='pearson')
correlation_matrix


# In[6]:


fig2=plt.figure()
sb.heatmap(correlation_matrix,xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns,
cmap='YlGnBu', annot=True, linewidth=0.5)
print('Correlation between Stocks in our portfolio')
plt.show(fig2)


# The financial system is similar to a web, meaning that institutions depend on each other. If a bank goes bankrupt, the whole financial system will panic. Thus, the government inject a bank when there is a problem.

# From the above, I guess BBCA and BBRI obtain the highest correlation. Maybe, both banks have intense transactions. According to news, both banks are approaching Alipay. BBRI targets SME's while BBCA targets large corporations. 
# 
# Bank Maya has a negative relationship with other banks, so does BDMN. This is interesting, I need to dig deep into their annual report as to why these two banks have negative correlations with the other 4. But maybe they could be used to offset the risk of other banks for our portofolio.   
# 
# Note: There could many reasons why, but deeper research has to be conducted. This is just my guess from reading the news.

# ### Risk and Return

# we will use the difference of daily adjusted closing price to analyse the returns. 

# In[7]:


daily_return=data.pct_change(1)
daily_return.dropna(inplace=True)
daily_return


# In[18]:


print('Daily Returns')
fig, ax=plt.subplots(figsize=(15,8))

for i in daily_return.columns.values :
    ax.plot(daily_return[i], lw =2 ,label = i)
    
ax.legend( loc='upper right', fontsize=10)
ax.set_title('volatility in Daily Simple Return')
ax.set_xlabel('Date')
ax.set_ylabel('Daily Simple Returns')
plt.show(fig)


# Based on the above graph, Bank Maya is the most volatile and followed by BBRI.The least volatile is either BBCA or BMRI. 

# In[16]:


print('Average Daily returns(%) of stocks in our portfolio')
avg_daily=daily_return.mean()
print(avg_daily)


# Well, the number is quite low and it seems like Bank Maya is really risky, but we will analyse further.

# #### Risk

# Box Plot

# In[20]:


daily_return.plot(kind="box", figsize=(20,10), title="Risk Box Plot")


# It is difficult to view the volatility on the previous graph. However, we can see it clearly now that BBCA is the least volatile followed by BMRI, while Bank Maya have a relatively unsual box plot and alot of outliers.
# 
# Next, we need to calculate the standard deviation to see the numerical comparison.

# In[26]:


print('Annualized Standard Deviation (Volatility(%), 252 trading days) of stocks in portfolio')
print(daily_return.std()*np.sqrt(252)*100)


# It is actually BBRI on the second place after BBCA. BBCA is quite well-known and private owned bank, while BBRI, BMRI, and BBNI are partially state-owned banks.

# #### Calculating RAR (Risk Adjusted Return)

# RAR is calculated by dividing return with the risk. This implies for every 1% of risk, how many percent of return will we get.

# In[31]:


avg_daily/(daily_return.std()*np.sqrt(252))*100


# The higher the value of the RAR, the better it is. Thus, BBCA is the most preffered, followed by BMRI. 

# ### Cumulative Returns

# In[33]:


daily_cummulative_return=(daily_return+1).cumprod()
daily_cummulative_return


# In[47]:


print('Cummulative Returns')
fig, ax=plt.subplots(figsize=(18,8))

for i in daily_cummulative_return.columns.values:
    ax.plot(daily_cummulative_return[i], lw=2, label=i)
    
ax.legend(loc='upper left', fontsize=12)
ax.set_title('Daily Cummulative Returns/Growth of Investment')
ax.set_xlabel('Date')
ax.set_ylabel('Growth of Returns of Each Investment')
plt.show(fig)


# Based on the above graph, *BBCA* was the most consistent bank with gradual increase and for the last nearly two years, has the highest cummulative return. Either *BDMN* or BBRI followed after. *Bank Maya* experienced the largest drop. My humble speculation is because of the scandal that happened in 2020 involving Maya and Jiwasraya (insurance company). Now, the company's value is gradually decreasing.
