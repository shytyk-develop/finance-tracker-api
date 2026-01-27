import urllib.request
import urllib.parse
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_rate_limit():
    print("--- Тестируем Rate Limit (Login) ---")
    url = f"{BASE_URL}/api/login"
    
    # Данные формы кодируются иначе для urllib
    data = urllib.parse.urlencode({"username": "test", "password": "password"}).encode()
    
    for i in range(1, 10):
        req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                print(f"Запрос {i}: Статус {response.getcode()}")
        except urllib.error.HTTPError as e:
            print(f"Запрос {i}: Статус {e.code}")
            if e.code == 429:
                print("УСПЕХ: Ограничение сработало! (429 Too Many Requests)")
                return
        except urllib.error.URLError:
            print("ОШИБКА: Не удалось подключиться. Сервер запущен?")
            return
        
    print("ОШИБКА: Лимит не сработал за 10 запросов.")

if __name__ == "__main__":
    test_rate_limit()