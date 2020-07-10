# Import every blueprint file
from demo.views import components, general


def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(components.components)

    # All done!
    app.logger.info("Blueprints registered")
