from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
approve = Table('approve', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('user_id', Integer),
)

approve = Table('approve', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('approver_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['approve'].columns['user_id'].drop()
    post_meta.tables['approve'].columns['approver_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['approve'].columns['user_id'].create()
    post_meta.tables['approve'].columns['approver_id'].drop()
