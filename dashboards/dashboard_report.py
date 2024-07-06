import pandas as pd 
import numpy as np
import hvplot.pandas  # noqa
import hvplot.dask  # noqa
from matplotlib import pyplot as plt
import panel as pn
import plotly.express as px

hvplot.extension('matplotlib')

# Load the required dataset
df =  pd.read_csv("sampledata/sample1k_widata.csv")

"""
TO DO - PLOTTING
- Create a pie/bar chart for bot shield. This will help the user identify how many bots and non bots ar
- Find a good plot for token gating - 
-  
"""

# Plot_1 -  a bar chart to count Bots and non bots - BOT SHIELD
bot_shield_df = df["Is Bot"].value_counts().reset_index()

plot_1 = px.pie(bot_shield_df, 
                 values='count', names='Is Bot',
                 title="Bot Shield - Composition of Bots and Non-bots")


# # Plot_2 - Histogram of total balance
# plot_2 = df["Total Balance"].hvplot.hist()

# # Plot_3 - Scatter Plot of Total Balance vs Transaction Count:
# plot_3 = df.hvplot.scatter(x="Total Balance", y="Transaction Count")

# Plot_4 - Heatmap of Total Balance vs Transaction Count segmented by Status Code
# PASS 

# Plot_5 - Bar Chart of Spend and Spend Games
# PASS

# Create the dashboard outlook 
template = pn.template.FastListTemplate(
    title="WALLET QUICK ANALYSIS",
    main = [plot_1,],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)

# template.show()
template.servable()