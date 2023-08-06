"""
Mock responses that mimic actual responses from Abode servers.
This file should be updated any time the Abode server responses
change so we can make sure abodepy can still communicate.
"""

import helpers.constants as const

AUTH_TOKEN = 'web-1eb04ba2236d85f49d4b9b4bb91665f2'
AUTH_TOKEN_2 = 'web-391fb500ad4d0734b11ea2cc494876f2'

def PANEL_RESPONSE(mode=const.MODE_STANDBY, battery=False, is_cellular=False):
    return '{\
       "version":"ABGW 0.0.2.17F ABGW-L1-XA36J 3.1.2.6.1 Z-Wave 3.95",\
       "report_account":"5555",\
       "online":"1",\
       "initialized":"1",\
       "net_version":"ABGW 0.0.2.17F",\
       "rf_version":"ABGW-L1-XA36J",\
       "zigbee_version":"3.1.2.6.1",\
       "z_wave_version":"Z-Wave 3.95",\
       "timezone":"America\/New_York",\
       "ac_fail":"0",\
       "battery":"'+str(int(battery))+'",\
       "ip":"192.168.1.1",\
       "jam":"0",\
       "rssi":"2",\
       "setup_zone_1":"1",\
       "setup_zone_2":"1",\
       "setup_zone_3":"1",\
       "setup_zone_4":"1",\
       "setup_zone_5":"1",\
       "setup_zone_6":"1",\
       "setup_zone_7":"1",\
       "setup_zone_8":"1",\
       "setup_zone_9":"1",\
       "setup_zone_10":"1",\
       "setup_gateway":"1",\
       "setup_contacts":"1",\
       "setup_billing":"1",\
       "setup_users":"1",\
       "is_cellular":"'+str(int(is_cellular))+'",\
       "plan_set_id":"1",\
       "dealer_id":"0",\
       "tz_diff":"-04:00",\
       "mode":{  \
          "area_1":"'+mode+'",\
          "area_2":"standby"\
       }\
    }'

USER_RESPONSE = '{\
          "id":"user@email.com",\
          "email":"user@email.com",\
          "first_name":"John",\
          "last_name":"Doe",\
          "phone":"5555551212",\
          "profile_pic":"https:\/\/s3.amazonaws.com\/my.goabode.com\/avatar\/default-image.svg",\
          "address":"555 None St.",\
          "city":"New York City",\
          "state":"NY",\
          "zip":"10108",\
          "country":"US",\
          "longitude":"0",\
          "latitude":"0",\
          "timezone":"America\/New_York_City",\
          "verified":"1",\
          "plan":"Basic",\
          "plan_id":"0",\
          "plan_active":"1",\
          "cms_code":"1111",\
          "cms_active":"0",\
          "cms_started_at":"",\
          "cms_expiry":"",\
          "cms_ondemand":"",\
          "step":"-1",\
          "cms_permit_no":"",\
          "opted_plan_id":"",\
          "stripe_account":"1",\
          "plan_effective_from":"",\
          "agreement":"1",\
          "associate_users":"1",\
          "owner":"1"\
       }'
    
LOGIN_RESPONSE = '\
    {\
       "token":"'+AUTH_TOKEN+'",\
       "expired_at":"2017-06-05 00:14:12",\
       "initiate_screen":"timeline",\
       "user":'+USER_RESPONSE+',\
       "panel":'+PANEL_RESPONSE()+',\
       "permissions":{  \
          "premium_streaming":"0",\
          "guest_app":"0",\
          "family_app":"0",\
          "multiple_accounts":"1",\
          "google_voice":"1",\
          "nest":"1",\
          "alexa":"1",\
          "ifttt":"1",\
          "no_associates":"100",\
          "no_contacts":"2",\
          "no_devices":"155",\
          "no_ipcam":"100",\
          "no_quick_action":"25",\
          "no_automation":"75",\
          "media_storage":"3",\
          "cellular_backup":"0",\
          "cms_duration":"",\
          "cms_included":"0"\
       },\
       "integrations":{  \
          "nest":{  \
             "is_connected":0,\
             "is_home_selected":0\
          }\
       }\
    }'
    
LOGIN_RESPONSE_2 = '\
    {\
       "token":"'+AUTH_TOKEN_2+'",\
       "expired_at":"2017-06-05 00:14:12",\
       "initiate_screen":"timeline",\
       "user":'+USER_RESPONSE+',\
       "panel":'+PANEL_RESPONSE()+',\
       "permissions":{  \
          "premium_streaming":"0",\
          "guest_app":"0",\
          "family_app":"0",\
          "multiple_accounts":"1",\
          "google_voice":"1",\
          "nest":"1",\
          "alexa":"1",\
          "ifttt":"1",\
          "no_associates":"100",\
          "no_contacts":"2",\
          "no_devices":"155",\
          "no_ipcam":"100",\
          "no_quick_action":"25",\
          "no_automation":"75",\
          "media_storage":"3",\
          "cellular_backup":"0",\
          "cms_duration":"",\
          "cms_included":"0"\
       },\
       "integrations":{  \
          "nest":{  \
             "is_connected":0,\
             "is_home_selected":0\
          }\
       }\
    }'
    
LOGIN_FAIL_RESPONSE = '{"code":400,"message":"Username and password do not match.","detail":null}'

API_KEY_INVALID_RESPONSE = '{"code":403,"message":"Invalid API Key"}'

LOGOUT_RESPONSE = '{"code":200,"message":"Logout successful."}'

EMPTY_DEVICE_RESPONSE = '[]'

def PANEL_MODE_RESPONSE(area=1, mode=const.MODE_STANDBY):
    return '{"area": "'+area+'", "mode": "'+mode+'"}'
