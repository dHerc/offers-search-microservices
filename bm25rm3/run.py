import pyterrier as pt
from flask import Flask, request


app = Flask(__name__)
pt.java.init()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "index\data.properties")
indexref = pt.IndexRef.of(filename)

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