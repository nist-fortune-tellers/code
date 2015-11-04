import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



ts = pd.Series(np.random.randn(10000), index=pd.date_range('1/1/2000', periods=10000))
ts = ts.cumsum()
ts.plot(kind = 'scatter')
plt.show()