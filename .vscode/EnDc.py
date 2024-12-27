from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense

# 모델 입력 크기
embedding_dim = 128
units = 256

# 인코더
encoder_inputs = Input(shape=(None,))
encoder_embedding = tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim)(encoder_inputs)
encoder_lstm, state_h, state_c = LSTM(units, return_state=True)(encoder_embedding)
encoder_states = [state_h, state_c]

# 디코더
decoder_inputs = Input(shape=(None,))
decoder_embedding = tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=embedding_dim)(decoder_inputs)
decoder_lstm, _, _ = LSTM(units, return_sequences=True, return_state=True)(decoder_embedding, initial_state=encoder_states)
decoder_outputs = Dense(len(tokenizer.word_index) + 1, activation='softmax')(decoder_lstm)

# 모델 구성
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
