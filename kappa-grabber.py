import requests
from bs4 import BeautifulSoup
import os
import string
import random
from concurrent.futures import ThreadPoolExecutor
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def random_string(length=5):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def check_and_download(url, download_path):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else 'downloaded_file'
            file_name = f"{title}_{random_string(6)}.png"
            file_path = os.path.join(download_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Файл сохранен: {file_path}")
        else:
            print(f"Ссылка не найдена: {url}")
    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")


def generate_and_check_links(base_url, download_path, num_attempts):
    for _ in range(num_attempts):
        random_suffix = random_string()
        url = base_url + random_suffix
        check_and_download(url, download_path)


def main():
    base_url = 'https://kappa.lol/'
    download_path = 'downloaded_files'
    os.makedirs(download_path, exist_ok=True)
    
    num_threads = 25  # Количество потоков
    num_attempts_per_thread = 2500000  # Количество попыток на поток

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_and_check_links, base_url, download_path, num_attempts_per_thread) for _ in range(num_threads)]
        
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
