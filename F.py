import time
import redis
from flask import Flask, render_template, request, jsonify
import torch
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def perform_tensor_operations():
    tensor_a = torch.tensor([1, 2, 3])
    tensor_b = torch.tensor([4, 5, 6])
    result = tensor_a + tensor_b
    return result


def create_seaborn_plot():
    data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    sns.histplot(data, bins=5, kde=False)
    plt.title('Seaborn Histogram Example')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.savefig("static/seaborn_plot.png", format="png")

@app.route('/')
def hello():
    count = get_hit_count()
    
    
    tensor_result = perform_tensor_operations()

    
    create_seaborn_plot()

    return render_template('index.html', count=count, tensor_result=tensor_result)

@app.route('/greetings')
def greetings():
    return 'Hello my new friend from the other universe!'

@app.route('/tensor_result', methods=['POST'])
def tensor_result():
    data = request.json['data']
    result = torch.tensor(data) * 2
    return jsonify({'result': result.tolist()})

@app.route('/seaborn_plot')
def seaborn_plot():
    return render_template('seaborn_plot.html')

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

if name == 'main':
    app.run(debug=True)
