# Before You Run
- This model was trained in google colab using an NVIDIA T4 and the notebook is not meant to be run in dev.edu as it will take too many resources and crash
- It can be run on your own machine, but if you don't have your environment set up to use your GPU for training it'll take a rediculous amount of time to train
   
- However, you can copy and run this notebook in google colab if you wish to. Make sure you have the T4 GPU (free) enabled in Notebook settings before you start your runtime.
- There is a simple tutorial notebook on how to do this if you want to run this notebook:
    - https://colab.research.google.com/notebooks/gpu.ipynb
 
### Info & Stats:
- EfficientNetB0_CIFAR10.keras trained on CIFAR10, a 10 class CV dataset which can be read about here:
    - https://www.cs.toronto.edu/~kriz/cifar.html
- 50,000 training images
- 10,000 testing images
- Test accuracy of 90.6%
- Using one NVIDIA T4 Tensor Core GPU offered for free by Google, training on 50,000 images and 10 classes took 7.3 minutes
