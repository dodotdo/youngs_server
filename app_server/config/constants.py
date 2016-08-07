class Constants:
    REDIS_YOUNGS_LIVE_LECTURE_KEY = 'youngs:lecture:live'

    @staticmethod
    def redis_youngs_live_lecture_key(lecture_id) :
        return Constants.REDIS_YOUNGS_LIVE_LECTURE_KEY + ':' + str(lecture_id)

    @staticmethod
    def redis_youngs_live_lecture_listener_key(lecture_id):
        return Constants.redis_youngs_live_lecture_key(lecture_id) + ':listener'


    @staticmethod
    def redis_youngs_live_lecture_occupy_key(lecture_id):
        return Constants.redis_youngs_live_lecture_key(lecture_id) + ':occupy'
