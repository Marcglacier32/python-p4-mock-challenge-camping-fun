"""implement relationships

Revision ID: 3924f619989a
Revises: 17737a3cfda4
Create Date: 2025-06-08 15:05:32.202085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3924f619989a'
down_revision = '17737a3cfda4'
branch_labels = None
depends_on = None



def upgrade():
    with op.batch_alter_table('signups') as batch_op:
        batch_op.create_foreign_key(
            'fk_signups_activity_id_activities',
            'activities',
            ['activity_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_signups_camper_id_campers',
            'campers',
            ['camper_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('signups') as batch_op:
        batch_op.drop_constraint('fk_signups_camper_id_campers', type_='foreignkey')
        batch_op.drop_constraint('fk_signups_activity_id_activities', type_='foreignkey')