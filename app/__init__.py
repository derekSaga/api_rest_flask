from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, upgrade
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,
                  db,
                  compare_type=True,
                  compare_server_default=True,
                  render_as_batch=False)
jwt = JWTManager(app)
ma = Marshmallow(app)
api = Api(app)

from .views import hotel_view, usuario_view, login_view, site_view
from .models import hotel_model, usuario_model, site_model

@app.before_first_request
def init_db():
    upgrade(directory='./migrations')
