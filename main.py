import random
import time
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.setrecursionlimit(2000000)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1

def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i; l = 2 * i + 1; r = 2 * i + 2
        if l < n and arr[i] < arr[l]: largest = l
        if r < n and arr[largest] < arr[r]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1): heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

SIZE = 1000000
datasets = {}

datasets['1. Float Asc'] = np.sort(np.random.uniform(-1000, 1000, SIZE))
datasets['2. Float Desc'] = np.sort(np.random.uniform(-1000, 1000, SIZE))[::-1]
for i in range(3, 6): datasets[f'{i}. Float Rand'] = np.random.uniform(-1000, 1000, SIZE)

for i in range(6, 11): datasets[f'{i}. Int Rand'] = np.random.randint(-10000, 10000, SIZE)

results = {
    "Dữ liệu": [], "QuickSort": [], "HeapSort": [], 
    "MergeSort": [], "sort (C++)": [], "sort (numpy)": []
}

n_run = 10000

print(f"\nBat dau chay thu nghiem voi n={n_run}...")

for name, data in datasets.items():
    current_data = data[:n_run]
    row = {"Dữ liệu": name}
    
    algos = [
        ("QuickSort", quick_sort),
        ("HeapSort", heap_sort),
        ("MergeSort", merge_sort),
        ("sort (C++)", sorted),
        ("sort (numpy)", np.sort)
    ]
    
    for algo_name, func in algos:
        if algo_name == "sort (numpy)": arr = np.array(current_data)
        else: arr = list(current_data)
            
        start = time.time()
        if algo_name == "HeapSort": func(arr)
        else: _ = func(arr)
        end = time.time()
        
        time_ms = round((end - start) * 1000, 2)
        row[algo_name] = time_ms
        print(f"{name} - {algo_name}: {time_ms} ms")
    
    for key in results:
        if key != "Dữ liệu": results[key].append(row[key])
    results["Dữ liệu"].append(name)

df = pd.DataFrame(results)
df.to_csv("ket_qua.csv", index=False)

df.set_index("Dữ liệu").plot(kind="bar", figsize=(12, 6))
plt.title("Thời gian thực hiện các thuật toán sắp xếp")
plt.ylabel("Thời gian (ms)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart.png")
plt.show()
