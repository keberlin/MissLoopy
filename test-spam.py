import spam, fileinput

for line in fileinput.input():
  print spam.MaskEverything(line),
