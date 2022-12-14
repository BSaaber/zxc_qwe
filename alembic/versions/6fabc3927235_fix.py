"""fix

Revision ID: 6fabc3927235
Revises: 9e21547717a0
Create Date: 2022-11-04 23:34:42.062567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fabc3927235'
down_revision = '9e21547717a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_hypothesis', sa.Column('sn_piece_id', sa.Integer(), nullable=True))
    op.drop_constraint('sn_hypothesis_tsn_piece_id_fkey', 'sn_hypothesis', type_='foreignkey')
    op.create_foreign_key(None, 'sn_hypothesis', 'sn', ['sn_piece_id'], ['id'])
    op.drop_column('sn_hypothesis', 'tsn_piece_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sn_hypothesis', sa.Column('tsn_piece_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'sn_hypothesis', type_='foreignkey')
    op.create_foreign_key('sn_hypothesis_tsn_piece_id_fkey', 'sn_hypothesis', 'sn', ['tsn_piece_id'], ['id'])
    op.drop_column('sn_hypothesis', 'sn_piece_id')
    # ### end Alembic commands ###
