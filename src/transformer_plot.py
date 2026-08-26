import matplotlib.pyplot as plt

transformer_rating = 1000
load = 752.99

remaining = transformer_rating - load

labels = [
    "Used Capacity",
    "Remaining Capacity"
]

values = [
    load,
    remaining
]

plt.figure(figsize=(7, 5))

plt.bar(labels, values)

plt.ylabel("Apparent Power (kVA)")

plt.title("Transformer Loading")

plt.grid(axis="y")

plt.tight_layout()

plt.show()