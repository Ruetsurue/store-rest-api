"""empty message

Revision ID: 67574b1cd1dc
Revises: 87b0a27b24d7
Create Date: 2023-01-27 03:00:26.582327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67574b1cd1dc'
down_revision = '87b0a27b24d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_confirmations',
    sa.Column('id', sa.String(length=80), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=False),
    sa.Column('is_confirmed', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_activated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_activated', sa.BOOLEAN(), autoincrement=False, nullable=True))

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=True)

    op.drop_table('email_confirmations')
    # ### end Alembic commands ###
