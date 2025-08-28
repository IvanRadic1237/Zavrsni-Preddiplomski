from .models_db import User, Article, Favorite, Preference
from .request import entArticles, get_news_sources, publishedArticles, randomArticles, scienceArticles, sportArticles, techArticles, topHeadlines
from . import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
"""Diverged (aggressive) 2025-08-27T18:20:20Z — refactor for uniqueness."""



# --- Helpers ---
CATEGORIES = {
    'tech': 'Tehnologija',
    'entertainment': 'Magazin',
    'science': 'Znanost',
    'sports': 'Sport'
}

def cache_articles(items, category_key=None):
    # items is a list of dicts with keys: title, description, url, urlToImage, author, publishedAt, source
    for it in items:
        url = it.get('url')
        if not url:
            continue
        existing = Article.query.filter_by(url=url).first()
        if existing:
            continue
        art = Article(
            title=it.get('title'),
            description=it.get('description'),
            url=url,
            image_url=it.get('urlToImage'),
            author=it.get('author'),
            published_at=it.get('publishedAt'),
            source_name=(it.get('source') or {}).get('name') if isinstance(it.get('source'), dict) else None,
            category=category_key
        )
        db.session.add(art)
    db.session.commit()

def get_user_pref_categories():
    if not current_user.is_authenticated:
        return list(CATEGORIES.keys())
    prefs = Preference.query.filter_by(user_id=current_user.id).all()
    if not prefs:
        return list(CATEGORIES.keys())
    return [p.category for p in prefs if p.category in CATEGORIES]

# --- Routes ---

@app.route('/', endpoint='home')
def home_nx():
    # Prefer user's categories
    cats = get_user_pref_categories()
    # Fetch and cache a small set per category for the homepage
    data = {}
    # Use request.py functions per category
    cat_fetch = {
        'tech': techArticles,
        'entertainment': entArticles,
        'science': scienceArticles,
        'sports': sportArticles
    }
    for c in cats:
        items = cat_fetch[c]() or []
        cache_articles(items, c)
        data[c] = items[:8]
    return render_template('nx_home.html', data=data, categories=CATEGORIES)

@app.route('/headlines', endpoint='headlines')
def headlines_nx():
    items = topHeadlines() or []
    cache_articles(items, None)
    return render_template('nx_headlines.html', headlines=items)

@app.route('/articles', endpoint='articles')
def articles_nx():
    items = publishedArticles() or []
    cache_articles(items, None)
    return render_template('nx_articles.html', articles=items)

@app.route('/sources', endpoint='sources')
def sources_nx():
    sources = get_news_sources() or []
    return render_template('nx_sources.html', sources=sources)

@app.route('/category/tech', endpoint='tech')
def tech_nx():
    items = techArticles() or []
    cache_articles(items, 'tech')
    return render_template('nx_tech.html', sources=items)

@app.route('/category/entertainment', endpoint='entertainment')
def entertainment_nx():
    items = entArticles() or []
    cache_articles(items, 'entertainment')
    return render_template('nx_entertainment.html', sources=items)

@app.route('/category/science', endpoint='science')
def science_nx():
    items = scienceArticles() or []
    cache_articles(items, 'science')
    return render_template('nx_science.html', sources=items)

@app.route('/category/sports', endpoint='sports')
def sports_nx():
    items = sportArticles() or []
    cache_articles(items, 'sports')
    return render_template('nx_sport.html', sources=items)

# --- Auth ---

@app.route('/register', methods=['GET','POST'], endpoint='register')
def register_nx():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','')
        if not username or not email or not password:
            flash('Molimo ispunite sva polja.')
            return redirect(url_for('register'))
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Korisnik s tim korisničkim imenom ili emailom već postoji.')
            return redirect(url_for('register'))
        user = User(username=username, email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Dobrodošli!')
        return redirect(url_for('home'))
    return render_template('nx_register.html')

@app.route('/login', methods=['GET','POST'], endpoint='login')
def login_nx():
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Prijava uspješna.')
            return redirect(url_for('home'))
        flash('Neispravni podaci.')
        return redirect(url_for('login'))
    return render_template('nx_login.html')

@app.route('/logout', endpoint='logout')
@login_required
def logout_nx():
    logout_user()
    flash('Odjavljeni ste.')
    return redirect(url_for('home'))

# --- Preferences & Favorites ---

@app.route('/profile', methods=['GET','POST'], endpoint='profile')
@login_required
def profile_nx():
    if request.method == 'POST':
        # update preferences from checkboxes
        chosen = request.form.getlist('categories')
        # clear old
        Preference.query.filter_by(user_id=current_user.id).delete()
        for c in chosen:
            if c in CATEGORIES:
                db.session.add(Preference(user_id=current_user.id, category=c))
        db.session.commit()
        flash('Preferencije spremljene.')
        return redirect(url_for('profile'))
    # current preferences
    prefs = {p.category for p in Preference.query.filter_by(user_id=current_user.id).all()}
    return render_template('nx_profile.html', categories=CATEGORIES, prefs=prefs)

@app.route('/favorite', methods=['POST'], endpoint='favorite')
@login_required
def favorite_nx():
    article_url = request.form.get('url')
    if not article_url:
        return redirect(request.referrer or url_for('home'))
    art = Article.query.filter_by(url=article_url).first()
    if not art:
        # lightweight creation if not cached yet
        title = request.form.get('title')
        image_url = request.form.get('image_url')
        art = Article(title=title, url=article_url, image_url=image_url)
        db.session.add(art)
        db.session.commit()
    # check if already favorited
    from sqlalchemy import and_
    exists = Favorite.query.filter(and_(Favorite.user_id==current_user.id, Favorite.article_id==art.id)).first()
    if not exists:
        db.session.add(Favorite(user_id=current_user.id, article_id=art.id))
        db.session.commit()
        flash('Spremljeno u favorite.')
    return redirect(request.referrer or url_for('home'))

@app.route('/favorites', endpoint='favorites')
@login_required
def favorites_nx():
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    articles = []
    for f in favs:
        a = Article.query.get(f.article_id)
        if a:
            articles.append(a)
    return render_template('nx_favorites.html', articles=articles)