#!/usr/bin/env python
import sys,os
import pickle
from model import model_judge
import numpy as np
import torch
import torch.nn as nn
import random as rd
from torch.utils.data import DataLoader

learning_rate = 1e-3
batch_size = 128
epochs = 350
loss_fn = nn.CrossEntropyLoss()
model = model_judge

a = pickle.load(open(sys.argv[1],'rb'))
rd.shuffle(a)
N = len(a)
n = N - int(N / 10)

train_data = list()
for x in a[:n]:
    train_data.append( [ torch.Tensor(x[0]),torch.Tensor(x[1]) ] )

test_data = list()
for x in a[n:]:
    test_data.append( [ torch.Tensor(x[0]),torch.Tensor(x[1]) ] )

train_dataloader = DataLoader(train_data, batch_size=batch_size,shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size)

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    loss = 0
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * batch_size + len(X)
            # print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
    return loss

def test_loop(dataloader, model, loss_fn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct +=  (((pred*y).abs()/(pred*y)) == torch.ones(pred.shape)).sum() 

    #test_loss /= num_batches
    #correct /= size
    # print(f"Test Error: \n Accuracy: {correct}/{size}, Avg loss: {test_loss:>8f} \n")
    return(correct,size,test_loss)

loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

os.system("mkdir judge_models")
ofp = open("train.log",'w') 
for t in range(epochs):
    # print(f"Epoch {t+1}\n-------------------------------")
    train_loss = train_loop(train_dataloader, model, loss_fn, optimizer)
    allc,allsize,all_loss = test_loop(train_dataloader, model, loss_fn)
    testc,testsize,test_loss = test_loop(test_dataloader, model, loss_fn)
    allc = int(allc)    
    allsize = int(allsize)    
    all_loss = int(all_loss)    
    testc = int(testc)    
    testsize = int(testsize)    
    test_loss = int(test_loss)    
    train_rate = allc/allsize
    test_rate = testc/testsize
    ofp.write( "\t".join( str(x) for x in (t, train_loss, allc,allsize,all_loss,testc,testsize,test_loss, train_rate, test_rate ) ) )
    ofp.write("\n")
    ofp.flush()
    if t % 20 == 0:
        torch.save(model, f'judge_models/{t}_model_judge.pth')
    

