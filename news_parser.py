import requests
import os

# Файл для хранения ID уже прочитанных новостей
SEEN_FILE = "seen_news.txt"

def load_seen_news():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(f.read().splitlines())

def save_seen_news(news_ids):
    with open(SEEN_FILE, "a") as f:
        for news_id in news_ids:
            f.write(f"{news_id}\n")

def fetch_latest_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?filter=important"
    seen_ids = load_seen_news()
    new_ids_to_save = []
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            posts = response.json().get('results', [])
            
            for post in posts:
                post_id = str(post.get('id'))
                
                # Проверяем, видели ли мы уже эту новость
                if post_id not in seen_ids:
                    title = post.get('title')
                    published_at = post.get('published_at')
                    
                    print(f"🕒 Время: {published_at}")
                    print(f"🔥 Заголовок: {title}")
                    print("-" * 40)
                    
                    new_ids_to_save.append(post_id)
            
            # Сохраняем новые ID в файл
            if new_ids_to_save:
                save_seen_news(new_ids_to_save)
                print(f"✅ Найдено новых новостей: {len(new_ids_to_save)}")
            else:
                print("🤷‍♂️ Новых важных новостей пока нет.")
                
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка скрипта: {e}")

if __name__ == "__main__":
    fetch_latest_crypto_news()
