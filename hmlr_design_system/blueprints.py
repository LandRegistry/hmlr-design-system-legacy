# Import every blueprint file
from hmlr_design_system.views import general
from hmlr_design_system.views import components


def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(components.components)

    # All done!
    app.logger.info("Blueprints registered")
