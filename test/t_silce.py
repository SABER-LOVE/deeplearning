import numpy as np



a = "m/0n1vy1h"
print(a[2:])

r1 = ['1','222','3']
r1.sort(key=lambda x:len(x),reverse=True)

print(r1)

y = [[1, 11],
     [2, 3],
     [4, 5],
     [6, 7],
     [8, 9],
     ]
y = np.array(y)
s = 0
e = 3
total_len = len(y)
total_index = total_len * 0.6 + 1
e = int(total_index)
print(e)
reverseIndex = int( total_len - total_index)
print(reverseIndex)
# 正向截取
# 逆向
z = y[s:e] # [ > s and <= e  ]
print(type(z))
print(z)

print(y[:reverseIndex])