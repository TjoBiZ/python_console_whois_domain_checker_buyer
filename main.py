import subprocess
import time
import requests
import os
from dotenv import load_dotenv      #pip install python-dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
domain = os.getenv('DOMAIN')
telegram_bot_token = os.getenv('BOT_TOKEN')
channel_name = os.getenv('CHANNEL_NAME')
text_searching = os.getenv('TEXT_SEARCHING')

attempts = 2
sleepy = 2
found = False

for _ in range(attempts):
    # Запускаем команду whois и получаем ее вывод
    result = subprocess.run(["whois", domain], capture_output=True, text=True)

    # Проверяем наличие текста - "D7102714-BIZ" в выводе команды если предположим в консоли на проверку домена whois
    # #whois tjo.biz
    # #Domain Name: tools.biz
    # #Registry Domain ID: D7102714-BIZ
    if text_searching in result.stdout:
        time.sleep(sleepy)
        found = True
        print("True")
        continue

    # Делаем паузу в X секунд между запросами whois
    time.sleep(sleepy)

# Если текст не был найден в выводе ни одной из попыток, выводим "False" в терминале
if not found:
    message_text = "Domain is available. Let's go to buy!!!"

    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": channel_name, "text": message_text}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Сообщение успешно отправлено!")
    else:
        print("Ошибка при отправке сообщения:", response.text)

    print("False")

# Сохраняем вывод команды whois в текстовый файл "whois.txt"
with open("whois.txt", "w") as output_file:
    output_file.write(result.stdout)
