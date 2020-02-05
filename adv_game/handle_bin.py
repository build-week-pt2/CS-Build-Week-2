with open("binary_file.txt") as f:
  arr = f.read()
  f.close()

codes = [i for i in arr.split('\\n') if len(i) == 8]


with open('secret.ls8', 'w') as f:
    f.write('\n'.join([str(i) for i in codes]) + '\n')