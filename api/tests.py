from time import strptime
from unicodedata import category
from django.test import TestCase

from .documents import NewsDocument
from .models import News
from datetime import datetime

import json

with open("/home/ruizhi.wang/news_ir/api/clean.json", "r") as f:
    data = f.read()

data = json.loads(data)

for element in data:

    tmp_news = News(
        category = element["category"],
        location = element["location"],
        title = element["title"],
        author = element["author"],
        created_time = datetime.strptime(element["create_time"], "%Y-%m-%d %H:%M:%S"),
        content = element["content"],
        image = element["image"]
    )
    try:
        tmp_news.save()
    except Exception as e:
        print(str(e))


# news = News(
#     category = "jobs",
#     location = "singapore",
#     title = "battle for tech talent driving up salaries staff attrition say observers",
#     author = "joanna seow",
#     created_time = datetime.strptime("2022-01-30 05:00:00", "%Y-%m-%d %H:%M:%S"),
#     content = "singapore nurses are in great demand but many particularly those from overseas have called it quits homesick anxious and plain exhausted they are choosing to be with their families over building a career here say hospital colleagues basic care assistant caroline she said a few staff nurses all foreigners have left ng teng fong general hospital s rehabilitation ward in the past year while one has resigned this year there were no resignations at all in 2020 late last year the suspension barring healthcare workers from taking leave overseas was lifted but the rigours of dealing with the healthcare crisis were still too much for some even though they can go back to spend time with the family for one or two weeks when will be the next time they can go back asks ng teng fong general hospital s assistant nurse clinician guo sasa who manages 16 to 17 nurses one has just resigned to return to india when she called home her two year old daughter would not respond which made her very upset says ms guo a malaysian who had not seen his baby since the pandemic started also left last year to spend time with his family the pandemic has not been easy in more ways than one wearing n95 masks can leave nurses with broken skin and a mark on the nose bridge though most take it in their stride she adds senior minister of state for health janil puthucheary said last november that around 1 500 healthcare workers resigned in the first half of 2021 compared with 2 000 annually pre pandemic even mild illness can hit hard as a staff member down with covid 19 can be out of action for many days when in the past medical leave might be just for a day or two for something common like the flu says mr joe ong chief executive of aber care which specialises in healthcare recruitment other nurses resigned for various reasons including long hours and fear of catching covid 19 says mr ong adding that he has seen a trend in the past two years of local nurses who have families leaving their hospital jobs to work at vaccination centres or doctors clinics vaccination centres mean they do not have to work the night shift and the pay is higher and this drew those who were on the verge of quitting he adds apart from nurses basic care and healthcare assistants healthcare institutions also find it challenging to recruit patient service associates psas who screen or bill patients among other tasks a national university polyclinics nup spokesman says there is now a smaller pool of available candidates with many taking up swab assisting and vaccination operations roles which pay a higher hourly rate nup is trying to retain psas by allowing them to move up to be operations executives they can also study to be care coordinators healthcare institutions are working harder at redesigning roles to make them more attractive in a bid to retain staff and draw new ones this includes recruiting help to lessen nurses workloads and if needed hiring temporary workers or volunteers to help out mrs olivia tay group chief human resource officer at the national healthcare group says the cluster tries to increase job satisfaction by automating manual tasks and empowering staff to make decisions when redesigning roles they can be trained to take on different career tracks from clinical and administration to education and research where suitable she says ms rupali gupta talent solutions leader at global hr consultancy mercer in singapore says healthcare institutions can help their staff by streamlining tasks and reducing rote work a way to address burnout is to review the rosters to avoid back to back shifts she adds adding in some countries leading healthcare providers are evaluating flexible schedules and five day work weeks join st's telegram channel here and get the latest breaking news delivered to you read 3 articles and stand to win rewards spin the wheel now mci p 031 10 2021 mci p 032 10 2021 published by sph media limited co regn no 202120748h copyright 2021 sph media limited all rights reserved",
#     image = "https://static1.straitstimes.com.sg/s3fs-public/styles/large30x20/public/articles/2022/01/29/yq-sgwrk-29012022.jpg?VersionId=DvSGAGOq8YS3iQTw.7QI22Hu7OhIG_Yo&itok=OhYB1Ln7" )

# news.save()



# s = NewsDocument.search().query("match", content="great demand")



# for hit in s:
#     print(
#         "News title : {}, content {}".format(hit.title, hit.content)
#     )

# s = NewsDocument.search().count()
# print(s)
# Create your tests here.
from elasticsearch_dsl import Q
from .documents import NewsDocument

# Looks up all the articles that contain `How to` in the title.
query = 'How to'
q = Q(
     'multi_match',
     query=query,
     fields=[
         'title'
     ])
search = NewsDocument.search().query(q)
response = search.execute()

# print all the hits
for hit in search:
    print(hit.title)

query = 'singapowe'  # notice the typo
q = Q(
     'multi_match',
     query=query,
     fields=[
         'title'
     ],
     fuzziness='auto')
search = NewsDocument.search().query(q)
response = search.execute()

# print all the hits
for hit in search:
    print(hit.title)