import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

docs = [
    "Introduction to artificial intelligence and intelligent agents",
    "Foundations of machine learning: regression and classification",
    "Deep learning with convolutional and recurrent networks",
    "Natural language processing and text analytics",
    "Computer vision and image understanding",
    "Database management systems and SQL query optimisation",
    "Computer networks and the TCP/IP protocol stack",
    "Operating systems: processes, memory and file systems",
    "Data structures and algorithm design techniques",
    "Web application development with client and server frameworks",
    "Cloud computing and virtualisation fundamentals",
    "Software engineering and agile development practices",
]

model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(docs, normalize_embeddings=True)
print("embedding matrix shape:", emb.shape)

def search(query, k=3):
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = emb @ q                      # cosine similarity
    order = np.argsort(-scores)[:k]
    return [(docs[i], float(scores[i])) for i in order]

for query in ["beginner course on machine learning",
              "how do computers store and retrieve data",
              "building websites with frontend and backend code"]:
    print("=" * 70)
    print("Query:", query)
    for text, score in search(query):
        print(f"  {score:.3f}  {text}")

# ---- keyword baseline for comparison ----
def keyword_search(query, k=3):
    qs = set(query.lower().split())
    scored = [(len(qs & set(d.lower().split())), d) for d in docs]
    return sorted(scored, reverse=True)[:k]

print("\nKeyword baseline:",
      keyword_search("beginner course on machine learning"))

# ---- 2-D visualisation ----
xy = PCA(n_components=2).fit_transform(emb)
plt.figure(figsize=(8, 6))
plt.scatter(xy[:, 0], xy[:, 1])
for (x, y), d in zip(xy, docs):
    plt.annotate(d.split(":")[0][:22], (x, y), fontsize=7)
plt.title("Course embeddings projected to two dimensions")
plt.savefig("embeddings.png", dpi=150, bbox_inches="tight")
