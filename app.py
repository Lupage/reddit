import base64
import pandas as pd
import requests
import streamlit as st

def get_reddit(subreddit, limit, sort_by):
	base_url = f'https://www.reddit.com/r/{subreddit}.json?limit={limit}'
	request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
	r = request.json()['data']['children']
	title = [element['data']['title'] for element in r]
	post = [element['data']['selftext'].replace("\n", " ") for element in r]
	comments = [element['data']['num_comments'] for element in r]
	score = [element['data']['score'] for element in r]
	url = ["https://www.reddit.com"+str(element['data']['permalink']) for element in r]
	results = list(zip(title, post, comments, score, url))
	df = pd.DataFrame(results)
	df.columns = ["Title", "Post", "Number of comments", "Score", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

st.set_page_config(layout="wide", page_title="Reddit Scraper")
st.header("***Reddit Scraper***", anchor=None)
with st.form(key='my_form'):
	subreddit = st.text_input(label='Subreddit')
	limit = st.text_input(label='Limit: 1-100')
	sort_by = st.selectbox("Sort By", ("Number of comments", "Score"))
	submit_button = st.form_submit_button(label='Submit')

if submit_button:
	if len(subreddit) == 0:
		st.warning("Please enter a subreddit")		
	else:
		df = get_reddit(subreddit, limit, sort_by)
		st.table(df)
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode()).decode()
		st.markdown('### **⬇️ Download output CSV File **')
		href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click.)"""
		st.markdown(href, unsafe_allow_html=True)
