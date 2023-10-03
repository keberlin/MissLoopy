from emails import *
from localization import *
from mlutils import *

id = 1
pid = 1
filename = PhotoFilename(pid)

EmailNewPhoto(filename, pid, id)
