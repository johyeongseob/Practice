import torch
import torch.nn as nn
import torchvision.datasets as dset
import torchvision.transforms as transforms 
from torch.utils.data import DataLoader

training_epochs = 15                                                                                # parameters
batch_size = 100

root = './data'                                                                                     # parameters
mnist_train = dset.MNIST (root=root, train=True, transform=transforms.ToTensor(), download=True)
mnist_test = dset.MNIST (root=root, train=False, transform=transforms.ToTensor(), download=True)

train_loader = DataLoader(mnist_train, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(mnist_test, batch_size=batch_size, shuffle=False)


dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

linear = torch.nn.Linear(28*28,10,bias=True).to(dev)                                                # MNIST data image of shape 28 * 28 = 784
torch.nn.init.normal_(linear.weight)                                                                # initialization


criterion = torch.nn.CrossEntropyLoss().to(dev)                                                     # Softmax is internally computed.
optimizer = torch.optim.SGD(linear.parameters(), lr=0.01)


for epoch in range(training_epochs+1):
    for i, (imgs, labels) in enumerate(train_loader):
        imgs, labels = imgs.to(dev), labels.to(dev)
        imgs = imgs.view(-1, 28*28)

    outputs = linear(imgs)
    loss    = criterion(outputs, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    _,argmax = torch.max(outputs, 1)
    accuracy = (labels == argmax).float().mean()

    if (i+1) % 100 == 0:
        print('Epoch [{}/{}], Step [{}/{}], Loss: {: .4f}, Accuracy: {: .2f}%'.format(
            epoch+1, training_epochs, i+1, len(train_loader), loss.item(), accuracy.item()* 100))


linear.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for i, (imgs, labels) in enumerate(test_loader):
        imgs, labels = imgs.to(dev), labels.to(dev)
        imgs = imgs.view(-1, 28 * 28)

        outputs =linear(imgs)

        _, argmax = torch.max(outputs, 1) # max()를 통해 최종 출력이 가장 높은 class 선택
        total += imgs.size(0)
        correct += (labels == argmax). sum().item()

    print('Test accuracy for {} images: {: .2f}%'.format(total, correct / total * 100))


# visualization

import matplotlib.pyplot as plt
import random

r = random.randint(0, len(mnist_test) - 1)
X_single_data = mnist_test.test_data[r:r + 1].view(-1, 28 * 28).float().to(device)
Y_single_data = mnist_test.test_labels[r:r + 1].to(dev)

plt.imshow(mnist_test.test_data[r:r + 1].view(28, 28), cmap="Greys", interpolation="nearest")
plt.show()
print("Label: ", Y_single_data.item())
single_prediction = linear(X_single_data)
print("Prediction: ", torch.argmax(single_prediction, 1).item())
