import configparser
from flask import Flask, Response
from flask_session import Session
from flask_cors import CORS
from waitress import serve
import auth
import home
import datetime
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

config = configparser.ConfigParser()
config.read('config.cfg')
app = Flask(__name__)
app.config['SECRET_KEY'] = config['flask']['secret_key']
app.config['JWT_SECRET_KEY'] = config['flask']['jwt_secret_key']
app.config['SESSION_TYPE'] = 'filesystem'
app.session_cookie_name = "session_cookie_name"
Session(app)
# jwt = JWTManager(app)

api_v1_cors_config = {
    "origins": ["http://localhost:8080", "http://localhost:5173", "http://10.29.51.15:8080", "http://10.29.90.96:8080", "http://172.20.15.5:3000"],
    "methods": ["GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"],
}

CORS(app, resources={
    r"/api/v1/*": api_v1_cors_config,
}, supports_credentials=True)

app.permanent_session_lifetime = datetime.timedelta(days=365)

app.register_blueprint(auth.auth_bp)
app.register_blueprint(home.home_bp)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000, threads=20)
    # app.run(port=5000, debug=True, threaded=True, host="0.0.0.0")
