from flask import Blueprint
from flask import flash
from flask import render_template
from flask import url_for
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import BooleanField
from wtforms.fields import RadioField
from wtforms.fields import SelectField
from wtforms.fields import SelectMultipleField
from wtforms.fields import StringField
from wtforms.fields import PasswordField
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

# This is the blueprint object that gets registered into the app in blueprints.py.
components = Blueprint('components', __name__)


@components.route("/")
def index():
    return render_template('app/index.html')


@components.route('/<component_name>/<demo_name>')
def component_demo(component_name, demo_name):

    readme = open('hmlr_design_system/components/{}/README.md'.format(component_name))

    return render_template('components/{}/demos/{}.html'.format(component_name, demo_name),
                           readme=readme.read()
                           )
