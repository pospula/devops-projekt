import os
import json
import csv
import logging
import time
from src.app import create_app, db
from src.models import User

OUTPUT_DIR = '/app/seed_output'
LOG_FILE = os.path.join(OUTPUT_DIR, 'seed.log')
CSV_FILE = os.path.join(OUTPUT_DIR, 'users.csv')
JSON_FILE = os.path.join(OUTPUT_DIR, 'data.json')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# zapis do pliku seed.log i konsoli
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def seed_database():
    app = create_app()
    with app.app_context():
        logger.info("Rozpoczynanie seedowania...")

        users_data = [
            {"username": "admin", "email": "admin@op.pl"},
            {"username": "jan_kowalski", "email": "jan@onet.pl"},
            {"username": "anna_nowak", "email": "anna@onet.pl"},
            {"username": "karol_wisniewski", "email": "friz@onet.pl"},
            {"username": "maria_nowak", "email": "maria@op.pl"}
        ]

        added_users = []

        # zapis do db
        for u_data in users_data:
            existing = User.query.filter_by(username=u_data['username']).first()
            if not existing:
                new_user = User(username=u_data['username'], email=u_data['email'])
                db.session.add(new_user)
                added_users.append(u_data)
                logger.info(f"Dodano do DB: {u_data['username']}")
            else:
                logger.warning(f"Użytkownik {u_data['username']} już istnieje w DB.")
        
        db.session.commit()
        logger.info(f"Zakończono operacje na bazie. Dodano {len(added_users)} nowych rekordów.")

        # users.csv
        try:
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["username", "email"])
                writer.writeheader()
                writer.writerows(users_data)
            logger.info(f"Wygenerowano plik CSV: {CSV_FILE}")
        except Exception as e:
            logger.error(f"Błąd zapisu CSV: {e}")

        # data.json
        try:
            with open(JSON_FILE, mode='w', encoding='utf-8') as f:
                json.dump({"users": users_data, "generated_at": time.ctime()}, f, indent=4)
            logger.info(f"Wygenerowano plik JSON: {JSON_FILE}")
        except Exception as e:
            logger.error(f"Błąd zapisu JSON: {e}")

        logger.info("Proces seedowania zakończony sukcesem.")

if __name__ == '__main__':
    time.sleep(2)
    seed_database()