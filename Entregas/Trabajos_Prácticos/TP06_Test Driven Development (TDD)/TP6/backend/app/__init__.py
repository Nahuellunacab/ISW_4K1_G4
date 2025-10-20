import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from .models import Base, seed_initial_data

SessionLocal = None

def create_app():
    global SessionLocal
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173","http://localhost:3000"]}})

    db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
    engine = create_engine(db_url, future=True)

    # Importante para cascadas en SQLite
    if db_url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cur = dbapi_connection.cursor()
            cur.execute("PRAGMA foreign_keys=ON;")
            cur.close()

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    Base.metadata.create_all(engine)
    with SessionLocal() as s:
        seed_initial_data(s)
        s.commit()

    app.config["SessionLocal"] = SessionLocal

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    return app
