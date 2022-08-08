import datetime
from datetime import date
import pandas as pd
import numpy as np

datetime = datetime.datetime.now()
datetime = datetime.strftime("%Y-%m-%d_%H-%M-%S")
print("Today's date: " + str(datetime))

rand = np.random.randint(0,1000)

row = [datetime, rand]

df = pd.DataFrame(row)

df.to_csv('data/'+str(datetime)+'.csv')