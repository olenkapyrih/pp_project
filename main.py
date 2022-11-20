from flask import Flask
from waitress import serve


app = Flask(__name__)
app.config['SECURITY_KEY'] = '1'

with app.app_context():
    import routes

if __name__ == '__main__':
    app.run(debug=True)
    serve(app)
