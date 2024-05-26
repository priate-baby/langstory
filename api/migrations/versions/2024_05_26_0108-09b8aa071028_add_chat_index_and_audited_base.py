"""add_chat_index_and_audited_base

Revision ID: 09b8aa071028
Revises: a74331d9e8f0
Create Date: 2024-05-26 01:08:42.765994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '09b8aa071028'
down_revision: Union[str, None] = 'a74331d9e8f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assistantmessage', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('assistantmessage', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('assistantmessage', sa.Column('chat_index', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'assistantmessage', 'user', ['last_updated_by'], ['uid'])
    op.create_foreign_key(None, 'assistantmessage', 'user', ['created_by'], ['uid'])
    op.add_column('chat', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('chat', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'chat', 'user', ['last_updated_by'], ['uid'])
    op.create_foreign_key(None, 'chat', 'user', ['created_by'], ['uid'])
    op.drop_constraint('externalevent_chat_id_fkey', 'externalevent', type_='foreignkey')
    op.drop_column('externalevent', 'chat_id')
    op.add_column('project', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('project', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'project', 'user', ['last_updated_by'], ['uid'])
    op.create_foreign_key(None, 'project', 'user', ['created_by'], ['uid'])
    op.add_column('systemmessage', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('systemmessage', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('systemmessage', sa.Column('chat_index', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'systemmessage', 'user', ['last_updated_by'], ['uid'])
    op.create_foreign_key(None, 'systemmessage', 'user', ['created_by'], ['uid'])
    op.add_column('toolmessage', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('toolmessage', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('toolmessage', sa.Column('chat_index', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'toolmessage', 'user', ['created_by'], ['uid'])
    op.create_foreign_key(None, 'toolmessage', 'user', ['last_updated_by'], ['uid'])
    op.add_column('usermessage', sa.Column('created_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('usermessage', sa.Column('last_updated_by', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.add_column('usermessage', sa.Column('chat_index', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'usermessage', 'user', ['created_by'], ['uid'])
    op.create_foreign_key(None, 'usermessage', 'user', ['last_updated_by'], ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usermessage', type_='foreignkey')
    op.drop_constraint(None, 'usermessage', type_='foreignkey')
    op.drop_column('usermessage', 'chat_index')
    op.drop_column('usermessage', 'last_updated_by')
    op.drop_column('usermessage', 'created_by')
    op.drop_constraint(None, 'toolmessage', type_='foreignkey')
    op.drop_constraint(None, 'toolmessage', type_='foreignkey')
    op.drop_column('toolmessage', 'chat_index')
    op.drop_column('toolmessage', 'last_updated_by')
    op.drop_column('toolmessage', 'created_by')
    op.drop_constraint(None, 'systemmessage', type_='foreignkey')
    op.drop_constraint(None, 'systemmessage', type_='foreignkey')
    op.drop_column('systemmessage', 'chat_index')
    op.drop_column('systemmessage', 'last_updated_by')
    op.drop_column('systemmessage', 'created_by')
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'last_updated_by')
    op.drop_column('project', 'created_by')
    op.add_column('externalevent', sa.Column('chat_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('externalevent_chat_id_fkey', 'externalevent', 'chat', ['chat_id'], ['uid'])
    op.drop_constraint(None, 'chat', type_='foreignkey')
    op.drop_constraint(None, 'chat', type_='foreignkey')
    op.drop_column('chat', 'last_updated_by')
    op.drop_column('chat', 'created_by')
    op.drop_constraint(None, 'assistantmessage', type_='foreignkey')
    op.drop_constraint(None, 'assistantmessage', type_='foreignkey')
    op.drop_column('assistantmessage', 'chat_index')
    op.drop_column('assistantmessage', 'last_updated_by')
    op.drop_column('assistantmessage', 'created_by')
    # ### end Alembic commands ###
