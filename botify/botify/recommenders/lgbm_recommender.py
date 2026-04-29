from .recommender import Recommender

class LGBMRecommender(Recommender):
    def __init__(self, recommendations_redis, catalog, fallback):
        self.recommendations_redis = recommendations_redis
        self.catalog = catalog
        self.fallback = fallback

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        data = self.recommendations_redis.get(str(user))
        if data is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        recs = self.catalog.from_bytes(data)
        if not recs:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        try:
            idx = recs.index(prev_track)
            return recs[idx + 1] if idx + 1 < len(recs) else recs[0]
        except ValueError:
            return recs[0]