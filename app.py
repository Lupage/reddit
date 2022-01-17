import base64
import pandas as pd
import requests
import streamlit as st

def get_reddit(subreddit,limit,sort_by):
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
	df.columns = ["Title", "Post", "Number of comments", "Upvotes", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

def get_search(subreddit,limit,sort_by):
	base_url = f'https://www.reddit.com/r/{subreddit}/search.json?q={search_query}&restrict_sr=on&limit=1{limit}'
	request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
	r = request.json()["data"]["children"]
	title = [element['data']['title'] for element in r]
	post = [element['data']['selftext'].replace("\n", " ") for element in r]
	comments = [element['data']['num_comments'] for element in r]
	upvotes = [element['data']['score'] for element in r]
	url = ["https://www.reddit.com"+str(element['data']['permalink']) for element in r]
	results = list(zip(title, post, comments, upvotes, url))
	df = pd.DataFrame(results)
	df.columns = ["Title", "Post", "Number of comments", "Upvotes", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

st.set_page_config(layout="wide", page_title="Reddit Scraper")

col1, col2 = st.columns(2)
col1.header("***Reddit Scraper***", anchor=None)
col2.subheader("An App by Francis Angelo Reyes of [Lupage Digital](https://www.lupagedigital.com/?utm_source=streamlit&utm_medium=referral&utm_campaign=reddit)")

with st.form(key='my_form'):
	subreddit = st.text_input(label='Subreddit')
	limit = st.text_input(label='Limit: 1-100')
	sort_by = st.selectbox("Sort By", ("Number of comments", "Upvotes"))
	submit_button_one = st.form_submit_button(label='Submit')

st.header("***Reddit Search Scraper***", anchor=None)
with st.form(key='my_forms'):
	subreddit = st.text_input(label='Subreddit')
	search_query = st.text_input(label='Search query').replace(" ","%20")
	limit = st.text_input(label='Limit: 1-100')
	sort_by = st.selectbox("Sort By", ("Number of comments", "Upvotes"))
	submit_button_two = st.form_submit_button(label='Submit')

if submit_button_one:
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

if submit_button_two:
	if len(subreddit) == 0:
		st.warning("Please enter a subreddit")		
	else:
		df = get_search(subreddit, limit, sort_by)
		st.table(df)
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode()).decode()
		st.markdown('### **⬇️ Download output CSV File **')
		href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click.)"""
		st.markdown(href, unsafe_allow_html=True)
