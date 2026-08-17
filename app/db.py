from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

os.environ.setdefault("NLS_LANG", "RUSSIAN_RUSSIA.CL8MSWIN1251")

DATABASE_URLS = {
    "200": "oracle+cx_oracle://erip_user:rjrf-rjkf@192.168.100.64:1521/?service_name=orcl200",    # Витебск
   #  "240": "oracle+cx_oracle://erip_user:rjrf-rjkf@192.168.140.100:1521/?service_name=orcl240",  # Орша
   #  "230": "oracle+cx_oracle://erip_user:rjrf-rjkf@192.168.130.100:1521/?service_name=ORCL230",  # Лепель
   #  "250": "oracle+cx_oracle://erip_user:rjrf-rjkf@192.168.150.200:1521/?service_name=orcl",     # Полоцк
   #  "220": "oracle+cx_oracle://erip_user:rjrf-rjkf@192.168.120.32:1521/?service_name=orcl220",   # Глубокое
}

# Создаем соединения для каждой БД
engines = {
    service_no: create_engine(url, pool_pre_ping=True, pool_recycle=3600)
    for service_no, url in DATABASE_URLS.items()
}

Base = declarative_base()

def get_engine(service_no: str):
    """Возвращает engine для нужного филиала. По умолчанию - Витебск (200)."""
    return engines.get(str(service_no), engines["200"])

def get_db_session(service_no: str):
    """Создает и возвращает сессию для нужной БД"""
    engine = get_engine(service_no)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()