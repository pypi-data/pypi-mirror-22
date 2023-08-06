import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_connection_string():
    # マルチデータベースを実現したい場合、ここを修正する
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
    target_dir = os.path.join(parent_dir, 'bot_common')
    return 'sqlite:///{}'.format(os.path.join(target_dir, 'zaif_bot.db'))


Base = declarative_base()
engine = create_engine(get_connection_string())
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
