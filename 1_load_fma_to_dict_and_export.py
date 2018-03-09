import DataIO
import sys
from datetime import datetime

start_time = datetime.now()

try:
    filename = sys.argv[1]
except IndexError:
    print('Please add an owl to import.')
    exit()

doc = DataIO.parse_owl(filename)
DataIO.write_dict_gz(doc, filename)

elapsed_time = datetime.now() - start_time
print('total time: {}'.format(elapsed_time))
