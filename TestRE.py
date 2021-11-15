import re

import pandas as pd

p = re.compile('^FILE|HINT')


for str in tmpDF.columns[666:] :
    a = p.findall(str)
    print(a)

a = pd.DataFrame([p.findall(str) for str in tmpDF.columns[666:]])