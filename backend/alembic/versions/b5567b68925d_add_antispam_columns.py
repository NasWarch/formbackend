"""add_antispam_columns

Adds per-form anti-spam toggle columns to the forms table:
- spam_protection_enabled
- turnstile_enabled
- spam_scoring_enabled

Revision ID: b5567b68925d
Revises: 05f54a92533c
Create Date: 2026-05-11 12:10:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5567b68925d'
down_revision: Union[str, None] = '05f54a92533c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('forms', sa.Column('spam_protection_enabled', sa.Boolean(),
                  nullable=False, server_default=sa.text('true')))
    op.add_column('forms', sa.Column('turnstile_enabled', sa.Boolean(),
                  nullable=False, server_default=sa.text('true')))
    op.add_column('forms', sa.Column('spam_scoring_enabled', sa.Boolean(),
                  nullable=False, server_default=sa.text('true')))


def downgrade() -> None:
    op.drop_column('forms', 'spam_scoring_enabled')
    op.drop_column('forms', 'turnstile_enabled')
    op.drop_column('forms', 'spam_protection_enabled')
