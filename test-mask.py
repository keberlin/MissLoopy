import fileinput

import mask

lines = []
for line in fileinput.input():
    lines.append(line)

print(mask.MaskEverything("".join(lines)))
