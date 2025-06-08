from flask import Flask, request
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto")

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_embedding():
    query = request.json['query']
    context = request.json['context']
    input = "Improve the search effectiveness by suggesting expansion terms for the query: " + query
    if (context):
        input += ", based on the given context information: " + context
    input_ids = tokenizer(input, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids)
    return tokenizer.decode(outputs[0])

if __name__ == "__main__":
    app.run(debug=False, port=5001)