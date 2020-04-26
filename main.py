from app import app
from waitress import serve
from paste.translogger import TransLogger
import logging.config
import logging
from datetime import datetime


LOG_FILENAME = 'app/temp_files/requests.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.info("\n")
logging.info("*** The application started: " + str(datetime.now()))


if __name__ == "__main__":
    # app.run(debug=True)
    serve(TransLogger(app, logger_name='chu', setup_console_handler=False), host='127.0.0.1', port=5000)

    # serve(app, host='127.0.0.1', port=5000)
    #serve(app, host='172.20.7.226', port=8080)
