import warnings
import torch
from model import Model
from dataset import CIFAR10

from utils import *
warnings.filterwarnings("ignore", message=".*This will likely lead to incorrect results due to broadcasting.*")
if __name__ == "__main__":
    DEVICE = ["cuda" if torch.cuda.is_available() else "cpu"][0]
    LR = 1E-5
    M = 0.9
    EPOCHS = 10
    MODEL = Model().to(DEVICE)
    DATASET = CIFAR10(splits=[80, 10, 10])

    TRAIN_DATALOADER, VAL_DATALOADER, TEST_DATALOADER = DATASET.get_dataloaders(batch_sizes=[64, 10, 10])

    CRITERION = torch.nn.MSELoss().to(DEVICE)
    OPTIMIZER = torch.optim.Adam(MODEL.parameters(), lr=LR)

    TRAINER = Trainer(TRAIN_DATALOADER, VAL_DATALOADER, MODEL, CRITERION, OPTIMIZER, EPOCHS, DEVICE)
    TRAINER.train_loop()