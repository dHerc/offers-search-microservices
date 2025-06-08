import psycopg
import contextlib
import pyterrier as pt
from os import environ, path

def dictionify(data):
    return {
        "docno": str(data[0]),
        "category": data[1],
        "title": data[2],
        "description": data[3],
        "features": data[4],
        "details": data[5]
    }

def yieldData():
    pg_conn = environ["PG_CONN"]
    with psycopg.connect(pg_conn) as conn:
        with conn.cursor() as cur:
            with contextlib.closing(cur.stream("SELECT id, category, title, description, features, details from offers")) as offers:
                items = map(dictionify, offers)
                for item in items:
                     yield item

def getQuery(data):
    return data.query

dirname = path.dirname(__file__)
filename = path.join(dirname, "index")
indexer = pt.IterDictIndexer(filename, text_attrs=["category", "title", "description", "features", "details"])
indexref = indexer.index(yieldData())