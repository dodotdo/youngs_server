
from youngs_server import app
from youngs_server.youngs_app import db

if __name__ == '__main__':
    db.create_all(app=app)
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
