"""thread_id_optional_on_message

Revision ID: d17ad032891f
Revises: 57bddb58b53d
Create Date: 2024-06-03 00:12:18.539020

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d17ad032891f"
down_revision: Union[str, None] = "57bddb58b53d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("message", "_thread_uid", existing_type=sa.UUID(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("message", "_thread_uid", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
