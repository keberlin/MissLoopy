import fileinput

import mask

lines = []
for line in fileinput.input():
  lines.append(line.decode('utf-8','ignore'))

print mask.MaskEverything(''.join(lines)).encode('utf-8')
