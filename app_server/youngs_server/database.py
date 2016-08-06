# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# declarative part is not used right now
# because there is clear benefit to using flask-sqlalchemy over sqlalchemy
# TODO But, it seems that flask-sqlalchemy is not maintained. Needs to be considered
# reference : flask-docs-kr.readthedocs.org/ko/latest/patterns/sqlalchemy.html

# Instantiate and start DB
db = SQLAlchemy()

# Likewise with Bcrypt extension
bcrypt = Bcrypt()
