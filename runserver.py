import sys
from youngs_server.youngs_app import youngs_app
reload(sys)
sys.setdefaultencoding('utf-8')

application = youngs_app


if __name__ == '__main__':
    print "starting test server..."

    application.run(host='0.0.0.0', port=5000, debug=True)