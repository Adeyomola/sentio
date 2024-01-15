from flask import Flask, render_template, session, redirect
import os
from dotenv import load_dotenv
load_dotenv()

secret_key=os.environ.get('SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secret_key
    )

    from verba.blog import blog
    app.register_blueprint(blog.bp)

    from verba.auth import auth
    app.register_blueprint(auth.bp)

    from verba.auth import profile
    app.register_blueprint(profile.bp)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if not session:
            return render_template('index.html', posts=blog.front_posts())
        elif 'firstname' in session:
            firstname = session['firstname']
        return render_template('home.html', firstname=firstname, posts=blog.author_posts())

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')

    import verba.db as db
    db.init_app(app)
    return app
app = create_app()