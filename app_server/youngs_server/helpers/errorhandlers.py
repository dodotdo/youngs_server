from flask import jsonify
from youngs_server.youngs_app import db, log
from youngs_server import app
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound, FlushError
from werkzeug.exceptions import HTTPException, abort


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    log.error(e)
    raise


@app.errorhandler(NoResultFound)
def handle_no_result_found(e):
    log.error(e)
    return jsonify({"message": "No Results Found"}), 404


@app.errorhandler(MultipleResultsFound)
def handle_multiple_results_found(e):
    log.error(e)
    return jsonify({"message": "Multiple Results Found"}), 409


@app.errorhandler(FlushError)
def handle_flush_error(e):
    log.error(e)
    return jsonify({"message": "Flush Error"}), 409


@app.errorhandler(exc.SQLAlchemyError)
def handle_sqlalchemy_error(e):
    log.error(e)
    db.session.rollback()
    return jsonify({"message": "SQLAlchemy Error"}), 406


@app.errorhandler(IOError)
def handle_io_error(e):
    log.error("IOError : " + str(e))
    raise


@app.errorhandler(Exception)
def handle_exception(e):
    log.critical('Unexpected Error : ' + str(e))
    raise
