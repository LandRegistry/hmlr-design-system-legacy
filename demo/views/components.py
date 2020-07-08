from flask import Blueprint
from flask import render_template

# This is the blueprint object that gets registered into the app in blueprints.py.
components = Blueprint('components', __name__)


@components.route("/")
def index():
    return render_template('index.html')


@components.route('/<component_name>/<demo_name>')
def component_demo(component_name, demo_name):

    readme = open('hmlr_design_system/components/{}/README.md'.format(component_name))

    return render_template('components/{}/demos/{}.html'.format(component_name, demo_name),
                           readme=readme.read()
                           )
