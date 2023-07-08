from elasticsearch import AsyncElasticsearch

from app.config import settings

elastic = AsyncElasticsearch(settings.ELASTICSEARCH_URL)
