#imports
import requests
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch.nn as nn
import torch
from torch.autograd import Variable
import dateutil
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import date, timedelta
import glob
import os

#enable or diable GPU compute
if torch.cuda.is_available():
    device = torch.device('cuda')
    print(torch.cuda.get_device_name(device))
else:
    device = torch.device('cpu')

class RNN(nn.Module):
    def __init__(self, i_size, h_size, n_layers, o_size, tickerName, scaler):
        super(RNN, self).__init__()
        self.tickerName=tickerName
        self.scaler=scaler
        self.rnn = nn.LSTM(
            input_size=i_size,
            hidden_size=h_size,
            num_layers=n_layers,
        )
        self.out = nn.Linear(h_size, o_size)

    def forward(self, x, h_state):
        r_out, hidden_state = self.rnn(x, h_state)
        
        hidden_size = hidden_state[-1].size(-1)
        r_out = r_out.view(-1, hidden_size)
        outs = self.out(r_out)

        return outs, hidden_state

def getTickersSP100():
  LIST_OF_COMPANIES_WIKI = 'https://en.wikipedia.org/wiki/S%26P_100'
  website_url = requests.get(LIST_OF_COMPANIES_WIKI).text
  soup = BeautifulSoup(website_url, "html.parser")
  my_table = soup.find('table',{'class':'wikitable sortable'})
  labels = []
  for row in my_table.tbody.findAll('tr'):
    if len(row.findAll('td'))==0:
      continue
    else:
      first_column=row.findAll('td')[0].contents[0].strip()
      labels.append(first_column)
  return labels

# function checks if the latest dataset exists on disk
# it returns the filename of the dataset to load and if it exists on disk
def checkExistingDataset(tickerName):
  today = date.today()
  # ASSUMPTION: 5 years of data
  tenYearsAgo = today-timedelta(days=365*10)
  filename = tickerName+tenYearsAgo.strftime('%Y%m%d_')\
  +today.strftime('%Y%m%d')+".pkt"
  existingFiles = glob.glob(tickerName+"*")
  fileFound = False
  for file in existingFiles:
    if file==filename:
      fileFound=True
      # found the file, now delete all the other files
    else:
      # delete file
      os.remove(file)
  return fileFound, filename

# function takes the output from checkExistingDataset
# if False, it gets the data from yfinance and saves it as the filename
# then it loads the same parquet and returns it
# if True, it loads the parquet and returns it
def createParquet(onDisk, filename, tickerName):
  if onDisk:
    return pd.read_parquet(filename, columns=['Open'])
  else:
    ticker = yf.Ticker(tickerName)
    data_set = ticker.history(period="10y")
    data_set.to_parquet(filename)
    data_set=pd.read_parquet(filename, columns = ['Open'])
    return data_set

# current ASSUMPTION: we're getting only the last 5 years of data
# this function checks if the following exists in the current directory: tickerNameStartDateEndDate.pkt
# if it exists and the end date matches the current date, it loads it instead.
# if it doesn't exist the function removes the glob tickerName* file and creates it out of new yFinance data
# then it loads the pkt(only the opening price) and starts working on it.
def createTrainTestDataset(tickerName):
  onDisk, fileName = checkExistingDataset(tickerName)
  data_set = createParquet(onDisk, fileName, tickerName)
  train_set, test_set = train_test_split(data_set, test_size=0.2, train_size=0.8, shuffle=False)
  sc = MinMaxScaler(feature_range = (0, 1))
  train_fit = sc.fit(train_set)
  train_scaled = sc.transform(train_set)
  # Creating a data structure with 60 timesteps and 1 output
  x_train = []
  y_train = []
  for i in range(INPUT_SIZE, train_scaled.shape[0]):
    x_train.append(train_scaled[i-INPUT_SIZE:i, 0])
    y_train.append(train_scaled[i, 0])
  x_train, y_train = np.array(x_train), np.array(y_train)
  # Reshaping
  x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
  return x_train, y_train, train_set, test_set, sc

# network hyper parameters
INPUT_SIZE = 60
HIDDEN_SIZE = 64
NUM_LAYERS = 2
OUTPUT_SIZE = 1
learning_rate = 0.001
num_epochs = 100

def createNetwork(tickerName, sc):
  rnn = RNN(INPUT_SIZE, HIDDEN_SIZE, NUM_LAYERS, OUTPUT_SIZE, tickerName, sc).to(device)
  criterion = nn.MSELoss()
  optimizer = torch.optim.Adam(rnn.parameters(), lr=learning_rate)
  hidden_state = None
  return rnn, optimizer, criterion, hidden_state

def trainNetwork(network, optimizer, criterion, hidden_state):
  for epoch in range(num_epochs):
    inputs = Variable(torch.from_numpy(x_train).float()).to(device)
    labels = Variable(torch.from_numpy(y_train).float()).to(device)
    output, hidden_state = network(inputs, hidden_state)
    loss = criterion(output.view(-1), labels)
    optimizer.zero_grad()
    loss.backward(retain_graph=True)                     # back propagation
    optimizer.step()                                     # update the parameters
    print('epoch {}, loss {}'.format(epoch,loss.item()))

def testNetwork(network, x_train, y_train, train_set, test_set, sc, tickerName):
  real_stock_price = test_set.values
  total_set = pd.concat((train_set['Open'], test_set['Open']), axis = 0)
  inputs = total_set[len(total_set) - len(test_set) - INPUT_SIZE:].values
  inputs = inputs.reshape(-1,1)
  inputs = sc.transform(inputs)

  x_test = []
  for i in range(INPUT_SIZE, inputs.shape[0]):
      x_test.append(inputs[i-INPUT_SIZE:i, 0])
  x_test = np.array(x_test)
  x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

  x_train_x_test = np.concatenate((x_train, x_test),axis=0)
  hidden_state = None
  test_inputs = Variable(torch.from_numpy(x_train_x_test).float()).cuda()
  predicted_stock_price, b = network(test_inputs, hidden_state)
  predicted_stock_price = np.reshape(predicted_stock_price.detach().cpu().numpy(), (test_inputs.shape[0], 1))
  predicted_stock_price = sc.inverse_transform(predicted_stock_price)

  real_stock_price_all = np.concatenate((train_set[INPUT_SIZE:], real_stock_price))
  print(real_stock_price_all.shape)
  print(predicted_stock_price.shape)
  # Visualising the results
  plt.figure(1, figsize=(12, 5))
  plt.plot(real_stock_price_all, color = 'red', label = 'Real')
  plt.plot(predicted_stock_price, color = 'blue', label = 'Pred')
  plt.title(tickerName+' Stock Price Prediction')
  plt.xlabel('Time')
  plt.ylabel(tickerName+' Stock Price')
  plt.legend()
  plt.savefig(tickerName+".png", quality=100)

tickers = getTickersSP100()
for tickerNumber, tickerName in enumerate(tickers):
  print(tickerName)
  if tickerName =="BRK.B":
    continue
  if len(glob.glob(tickerName+"*.pt")):
    continue
  print("creating test/train dataset")
  x_train, y_train, train_set, test_set, sc = createTrainTestDataset(tickerName)
  print("creating network")
  network, optimizer, criterion, hidden_state = createNetwork(tickerName, sc)
  print("training network")
  trainNetwork(network, optimizer, criterion, hidden_state)
  print("testing network")
  testNetwork(network, x_train, y_train, train_set, test_set, sc, tickerName)
  torch.save(network.state_dict(), tickerName+".pt")
  # release memory
  del network
  del optimizer
  del criterion
  del hidden_state
  torch.cuda.empty_cache()
