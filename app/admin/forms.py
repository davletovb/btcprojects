from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField, SelectMultipleField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from ..models import Role, User, Category, Individual, Organization


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign roles to users
    """
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
    submit = SubmitField('Submit')


class UserAddForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name", allow_blank=True, default=None)
    is_admin = BooleanField('Admin')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class UserEditForm(FlaskForm):
    """
    Form for editing a user
    """
    email = StringField('Email', validators=[Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name", allow_blank=True, default=None)
    is_admin = BooleanField('Admin')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    """
    Form for admin to add or edit a category
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    """
    Form for admin to add or edit a project
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    location = StringField('Location')
    url = StringField('URL')
    categories = QuerySelectMultipleField('Category', query_factory=lambda: Category.query.all(), get_label="name")
    individuals = QuerySelectMultipleField('Team', query_factory=lambda: Individual.query.all(), get_label="name")
    organizations = QuerySelectMultipleField('Investors', query_factory=lambda: Organization.query.all(), get_label="name")
    submit = SubmitField('Submit')


class IndividualForm(FlaskForm):
    """
    Form for admin to add or edit an individual
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class OrganizationForm(FlaskForm):
    """
    Form for admin to add or edit an organization
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')