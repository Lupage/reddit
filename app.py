import base64
import pandas as pd
import requests
import streamlit as st

def get_reddit_search(search_query, sort_by):
	base_url = f'https://www.reddit.com/search.json?q={search_query}&limit=100'
	request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
	r = request.json()["data"]["children"]
	subreddit_name = ["r/"+str(element['data']['subreddit']) for element in r]
	title = [element['data']['title'] for element in r]
	post = [element['data']['selftext'].replace("\n", " ") for element in r]
	comments = [element['data']['num_comments'] for element in r]
	upvotes = [element['data']['score'] for element in r]
	url = ["https://www.reddit.com"+str(element['data']['permalink']) for element in r]
	results = list(zip(subreddit_name, title, post, comments, upvotes, url))
	df = pd.DataFrame(results)
	df.columns = ["Subreddit", "Title", "Post", "Number of comments", "Upvotes", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

def get_subreddit_search(subreddit, search_query, sort_by):
	base_url = f'https://www.reddit.com/r/{subreddit}/search.json?q={search_query}&restrict_sr=on&limit=100'
	request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
	r = request.json()["data"]["children"]
	subreddit_name = ["r/"+str(element['data']['subreddit']) for element in r]
	title = [element['data']['title'] for element in r]
	post = [element['data']['selftext'].replace("\n", " ") for element in r]
	comments = [element['data']['num_comments'] for element in r]
	upvotes = [element['data']['score'] for element in r]
	url = ["https://www.reddit.com"+str(element['data']['permalink']) for element in r]
	results = list(zip(subreddit_name, title, post, comments, upvotes, url))
	df = pd.DataFrame(results)
	df.columns = ["Subreddit", "Title", "Post", "Number of comments", "Upvotes", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

def get_subreddit(subreddit, sort_by):
	base_url = f'https://www.reddit.com/r/{subreddit}.json?&limit=100'
	request = requests.get(base_url, headers = {'User-agent': 'yourbot'})
	r = request.json()["data"]["children"]
	subreddit = ["r/"+str(element['data']['subreddit']) for element in r]
	title = [element['data']['title'] for element in r]
	post = [element['data']['selftext'].replace("\n", " ") for element in r]
	comments = [element['data']['num_comments'] for element in r]
	upvotes = [element['data']['score'] for element in r]
	url = ["https://www.reddit.com"+str(element['data']['permalink']) for element in r]
	results = list(zip(subreddit, title, post, comments, upvotes, url))
	df = pd.DataFrame(results)
	df.columns = ["Subreddit", "Title", "Post", "Number of comments", "Upvotes", "URL"]
	df.sort_values(by=sort_by, ascending=False, inplace=True)
	df = df.reset_index(drop=True)
	df.index = df.index + 1
	return df

st.set_page_config(layout="wide", page_title="Reddit Scraper")

st.header("An App by Francis Angelo Reyes of [Lupage Digital](https://www.lupagedigital.com/?utm_source=streamlit&utm_medium=referral&utm_campaign=reddit)")

st.subheader("***Reddit Scraper***", anchor=None)

with st.form(key='Subreddit search'):
	col1, col2 = st.columns(2)
	with col1:
		search_query = st.text_input(value="god of war", label='Search query. If empty, it scrapes a subreddit').replace(" ","%20")
		subreddit = st.text_input(value="Playstation", label='Subreddit. For example, r/Playstation is Playstation. If empty, it scrapes entire Reddit')
	with col2:	
		sort_by = st.selectbox("Sort By", ("Number of comments", "Upvotes"))
	
	submit_button = st.form_submit_button(label='Submit')

if submit_button:
	if len(search_query) == 0 and len(subreddit) == 0:
		st.warning("Please enter a search query or subreddit")		
	elif len(search_query) > 0 and len(subreddit) == 0:
		df = get_reddit_search(search_query, sort_by)
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode()).decode()
		st.markdown('### **⬇️ Download output CSV File **')
		href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click.)"""
		st.markdown(href, unsafe_allow_html=True)
		st.table(df)
	elif len(subreddit) > 0 and len(search_query)== 0:
		df = get_subreddit(subreddit, sort_by)
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode()).decode()
		st.markdown('### **⬇️ Download output CSV File **')
		href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click.)"""
		st.markdown(href, unsafe_allow_html=True)
		st.table(df)
	else:
		df = get_subreddit_search(subreddit, search_query, sort_by)
		csv = df.to_csv()
		b64 = base64.b64encode(csv.encode()).decode()
		st.markdown('### **⬇️ Download output CSV File **')
		href = f"""<a href="data:file/csv;base64,{b64}">Download CSV File</a> (Right-click and save as "filename.csv". Don't left-click.)"""
		st.markdown(href, unsafe_allow_html=True)
		st.table(df)
