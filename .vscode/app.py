# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
#     # 입력 처리 후 모델 예측
#     response = model.predict(process_input(user_input))
#     return jsonify({'response': generate_response(response)})

# if __name__ == '__main__':
#     app.run(port=5000)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"
