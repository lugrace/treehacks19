
from tweepy import OAuthHandler
import queue
import tweepy

import http.client
import json

# TWITTER API CREDENTIALS
consumer_key = 'oeaiWzPmHLx20OLsp5g5QPFbw'
consumer_secret = '3b55vyoax4DIkhvTX6KUGP9sSjhxo9ZxOfpUUtsz6tpPVfZfw3'
access_token = '926830219356340225-z2qjfLCagnxp99AL4UhzQ94LUQbo9RR'
access_secret = 'uX5IWIi0ERKLySSQEYIVOSIcjEuHCmJlPwEK2zSLLLgGk'

# acronym dictionary

f = open("college_acronyms.txt", 'r')
colleges = {}
line = f.readline()
while line != "":
    line = line.split(' - ')
    fullname = line[1][:-1].split(', ')
    for x in fullname:
        colleges[x] = line[0]
    line = f.readline()

input_word = 'Cornell University'
acronym_word = colleges[input_word]
tweet_data = queue.Queue()

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q=input_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
    #print(tweet.text)
    tweet_data.put(tweet.text)
for tweet in tweepy.Cursor(api.search, q=acronym_word, count=3500, result_type="recent", include_entities=True, lang="en").items(100):     # the values inside items defines how many searches we want
    #print(tweet.text)
    tweet_data.put(tweet.text)
#---
#analyzing tweets
accessKey = 'f15920f0f61947c29e12c7f1f12174f9'
uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/sentiment'
path2 = '/text/analytics/v2.0/keyPhrases'

def GetSentiment (documents):
    "Gets the sentiments for a set of documents and returns the information."

    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read()

def GetKeyWords (documents):
    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = http.client.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path2, body, headers)
    response = conn.getresponse ()
    return response.read()
tweetlist = []

x = 1
while tweet_data.empty() == False:
    tweetlist.append({'id': str(x), 'language': 'en', 'text': str(tweet_data.get())})
    x+=1
documents = { 'documents': tweetlist }

percentresults = eval(GetSentiment(documents))
avpercent = 0.0
positive = 0.0
negative = 0.0
sortnums = []
for z in percentresults["documents"]:
    avpercent += z["score"]
    sortnums.append([z["score"], z['id']])
    if z["score"] < 0.01:
        negative+=1
    elif z["score"] > 0.8:
        positive+=1
sortnums = sorted(sortnums)
examplebad = [tweetlist[int(sortnums[0][1])-1]['text'], tweetlist[int(sortnums[1][1])-1]['text'], tweetlist[int(sortnums[2][1])-1]['text']]
examplegood = [tweetlist[int(sortnums[-1][1])-1]['text'], tweetlist[int(sortnums[-2][1])-1]['text'], tweetlist[int(sortnums[-3][1])-1]['text']]
avpercent = avpercent/len(percentresults["documents"])
negative = negative/len(percentresults["documents"])
positive = positive/len(percentresults["documents"])

#print(examplebad)
#print(examplegood)
#print(avpercent, negative, positive)

#keywords
wordqueue = queue.Queue()
keywords = eval(GetKeyWords(documents))
badfile = open("badfile.txt", 'r')
badline = badfile.readline()
badwords = {}
while badline != "":
    badline.strip()
    badline = badline[:-1]
    badwords[badline] = 0
    badline = badfile.readline()
goodfile = open("goodfile.txt", 'r')
goodline = goodfile.readline()
goodwords = {}
while goodline != "":
    goodline.strip()
    goodline = goodline[:-1]
    goodwords[goodline] = 0
    goodline = goodfile.readline()
#print(goodwords)
#print(badwords)
for w in keywords["documents"]:
    for wordphrase in w["keyPhrases"]:
        for word in wordphrase.split(" "):
            wordqueue.put(word.lower())

while wordqueue.empty() != True:
    inbad = False
    findword = wordqueue.get()
    #print(findword)
    for x in badwords.keys():
        if x in findword:
            badwords[x] +=1
            inbad = True
            break
    if inbad != True:
        for x in goodwords.keys():
            if x in findword:
                goodwords[x] +=1
                break
badstringinput = ""
for x in badwords.keys():
    badstringinput += (x+" ")*badwords[x]
goodstringinput = ""
for x in goodwords.keys():
    goodstringinput += (x+" ")*goodwords[x]
print(badstringinput)
print(goodstringinput)

# b'{"documents":[{"score":0.5,"id":"1"},{"score":0.5,"id":"2"},{"score":0.5,"id":"3"},{"score":0.99576568603515625,"id":"4"},{"score":0.5,"id":"5"},{"score":0.5,"id":"6"},{"score":0.5,"id":"7"},{"score":0.5,"id":"8"},{"score":0.5,"id":"9"},{"score":0.5,"id":"10"},{"score":0.5,"id":"11"},{"score":0.98195630311965942,"id":"12"},{"score":0.5,"id":"13"},{"score":0.5,"id":"14"},{"score":0.00027474761009216309,"id":"15"},{"score":0.99983382225036621,"id":"16"},{"score":0.90085983276367188,"id":"17"},{"score":0.030197322368621826,"id":"18"},{"score":0.99983382225036621,"id":"19"},{"score":0.98927581310272217,"id":"20"},{"score":0.9661867618560791,"id":"21"},{"score":0.98956900835037231,"id":"22"},{"score":0.97514176368713379,"id":"23"},{"score":0.5,"id":"24"},{"score":0.99990856647491455,"id":"25"},{"score":0.5,"id":"26"},{"score":0.5,"id":"27"},{"score":0.5,"id":"28"},{"score":0.5,"id":"29"},{"score":0.027403503656387329,"id":"30"},{"score":0.5,"id":"31"},{"score":0.5,"id":"32"},{"score":0.5,"id":"33"},{"score":0.80331122875213623,"id":"34"},{"score":0.99983382225036621,"id":"35"},{"score":0.5,"id":"36"},{"score":0.79018628597259521,"id":"37"},{"score":0.031860858201980591,"id":"38"},{"score":0.99973177909851074,"id":"39"},{"score":0.5,"id":"40"},{"score":0.5,"id":"41"},{"score":0.5,"id":"42"},{"score":0.98795533180236816,"id":"43"},{"score":0.5,"id":"44"},{"score":0.5,"id":"45"},{"score":0.5,"id":"46"},{"score":0.5,"id":"47"},{"score":0.5,"id":"48"},{"score":0.99983382225036621,"id":"49"},{"score":0.085767030715942383,"id":"50"},{"score":0.99983382225036621,"id":"51"},{"score":0.98927581310272217,"id":"52"},{"score":0.99983382225036621,"id":"53"},{"score":0.5,"id":"54"},{"score":0.029460877180099487,"id":"55"},{"score":0.5,"id":"56"},{"score":0.030197322368621826,"id":"57"},{"score":0.99974209070205688,"id":"58"},{"score":0.5,"id":"59"},{"score":0.5,"id":"60"},{"score":0.5,"id":"61"},{"score":0.036564737558364868,"id":"62"},{"score":0.99985039234161377,"id":"63"},{"score":0.5,"id":"64"},{"score":0.5,"id":"65"},{"score":0.99971729516983032,"id":"66"},{"score":0.93538093566894531,"id":"67"},{"score":0.9845585823059082,"id":"68"},{"score":0.5,"id":"69"},{"score":0.5,"id":"70"},{"score":0.5,"id":"71"},{"score":0.5,"id":"72"},{"score":0.5,"id":"73"},{"score":0.99971729516983032,"id":"74"},{"score":0.5,"id":"75"},{"score":0.5,"id":"76"},{"score":0.5,"id":"77"},{"score":0.5,"id":"78"},{"score":0.5,"id":"79"},{"score":0.5,"id":"80"},{"score":0.5,"id":"81"},{"score":0.5,"id":"82"},{"score":0.5,"id":"83"},{"score":0.5,"id":"84"},{"score":0.5,"id":"85"},{"score":0.5,"id":"86"},{"score":0.95794278383255,"id":"87"},{"score":0.5,"id":"88"},{"score":0.5,"id":"89"},{"score":0.5,"id":"90"},{"score":0.5,"id":"91"},{"score":0.96196854114532471,"id":"92"},{"score":0.5,"id":"93"},{"score":0.5,"id":"94"},{"score":0.5,"id":"95"},{"score":0.5,"id":"96"},{"score":0.5,"id":"97"},{"score":0.5,"id":"98"},{"score":0.5,"id":"99"},{"score":0.5,"id":"100"},{"score":0.5,"id":"101"},{"score":0.78485512733459473,"id":"102"},{"score":3.2514333724975586E-05,"id":"103"},{"score":0.5,"id":"104"},{"score":0.010401070117950439,"id":"105"},{"score":0.5,"id":"106"},{"score":0.99989914894104,"id":"107"},{"score":0.5,"id":"108"},{"score":0.98123776912689209,"id":"109"},{"score":0.5,"id":"110"},{"score":0.5,"id":"111"},{"score":0.5,"id":"112"},{"score":0.78485512733459473,"id":"113"},{"score":0.5,"id":"114"},{"score":0.98855149745941162,"id":"115"},{"score":0.5,"id":"116"},{"score":0.78485512733459473,"id":"117"},{"score":0.81321215629577637,"id":"118"},{"score":0.981331467628479,"id":"119"},{"score":0.99953246116638184,"id":"120"},{"score":0.5,"id":"121"},{"score":0.5,"id":"122"},{"score":0.5,"id":"123"},{"score":0.94708085060119629,"id":"124"},{"score":0.91334795951843262,"id":"125"},{"score":0.24706166982650757,"id":"126"},{"score":0.9961668848991394,"id":"127"},{"score":0.99989914894104,"id":"128"},{"score":0.5,"id":"129"},{"score":0.00040596723556518555,"id":"130"},{"score":0.8765716552734375,"id":"131"},{"score":0.5,"id":"132"},{"score":0.5,"id":"133"},{"score":0.5,"id":"134"},{"score":0.80535906553268433,"id":"135"},{"score":0.5,"id":"136"},{"score":0.5,"id":"137"},{"score":0.5,"id":"138"},{"score":0.98794162273406982,"id":"139"},{"score":0.91334795951843262,"id":"140"},{"score":0.5,"id":"141"},{"score":0.5,"id":"142"},{"score":0.5,"id":"143"},{"score":0.5,"id":"144"},{"score":0.5,"id":"145"},{"score":0.02687680721282959,"id":"146"},{"score":0.99993294477462769,"id":"147"},{"score":0.97770053148269653,"id":"148"},{"score":0.5,"id":"149"},{"score":0.12884187698364258,"id":"150"},{"score":0.99949896335601807,"id":"151"},{"score":0.8765716552734375,"id":"152"},{"score":0.5,"id":"153"},{"score":0.5,"id":"154"},{"score":0.0095052421092987061,"id":"155"},{"score":0.87046492099761963,"id":"156"},{"score":0.5,"id":"157"},{"score":1.6391277313232422E-06,"id":"158"},{"score":0.9669797420501709,"id":"159"},{"score":0.5,"id":"160"},{"score":0.5,"id":"161"},{"score":0.5,"id":"162"},{"score":4.1365623474121094E-05,"id":"163"},{"score":1.6391277313232422E-06,"id":"164"},{"score":0.5,"id":"165"},{"score":0.99262285232543945,"id":"166"},{"score":0.97372043132781982,"id":"167"},{"score":0.85726678371429443,"id":"168"},{"score":0.18477606773376465,"id":"169"},{"score":0.5,"id":"170"},{"score":0.00013101100921630859,"id":"171"},{"score":0.85726678371429443,"id":"172"},{"score":0.5,"id":"173"},{"score":0.97372043132781982,"id":"174"},{"score":0.5,"id":"175"},{"score":0.5,"id":"176"},{"score":0.9669797420501709,"id":"177"},{"score":0.5,"id":"178"},{"score":0.5,"id":"179"},{"score":0.010572522878646851,"id":"180"},{"score":0.03321152925491333,"id":"181"},{"score":0.9614100456237793,"id":"182"},{"score":0.024915039539337158,"id":"183"},{"score":0.5,"id":"184"},{"score":0.5,"id":"185"},{"score":0.5,"id":"186"},{"score":0.5,"id":"187"},{"score":0.5,"id":"188"},{"score":0.5,"id":"189"},{"score":0.00027474761009216309,"id":"190"},{"score":0.98823952674865723,"id":"191"},{"score":0.01024666428565979,"id":"192"},{"score":0.8765716552734375,"id":"193"},{"score":0.5,"id":"194"},{"score":0.03321152925491333,"id":"195"},{"score":0.5,"id":"196"},{"score":0.5,"id":"197"},{"score":0.98158979415893555,"id":"198"},{"score":0.99949896335601807,"id":"199"},{"score":0.5,"id":"200"}],"errors":[]}'
