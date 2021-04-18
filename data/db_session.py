import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from sqlalchemy.orm import Session

ORMBase = dec.declarative_base()

__factory = None
global_session = None


def create_session() -> Session:
    global __factory
    return __factory()


def global_init(db_file):
    global __factory, global_session
    if __factory:
        return
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    ORMBase.metadata.create_all(engine)
    global_session = create_session()
