import time
from src.app import create_app, db

def run_migrations():
    print('Czekam na start bazy...')
    time.sleep(5)
    
    app = create_app()
    with app.app_context():
        print('Tworzenie tabel...')
        try:
            db.create_all()
            print('Migracje zakończone sukcesem (tabele utworzone).')
        except Exception as e:
            print(f'Błąd migracji: {e}')
            exit(1)

if __name__ == '__main__':
    run_migrations()