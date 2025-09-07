import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title=("Monte Carlo Portfolio Simulator"), layout= "centered" )
st. title("Monte Carlo Portfolio Simulator")
st.markdown("Explore how your investment could grow over time with a Monte Carlo simulation.")

initial_investment = st.number_input("Initial Investment (€)", value=10000)
years = st.slider("Years", 1, 50, 30)
simulations = st.slider("Simulations", 10, 500, 100)

all_paths = []
np.random.seed(42)

for sim in range(simulations):
    balance = initial_investment
    path = [balance]
    for year in range(1, years + 1):
        annual_return = np.random.normal(loc=0.07, scale=0.124)
        balance *= (1+ annual_return)
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

st.subheader(f"Descriptive table of Final Portfolio Values (Year {years})")
st.table(df.style.format("{:,.2f}"))
