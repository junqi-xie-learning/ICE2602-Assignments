# SJTU EE208

'''
Train CIFAR-10 with PyTorch.
'''

import os

import torch
import torchvision
import torchvision.transforms as transforms

# Data pre-processing, DO NOT MODIFY
print('==> Preparing data..')
transform_train = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)

testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False)

classes = ("airplane", "automobile", "bird", "cat",
           "deer", "dog", "frog", "horse", "ship", "truck")


def train(model, criterion, optimizer, epoch):
    model.train()
    train_loss = 0
    correct = 0
    total = 0
    for batch_idx, (inputs, targets) in enumerate(trainloader):
        optimizer.zero_grad()
        outputs = model(inputs)
        '''
        The outputs are of size [128x10].
        128 is the number of images fed into the model 
        (Yes, we feed a certain number of images into the model at the same time, 
        instead of one by one.)
        For each image, its output is of length 10.
        Index i of the highest number suggests that the prediction is classes[i].
        '''
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        # print('Epoch [{}] Batch [{}/{}] Loss: {:.3f} | Traininig Acc: {:.3f} ({}/{})'.format(
        #     epoch, batch_idx + 1, len(trainloader), train_loss / (batch_idx + 1),
        #     100. * correct / total, correct, total))
    print('Epoch [{}] | Traininig Acc: {:.3f} ({}/{})'.format(
        epoch, 100. * correct / total, correct, total))


def test(model, criterion, epoch):
    print('==> Testing...')
    model.eval()
    with torch.no_grad():
        ##### TODO: calc the test accuracy #####
        # Hint: You do not have to update model parameters.
        #       Just get the outputs and count the correct predictions.
        #       You can turn to `train` function for help.
        correct = 0
        total = 0
        for batch_idx, (inputs, targets) in enumerate(testloader):
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
        acc = 100. * correct / total
        ########################################
    # Save checkpoint.
    print('Test Acc: {}'.format(acc))
    print('Saving...')
    state = {
        'net': model.state_dict(),
        'acc': acc,
        'epoch': epoch,
    }
    if not os.path.isdir('checkpoint'):
        os.mkdir('checkpoint')
    torch.save(state, './checkpoint/ckpt_{}_acc_{}.pth'.format(epoch, acc))
