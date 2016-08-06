class GoogleLanguage():
    language = {
        'Arablic':'ar',
        'Korean':'ko',
        'Japanese':'ja',
        'Spanish':'es',
        'English':'en',
        'Dutch':'nl',
        'French':'fr',
        'Chinese Simplified':'zh-CN',
        'Chinese Traditional':'zh-TW',
        'Italian':'it'
    }


class RQMServer():
    region = dict({
        '00': 'https://useast.push.samsungosp.com:8090/spp/pns/api/push',  # US East
        '50': 'https://useast.gateway.push.samsungosp.com:8090/spp/pns/api/push',  # US West
        '02': 'https://apsoutheast.push.samsungosp.com:8090/spp/pns/api/push',  # Asia Pacific Southeast
        '03': 'https://euwest.push.samsungosp.com:8090/spp/pns/api/push',  # EU West
        '04': 'https://apnortheast.push.samsungosp.com:8090/spp/pns/api/push',  # Asia Pacific Northeast
        '05': 'https://apkorea.push.samsungosp.com:8090/spp/pns/api/push',  # Korea
        '06': 'https://apchina.push.samsungosp.com.cn:8090/spp/pns/api/push',  # China
        '52': 'https://apsoutheast.gateway.push.samsungosp.com:8090/spp/pns/api/push', #Asia Pacific Southeast
        '53': 'https://euwest.gateway.push.samsungosp.com:8090/spp/pns/api/push', #EU West
        '54': 'https://apnortheast.gateway.push.samsungosp.com:8090/spp/pns/api/push', #Asia Pacific Northeast
        '55': 'https://apkorea.gateway.push.samsungosp.com:8090/spp/pns/api/push', #Korea
        '56': 'https://apchina.gateway.push.samsungosp.com.cn:8090/spp/pns/api/push' #China
    })


class FOStatus():
    status_list = ['VC', 'OC', 'VD', 'OD', 'RSA', 'PICKUP', 'C', 'D']


class RequirementStatus():
    status_list = ['HURRY', 'NONE', 'WIP', 'DONE']
    # const of requirement status for db save
    status = {
        'HURRY': 4,
        'NONE': 3,
        'WIP': 2,
        'DONE': 1
    }

    @staticmethod
    def val_to_status(val):
        for status, value in RequirementStatus.status.items():
            if value == val:
                return status
        return None



target_language = ['es', 'ar']