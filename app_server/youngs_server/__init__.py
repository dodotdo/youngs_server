
from .youngs_app import create_app


app = create_app('config.default.DevelopmentConfig')

import youngs_server.helpers.login_module
import youngs_server.views
import youngs_server.helpers.errorhandlers