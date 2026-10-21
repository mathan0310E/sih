import torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

torch.manual_seed(0)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
CLASSES = ["T-shirt", "Trouser", "Pullover", "Dress", "Coat",
           "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

tf = transforms.Compose([transforms.ToTensor(),
                         transforms.Normalize((0.5,), (0.5,))])
tr = datasets.FashionMNIST("./data", train=True, download=True, transform=tf)
te = datasets.FashionMNIST("./data", train=False, transform=tf)
trl = DataLoader(tr, batch_size=128, shuffle=True, drop_last=True)
tel = DataLoader(te, batch_size=256)

# ---------------- CNN classifier ----------------
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2))
        self.head = nn.Sequential(nn.Flatten(),
                                  nn.Linear(64 * 7 * 7, 128), nn.ReLU(),
                                  nn.Linear(128, 10))
    def forward(self, x):
        return self.head(self.features(x))

cnn = CNN().to(DEV)
opt = optim.Adam(cnn.parameters(), lr=1e-3)
crit = nn.CrossEntropyLoss()
for ep in range(5):
    cnn.train(); tot = 0.0
    for x, y in trl:
        x, y = x.to(DEV), y.to(DEV)
        opt.zero_grad()
        loss = crit(cnn(x), y)
        loss.backward(); opt.step()
        tot += loss.item() * x.size(0)
    cnn.eval(); correct = 0
    with torch.no_grad():
        for x, y in tel:
            x, y = x.to(DEV), y.to(DEV)
            correct += (cnn(x).argmax(1) == y).sum().item()
    print(f"epoch {ep+1}: loss={tot/len(tr):.4f} "
          f"accuracy={100*correct/len(te):.2f}%")

# ---------------- GAN generator ----------------
class Gen(nn.Module):
    def __init__(self, z=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(z, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, 784), nn.Tanh())
    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

class Disc(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(),
            nn.Linear(784, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 1), nn.Sigmoid())
    def forward(self, x):
        return self.net(x)

G, D = Gen().to(DEV), Disc().to(DEV)
oG = optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
oD = optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
bce = nn.BCELoss()
for ep in range(8):    # lab-scale: fewer epochs on CPU
    for x, _ in trl:
        x = x.to(DEV); n = x.size(0)
        one = torch.ones(n, 1, device=DEV)
        zero = torch.zeros(n, 1, device=DEV)
        oD.zero_grad()
        z = torch.randn(n, 64, device=DEV)
        lD = bce(D(x), one) + bce(D(G(z).detach()), zero)
        lD.backward(); oD.step()
        oG.zero_grad()
        fake = G(torch.randn(n, 64, device=DEV))
        lG = bce(D(fake), one)
        lG.backward(); oG.step()
    if (ep + 1) % 4 == 0:
        print(f"GAN epoch {ep+1}: lossD={lD.item():.3f} lossG={lG.item():.3f}")

with torch.no_grad():
    grid = G(torch.randn(16, 64, device=DEV)).cpu().squeeze(1)
fig, ax = plt.subplots(2, 8, figsize=(12, 3.5))
for i, im in enumerate(grid):
    ax.flat[i].imshow(im, cmap="gray"); ax.flat[i].axis("off")
plt.savefig("fashion_gan.png", dpi=150, bbox_inches="tight")
