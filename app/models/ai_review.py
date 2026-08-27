from datetime import datetime, timezone

from app.extensions import db


class AIReview(db.Model):
    """Human review of an AI-generated assessment."""

    __tablename__ = "ai_reviews"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("ai_assessments.id"),
        nullable=False,
        index=True,
    )

    decision = db.Column(
        db.String(30),
        nullable=False,
    )

    comments = db.Column(
        db.Text,
        nullable=True,
    )

    modified_output = db.Column(
        db.JSON,
        nullable=True,
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    reviewed_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    assessment = db.relationship(
        "AIAssessment",
        back_populates="reviews",
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewer_id],
    )

    def __repr__(self):
        return (
            f"<AIReview {self.id}: "
            f"assessment={self.assessment_id}, "
            f"decision={self.decision}>"
        )
