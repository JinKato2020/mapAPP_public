import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.header("グラフ・メディア表示")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
st.pyplot(fig)

st.image("https://www.streamlit.io/images/brand/streamlit-logo-light.svg", caption="Streamlit Logo")