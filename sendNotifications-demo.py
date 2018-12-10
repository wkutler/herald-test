import requests
import json
import os
import pyrebase
import time
from pusher_push_notifications import PushNotifications

while True:
    config = {
      "apiKey": "AIzaSyDTWo_NRBBAr3Zp4OcHuwRL7GkBuu9So-s",
      "authDomain": "herald-5b6cc.firebaseapp.com",
      "databaseURL": "https://herald-5b6cc.firebaseio.com/",
      "storageBucket": "herald-5b6cc.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    all_users = db.child('users').get()
    for user in all_users.each():
        #iterate through all users
        username = user.key()
        if username == 'wkutler':
            token = user.val()['token']
            last_timestamp = user.val()['last_commit_timestamp']
            print('///////////')
            print('checking notifications for ' + username)
            print('last timestamp: ' + str(last_timestamp))
            response = requests.get('https://heraldapp.herokuapp.com/backendConfig/' + username
                + '&' + token + '/notification/' + str(last_timestamp))
            print(response)
            print(response.json())
            notification = response.json()['notification']
            if notification != 'NA':
                #new commits added, so send push notification
                new_time = response.json()['new_timestamp']
                data = {'last_commit_timestamp': new_time, 'token': token}
                db.child('users').child(username).set(data)
                pn_client = PushNotifications(
                    instance_id='3205f451-bb8e-400c-ac13-88d5750a6bfc',
                    secret_key='78C3B49B6A8C52FD8A7392C8794CE43CC4562B4C1D71288F8F4CBEA58DB8E7AF',
                )
                response = pn_client.publish(
                  interests=[username],
                  publish_body={
                    'apns': {
                      'aps': {
                        'alert': notification,
                      },
                    },
                  },
                )
                print(response)
