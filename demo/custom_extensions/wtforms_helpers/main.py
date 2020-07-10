from deepmerge import Merger


class WTFormsHelpers(object):
    """WTForms helpers

    Register some template helpers to allow developers to
    map WTForms elements to the GOV.UK jinja macros
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_template_global(wtforms_errors)


def wtforms_errors(form, params={}):
    wtforms_params = {"titleText": "There is a problem", "errorList": []}

    wtforms_params["errorList"] = flatten_errors(form.errors)

    return merger.merge(wtforms_params, params)


def flatten_errors(errors, prefix=""):
    errorList = []

    for key, value in errors.items():

        if isinstance(value, dict):
            # Recurse to handle subforms
            errorList += flatten_errors(value, prefix=prefix + key + "-")
        else:
            errorList.append({"text": value[0], "href": "#{}{}-error".format(prefix, key)})

    return errorList


merger = Merger(
    # pass in a list of tuple, with the
    # strategies you are looking to apply
    # to each type.
    [(list, ["append"]), (dict, ["merge"])],
    # next, choose the fallback strategies,
    # applied to all other types:
    ["override"],
    # finally, choose the strategies in
    # the case where the types conflict:
    ["override"],
)
