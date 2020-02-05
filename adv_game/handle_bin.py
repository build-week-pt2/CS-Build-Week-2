with open("bin_res.txt") as f:
  arr = [i for i in f.readlines()]
  f.close()

for i in arr:
    print(int(i[0:8], 2))
