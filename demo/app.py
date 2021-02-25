from glob import glob
from os import path

from flask import url_for
from jinja2 import (ChoiceLoader, FileSystemLoader, PackageLoader,
                    PrefixLoader, Template, contextfilter)
from markupsafe import Markup

from demo.landregistry_flask import LandRegistryFlask

app = LandRegistryFlask(__name__, template_folder="templates", static_folder="assets/dist", static_url_path="/ui",)


# Set Jinja up to be able to load templates from packages (See gadget-govuk-ui for a full example)
app.jinja_loader = ChoiceLoader(
    [
        PackageLoader("demo"),
        PrefixLoader(
            {
                "components": FileSystemLoader("hmlr_design_system/components"),
                "govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja"),
                "govuk_frontend_wtf": PackageLoader("govuk_frontend_wtf"),
            }
        ),
    ]
)

app.config.from_pyfile("config.py")


def parse_path(demo_path):
    demo_path = path.relpath(demo_path, "hmlr_design_system/components").replace("/demos", "").replace(".html", "")
    path_parts = demo_path.split("/")
    return url_for("components.component_demo", component_name=path_parts[0], demo_name=path_parts[1],)


@app.context_processor
def inject_global_values():
    """Inject global template values

    Use this to inject values into the templates that are used globally.
    This might be things such as google analytics keys, or even the current username
    """

    demos = glob("hmlr_design_system/components/**/demos/*.html")
    parsed_demos = sorted(list(map(parse_path, demos)))

    return dict(service_name="HMLR Design System", demos=parsed_demos)


@contextfilter
@app.template_filter()
def dangerous_eval(context, value):
    return Markup(Template(value).render(context))


unique_id_counter = 0


@contextfilter
@app.template_filter("unique_id")
def unique_id(context, value):
    global unique_id_counter
    unique_id_counter += 1
    return value + str(unique_id_counter)
