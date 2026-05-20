import os

files = [f"raw/ordenes_medicas/ordenes_{i:02d}.csv" for i in range(1, 31)]

os.makedirs("manifests/run_2", exist_ok=True)
os.makedirs("manifests/run_3", exist_ok=True)

groups_2 = {
    "worker_a.txt": files[:15],
    "worker_b.txt": files[15:]
}

groups_3 = {
    "worker_a.txt": files[:10],
    "worker_b.txt": files[10:20],
    "worker_c.txt": files[20:]
}

for name, group in groups_2.items():
    with open(f"manifests/run_2/{name}", "w") as f:
        f.write("\n".join(group))

for name, group in groups_3.items():
    with open(f"manifests/run_3/{name}", "w") as f:
        f.write("\n".join(group))

print("Manifiestos creados")
