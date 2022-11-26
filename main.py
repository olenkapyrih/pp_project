from flask import Flask
from waitress import serve

app = Flask(__name__)

with app.app_context():
    import routes

if __name__ == '__main__':
    app.run(debug=True)
    serve(app)
