from flask import Blueprint
from flask import flash
from flask import render_template
from flask import url_for
from flask_wtf import FlaskForm
from glob import glob
from os import path
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
    def parse_path(demo_path):
        demo_path = path.relpath(demo_path, 'components').replace('/demos', '').replace('.html', '')
        path_parts = demo_path.split('/')
        return url_for('components.component_demo', component_name=path_parts[0], demo_name=path_parts[1])

    demos = glob('components/**/demos/*.html')
    parsed_demos = sorted(list(map(parse_path, demos)))
    print(parsed_demos)

    return render_template('app/index.html', demos=parsed_demos)


@components.route('/<component_name>/<demo_name>')
def component_demo(component_name, demo_name):

    readme = open('components/{}/README.md'.format(component_name))

    return render_template('components/{}/demos/{}.html'.format(component_name, demo_name),
                           readme=readme.read()
                           )
