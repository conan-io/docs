import os
import json
import re

import boto3
import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth


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

    def __init__(self, host, region):
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, "es")

        es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        self.es = es

    def _gendata(self, version, folder):
        data = build_documents(version, folder)
        for doc in data:
            doc["_index"] = "docs"
            doc["_type"] = "docs"
            yield doc

    def create_index(self):
        doc = """
{
    "settings": {
        "analysis": {
          "analyzer": {
            "htmlStripAnalyzer": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": ["standard","lowercase"],
              "char_filter": [
                "html_strip"
              ]
            }
          }
        }
    },
    "mappings": {
      "docs": {
        "properties": {
          "html": {"type": "text", "analyzer": "htmlStripAnalyzer"},
          "title" : { "type" : "text" },
          "parent_title" : { "type" : "text" },
          "version": {"type": "text"},
          "url" : { "type" : "text" }
        }
      }
    }
}
"""
        self.es.indices.create(index="docs", body=doc)

    def remove_index(self):
        try:
            self.es.indices.delete(index="docs")
        except elasticsearch.exceptions.NotFoundError:
            pass

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
    text = clean_html(text)
    cut_tags = ["\n"]
    to_show = 100
    indice = text.find(word)
    rind = indice + len(word)

    if indice == -1:
        return None

    left_chunk = text[0:indice] if indice < to_show - 1 else text[indice-to_show:indice]

    for cut_tag in cut_tags:
        if cut_tag in left_chunk:
            left_chunk = left_chunk.split(cut_tag)[-1]

    left_chunk = clean_html(left_chunk).replace("¶", "")

    right_chunk = text[rind:rind+to_show] if (rind + to_show) < len(text) else text[rind:]

    for cut_tag in cut_tags:
        if cut_tag in right_chunk:
            right_chunk = right_chunk.split(cut_tag)[0]

    right_chunk = clean_html(right_chunk).replace("¶", "")

    return left_chunk.strip() + " **" + word + "** " +right_chunk.strip()


def find_relevant_text(html, keywords):

    # First look for everything
    all = find_single_word(html, keywords)
    if all:
        return all
    else:
        for keyword in keywords.split(" "):
            partial = find_single_word(html, keyword)
            if partial:
                return partial
        # Try replacing non alphanumerical from keyword
        for keyword in keywords.split(" "):
            partial = find_single_word(html, re.sub('[^0-9a-zA-Z]+', '', keyword))
            if partial:
                return partial
    return None


if __name__ == "__main__":
    host = 'search-conan-docs-475m2ibdrsrg4yxka2yev5zaha.us-east-1.es.amazonaws.com'  # For example, my-test-domain.us-east-1.es.amazonaws.com
    region = 'us-east-1'  # e.g. us-west-1

    manager = ElasticManager(host, region)
    #manager.remove_index()
    #manager.create_index()
    #manager.index("1.15", "/home/luism/workspace/docs/_build/json")
    #time.sleep(5)
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
        if relevant_text:
            print("{}: {} ('{}') [{}]".format(parent_title, title, relevant_text, slug))
        else:
            print("{}: {} [{}]".format(parent_title, title, slug))
