from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
department = Table('department', post_meta,
    Column('department_id', Integer, primary_key=True, nullable=False),
    Column('state', String(length=120)),
    Column('school_id', String(length=120)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('department_id', String(length=120)),
)

author = Table('author', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('email', String),
    Column('role', SmallInteger),
    Column('school', String),
    Column('subject', String),
)

author = Table('author', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('subject', String(length=120)),
    Column('user_department', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['department'].create()
    post_meta.tables['post'].columns['department_id'].create()
    pre_meta.tables['author'].columns['school'].drop()
    post_meta.tables['author'].columns['user_department'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['department'].drop()
    post_meta.tables['post'].columns['department_id'].drop()
    pre_meta.tables['author'].columns['school'].create()
    post_meta.tables['author'].columns['user_department'].drop()
