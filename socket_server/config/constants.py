class Constants:
    REDIS_YOUNGS_LECTURE_LIVE_KEY = 'youngs:lecture:live'

    @staticmethod
    def redis_youngs_lecture_key(channel_id) :
        return Constants.REDIS_YOUNGS_LECTURE_LIVE_KEY + ':' + str(channel_id)

    @staticmethod
    def redis_youngs_lecture_occupy_key(channel_id):
        return Constants.redis_youngs_lecture_key(channel_id) + ':occupy'

    @staticmethod
    def redis_youngs_lecture_listener_key(channel_id):
        return Constants.redis_youngs_lecture_key(channel_id) + ':listener'

    @staticmethod
    def redis_youngs_auth_token(token):
        return 'auth:token:'+token