import torch, torch.nn as nn, torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

torch.manual_seed(0)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
LATENT, BATCH, EPOCHS = 64, 128, 10   # 10 epochs is lab-scale on CPU

# ---- data: scale pixels to [-1, 1] ----
tf = transforms.Compose([transforms.ToTensor(),
                         transforms.Normalize((0.5,), (0.5,))])
train = datasets.MNIST("./data", train=True, download=True, transform=tf)
loader = DataLoader(train, batch_size=BATCH, shuffle=True, drop_last=True)

class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(LATENT, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, 784), nn.Tanh())
    def forward(self, z):
        return self.net(z).view(-1, 1, 28, 28)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 1), nn.Sigmoid())
    def forward(self, x):
        return self.net(x)

G, D = Generator().to(DEV), Discriminator().to(DEV)
optG = optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
optD = optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
bce = nn.BCELoss()
fixed_z = torch.randn(16, LATENT, device=DEV)
hist = {"D": [], "G": []}

for ep in range(EPOCHS):
    dsum = gsum = 0.0
    for real, _ in loader:
        real = real.to(DEV)
        n = real.size(0)
        ones = torch.ones(n, 1, device=DEV)
        zeros = torch.zeros(n, 1, device=DEV)

        # ---- discriminator ----
        optD.zero_grad()
        loss_real = bce(D(real), ones)
        fake = G(torch.randn(n, LATENT, device=DEV))
        loss_fake = bce(D(fake.detach()), zeros)
        lossD = loss_real + loss_fake
        lossD.backward(); optD.step()

        # ---- generator (non-saturating loss) ----
        optG.zero_grad()
        lossG = bce(D(fake), ones)
        lossG.backward(); optG.step()

        dsum += lossD.item(); gsum += lossG.item()
    hist["D"].append(dsum / len(loader))
    hist["G"].append(gsum / len(loader))
    print(f"epoch {ep+1:02d}  lossD={hist['D'][-1]:.4f}  "
          f"lossG={hist['G'][-1]:.4f}")

# ---- sample grid ----
with torch.no_grad():
    samples = G(fixed_z).cpu().squeeze(1)
fig, axes = plt.subplots(4, 4, figsize=(5, 5))
for ax, img in zip(axes.flat, samples):
    ax.imshow(img, cmap="gray"); ax.axis("off")
plt.savefig("gan_samples.png", dpi=150, bbox_inches="tight")
torch.save(G.state_dict(), "generator.pt")
