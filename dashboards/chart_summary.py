# Summary of Charts
import pandas as pd
import pandas as pd 
import panel as pn
import hvplot.pandas
import holoviews as hv
import numpy as np
import seaborn as sns 
import ast
import sys

from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c
from math import pi

# Create the dashboard interface 
hv.extension('bokeh')

pn.extension(sizing_mode="stretch_width")

# Load the relevant data 
df_lists = pd.read_html("sampledata/sample1k_widata_summary.html")
# print(len(df_lists))

# inspect the first dataframe 
# print(df_lists[1]) # A pie chart will be plotted
compare_wallet_type_df = df_lists[1]
print(compare_wallet_type_df)

# print(df_lists[2]) # can be added as a table in the dashboard 

# print(df_lists[3]) # can also be added as table 

# print(df_lists[4])

# print(df_lists[6])

# Get the dashboards 
# **Set up the environment**

# CREATE DATASET TO TEST THIS 
# Create sample data
df = pd.read_csv("sampledata/sample1k_widata.csv")
print(df.head())

# Status Overview using Bokeh for Pie Chart
status_counts = df['Status Code'].value_counts().reset_index()
status_counts.columns = ['Status Code', 'Count']
status_counts['angle'] = status_counts['Count'] / status_counts['Count'].sum() * 2 * pi
status_counts['color'] = Category20c[len(status_counts)]

p = figure(height=350, title="Status Code Distribution", toolbar_location=None,
           tools="hover", tooltips="@Status Code: @Count", x_range=(-0.5, 1.0))

p.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Status Code', source=status_counts)

p.axis.axis_label = None
p.axis.visible = False
p.grid.grid_line_color = None

# Layout the dashboard
dashboard = pn.Column(
    pn.pane.Markdown("# Wallet Dashboard"),
    pn.Row(p),
    # pn.Row(balance_hist, balance_vs_transactions),
    # pn.Row(spend_bar),
    # pn.Row(hodler_line, activity_vs_engagement),
    # pn.Row(velocity_box)
)

# Display the dashboard
dashboard.show()

sys.exit(1)


# plots are made based on the selected columns
def create_plot(column):
    return df.hvplot.line(x='x', y=column, title=f'Plot of {column} vs x')
    # return df.hvplot.pie(df_lists[1])

# Create a dropdown widget for selecting the column to plot
column_select = pn.widgets.Select(name='Select column', options=['y', 'z'], value='y')


# Bind the create_plot function to the column_select widget
interactive_plot = pn.bind(create_plot, column_select)

# DASHBOARD LAYOUT
dashboard = pn.Column(
    pn.pane.Markdown("# Test Dashboard"),
    column_select,
    interactive_plot
)

# Test a pie chart separately
print("GOT IT NOW!")
from matplotlib import pyplot as plt
df_lists[1].plot(kind="pie", subplots=True)
plt.show()

# Display the dashboard
dashboard.show()