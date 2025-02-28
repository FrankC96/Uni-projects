### This is a university project for colorizing a grayscale image to color using autoencoders.
---
Starting with the data we will be using the Cifar-10 dataset which consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images. [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html)

We will be splitting the data as 40000 training images, 10000 validation images and 10000 test images. We need the validation set to check for overfitting during the training process and we leave the test set for introducing the model to actual unseen data.

