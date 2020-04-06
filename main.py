from app import app
from waitress import serve


if __name__ == "__main__":
    app.run(debug=True)
    #serve(app, host='172.20.7.226', port=8080)
    #app.run('0.0.0.0', 8080)
    # app.run('0.0.0.0', 80)