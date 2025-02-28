import torch
import pickle
from pathlib import Path
from PIL import Image
import numpy as np
from torch.utils.data import Dataset, DataLoader

class CIFAR10_TORCH(Dataset):
    def __init__(self, data_dict, transform=None):
        self.imgs = np.array(data_dict["image"]).astype(np.uint8)
        self.cls = np.array(data_dict["class"]).astype(np.uint8)

    def __len__(self):
        return self.cls.shape[0]

    def __getitem__(self, idx):
        sample = {"rgb_img": torch.tensor, "gray_img": torch.tensor, "cls": torch.tensor}

        if torch.is_tensor(idx):
            idx = idx.tolist()
        img = np.rot90(np.reshape(self.imgs[3], [32, 32, 3], order='F'), k=3)
        img_gray = Image.fromarray(img).convert('L')
        img_gray_np = np.array(img_gray).astype(np.float32).reshape([1, 32, 32])
        img_rgb_np = np.array(img).astype(np.float32).reshape([3, 32, 32])

        sample["rgb_img"] = torch.tensor(img_rgb_np / 255.0)
        sample["gray_img"] = torch.tensor(np.stack([img_gray_np for _ in range(3)], axis=1) / 255.0)
        sample["cls"] = torch.tensor(self.cls[idx])
        
        return sample
    
class CIFAR10(CIFAR10_TORCH):
    def __init__(self, root="./assets/cifar-10-batches-py", splits=[]):
        self.root = Path(root)
        self.splits = splits
        assert self.root.exists()
        
        # indeces for indicating the end of a set
        self.train_idx = None
        self.test_idx = None
        self.val_idx = None

        print("CIFAR-10 directory found!")

    def get_sets(self):
        return self.extract_sets()

    def extract_sets(self):
        """"
        Extract ONLY the data files from the dataset directory
        After storing all data in IMG_DATA, CLS_DATA. We split them to a user-defined
        splits for the each set. 
        """
        def unpickle(file):
            # https://www.cs.toronto.edu/~kriz/cifar.html
            import pickle
            with open(file, 'rb') as fo:
                dict = pickle.load(fo, encoding='bytes')
            return dict
        
        FILES = []
        for file in Path.iterdir(self.root):
            if file.suffix == "":
                FILES.append(file)
        
        # store ALL data  to a numpy array
        IMG_DATA = np.full([len(FILES)*10000, 3*1024], np.nan)
        CLS_DATA = np.full([len(FILES)*10000, ], np.nan)
        for idx, file in enumerate(FILES):
            data_dir = unpickle(file)
            IMG_DATA[idx*10000:(idx+1)*10000] = np.array(data_dir[b"data"])
            CLS_DATA[idx*10000:(idx+1)*10000] = np.array(data_dir[b"labels"])
        
        self.train_idx = [0, len(IMG_DATA)*self.splits[0]//100]

        self.val_idx = [len(IMG_DATA)*self.splits[0]//100, 
                        len(IMG_DATA)*(self.splits[0]+self.splits[1])//100]
        
        self.test_idx = [len(IMG_DATA)*(self.splits[0]+self.splits[1])//100,
                         len(IMG_DATA)]
        train_set = {
            "image": IMG_DATA[self.train_idx[0]: self.train_idx[1]],
            "class": CLS_DATA[self.train_idx[0]: self.train_idx[1]]
        }
        val_set = {
            "image": IMG_DATA[self.val_idx[0]: self.val_idx[1]],
            "class": CLS_DATA[self.val_idx[0]: self.val_idx[1]]
        }
        test_set = {
            "image": IMG_DATA[self.test_idx[0]: self.test_idx[1]],
            "class": CLS_DATA[self.test_idx[0]: self.test_idx[1]]
        }

        return CIFAR10_TORCH(train_set), CIFAR10_TORCH(val_set), CIFAR10_TORCH(test_set)

    def get_dataloaders(self, batch_sizes):
        train_ds, val_ds, test_ds = self.get_sets()

        train_dl = DataLoader(train_ds, batch_size=batch_sizes[0], shuffle=True)
        val_dl = DataLoader(val_ds, batch_size=batch_sizes[1], shuffle=True)
        test_dl = DataLoader(test_ds, batch_size=batch_sizes[2], shuffle=False)

        return train_dl, val_dl, test_dl