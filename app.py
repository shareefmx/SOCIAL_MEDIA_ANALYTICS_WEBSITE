from flask import Flask, render_template, url_for, request, redirect
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

#Youtube starts here
api_key='AIzaSyCFSEd7xI7IAh4X67Z07dagb0z5odMWjUA'

youtube = build('youtube', 'v3', developerKey=api_key)
def get_channel_stats(youtube, ch_username):
    all_data = []
    request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forUsername=ch_username
        )
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Description = response['items'][i]['snippet']['description'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'])
        all_data.append(data)

    return all_data
#Youtube ends here
#Twitter starts here
api_key = 'z9CREzdGc3vxdmHjFVZ724XeK'
api_key_secret = '5JAED00x8ohda2jn6Bm15Jhb8HQs2KMGOGfLnC8hkLMhnZqpu2'
access_token = '1208139911766925312-6ka8h7pjEdaEWbkSnp6VsTL6GxIHDe'
access_token_secret = 'WKSmnEHYVKXzbvueGlvDMvDjVdm4oj60sV0jlBxmhu2lu'
# Import Tweepy
import tweepy

# Authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
#Twitter ends here

#Trending List
wikiurl="https://en.wikipedia.org/wiki/List_of_most-subscribed_YouTube_channels"
table_class="wikitable sortable jquery-tablesorter"
response=requests.get(wikiurl)

soup = BeautifulSoup(response.text, 'html.parser')
indiatable=soup.find('table',{'class':"wikitable"})

df=pd.read_html(str(indiatable))
df=pd.DataFrame(df[0])

wikiurl1="https://en.wikipedia.org/wiki/List_of_most-followed_Instagram_accounts#:~:text=Most-followed%20accounts%20%20%20%20Rank%20%20,%20%2073.9%20%2022%20more%20rows%20"
table_class1="wikitable sortable jquery-tablesorter"
response1=requests.get(wikiurl1)

soup1 = BeautifulSoup(response1.text, 'html.parser')
indiatable1=soup1.find('table',{'class':"wikitable"})

df1=pd.read_html(str(indiatable1))
df1=pd.DataFrame(df1[0])

wikiurl2="https://en.wikipedia.org/wiki/List_of_most-followed_Facebook_pages#:~:text=Most-followed%20Facebook%20pages%20%20%20%20Rank%20,%20United%20Kingdom%20%2036%20more%20rows%20"
table_class2="wikitable sortable jquery-tablesorter"
response2=requests.get(wikiurl2)

soup2 = BeautifulSoup(response2.text, 'html.parser')
indiatable2=soup2.find('table',{'class':"wikitable"})

df2=pd.read_html(str(indiatable2))
df2=pd.DataFrame(df2[0])

wikiurl3="https://en.wikipedia.org/wiki/List_of_most-followed_Twitter_accounts#:~:text=Most%20followed%20accounts%20on%20Twitter%20%20%20,%20%20113.6%20%2022%20more%20rows%20"
table_class3="wikitable sortable jquery-tablesorter"
response3=requests.get(wikiurl3)

soup3 = BeautifulSoup(response3.text, 'html.parser')
indiatable3=soup3.find('table',{'class':"wikitable"})

df3=pd.read_html(str(indiatable3))
df3=pd.DataFrame(df3[0])

wikiurl4="https://en.wikipedia.org/wiki/List_of_most-followed_TikTok_accounts"
table_class4="wikitable sortable jquery-tablesorter"
response4=requests.get(wikiurl4)

soup4 = BeautifulSoup(response4.text, 'html.parser')
indiatable4=soup4.find('table',{'class':"wikitable"})

df4=pd.read_html(str(indiatable4))
df4=pd.DataFrame(df4[0])

wikiurl5="https://en.wikipedia.org/wiki/List_of_most-followed_Twitch_channels"
table_class5="wikitable sortable jquery-tablesorter"
response5=requests.get(wikiurl5)

soup5 = BeautifulSoup(response5.text, 'html.parser')
indiatable5=soup5.find('table',{'class':"wikitable"})

df5=pd.read_html(str(indiatable5))
df5=pd.DataFrame(df5[0])


data = df[['Rank','Name']]
data1 = df1[['Owner']]
data2 = df2[['Page name']]
#data3 = df3[['Account name']]
dattt=df4.rename(columns={"Owner":"sp"})
data4 = dattt[['sp']]

data5 = df5[['Channel']]
da=pd.concat([data,data1,data2,data4,data5],axis=1)

dst=da.rename(columns={"Name":"ytaccts","Owner":"igaccts","Page name":"fbaccts","Channel":"twaccts","sp":"tikaccts"})
ytaccounts = dst['ytaccts'].head(10)
igaccounts = dst['igaccts'].head(10)
fbaccounts = dst['fbaccts'].head(10)
twaccounts = dst['twaccts'].head(10)
tikaccounts = dst['tikaccts'].head(10)
#Trending List End
@app.route('/', methods=['POST','GET'])

def index():
    if(request.method == 'POST'):
        platform = request.form['platform']
        channelname = request.form['channelname']
        if(platform == 'youtubedetails'):
            return redirect(url_for('youtubedetails', channelname = channelname))
        elif(platform == 'twitterdetails'):
            return redirect(url_for('twitterdetails', accountname = channelname))
        else:
            return "Wrong input"
    else:
        return render_template('indexmain.html')
@app.route('/youtubedetails/<channelname>', methods=['POST','GET'])
def youtubedetails(channelname):
    youtubedata = get_channel_stats(youtube, channelname)
    return render_template('youtubedetails.html', channelname = channelname.upper(), subcount = youtubedata[0]['Subscribers'].upper(), viewcount = youtubedata[0]['Views'].upper(), channeldesc = youtubedata[0]['Description'], vidcount = youtubedata[0]['Total_videos'].upper())


@app.route('/twitterdetails/<accountname>', methods=['POST','GET'])
def twitterdetails(accountname):
    user2 = api.get_user(screen_name=accountname)
    return render_template('twitterdetails.html', handlename = accountname.upper(), acc_desc_tt = user2.description, followcount_tt = user2.followers_count, createdate = (user2.created_at).strftime("%d/%m/%Y"), followingcount_tt = user2.friends_count, contact = user2.url); 

@app.route('/about')
def aboutpage():
    return render_template('about.html')
    
@app.route('/livecount')
def livecounter():
    return render_template('livecount.html')

@app.route('/top')
def toppage():
    return render_template('top.html', ytaccounts=ytaccounts, igaccounts=igaccounts, tikaccounts=tikaccounts, twaccounts=twaccounts, fbaccounts=fbaccounts)

@app.route('/compare')
def comparepage():
    return render_template('compare.html')
    
if __name__ == "__main__":
    app.run(debug=True)