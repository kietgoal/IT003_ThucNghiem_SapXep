import random
import time
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Tăng giới hạn đệ quy để tránh lỗi khi sort 1 triệu phần tử
sys.setrecursionlimit(2000000)

# --- 1. CÀI ĐẶT CÁC THUẬT TOÁN ---

def quick_sort(arr):
    # Dùng Random Pivot để tránh O(n^2) với mảng đã sắp xếp
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

# --- 2. TẠO DỮ LIỆU (10 Dataset) ---
print("dang tao du lieu (1 Trieu phan tu/day)... doi xiu nhe...")
SIZE = 1_000_000
datasets = {}

# 5 Dãy số thực (Float)
# Dãy 1: Tăng dần
datasets['1. Float Asc'] = np.sort(np.random.uniform(-1000, 1000, SIZE))
# Dãy 2: Giảm dần
datasets['2. Float Desc'] = np.sort(np.random.uniform(-1000, 1000, SIZE))[::-1]
# Dãy 3,4,5: Ngẫu nhiên
for i in range(3, 6): datasets[f'{i}. Float Rand'] = np.random.uniform(-1000, 1000, SIZE)

# 5 Dãy số nguyên (Int) - Ngẫu nhiên
for i in range(6, 11): datasets[f'{i}. Int Rand'] = np.random.randint(-10000, 10000, SIZE)

# --- 3. CHẠY THỰC NGHIỆM ---
results = {
    "Dữ liệu": [], "QuickSort": [], "HeapSort": [], 
    "MergeSort": [], "sort (C++)": [], "sort (numpy)": []
}

# Để tiết kiệm thời gian demo, mình sẽ chạy mẫu 10.000 phần tử thôi. 
# KHI NỘP BÀI THẬT: Bạn sửa dòng dưới thành n_run = SIZE (tức 1_000_000)
# Lưu ý: Chạy 1 triệu phần tử với Python thuần sẽ mất khoảng 15-20 phút.
n_run = 10000  # <--- SỬA SỐ NÀY THÀNH SIZE KHI CHẠY THẬT

print(f"\nBat dau chay thu nghiem voi n={n_run}...")
print("-" * 70)

for name, data in datasets.items():
    # Lấy mẫu dữ liệu để chạy
    current_data = data[:n_run]
    row = {"Dữ liệu": name}
    
    # List các thuật toán cần test
    algos = [
        ("QuickSort", quick_sort),
        ("HeapSort", heap_sort),
        ("MergeSort", merge_sort),
        ("sort (C++)", sorted),      # Python native sort (TimSort - C implementation)
        ("sort (numpy)", np.sort)    # Numpy sort
    ]
    
    for algo_name, func in algos:
        # Copy dữ liệu ra mảng mới để không ảnh hưởng mảng gốc
        if algo_name == "sort (numpy)": arr = np.array(current_data)
        else: arr = list(current_data)
            
        start = time.time()
        if algo_name == "HeapSort": func(arr) # In-place
        else: _ = func(arr)
        end = time.time()
        
        # Đổi ra miliseconds (ms) cho giống mẫu báo cáo
        time_ms = round((end - start) * 1000, 2)
        row[algo_name] = time_ms
        print(f"{name} - {algo_name}: {time_ms} ms")
    
    # Lưu vào bảng kết quả
    for key in results:
        if key != "Dữ liệu": results[key].append(row[key])
    results["Dữ liệu"].append(name)

# --- 4. XUẤT BÁO CÁO ---
df = pd.DataFrame(results)
df.to_csv("ket_qua.csv", index=False)
print("\nDa xuat file 'ket_qua.csv' (dung de copy vao bao cao).")

# Vẽ biểu đồ cột (Bar Chart)
df.set_index("Dữ liệu").plot(kind="bar", figsize=(12, 6))
plt.title("Thời gian thực hiện các thuật toán sắp xếp")
plt.ylabel("Thời gian (ms)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart.png")
print("Da xuat file 'chart.png' (dung de chen vao bao cao).")
plt.show()
