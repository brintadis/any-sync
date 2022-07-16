"""add spotify 500

Revision ID: 375d9b95a5a9
Revises: 02cbc6bd0e7f
Create Date: 2022-07-09 22:01:35.847730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '375d9b95a5a9'
down_revision = '02cbc6bd0e7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('yandex_token', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('spotify_token', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'spotify_token')
    op.drop_column('user', 'yandex_token')
    # ### end Alembic commands ###