from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


project_category = db.Table('project_category',
                            db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
                            db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
                            )

project_individual = db.Table('project_individual',
                              db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
                              db.Column('individual_id', db.Integer, db.ForeignKey('individuals.id'), primary_key=True)
                              )

project_organization = db.Table('project_organization',
                                db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
                                db.Column('organization_id', db.Integer, db.ForeignKey('organizations.id'),
                                          primary_key=True)
                                )


class Project(db.Model):
    """
    Create a Project table
    """

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    location = db.Column(db.String(100))
    url = db.Column(db.String(100))
    categories = db.relationship('Category', secondary=project_category, lazy='dynamic')
    individuals = db.relationship('Individual', secondary=project_individual, lazy='dynamic')
    organizations = db.relationship('Organization', secondary=project_organization, lazy='dynamic')

    def __repr__(self):
        return '<Project: {}>'.format(self.name)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    projects = db.relationship('Project', secondary=project_category, lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.name)


class Individual(db.Model):
    __tablename__ = 'individuals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '{}'.format(self.name)


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '{}'.format(self.name)
