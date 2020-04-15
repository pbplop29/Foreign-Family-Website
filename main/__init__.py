from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_login import LoginManager



app = Flask(__name__)

app.config['SECRET_KEY'] = '356c2f03e9fd4d3c4287a1366c97fa34'

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeliOkUAAAAALX3eKwlCvJOl0sLp7ZmjTw_3Cl5'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeliOkUAAAAAAGneP7hgqYgwbn7L-daVuK8G_wT'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'



from main import routes