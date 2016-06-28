#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import fnmatch
import base64
from apiclient import errors
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import os
import httplib2
from apiclient.discovery import build
import urllib2
from oauth2client.client import flow_from_clientsecrets
import sys
from email.mime.text import MIMEText


def complete():
    users = ['baluja@gmail.com', 'azb2003@gmail.com',
             'kfbaluja@gmail.com', 'carinanicolekarp@gmail.com']

    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                'gmail-python-quickstart.json')
        flags = \
            argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('cs2.json',
                    'https://mail.google.com/')
            flow.user_agent = 'hi'
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:

                  # Needed only for compatibility with Python 2.6

                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    user = 'me'
    credentials = get_credentials()

    print(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('gmail', 'v1', http=http)
    os.chdir('gimages')

    def sending(user_id, msg_id):
        message = service.users().messages().get(userId=user_id,
                id=msg_id).execute()
        global sender
        for i in message['payload']['headers']:
            print(i)
            if i['name'] == 'Return-Path':

                print(i['value'])
                sender = i['value']
                print('triggered')
                sender = sender[1:-1]
                print('Sender found!: ' + sender)

    def GetAttachments(
        service,
        user_id,
        msg_id,
        store_dir,
        ):

        global nextname
        global idd
        global filetype
        nextname = '1'
        message = service.users().messages().get(userId=user_id,
                id=msg_id).execute()

      # print (message['payload']['parts'])

        print(sender)
        if sender in users:
            while os.path.isfile(nextname + '.jpg') != False:
                nextname = int(nextname) + 1
                nextname = str(nextname)
            storage = store_dir
            for i in message['payload']['parts']:
                if i['filename']:
                    print('-++++++++++++++++++++++-')
                    print('i')
                    print(i['body']['attachmentId'])
                    filetype = i['mimeType'].split('/')[1]
                    print('-++++++++++++++++++++++-')
                    print(message['payload']['parts'])
                    print('-++++++++++++++++++++++-')
                    print('Found data!')
                    idd = i['body']['attachmentId']
                    print(idd)
                    att = \
                        service.users().messages().attachments().get(userId=user_id,
                            messageId=msg_id, id=idd).execute()
                    data = att['data']
                    file_data = \
                        base64.urlsafe_b64decode(data.encode('UTF-8'))
            print('================================')
            print('')
            print('================================')
            print('')
            print('================================')
            print('')
            path = '' + nextname + '.' + filetype

            f = open(path, 'wb')
            f.write(file_data)
            f.close()
            os.rename(path, nextname + '.jpg')
        else:
            print('Invalid sender')

    def msgResponse():
        message = MIMEText('Thanks for the picture, ' + sender)
        message['to'] = sender
        message['from'] = 'testingazb@gmail.com'
        message['subject'] = 'Image Recieved!'
        body = {'raw': base64.b64encode(message.as_string())}

        try:
            message = service.users().messages().send(userId='me',
                    body=body).execute()
            print('Message Id: %s' % message['id'])
            print(message)
        except Exception, error:
            print('An error occurred: %s' % error)

    def delete(service, user_id, msg_id):

        service.users().messages().delete(userId=user_id,
                id=msg_id).execute()

    def ListLabels(service, user_id):
        """Get a list all labels in the user's mailbox.
      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value user
        can be used to indicate the authenticated user.

      Returns:
        A list all Labels in the user's mailbox.
      """

        try:
            response = \
                service.users().labels().list(userId=user_id).execute()
            labels = response['labels']
            return labels
        except errors.HttpError, error:
            print('An error occurred2')

    def ListMessagesWithLabels(service, user_id, query=''):
        """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value user
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """

        try:
            response = service.users().messages().list(userId=user_id,
                    q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = \
                    service.users().messages().list(userId=user_id,
                        q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError, error:
            print('An error occurred3')

    print(service.users().messages().list(userId='me'
          ).execute().values())

    def downloadAttach():
        messsages = service.users().messages().list(userId='me'
                ).execute().values()
        if messsages[0] > 0:
            print(messsages)
            messages = messsages[1]
            print(messages)
            if messages[0] > 0:
                print('____')
                print(messsages)
                print('____')
                for m in range(messsages[0]):
                    print('triggered')
                    print(messages)
                    print(m)
                    messages = messages[m]
                    sending('me', messages['id'])
                    print('____ messages[m]')
                    print(messages)
                    print('____ sender')
                    print(sender)
                    print('else')
                    if sender == 'testingazb@gmail.com':
                        print('This message is in sent. IGNORED.')
                        delete(service, user, messages['id'])
                    elif sender in users:
                        print(messsages)
                        print(messages)
                        GetAttachments(service, user, messages['id'],
                                'gimages')
                        delete(service, user, messages['id'])
                        print('Image #' + nextname + ' recieved :D')
                        msgResponse()
                    else:
                        print('denied. illegal user')
                        delete(service, user, messages['id'])
                    break
        else:
            print('No new images D:')

    downloadAttach()


complete()
