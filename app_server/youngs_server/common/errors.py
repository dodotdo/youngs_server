from youngs_server.youngs_app import log
from ..models.host_models import Member, Lecture
from ..customlib.flask_restful import abort


def __check_lecture_exist(lecture_id):
    return True if Lecture.query.get(lecture_id) is not None else False


def abort_if_room_exist(room_number):
    if __check_room_exist(room_number):
        abort(409, message="Room {} already exist".format(room_number))


def abort_if_lecture_not_exist(lecture_id):
    if not __check_lecture_exist(lecture_id):
        abort(404, message="Lecture {} not exists".format(lecture_id))


def __check_member_email_exist(email):
    return True if Member.query.filter_by(email=email).first() is not None else False


def abort_if_member_email_exist(email):
    if __check_member_email_exist(email):
        abort(409, message="Member email {} already exist".format(email))


def abort_if_member_email_not_exist(email):
    if not __check_member_email_exist(email):
        log.warn("member not exist")
        abort(404, message="Member email {} not exists".format(email))


def __check_member_id_exist(id):
    return True if Member.query.get(id) is not None else False


def abort_if_member_id_exist(id):
    if __check_member_id_exist(id):
        abort(409, message="Member id {} already exist".format(id))


def abort_if_member_id_not_exist(id):
    if not __check_member_id_exist(id):
        abort(404, message="Member id {} not exists".format(id))


def __check_inspection_assigned(room_number, assign_date, member_id):
    return True if Inspection.query.filter_by(room_number=room_number, assign_date=assign_date).first() \
        is not None else False


def abort_if_inspection_assigned(room_number, assign_date, member_id):
    if __check_inspection_assigned(room_number, assign_date, member_id):
        abort(409, message="The room {} on {} is already assigned".format(room_number, assign_date))


def abort_if_inspection_not_assigned(room_number, assign_date, member_id):
    if not __check_inspection_assigned(room_number, assign_date, member_id):
        abort(404, message="The room {} on {} is not assigned to you".format(room_number, assign_date))


def __check_inspection_result_id_exist(id):
    return True if Inspection.query.get(id) is not None else False


def abort_if_inspection_result_id_not_exist(inspection_id):
    if not __check_inspection_result_id_exist(inspection_id):
        abort(404, message='Inspection ID {} is not exists'.format(inspection_id))



def abort_if_clean_assign_duplicated(room_number, member_id, args):
    clean = Clean.query.filter_by(room_number=room_number, assign_date=args.assign_date).first()

    if clean is not None:
        if clean.member_id == member_id:
            abort(409, message="The room {} on {} is already assigned to {}".
                  format(room_number, args.assign_date, Member.query.get(member_id)))
        else:
            abort(409, message="The room {} on {} is already assigned to someone".
                  format(room_number, args.assign_date))
