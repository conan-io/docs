import os
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def build_documents(version, build_folder):
    for root, _, files in os.walk(build_folder):
        for filename in files:
            if not filename.endswith(".fjson"):
                continue
            abs_path = os.path.join(root, filename)
            with open(abs_path, "r") as f:
                data = json.load(f)
                if not data.get("title"):
                    continue
                title = data["title"]
                slug = data["current_page_name"] + ".html"
                parent_title = data["parents"][0]["title"] if data["parents"] else ""
                html = data["body"]
                element = {"version": version, "title": title, "parent_title": parent_title,
                           "slug": slug, "html": html}
                yield element


class ElasticManager(object):

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.es = Elasticsearch(url)

    def _gendata(self, version, folder):
        data = build_documents(version, folder)
        for doc in data:
            doc["_index"] = "docs"
            doc["_type"] = "docs"
            yield doc

    def index(self, version, folder):
        bulk(self.es, self._gendata(version, folder))

    def search(self, version, keywords):

        body = {
                "from": 0, "size": 5,
                "query": {
                    "bool": {
                       "filter": [
                            {"match": {"version":  version}}
                       ],
                       "should": [
                            {"match": {
                                "html": {
                                    "query": keywords,
                                    "boost": 1
                                }
                            }},
                            {"match": {
                                "title": {
                                    "query": keywords,
                                    "boost": 3
                                }
                            }}
                       ]
                    }
                }
            }
        return self.es.search(index="docs", body=body)


def clean_html(raw_html):
    import re
    clean_r = re.compile('<.*?>')
    clean_text = re.sub(clean_r, '', raw_html)
    return clean_text


def find_single_word(text, word):
    to_show = 100
    indice = text.find(word)
    if not indice:
        return None
    last_index = indice + len(keyword) + to_show
    if last_index > (len(text) - 1):
        last_index = len(text) - 1
    min_index = indice - to_show
    if min_index < 0:
        min_index = 0
    relevant_text = text[min_index: last_index].replace("\n", " ")
    return relevant_text.strip().replace(word, "__{}__".format(word))


def find_relevant_text(html, keywords):

    html = clean_html(html).replace("¶", "")

    # First look for everything
    all = find_single_word(html, keywords)
    if all:
        return all
    else:
        for keyword in keywords.split(" "):
            partial = find_single_word(html, keyword)
            if partial:
                return partial
    return None


if __name__ == "__main__":
    manager = ElasticManager("localhost:9200", "", "")
    # manager.index("1.15", "/home/luism/workspace/docs/_build/json")
    # exit(1)
    keyword = "--build missing"
    data = manager.search("1.15", keyword)
    for result in data["hits"]["hits"]:
        print("***************")
        result = result["_source"]
        parent_title = result.get("parent_title")
        title = result["title"]
        slug = result["slug"]
        relevant_text = find_relevant_text(result["html"], keyword)
        print("{}: {} ('{}') [{}]".format(parent_title, title, relevant_text, slug))
