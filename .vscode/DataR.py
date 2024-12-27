import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 예제 데이터
questions = ["안녕하세요?", "이게 안되네", " 사용법 알려줘"]
answers = ["안녕하세요! 어떻게 도와드릴까요?", "오늘 날씨는 맑아요.", "TensorFlow 사용법은 ..."]

# 토크나이저 설정
tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers)

# 시퀀스 변환
question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

# 패딩
max_len = max(len(seq) for seq in question_sequences + answer_sequences)
question_padded = pad_sequences(question_sequences, maxlen=max_len, padding='post')
answer_padded = pad_sequences(answer_sequences, maxlen=max_len, padding='post')
