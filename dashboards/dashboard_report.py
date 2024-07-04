import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt 
import holoviews as hv
from holoviews import opts

hv.extension('bokeh')

# Load dataset 
df = pd.read_csv("sampledata/sample1k_widata.csv")

# Analyze Status code
df["Status Code"].value_counts().plot(kind="bar")
plt.show()