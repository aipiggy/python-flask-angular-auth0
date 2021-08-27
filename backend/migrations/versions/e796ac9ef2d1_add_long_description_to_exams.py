"""add long_description to exams

Revision ID: e796ac9ef2d1
Revises: 
Create Date: 2021-08-27 11:41:41.513706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e796ac9ef2d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('exams', sa.Column(
        'long_description',
        sa.Text,
        nullable=False,
        server_default='Default exam description')
    )


def downgrade():
    pass
