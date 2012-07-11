#!/usr/bin/env python
# encoding: utf-8
"""
tweetbc.py

Created by Hilary Mason on 2010-04-25.
Copyright (c) 2010 Hilary Mason. All rights reserved.
"""

import sys, os
import subprocess
import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy


class tweetBC(object):
    #credentials
    TWITTER_USERNAME = 'bc_l' # configure me
    TWITTER_PASSWORD = 'XXX' # configure me
    MESSAGE_CACHE = 'last_seen.txt' # possibly configure me
    CONSUMERKEY = 'check your email hilary'
    CONSUMERSECRET = 'check your email hilary'
    APPTOKENKEY = '188131343-OgIQY14spwhSWgmj3BKNbNUfCKJs13koktkCult5'
    APPTOKENSECRET = 'c05IzVvFrztD8Val5ej9W8399x2E20zilDAHvwL8078'
    #/credentials
    
    def __init__(self):
        api = self.login_twitter(self.CONSUMERKEY, self.CONSUMERSECRET, self.APPTOKENKEY, self.APPTOKENSECRET)

        last_time_i_checked = self.get_last_seen()
        talked_to_me = api.mentions(since_id=last_time_i_checked)

        for m in talked_to_me:
            #the bc -l part
            p = subprocess.Popen("bc -l", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = p.communicate(m.text + "\n")
            answer = out.strip()
            #/bc -l
            
            #long, valid tweet
            if (m.sender_screen_name.length + m.text.length + answer.length > 140):
                print "@%s %s = %s" % (m.sender_screen_name, m.text, answer)
                
                try:
                    #hi tweeple
                    api.update_status("@%s %s" % (m.sender_screen_name, answer))
                    
                except:
                    pass
            
            #short, valid tweet
            elif answer:
                print "@%s %s = %s" % (m.sender_screen_name, m.text, answer)
                
                try:
                    #hi tweeple
                    api.update_status("@%s %s = %s" % (m.sender_screen_name, m.text, answer))
                except:
                    pass
            
            #else: does there need to be another checker for longlong responses like scale=135?
            
            
            last_time_i_checked = m.id
            
        #remember stuff on @bc_l's private brain
        f = open(self.MESSAGE_CACHE, 'w')
        f.write(str(last_time_i_checked))
        f.close()
    
    def get_last_seen(self):
        try:
            f = open(self.MESSAGE_CACHE, 'r')
            last_time_i_checked = f.read()
            f.close()
        except IOError:
            last_time_i_checked = None
            
        return last_time_i_checked

    def login_twitter(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api
        


if __name__ == '__main__':
    t = tweetBC()
