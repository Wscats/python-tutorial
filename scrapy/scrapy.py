import requests
r = requests.get('https://search-api.helijia.com/search-api/search/item_query?type=product&hiddenCross=1&city=110100&category=tag_mei_jia&artisanType=1&entryWayId=5&address=%E5%8C%97%E4%BA%AC%E5%B8%82%20&start=140&num=20&offset=140&size=20&pageSize=20&pageNo=7&t=1520845615404')
print(r.content)