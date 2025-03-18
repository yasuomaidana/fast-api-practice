"""init

Revision ID: 32a8e8d8c2ea
Revises: 
Create Date: 2025-03-18 11:21:29.986440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel
import models


# revision identifiers, used by Alembic.
revision: str = '32a8e8d8c2ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_method',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('place_type', sa.Enum('BAR', 'RESTAURANT', 'HOTEL', 'CONVENIENCE_STORE', 'GOVERNMENT', 'HOSPITAL', 'STORE', 'SCHOOL', 'PHARMACY', name='placetype'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_name',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('placeId', sa.Integer(), nullable=False),
    sa.Column('paymentMethodId', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['paymentMethodId'], ['payment_method.id'], ),
    sa.ForeignKeyConstraint(['placeId'], ['place.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productNameId', sa.Integer(), nullable=False),
    sa.Column('productType', sa.Enum('MEAT', 'DAIRY', 'FRUIT', 'VEGETABLE', 'FISH', 'BAKERY', 'ALCOHOL', 'BEVERAGE', 'GROCERY', 'CLEANING', 'PERSONAL_CARE', 'MEDICINE', 'CLOTHING', 'ELECTRONICS', 'TOYS', 'BOOKS', 'STATIONERY', 'HARDWARE', 'TOOLS', 'AUTOMOTIVE', 'PET', 'CEREALS', 'SNACKS', 'SWEETS', 'DESSERTS', 'HEALTH', 'FITNESS', 'SPORTS', 'TRANSPORT', 'TRAVEL', 'ENTERTAINMENT', 'EDUCATION', 'HOBBIES', 'ART', 'CRAFTS', 'GARDENING', 'FURNITURE', 'DECORATION', 'STUDENT_LOAN', 'MORTGAGE', 'CAR_LOAN', 'PERSONAL_LOAN', 'BUSINESS_LOAN', 'INSURANCE', 'INVESTMENT', 'SAVINGS', 'ELECTRICITY', 'WATER', 'GAS', 'INTERNET', 'PHONE', 'TV', 'STREAMING', 'GAMING', 'MUSIC', 'MOVIES', 'SERIES', 'FOOD', 'RENT', 'SOFTWARE', 'SUBSCRIPTION', name='producttype'), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['productNameId'], ['product_name.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('purchased_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productId', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('invoiceId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['invoiceId'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['productId'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tax_type', sa.Enum('VAT', 'INCOME_TAX', name='taxtype'), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('invoiceId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['invoiceId'], ['invoice.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tax')
    op.drop_table('purchased_item')
    op.drop_table('product')
    op.drop_table('invoice')
    op.drop_table('product_name')
    op.drop_table('place')
    op.drop_table('payment_method')
    # ### end Alembic commands ###
