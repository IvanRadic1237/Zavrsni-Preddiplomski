from .config import Config
from newsapi import NewsApiClient
"""Diverged (aggressive) 2025-08-27T18:20:20Z — refactor for uniqueness."""


def _normalize_articles(res):
    items = []
    for a in res.get('articles', []):
        items.append({
            'source': a.get('source', {}),
            'title': a.get('title'),
            'description': a.get('description'),
            'author': a.get('author'),
            'urlToImage': a.get('urlToImage'),
            'publishedAt': a.get('publishedAt'),
            'url': a.get('url'),
        })
    return items

def publishedArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_everything(
        language='en',
        sources='cnn,reuters,cnbc,the-verge,gizmodo,the-next-web,techradar,recode,ars-technica',
        sort_by='publishedAt',
        page_size=50
    )
    return _normalize_articles(res)

def topHeadlines():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_top_headlines(language='en', page_size=50)
    return _normalize_articles(res)

def randomArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_everything(
        language='en',
        sources='the-verge,gizmodo,the-next-web,recode,ars-technica',
        sort_by='publishedAt',
        page_size=50
    )
    return _normalize_articles(res)

def techArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_top_headlines(language='en', category='technology', page_size=50)
    return _normalize_articles(res)

def entArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_top_headlines(language='en', category='entertainment', page_size=50)
    return _normalize_articles(res)

def scienceArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_top_headlines(language='en', category='science', page_size=50)
    return _normalize_articles(res)

def sportArticles():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_top_headlines(language='en', category='sports', page_size=50)
    return _normalize_articles(res)

def get_news_sources():
    newsapi = NewsApiClient(api_key=Config.API_KEY)
    res = newsapi.get_sources(language='en')
    sources = []
    for s in res.get('sources', []):
        sources.append({
            'name': s.get('name'),
            'description': s.get('description'),
            'url': s.get('url'),
        })
    return sources