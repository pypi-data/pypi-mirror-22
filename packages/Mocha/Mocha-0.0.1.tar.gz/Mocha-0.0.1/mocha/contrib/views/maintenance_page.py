
from harambe import Harambe
from harambe.contrib.app_option import AppOption

__options__ = {}

class Main(Harambe):

    NS = "MaintenancePage"

    app_option = AppOption(__name__)

    @classmethod
    def _register(cls, app, **kwargs):
        template = __options__.get("template", "maintenance_page/Main/index.jade")
        super(cls, cls)._register(app, **kwargs)

        cls.app_option.init({
            "status": False,
            "exclude": []
        }, "Maintenance Page Option")

        @app.before_request
        def on_maintenance():
            if cls.app_option.get("status") is True:
                return cls.render(_layout=template), 503


