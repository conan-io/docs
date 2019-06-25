import json
import os

import boto3
import elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth
from bs4 import BeautifulSoup


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
                soup = BeautifulSoup(html, 'html.parser')
                h1_elements = [a.get_text().replace("¶", "") for a in soup.find_all("h1")]
                h2_elements = [a.get_text().replace("¶", "") for a in soup.find_all("h2")]
                h3_elements = [a.get_text().replace("¶", "") for a in soup.find_all("h3")]

                element = {"version": version, "title": title, "parent_title": parent_title,
                           "slug": slug, "html": html, "h1": h1_elements, "h2": h2_elements,
                           "h3": h3_elements}
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
          "url" : { "type" : "text" },
          "h1" : { "type" : "text" },
          "h2" : { "type" : "text" },
          "h3" : { "type" : "text" }
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

    def ping(self):
        return self.es.info()
