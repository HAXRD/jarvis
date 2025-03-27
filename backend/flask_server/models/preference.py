from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from extensions import db

class UserPreference(db.Model):
    __tablename__ = "user_preferences"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True)
    theme = db.Column(db.String(50), default="light")
    model_preference = db.Column(db.String(100), default="default")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="preferences")

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "theme": self.theme,
            "model_preference": self.model_preference,
            "updated_at": self.updated_at.isoformat()
        }