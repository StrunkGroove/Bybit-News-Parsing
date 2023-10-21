import os
import redis


class RedisProcess:
    """
    Класс для работы с Redis
    """

    def __init__(self):
        """
        Инициализирует класс
        """
        db = os.environ.get('REDIS_DB', 0)
        port = os.environ.get('REDIS_PORT', 6379)
        self.redis = redis.StrictRedis(host="redis", port=port, db=db)

    def save(self, title: str) -> str:
        """
        Сохраняет заголовок
        """
        value = ''
        self.redis.setnx(title, value) # title - ключ, value - значение
    
    def exists(self, title: str) -> str:
        """
        Проверяет заголовок на уникальность
        :return: Значение ключа `title` в Redis, или `None`, если ключ не существует.
        """
        return self.redis.get(title)