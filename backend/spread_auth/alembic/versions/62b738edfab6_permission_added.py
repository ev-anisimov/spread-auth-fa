"""Permission added

Revision ID: 62b738edfab6
Revises: bf70e6197717
Create Date: 2025-01-20 16:08:43.298115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '62b738edfab6'
down_revision: Union[str, None] = 'bf70e6197717'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('project', sa.Integer(), nullable=False),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('access', sa.Enum('Full', 'Read', 'Denied', name='accesstype'), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('invalid', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permission_id'), 'permission', ['id'], unique=False)
    op.add_column('userrole', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userrole', 'updated_at')
    op.drop_index(op.f('ix_permission_id'), table_name='permission')
    op.drop_table('permission')
    # ### end Alembic commands ###
