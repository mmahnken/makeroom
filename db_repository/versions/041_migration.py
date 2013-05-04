from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
school = Table('school', pre_meta,
    Column('ls_school_id', Integer, primary_key=True, nullable=False),
)

student = Table('student', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String),
    Column('last_name', String),
    Column('birthday', String),
    Column('grade', Integer),
    Column('lsid', String),
    Column('teacher_id', Integer),
    Column('ls_school_id', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['school'].drop()
    pre_meta.tables['student'].columns['grade'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['school'].create()
    pre_meta.tables['student'].columns['grade'].create()
