mport print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


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

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_label_id(service, user_id, label_name):
    """Get a list all labels in the user's mailbox.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.

    Returns:
      A list all Labels in the user's mailbox.
    """
    foss_label_id = ""
    try:
        response = service.users().labels().list(userId=user_id).execute()
        labels = response['labels']
        for label in labels:
            if label['name'] == label_name:
                # print('Label id: %s - Label name: %s' % (label['id'], label['name']))
                foss_label_id = label['id']
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

    return foss_label_id


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      label_ids: Only return Messages with these labelIds applied.

    Returns:
      List of Messages that have all required Labels applied. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print
        'An error occurred: %s' % error


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    foss_label = get_label_id(service=service, user_id='me', label_name='FOSS')

    print ("FOSS label = " + foss_label)

    print(len(ListMessagesWithLabels(service, "me", [foss_label])))

if __name__ == '__main__':
    main()

