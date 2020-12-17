# SJTU EE208

'''
Fit a curve with PyTorch.
'''

from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import torch

from models import Naive_NN

NUM_TRAIN_SAMPLES = 200
NUM_TRAIN_EPOCHS = 1000  # try: 100, 1000, 10000, 50000
LEARNING_RATE = 0.01  # try: 1, 0.1, 0.01, 0.001

torch.manual_seed(2020)


def f(x):
    '''
    Actual function (ground truth).
    '''
    return x**2 + 2 * np.sin(x) + np.cos(x - 1) - 5


# Create dataset
class MyDataset(torch.utils.data.Dataset):
    def __init__(self):
        super(MyDataset, self).__init__()
        self.x, self.y = self.generate_data(NUM_TRAIN_SAMPLES)

    def generate_data(self, num):
        # Generate num training data disturbed by noise.
        x = (torch.rand([num, 1]) - 0.5) * 10.0
        y_noise = f(x) + torch.randn([num, 1]) * 3
        return x, y_noise

    def get_all_data(self):
        return self.x.detach(), self.y.detach()

    def __len__(self):
        return NUM_TRAIN_SAMPLES

    def __getitem__(self, index):
        return self.x[index], self.y[index]


model = Naive_NN()
dataset = MyDataset()
dataloader = torch.utils.data.DataLoader(dataset, batch_size=200, shuffle=True)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)


# train
model.train()
for epoch in range(NUM_TRAIN_EPOCHS):
    loss_avg = []
    for x, target_y in dataloader:
        model.zero_grad()  # Reset gradients
        predicted_y = model(x)  # Forward pass
        mse = (predicted_y - target_y) ** 2  # Calc loss (mean squared error)
        loss = torch.mean(mse)
        loss.backward()  # Backward pass (determine the weights' updating direction)
        optimizer.step()  # Apply weight updating with certain learning rate
        loss_avg.append(torch.sum(mse).detach())  # Monitor loss
    print('Epoch [%d/%d], Loss=%f' %
          (epoch + 1, NUM_TRAIN_EPOCHS, sum(loss_avg) / len(dataset)))


# save model
torch.save(model.state_dict(), 'model.pth')


# test curve
model.eval()
with torch.no_grad():
    x = torch.linspace(-5, 5, 50).reshape([50, 1])
    y = model(x)
    plt.plot(x, y, color='y', label='learnt curve')  # learnt curve
    plt.plot(x, f(x), color='r', label='ground-truth curve')  # ground-truth curve
    plt.scatter(*(dataset.get_all_data()), label='training set')  # training set
    plt.legend()
    plt.show()
