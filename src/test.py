
print("hleeoooe")
a = 12
b = 14
c = a+ b
print(c)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

arr = [1, 23, 234, 2, 4, 9, 10]
print(bubble_sort(arr))