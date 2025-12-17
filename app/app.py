import os
from flask import Flask, jsonify, request
from models import db, User

def create_app(config_name='default'):
    app = Flask(__name__)

    # Konfiguracja bazy danych z Env Vars (domyślne wartości dla bezpieczeństwa)
    db_user = os.getenv('POSTGRES_USER', 'user')
    db_password = os.getenv('POSTGRES_PASSWORD', 'password')
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_name = os.getenv('POSTGRES_DB', 'flaskdb')

    # Connection String dla PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Tworzenie tabel (w środowisku produkcyjnym użyjemy migracji, tutaj dla uproszczenia startu)
    with app.app_context():
        db.create_all()

    # --- ENDPOINTS ---

    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint do sprawdzania stanu aplikacji (Healthcheck)"""
        return jsonify({"status": "ok", "service": "flask-app"}), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        """Dodawanie użytkownika (Test zapisu DB)"""
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({"error": "Bad Request"}), 400
        
        new_user = User(username=data['username'], email=data['email'])
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(new_user.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route('/users', methods=['GET'])
    def get_users():
        """Pobieranie użytkowników (Test odczytu DB)"""
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)