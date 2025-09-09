import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title=("Monte Carlo Portfolio Simulator"), layout= "centered" )
st. title("Monte Carlo Portfolio Simulator📈")
st.markdown("Explore how your investment could grow over time with a Monte Carlo simulation.")

initial_investment = st.number_input("Initial Investment (€)", value=10000)
years = st.slider("Years", 1, 50, 30)
simulations = st.slider("Simulations", 10, 500, 100)

st.subheader("Adjust Portfolio Weights")
stocks_w= st.number_input("Stocks", min_value=0.0, max_value=1.0, value=0.6)
bonds_w=st.number_input("Bonds", min_value=0.0, max_value=1.0, value=0.3)
cryptos_w=st.number_input("Crypto", min_value=0.0, max_value=1.0, value=0.1)
total = stocks_w + bonds_w + cryptos_w
weights =np.array([stocks_w, bonds_w, cryptos_w]) / total

total = stocks_w + bonds_w + cryptos_w

assets = ["Stocks", "Bonds", "Crypto"]
mu=np.array([0.07, 0.03, 0.15])
sigma=np.array([0.15, 0.05, 0.60])
corr= np.array([
    [1,0.2,0.1],
    [0.2,1,-0.05],
    [0.1,-0.05,1]
])
cov = np.outer(sigma, sigma)*corr


if np.isclose(total,1.0, atol=0.001):
    weights= np.array([stocks_w,bonds_w,cryptos_w])

    fig, ax = plt.subplots(figsize=(5,3))
    ax.pie(weights, labels=assets, autopct="%1.1f%%", startangle=90, colors=["#4daf4a","#377eb8","#e41a1c"], wedgeprops={"edgecolor": "Black", "linewidth": 1.5, "linestyle": "solid"}, 
           textprops={"fontsize":9, "fontweight": "bold", "color": "white"})
    ax.set_title("Portfolio Allocation", textprops={"fontsize":12, "fontweight":"bold", "color": "white"})
    st.pyplot(fig)
else:
    st.warning(f"Warning: The total portfolio weight is {total*100:,.2f}%. It needs to sum up to 100%. Normalizing the weights.")
    stocks_w /= total
    bonds_w /= total
    cryptos_w /= total



chart_type = st.selectbox(
    "Choose a chart to display:",
    ["Simulation Paths", "Distribution (Histogram)", "Boxplot", "Cumulative Probability CDF"]
)

all_paths = []
np.random.seed(42)

for sim in range(simulations):
    balance = initial_investment
    path = [balance]
    for year in range(1, years + 1):
        annual_return = np.random.multivariate_normal(mu, cov)
        portfolio_return=np.dot(weights, annual_return)
        balance *= (1+ portfolio_return)
        path.append(balance)
    all_paths.append(path)

all_paths = np.array(all_paths)
final_values=all_paths[:,-1]

mean_final=np.mean(final_values)
median_final=np.median(final_values)
p10_final=np.percentile(final_values,10)
p90_final=np.percentile(final_values,90)
min_final=np.min(final_values)
max_final=np.max(final_values)

stats = {
    "Mean": [mean_final],
    "Median": [median_final],
    "10th %": [p10_final],
    "90th %": [p90_final],
    "Min": [min_final],
    "Max": [max_final]
}

df = pd.DataFrame(stats)

if chart_type == "Simulation Paths":
    fig, ax = plt.subplots(figsize=(10,6))
    for path in all_paths:
        ax.plot(path, alpha=0.5)
    ax.set_title(f"Monte Carlo Simulation of Portfolio growth ({years} years)")
    ax.set_xlabel("Years")
    ax.set_ylabel("Portfolio Value (€)")
    ax.axhline(initial_investment, color="black", linestyle="--", label="Initial Investment")
    ax.legend()

    median_path = np.percentile(all_paths, 50, axis=0)
    p10_path = np.percentile(all_paths, 10, axis=0)
    p90_path = np.percentile (all_paths, 90, axis=0)

    ax.fill_between(range(years+1), p10_path, p90_path, color="lightblue", alpha=0.2, label="10th-90th percentile")
    ax.plot(median_path, color="blue", linewidth=2, label="Median Path")

    st.pyplot(fig)

elif chart_type =="Boxplot":
    fig, ax= plt.subplots()
    ax.boxplot(final_values, vert=False)
    ax.set_title("Boxplot of Final Portfolio Values")
    ax.set_xlabel("Final Value (€)")
    st.pyplot(fig)

elif chart_type =="Distribution (Histogram)":
    fig, ax = plt.subplots()
    ax.hist(final_values, bins =30, color="skyblue", edgecolor="black")
    ax.set_title("Distribution of Final Portfolio Values")
    ax.set_xlabel("Final value (€)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

elif chart_type =="Cumulative Probability CDF":
    sorted_vals = np.sort(final_values)
    cdf= np.arange(1, len(sorted_vals)+1) / len(sorted_vals)
    fig, ax= plt.subplots()
    ax.plot(sorted_vals, cdf, color="Blue")
    ax.set_title("Cumulative Probability of Final Portfolio Value")
    ax.set_xlabel("Final Value (€)")
    ax.set_ylabel("Cumulative Probability")
    st.pyplot(fig)

st.subheader(f"Descriptive table of Final Portfolio Values (Year {years})")
st.table(df.style.format("{:,.2f}"))
