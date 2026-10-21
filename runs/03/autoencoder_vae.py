import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

torch.manual_seed(0)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
tf = transforms.ToTensor()
train = datasets.MNIST("./data", train=True, download=True, transform=tf)
test = datasets.MNIST("./data", train=False, transform=tf)
loader = DataLoader(train, batch_size=128, shuffle=True)

# ---------------- plain autoencoder ----------------
class AE(nn.Module):
    def __init__(self, zdim=16):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU())
        self.fc = nn.Linear(32 * 7 * 7, zdim)
        self.fcd = nn.Linear(zdim, 32 * 7 * 7)
        self.dec = nn.Sequential(
            nn.ConvTranspose2d(32, 16, 4, stride=2, padding=1), nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 4, stride=2, padding=1), nn.Sigmoid())
    def forward(self, x):
        h = self.fc(self.enc(x).flatten(1))
        return self.dec(self.fcd(h).view(-1, 32, 7, 7))

ae = AE().to(DEV)
opt = torch.optim.Adam(ae.parameters(), lr=1e-3)
for ep in range(5):
    tot = 0.0
    for x, _ in loader:
        x = x.to(DEV)
        opt.zero_grad()
        loss = F.mse_loss(ae(x), x)
        loss.backward(); opt.step()
        tot += loss.item() * x.size(0)
    print(f"AE epoch {ep+1}: mse={tot/len(train):.5f}")

# ---------------- variational autoencoder ----------------
class VAE(nn.Module):
    def __init__(self, zdim=16):
        super().__init__()
        self.enc = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU())
        self.fc_mu = nn.Linear(32 * 7 * 7, zdim)
        self.fc_lv = nn.Linear(32 * 7 * 7, zdim)
        self.fcd = nn.Linear(zdim, 32 * 7 * 7)
        self.dec = nn.Sequential(
            nn.ConvTranspose2d(32, 16, 4, stride=2, padding=1), nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 4, stride=2, padding=1), nn.Sigmoid())
    def encode(self, x):
        h = self.enc(x).flatten(1)
        return self.fc_mu(h), self.fc_lv(h)
    def reparam(self, mu, lv):
        eps = torch.randn_like(mu)          # reparameterisation trick
        return mu + torch.exp(0.5 * lv) * eps
    def decode(self, z):
        return self.dec(self.fcd(z).view(-1, 32, 7, 7))
    def forward(self, x):
        mu, lv = self.encode(x)
        return self.decode(self.reparam(mu, lv)), mu, lv

def vae_loss(x, xr, mu, lv):
    rec = F.binary_cross_entropy(xr, x, reduction="sum") / x.size(0)
    kl = -0.5 * torch.sum(1 + lv - mu.pow(2) - lv.exp()) / x.size(0)
    return rec + kl, rec, kl

vae = VAE().to(DEV)
optv = torch.optim.Adam(vae.parameters(), lr=1e-3)
for ep in range(5):
    tot = 0.0
    for x, _ in loader:
        x = x.to(DEV)
        optv.zero_grad()
        xr, mu, lv = vae(x)
        loss, _, _ = vae_loss(x, xr, mu, lv)
        loss.backward(); optv.step()
        tot += loss.item() * x.size(0)
    print(f"VAE epoch {ep+1}: loss={tot/len(train):.4f}")

# ---------------- samples and interpolation ----------------
with torch.no_grad():
    z = torch.randn(16, 16, device=DEV)
    grid = vae.decode(z).cpu().squeeze(1)
    a, b = torch.randn(16, device=DEV), torch.randn(16, device=DEV)
    steps = torch.stack([vae.decode((a + t * (b - a)).unsqueeze(0))
                         .cpu().squeeze() for t in torch.linspace(0, 1, 10)])
fig, ax = plt.subplots(2, 8, figsize=(12, 3.5))
for i, im in enumerate(grid):
    ax.flat[i].imshow(im, cmap="gray"); ax.flat[i].axis("off")
plt.savefig("vae_samples.png", dpi=150, bbox_inches="tight")
