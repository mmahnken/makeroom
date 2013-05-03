from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
school = Table('school', post_meta,
    Column('ls_school_id', Integer, primary_key=True, nullable=False),
)

department = Table('department', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('state', String),
    Column('school_id', String),
)

department = Table('department', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('department_key', Integer),
    Column('state', String(length=120)),
    Column('ls_school_id', String(length=120)),
)

student = Table('student', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String),
    Column('last_name', String),
    Column('birthday', String),
    Column('grade', Integer),
    Column('lsid', String),
    Column('school_id', String),
    Column('teacher_id', Integer),
)

student = Table('student', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('birthday', String(length=120)),
    Column('lsid', String(length=120)),
    Column('grade', Integer),
    Column('ls_school_id', String(length=120)),
    Column('teacher_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['school'].create()
    pre_meta.tables['department'].columns['school_id'].drop()
    post_meta.tables['department'].columns['department_key'].create()
    post_meta.tables['department'].columns['ls_school_id'].create()
    pre_meta.tables['student'].columns['school_id'].drop()
    post_meta.tables['student'].columns['ls_school_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['school'].drop()
    pre_meta.tables['department'].columns['school_id'].create()
    post_meta.tables['department'].columns['department_key'].drop()
    post_meta.tables['department'].columns['ls_school_id'].drop()
    pre_meta.tables['student'].columns['school_id'].create()
    post_meta.tables['student'].columns['ls_school_id'].drop()
