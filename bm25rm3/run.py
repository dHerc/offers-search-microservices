import pyterrier as pt
from flask import Flask, request


app = Flask(__name__)
pt.java.init()
indexref = pt.IndexRef.of("D:\magisterka\python_BM25\index_full\data.properties")

pipe = (pt.terrier.Retriever(indexref, wmodel="BM25") >> 
    pt.rewrite.RM3(indexref) >> 
    pt.terrier.Retriever(indexref, wmodel="BM25")
)

@app.route('/', methods=['POST'])
def generate_embedding():
    query=request.json['query']
    terms = pipe.search(query)[['query']].to_numpy()[0][0]
    return terms

if __name__ == "__main__":
    app.run(debug=False, port=5002)