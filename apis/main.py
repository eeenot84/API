import os
import json
import logging
from datetime import datetime
import requests

# --- Настройка логирования ---
logger = logging.getLogger("spacex_logger")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Константы ---
URL = "https://api.spacexdata.com/v5/launches/latest"
OUTPUT_DIR = "tmp"
OUTPUT_FILE = "spacex.json"

# --- Функция загрузки данных ---
def fetch_spacex_data():
    logger.info(f"Запрос к API: {URL}")
    response = requests.get(URL)
    logger.info(f"Статус ответа: {response.status_code}")

    response.raise_for_status()  # Бросает ошибку, если статус != 200
    return response.json()

# --- Функция получения business_date ---
def extract_business_date(data: dict) -> str:
    return data.get("date_utc")

# --- Функция обогащения и сохранения данных ---
def save_data_with_metadata(data: dict, business_date: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    enriched_data = {
        **data,
        "updated_at": datetime.utcnow().isoformat(),  # Дата выгрузки (UTC)
        "business_date": business_date                # Дата запуска (если есть)
    }

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched_data, f, ensure_ascii=False, indent=4)

    logger.info(f"Файл сохранён: {output_path}")

# --- Точка входа ---
def main():
    logger.info("Старт скрипта SpaceX API")
    data = fetch_spacex_data()
    business_date = extract_business_date(data)
    save_data_with_metadata(data, business_date)
    logger.info("Завершено успешно.")

if __name__ == "__main__":
    main()