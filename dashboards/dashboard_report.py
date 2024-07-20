import pandas as pd 
import numpy as np
import hvplot.pandas  # noqa
import hvplot.dask  # noqa
# from matplotlib import pyplot as plt
import panel as pn
import plotly.express as px
import io

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
                 title="Composition of Bots, Non-bots",
                 width=350, height=350,
                 hole=0.5)
plot_1.update_layout(showlegend=False,
                     margin=dict(l=0, r=50, t=50, b=50),
                     annotations=[dict(text=f"{df.shape[0]}<br>WALLETS", 
                                       showarrow=False, 
                                       font_size=25)])

# Plot 2 - TOKEN GATING 
## Chart ideas
    # - Distribution of total Balance - row 1
    # - Wallets with top balances(top 10) - row 2
    # - Wallets with least balances(bottom 5) - row 2

## Distribution of Total Balance
plot_2a = px.histogram(df, x="Total Balance", nbins=100,
                       title="TOKEN GATING - Distribution of Total Balance",
                       width=1500, height=400)
plot_2b = px.box(df, y="Total Balance",
                 title="TOKEN GATING - Distribution of Total Balance")

## Top Balances in a bar chart
top_balances_df = df[["Wallet Address", "Is Bot", "Total Balance"]]\
    .sort_values(by="Total Balance", ascending=False)[:10].reset_index(drop=True)

plot_2c = px.bar(top_balances_df, 
                 x="Total Balance", y="Wallet Address", 
                 color="Is Bot", orientation='h',
                 title="TOKEN GATING - Top 10 Balances",
                 height=350)

## Low Balances in a bar chart
low_balances_df = df[["Wallet Address", "Is Bot", "Total Balance"]]\
    .sort_values(by="Total Balance", ascending=True)[:50].reset_index(drop=True)

plot_2d = px.bar(low_balances_df, 
                 x="Total Balance", y="Wallet Address", 
                 color="Is Bot", orientation='h',
                 title="TOKEN GATING - Bottom 50 Balances",
                 height=350)

# Plot 3 - Is about personalization
## The effect of Hodling against the total balance - scatter chart
plot_3a = px.scatter(df,
                    x="Hodler Score", y="Total Balance",
                    color="Is Bot")

## Regenerate the box plot by removing the outliers
def calculate_fences(df, category):
    """
    Removes the outliers from the data set like extreme high balances 
    or low balances in the wallets
    - Returns a clean dataset with no outliers
    """
    category_data = df[category]
    Q1 = np.percentile(category_data, 25)
    Q3 = np.percentile(category_data, 75)
    IQR = Q3 - Q1
    lower_fence = Q1 - (1.5 * IQR)
    upper_fence = Q3 + (1.5 * IQR)
    return lower_fence, upper_fence

lower_fence, upper_fence = calculate_fences(df, "Total Balance")
clean_df = df[(df["Total Balance"]>=lower_fence)&(df["Total Balance"]<=upper_fence)]

# Replot the plot_3a
plot_3b = px.scatter(clean_df,
                    x="Hodler Score", y="Total Balance",
                    color="Is Bot", trendline="ols",
                    width=1500)
iwallet_data = clean_df.interactive()


# SIDE BAR WIDGETS
## Add a short title
short_title = pn.pane.Markdown("# Lorem Ipsum")
## Add a short guide``
short_explanation = pn.pane.Markdown("""
The standard chunk of Lorem Ipsum used since the 1500s is reproduced 
below for those interested. Sections 1.10.32 and 1.10.33 from "de 
Finibus Bonorum et Malorum" by Cicero are also reproduced in their 
exact original form, accompanied by English versions from the 1914 
translation by H. Rackham.
""")
## Allow the user to choose a file 
# Create a file input widget
file_input = pn.widgets.FileInput(name='Upload wallet data', accept=".csv")
## Add a pie chart - plot_1
plot_1_title = pn.pane.Markdown("## BOT AUDIT")
footer_note = pn.pane.Markdown("Powered by THIRDWAVES lab")
## Include a company logo

# File input events

## Define a function to handle file upload and update the data
def load_data(event):
    file = event.new
    if file is not None:
        data = pd.read_csv(io.BytesIO(file))
        #update_dashboard(data)
        print("UPDATED FILE INPUT!!!")

file_input.param.watch(load_data, 'value')

# Create a new dashboard outlook 
## TAB 1
bot_audit_tab = pn.Column(
    plot_2a,
    pn.Row(plot_2c, plot_2d)
    )
other_tab = pn.Column(
    plot_3b,
    iwallet_data
    )

tabs = pn.Tabs(("Bot Audit", bot_audit_tab),
               ("Other tab", other_tab))

## Create the outlook now
template = pn.template.FastListTemplate(
    title = "WALLET QUICK ANALYSIS",
    sidebar = [
        short_title,
        short_explanation,
        pn.pane.Markdown("## UPLOAD A FILE"),
        file_input,
        # file_chooser,
        plot_1_title,
        plot_1,
        footer_note
        ],
    main = [tabs],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)

# template.show()
template.servable()