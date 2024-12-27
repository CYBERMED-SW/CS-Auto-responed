# 데이터 분리
from sklearn.model_selection import train_test_split

X_train, X_val, y_train, y_val = train_test_split(question_padded, answer_padded, test_size=0.2)

# 학습
model.fit([X_train, y_train[:, :-1]], y_train[:, 1:], epochs=10, validation_data=([X_val, y_val[:, :-1]], y_val[:, 1:]))
