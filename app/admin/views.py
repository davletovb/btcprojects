from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import RoleForm, UserAddForm, UserEditForm, UserAssignForm, CategoryForm, ProjectForm, IndividualForm, \
    OrganizationForm
from .. import db
from ..models import Role, User, Category, Project, Individual, Organization


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Role Views

@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


# User Views

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a role.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/assign.html',
                           user=user, form=form,
                           title='Assign User')


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Handle requests to the /ysers/add route
    Add a user to the database through the registration form
    """
    check_admin()

    add_user = True

    form = UserAddForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data, is_admin=form.is_admin.data, role_id=form.role.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successfully added the user!')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    # load registration template
    return render_template('admin/users/user.html', add_user=add_user, form=form, title='Add User')


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Edit a user
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)

    # prevent admin from being edited
    # if user.is_admin:
    #     abort(403)

    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully edited the user.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html', user=user, form=form, add_user=add_user,
                           title='Edit User')


# Category Views

@admin.route('/categories')
@login_required
def list_categories():
    check_admin()
    """
    List all categories
    """
    categories = Category.query.all()
    return render_template('admin/categories/categories.html',
                           categories=categories, title='Categories')


@admin.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """
    Add a category to the database
    """
    check_admin()

    add_category = True

    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data)

        try:
            # add category to the database
            db.session.add(category)
            db.session.commit()
            flash('You have successfully added a new category.')
        except:
            # in case category name already exists
            flash('Error: category name already exists.')

        # redirect to the category page
        return redirect(url_for('admin.list_categories'))

    # load category template
    return render_template('admin/categories/category.html', add_category=add_category,
                           form=form, title='Add Category')


@admin.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """
    Edit a category
    """
    check_admin()

    add_category = False

    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.add(category)
        db.session.commit()
        flash('You have successfully edited the category.')

        # redirect to the categories page
        return redirect(url_for('admin.list_categories'))

    form.description.data = category.description
    form.name.data = category.name
    return render_template('admin/categories/category.html', add_category=add_category,
                           form=form, title="Edit Category")


@admin.route('/categories/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    """
    Delete a category from the database
    """
    check_admin()

    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('You have successfully deleted the category.')

    # redirect to the categories page
    return redirect(url_for('admin.list_categories'))

    return render_template(title="Delete Category")


# Project Views

@admin.route('/projects')
@login_required
def list_projects():
    check_admin()
    """
    List all projects
    """
    projects = Project.query.all()
    return render_template('admin/projects/projects.html',
                           projects=projects, title='Projects')


@admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Add a project to the database
    """
    check_admin()

    add_project = True

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, location=form.location.data,
                          url=form.url.data, categories=form.categories.data, individuals=form.individuals.data,
                          organizations=form.organizations.data)

        try:
            # add project to the database
            db.session.add(project)
            db.session.commit()
            flash('You have successfully added a new project.')
        except:
            # in case project name already exists
            flash('Error: project name already exists.')

        # redirect to the project page
        return redirect(url_for('admin.list_projects'))

    # load project template
    return render_template('admin/projects/project.html', add_project=add_project,
                           form=form, title='Add Project')


@admin.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project
    """
    check_admin()

    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.location = form.location.data
        project.url = form.url.data
        project.categories = form.categories.data
        project.individuals = form.individuals.data
        project.organizations = form.organizations.data
        db.session.add(project)
        db.session.commit()
        flash('You have successfully edited the project.')

        # redirect to the projects page
        return redirect(url_for('admin.list_projects'))

    form.description.data = project.description
    form.name.data = project.name
    return render_template('admin/projects/project.html', add_project=add_project,
                           form=form, title="Edit Project")


@admin.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """
    Delete a project from the database
    """
    check_admin()

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    # redirect to the projects page
    return redirect(url_for('admin.list_projects'))

    return render_template(title="Delete Project")


# Individual Views

@admin.route('/individuals')
@login_required
def list_individuals():
    check_admin()
    """
    List all individuals
    """
    individuals = Individual.query.all()
    return render_template('admin/individuals/individuals.html',
                           individuals=individuals, title='Individuals')


@admin.route('/individuals/add', methods=['GET', 'POST'])
@login_required
def add_individual():
    """
    Add a individual to the database
    """
    check_admin()

    add_individual = True

    form = IndividualForm()
    if form.validate_on_submit():
        individual = Individual(name=form.name.data, description=form.description.data)

        try:
            # add individual to the database
            db.session.add(individual)
            db.session.commit()
            flash('You have successfully added a new individual.')
        except:
            # in case individual name already exists
            flash('Error: individual name already exists.')

        # redirect to the individual page
        return redirect(url_for('admin.list_individuals'))

    # load individual template
    return render_template('admin/individuals/individual.html', add_individual=add_individual,
                           form=form, title='Add Individual')


@admin.route('/individuals/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_individual(id):
    """
    Edit a individual
    """
    check_admin()

    add_individual = False

    individual = Individual.query.get_or_404(id)
    form = IndividualForm(obj=individual)
    if form.validate_on_submit():
        individual.name = form.name.data
        individual.description = form.description.data
        db.session.add(individual)
        db.session.commit()
        flash('You have successfully edited the individual.')

        # redirect to the individuals page
        return redirect(url_for('admin.list_individuals'))

    form.description.data = individual.description
    form.name.data = individual.name
    return render_template('admin/individuals/individual.html', add_individual=add_individual,
                           form=form, title="Edit Individual")


@admin.route('/individuals/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_individual(id):
    """
    Delete an individual from the database
    """
    check_admin()

    individual = Individual.query.get_or_404(id)
    db.session.delete(individual)
    db.session.commit()
    flash('You have successfully deleted the individual.')

    # redirect to the individuals page
    return redirect(url_for('admin.list_individuals'))

    return render_template(title="Delete Individual")


# Organization Views

@admin.route('/organizations')
@login_required
def list_organizations():
    check_admin()
    """
    List all organizations
    """
    organizations = Organization.query.all()
    return render_template('admin/organizations/organizations.html',
                           organizations=organizations, title='Organizations')


@admin.route('/organizations/add', methods=['GET', 'POST'])
@login_required
def add_organization():
    """
    Add an organization to the database
    """
    check_admin()

    add_organization = True

    form = OrganizationForm()
    if form.validate_on_submit():
        organization = Organization(name=form.name.data, description=form.description.data)

        try:
            # add organization to the database
            db.session.add(organization)
            db.session.commit()
            flash('You have successfully added a new organization.')
        except:
            # in case organization name already exists
            flash('Error: organization name already exists.')

        # redirect to the organizations page
        return redirect(url_for('admin.list_organizations'))

    # load organization template
    return render_template('admin/organizations/organization.html', add_organization=add_organization,
                           form=form, title='Add Organization')


@admin.route('/organizations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_organization(id):
    """
    Edit an organization
    """
    check_admin()

    add_organization = False

    organization = Organization.query.get_or_404(id)
    form = OrganizationForm(obj=organization)
    if form.validate_on_submit():
        organization.name = form.name.data
        organization.description = form.description.data
        db.session.add(organization)
        db.session.commit()
        flash('You have successfully edited the organization.')

        # redirect to the organizations page
        return redirect(url_for('admin.list_organizations'))

    form.description.data = organization.description
    form.name.data = organization.name
    return render_template('admin/organizations/organization.html', add_organization=add_organization,
                           form=form, title="Edit Organization")


@admin.route('/organizations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_organization(id):
    """
    Delete an organization from the database
    """
    check_admin()

    organization = Organization.query.get_or_404(id)
    db.session.delete(organization)
    db.session.commit()
    flash('You have successfully deleted the organization.')

    # redirect to the organizations page
    return redirect(url_for('admin.list_organizations'))

    return render_template(title="Delete Organization")