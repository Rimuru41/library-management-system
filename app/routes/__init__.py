from .add_and_edit import main as add
from .authentication import main as auth
from .members import main as members
from .no_templates import main as direct
from .view import main as view
from .staff import main as staff

def register_routes(app):
    app.register_blueprint(add)
    app.register_blueprint(auth)
    app.register_blueprint(members)
    app.register_blueprint(direct)
    app.register_blueprint(view)
    app.register_blueprint(staff)
