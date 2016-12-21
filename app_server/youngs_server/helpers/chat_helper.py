import os
from subprocess import check_output  # for system command call
from flask import current_app
from flask_restful import abort
from youngs_server.youngs_app import log
from youngs_server.models.host_models import ChatMember, ChatChannel, Employee


def generate_voice_url(message, voice_format):

    if message.voice_filename is not None:
        filename = message.voice_filename
        if voice_format == 'mp3':
            filepath_amr = "./app/static/voice/" + filename
            filepath_mp3 = "./app/static/voice/" + filename[:-3] + "mp3"
            if not os.path.exists(filepath_mp3):
                output = check_output("ffmpeg -i " + filepath_amr + " -ar 22050 " + filepath_mp3, shell=True)
            msg_url = current_app.config['BASE_SERVER'] + \
                       '/api/v2/chats/msg/' + message.filename[:-3] + 'mp3'
        else:
            msg_url = current_app.config['BASE_SERVER'] + '/api/v2/chats/msg/' + filename
    else:
        msg_url = None

    return msg_url


def _check_channel_name_exist(name):
    return True if ChatChannel.query.filter_by(name=name).first() is not None else False


def _check_channel_id_exist(channel_id):
    return True if ChatChannel.query.filter_by(id=channel_id).first() is not None else False


def abort_if_channel_name_exist(name):
    if _check_channel_name_exist(name):
        abort(409, message="Channel Name {} is already exists".format(name))


def abort_if_channel_name_not_exist(name):
    if not _check_channel_name_exist(name):
        abort(409, message="Channel Name {} is already exists".format(name))


def abort_if_channel_id_not_exist(name):
    if not _check_channel_id_exist(name):
        abort(404, message="Channel Name {} is not exists".format(name))

def _check_channel_member_exist(channel_id, employee_id):
    if ChatMember.query.outerjoin(Employee).\
            filter(ChatMember.channel_id == channel_id, ChatMember.person_id == employee_id).first() is not None:
        return True
    return False

def abort_if_channel_member_exist(channel_id, employee_id):
    if _check_channel_member_exist(channel_id, employee_id):
        abort(409, message="Employee {} on {} channel is already exists".format(employee_id, channel_id))

def abort_if_channel_member_not_exist(channel_id, employee_id):
    if not _check_channel_member_exist(channel_id, employee_id):
        abort(409, message="Employee {} on {} channel is already exists".format(employee_id, channel_id))
