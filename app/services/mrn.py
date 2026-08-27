from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db
from app.models import Patient


def generate_mrn():
    """Generate a unique human-readable Medical Record Number."""

    year = datetime.now(timezone.utc).year

    while True:
        random_part = uuid4().hex[:8].upper()
        mrn = f"IHIS-{year}-{random_part}"

        existing_patient = db.session.execute(
            db.select(Patient).filter_by(mrn=mrn)
        ).scalar_one_or_none()

        if existing_patient is None:
            return mrn
