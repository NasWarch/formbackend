"""Tests for Form and Submission models."""

import pytest
from sqlalchemy.orm import Session


class TestFormModel:
    """Form model represents a form configuration owned by a user."""

    def test_create_form(self, db_session: Session):
        """Should create a form with all required fields."""
        from app.models.user import User
        from app.models.form import Form

        user = User(email="form-owner@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(
            user_id=user.id,
            name="Contact Form",
            slug="contact-form",
        )
        db_session.add(form)
        db_session.flush()

        assert form.id is not None
        assert form.name == "Contact Form"
        assert form.slug == "contact-form"
        assert form.user_id == user.id
        assert form.submission_count == 0

    def test_form_slug_unique(self, db_session: Session):
        """Two forms cannot share the same slug for the same user."""
        from app.models.user import User
        from app.models.form import Form

        user = User(email="unique-test@example.com")
        db_session.add(user)
        db_session.flush()

        form1 = Form(user_id=user.id, name="Form 1", slug="my-form")
        db_session.add(form1)
        db_session.flush()

        form2 = Form(user_id=user.id, name="Form 2", slug="my-form")
        db_session.add(form2)
        with pytest.raises(Exception):
            db_session.flush()

    def test_form_default_active(self, db_session: Session):
        """New forms should be active by default."""
        from app.models.user import User
        from app.models.form import Form

        user = User(email="active-test@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(user_id=user.id, name="Active Form", slug="active-form")
        db_session.add(form)
        db_session.flush()

        assert form.is_active is True

    def test_form_relationship_with_user(self, db_session: Session):
        """Form.user should return the owner."""
        from app.models.user import User
        from app.models.form import Form

        user = User(email="rel-test@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(user_id=user.id, name="Rel Form", slug="rel-form")
        db_session.add(form)
        db_session.flush()

        assert form.user.email == "rel-test@example.com"


class TestSubmissionModel:
    """Submission model stores form submissions."""

    def test_create_submission(self, db_session: Session):
        """Should create a submission with form data."""
        from app.models.user import User
        from app.models.form import Form, Submission

        user = User(email="sub-test@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(user_id=user.id, name="Sub Form", slug="sub-form")
        db_session.add(form)
        db_session.flush()

        submission = Submission(
            form_id=form.id,
            data={"name": "John", "email": "john@example.com", "message": "Hello"},
            ip_address="127.0.0.1",
        )
        db_session.add(submission)
        db_session.flush()

        assert submission.id is not None
        assert submission.data["name"] == "John"
        assert submission.form_id == form.id

    def test_submission_updates_form_count(self, db_session: Session):
        """Creating a submission should increment the form's submission_count."""
        from app.models.user import User
        from app.models.form import Form, Submission

        user = User(email="count-test@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(user_id=user.id, name="Count Form", slug="count-form")
        db_session.add(form)
        db_session.flush()

        submission = Submission(form_id=form.id, data={"test": "data"})
        db_session.add(submission)
        db_session.flush()

        # Reload form to check count
        db_session.refresh(form)
        assert form.submission_count == 1

    def test_submission_form_relationship(self, db_session: Session):
        """Submission.form should return the parent form."""
        from app.models.user import User
        from app.models.form import Form, Submission

        user = User(email="rel2-test@example.com")
        db_session.add(user)
        db_session.flush()

        form = Form(user_id=user.id, name="Rel2 Form", slug="rel2-form")
        db_session.add(form)
        db_session.flush()

        submission = Submission(form_id=form.id, data={"x": "y"})
        db_session.add(submission)
        db_session.flush()

        assert submission.form.name == "Rel2 Form"
