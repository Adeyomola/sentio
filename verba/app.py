from flask import Flask, render_template, session, redirect
import sqlalchemy
import os
from dotenv import load_dotenv
load_dotenv()

secret_key=os.environ.get('SECRET_KEY')

db_password=os.environ.get('DB_PASSWORD')
db_user=os.environ.get('DB_USER')
host=os.environ.get('HOST')
db_name=os.environ.get('DATABASE')

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        ENGINE= sqlalchemy.create_engine(f"mysql://{db_user}:{db_password}@{host}/{db_name}")
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from verba.blog import blog
    app.register_blueprint(blog.bp)

    from verba.auth import auth
    app.register_blueprint(auth.bp)

    from verba.auth import profile
    app.register_blueprint(profile.bp)


    @app.route('/', methods=['GET', 'POST'])
    def home():
        if session:
            return render_template('home.html', posts=blog.author_posts())
        elif not session:
            return render_template('index.html', posts=blog.front_posts())
    

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')

    import verba.db as db
    db.init_app(app)
    return app
app = create_app()