# Powerful data structures for data analysis
import pandas as pd

# app framework
import streamlit as st

# High-level plotly wrapper for visualization
import plotly.express as px

####################
# Mainpage
####################
# Set streamlits configurations, add page title and page icon as well as the specification of the screen layout
st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

# title the dashboard
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

####################
# Read in Excel Data
####################
# to prevent streamlit from re running our entire script and loading the dataframe repetitively
# create a function and use the streamlit @cache to store the function to memory
# this will optimize  the apps performance. 

@st.cache
def get_data_from_excel():
# Read in the excel spreadsheet that we will be working with
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000)
    # add 'hour' column to the dataframe
    # convert the column to a datetime object using pandas 'to_datetime()' method
    # format the time into hours minutes seconds and then extract the hour using the dt.hour 
    df["hour"] = pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

####################
# Sidebar
####################
st.sidebar.header("Please Filter Here:")

# create filters on the sidebar based on city, customer type and gender
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Create a query based on filters 'city', 'customer_type', and 'gender'
# use @ to refer to the variable
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

st.dataframe(df_selection)


####################
# Top KPIs
####################
# Display the 'total_sales', 'average_rating', 'star_rating', and 'average_sale_by_transaction'

# total_sales is the sum of the 'total' column, returning an int number without decimal values.
total_sales = int(df_selection["Total"].sum())
# round the mean of the 'rating' column by 1 decimal, this will be 'average_rating'
average_rating = round(df_selection["Rating"].mean(), 1)
# Illustrate the rating score by using the star emoji
# average the rating to the nearest round number by using int
star_rating = ":star:" * int(round(average_rating, 0))
# calculate the 'average_sale_by_transaction' by applying the .mean() method to the 'Total' column
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# Create columns to display the KPI more visually appealing
# Display the 'total_sales', 'average_rating' and 'average_sale_by_transaction'
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with col2:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with col3:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

# seperate by using the '---' markdown method
st.markdown("---")

####################
# Visual analysis
####################
# Sales

# Aggregate the average sales of the 'Product line' using the 'groupby()' and 'sum()' methods 
# filter the data by the 'Total' sales as this is all we are interested in
# Sort the values by 'Total', by default lowest to the highest number is listed
sales_by_product_line = (
    df.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
# use the plotly express library to plot the data 
fig_product_sales = px.bar(
    sales_by_product_line,
    # horizantal barchart
    orientation = "h",
    x = 'Total',
    y = sales_by_product_line.index,
    title = "<b>Sales By Product Line</b>",
    # set the color of the bars and multiply the hexadecimal code with the length of the 'sales_by_product_line'
    color_discrete_sequence = ["#0083B8"] * len(sales_by_product_line),
    template = "plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# Sales by Hour [Bar Chart]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]

# use the plotly express library to plot the data 
fig_hourly_sales = px.bar(
    sales_by_hour,    
    x = sales_by_hour.index,
    y = 'Total',
    title = "<b>Sales By Hour</b>",
    # set the color of the bars and multiply the hexadecimal code with the length of the 'sales_by_hour'
    color_discrete_sequence = ["#0083B8"] * len(sales_by_hour),
    template = "plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
)

# plot the charts side by side
col1, col2 = st.columns(2)
col1.plotly_chart(fig_hourly_sales, use_container_width=True)
col2.plotly_chart(fig_product_sales, use_container_width=True)

####################
# Hide Streamlit Style
####################

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
            