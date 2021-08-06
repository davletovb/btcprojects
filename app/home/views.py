from flask import abort, render_template
from flask_login import current_user, login_required

from ..models import Project
from ..admin.forms import IndividualForm, OrganizationForm

from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/projects')
def projects():
    """
    Render the list of projects template on the /projects route
    """
    projects = Project.query.all()
    return render_template('home/projects/projects.html', projects=projects, title='Projects')


@home.route('/projects/<int:id>', methods=['GET', 'POST'])
def project(id):
    """
    View a project
    """
    project = Project.query.get_or_404(id)

    return render_template('home/projects/project.html', project=project, title="Project")


@home.route('/individuals/<int:id>', methods=['GET', 'POST'])
def individual(id):
    """
    View an individual
    """
    individual = Project.query.get_or_404(id)
    form = IndividualForm(obj=individual)
    form.name.data = individual.name
    form.description.data = individual.description

    return render_template('home/individuals/individual.html', form=form, title="Individual")


@home.route('/organizations/<int:id>', methods=['GET', 'POST'])
def organization(id):
    """
    View an organization
    """
    organization = Project.query.get_or_404(id)
    form = OrganizationForm(obj=organization)
    form.name.data = organization.name
    form.description.data = organization.description

    return render_template('home/organizations/organization.html', form=form, title="Organization")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")