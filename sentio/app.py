from flask import Flask, render_template, session, redirect


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    from sentio.blog import blog
    app.register_blueprint(blog.bp)

    from sentio.auth import auth
    app.register_blueprint(auth.bp)

    from sentio.blog.blog import author_posts
    @app.route('/', methods=['GET', 'POST'])
    def home():
        if not session:
            return render_template('index.html')
        elif 'firstname' in session:
            firstname = session['firstname']
        return render_template('home.html', firstname=firstname, posts=author_posts())

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/login')

    import sentio.db as db
    db.init_app(app)
    return app
app = create_app()