import os
import time
from src.app import create_app, db
from src.models import User

def seed_database():
    app = create_app()
    with app.app_context():
        print("Seedowanie bazy...")
        
        # przykłądowe dane
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            db.session.add(admin)
            db.session.commit()
            print("Dodano użytkownika admin")
        else:
            print("Użytkownik admin już istnieje.")

        # raport
        # /app/seed_output będzie zmapowane w docker-compose
        output_dir = '/app/seed_output'
        os.makedirs(output_dir, exist_ok=True)
        
        report_path = os.path.join(output_dir, 'seed_report.txt')
        with open(report_path, 'w') as f:
            f.write("=== RAPORT SEEDOWANIA ===\n")
            f.write(f"Status: Sukces\n")
            f.write(f"Czas: {time.ctime()}\n")
            f.write(f"Utworzono: Użytkownik admin\n")
        
        print(f"--> Raport zapisano w: {report_path}")

if __name__ == '__main__':
    time.sleep(5) 
    seed_database()