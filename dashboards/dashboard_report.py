import pandas as pd 
import numpy as np
import hvplot.pandas  # noqa
import hvplot.dask  # noqa
from matplotlib import pyplot as plt
import panel as pn

hvplot.extension('matplotlib')

# Load the required dataset
df =  pd.read_csv("sampledata/sample1k_widata.csv")

# Plot_1 -  a bar chart to count status codes 
status_code_df = df["Status Code"].value_counts().reset_index()

plot_1 = status_code_df.hvplot.bar(x="Status Code", y="count")

# Plot 2- Histogram of total balance
plot_2 = df["Total Balance"].hvplot.hist()

# Create the dashboard outlook 
template = pn.template.FastListTemplate(
    title="WALLET QUICK ANALYSIS",
    main = [plot_1, plot_2],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)

# template.show()
template.servable()