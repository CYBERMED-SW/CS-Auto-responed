from langdetect import detect

text = "Wie kann ich eine Lizenz erhalten?"
detected_language = detect(text)
print(detected_language)  # 예상 출력: 'de' (독일어)