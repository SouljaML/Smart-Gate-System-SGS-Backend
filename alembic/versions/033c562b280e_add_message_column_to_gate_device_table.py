"""Add message column to gate_device_table

Revision ID: 033c562b280e
Revises: c1b02ec2105c
Create Date: 2025-04-04 10:08:44.821150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '033c562b280e'
down_revision = 'c1b02ec2105c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('otps')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_pins_id', table_name='pins')
    op.drop_table('pins')
    op.drop_index('ix_gate_device_table_id', table_name='gate_device_table')
    op.drop_table('gate_device_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gate_device_table',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('device_id', sa.VARCHAR(), nullable=False),
    sa.Column('always_open', sa.BOOLEAN(), nullable=True),
    sa.Column('last_seen', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('device_id')
    )
    op.create_index('ix_gate_device_table_id', 'gate_device_table', ['id'], unique=False)
    op.create_table('pins',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('pin', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_pins_id', 'pins', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=False),
    sa.Column('last_name', sa.VARCHAR(), nullable=False),
    sa.Column('phone_id', sa.VARCHAR(), nullable=False),
    sa.Column('car_reg', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('device_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['gate_device_table.device_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_id')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('otps',
    sa.Column('id', sa.VARCHAR(), nullable=False),
    sa.Column('phone_id', sa.VARCHAR(), nullable=False),
    sa.Column('otp', sa.VARCHAR(), nullable=False),
    sa.Column('expiry', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['phone_id'], ['users.phone_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
