import fileinput

import spam

for line in fileinput.input():
  print spam.MaskEverything(line),
