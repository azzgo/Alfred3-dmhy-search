#*-* coding:utf-8 *-*
import sys
sys.path.append('./lib')

import json
import requests
from lxml import etree

def search(query):
  try: 
    response = requests.get("http://share.dmhy.org/topics/rss/rss.xml", params={"keyword": query})
    tree = etree.fromstring(response.content)
    items = tree.xpath('//item')
    return outputConventer(items)
  except Exception as err:
    sys.stderr.write(str(err))
    return json.dumps({
      "items": [{
        "title": "未知错误"
      }]
    })

def outputConventer(items):
  if len(items) == 0:
    output = dict(items=[{"title": "查询不到"}])
  else:
    output = dict(items=[
    {
      "title": item.xpath('./title')[0].text, 
      "subtitle": item.xpath('./pubDate')[0].text,
      "arg": item.xpath('./enclosure')[0].get('url'),
      "mods": {
        "cmd": {
          "valid": True,
          "arg": item.xpath('./link')[0].text,
          "subtitle": "open detail page"
        }
      }
    } for item in items])
  
  return json.dumps(output)

if __name__ == '__main__':
  arg = sys.argv[1]
  print search(arg)
