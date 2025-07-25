data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

st.header("データ表示")
st.dataframe(df)
st.table(df)
st.metric(label="売上", value=12345, delta=123)
st.json({'name': 'Alice', 'age': 30})