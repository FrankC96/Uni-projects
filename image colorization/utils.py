import torch
from tqdm import tqdm, trange
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class Trainer:
    train_dataloader: torch.nn.Module
    val_dataloader: torch.nn.Module
    model:  torch.nn.Module
    loss_crit: torch.nn.Module
    optimizer: torch.optim.Optimizer
    epochs: int
    device: str

    def train(self):
        train_running_loss = 0.0
        for sample in self.train_dataloader:
            rgb_img = sample["rgb_img"].to(self.device)
            gray_img = sample["rgb_img"].to(self.device)
            cls = sample["cls"].to(self.device)

            self.optimizer.zero_grad()

            outputs = self.model(gray_img)

            loss = self.loss_crit(outputs, rgb_img).to(self.device)
            loss.backward()

            self.optimizer.step()

            train_running_loss += loss.item()

        val_running_loss = 0.0
        for sample in self.val_dataloader:
            rgb_img = sample["rgb_img"].to(self.device)
            gray_img = sample["rgb_img"].to(self.device)
            cls = sample["cls"].to(self.device)

            outputs = self.model(gray_img)
            
            loss = self.loss_crit(outputs, rgb_img).to(self.device)
            val_running_loss += loss.item()
    
            return train_running_loss, val_running_loss

    def train_loop(self):
        
        TRAIN_LOSS, VAL_LOSS = [], []
        for epoch in trange(self.epochs):
            train_loss, val_loss = self.train()
            
            TRAIN_LOSS.append(train_loss)
            VAL_LOSS.append(val_loss)

        plt.plot(range(self.epochs), TRAIN_LOSS, "b-o")
        plt.plot(range(self.epochs), VAL_LOSS, "b--o")
        plt.grid()

        plt.savefig("train_val_loss.png")
        print(TRAIN_LOSS[-1], VAL_LOSS[-1])