from sentence_transformers import SentenceTransformer
import sys
from flask import Flask, request

app = Flask(__name__)
model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)

def stringify_embeddings(embeddings):
    return ','.join(map(str, embeddings))

@app.route('/', methods=['POST'])
def generate_embedding():
    sentences=request.json['sentences']
    embeddings = model.encode(sentences)
    return '\n'.join(map(stringify_embeddings, embeddings))

@app.route('/', methods=['GET'])
def generate_single_embeddings():
    sentence=request.args.get('sentence')
    embeddings = model.encode(sentence)
    return stringify_embeddings(embeddings)

if __name__ == "__main__":
    app.run(debug=False)
