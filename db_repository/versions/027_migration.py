from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
goal = Table('goal', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=200)),
)

mod = Table('mod', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goal'].create()
    post_meta.tables['mod'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['goal'].drop()
    post_meta.tables['mod'].drop()
