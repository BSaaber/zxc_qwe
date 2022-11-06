"""add sn migration

Revision ID: 62d3d9814ba0
Revises: d95816664790
Create Date: 2022-11-04 11:14:10.477109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62d3d9814ba0'
down_revision = 'd95816664790'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sn',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('uom', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_sn_id'), 'sn', ['id'], unique=False)
    op.create_table('sn_hypothesis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('tsn_piece_id', sa.Integer(), nullable=True),
    sa.Column('spgz_piece_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spgz_piece_id'], ['spgz.id'], ),
    sa.ForeignKeyConstraint(['tsn_piece_id'], ['sn.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sn_hypothesis_id'), 'sn_hypothesis', ['id'], unique=False)
    op.create_table('tsn_hypothesis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('tsn_piece_id', sa.Integer(), nullable=True),
    sa.Column('spgz_piece_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['spgz_piece_id'], ['spgz.id'], ),
    sa.ForeignKeyConstraint(['tsn_piece_id'], ['tsn.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tsn_hypothesis_id'), 'tsn_hypothesis', ['id'], unique=False)
    op.drop_index('ix_hypothesis_id', table_name='hypothesis')
    op.drop_table('hypothesis')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hypothesis',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tsn_piece_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('spgz_piece_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['spgz_piece_id'], ['spgz.id'], name='hypothesis_spgz_piece_id_fkey'),
    sa.ForeignKeyConstraint(['tsn_piece_id'], ['tsn.id'], name='hypothesis_tsn_piece_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='hypothesis_pkey')
    )
    op.create_index('ix_hypothesis_id', 'hypothesis', ['id'], unique=False)
    op.drop_index(op.f('ix_tsn_hypothesis_id'), table_name='tsn_hypothesis')
    op.drop_table('tsn_hypothesis')
    op.drop_index(op.f('ix_sn_hypothesis_id'), table_name='sn_hypothesis')
    op.drop_table('sn_hypothesis')
    op.drop_index(op.f('ix_sn_id'), table_name='sn')
    op.drop_table('sn')
    # ### end Alembic commands ###
