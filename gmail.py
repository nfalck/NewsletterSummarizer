import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from base64 import urlsafe_b64decode
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def make_file(sender, subject, text):
  """Make a txt file with the sender, subject and text of the email"""
  url_pattern = r'\s*\[\d+\]\s*(https?://\S+|www\.\S+)\s*' # pattern for links and spaces before and after
  clean_text = re.sub(url_pattern, '', text) # removing the links
  # writing sender, subject and text
  with open("collectedemails.txt", 'a') as file:
    file.write(f"Sender:{sender}\n")
    file.write(f"Subject:{subject}\n")
    file.write(f"Text:{clean_text}\n")

def query_setter(emails):
  """ Creating the query for the Gmail Search functionality by incorporating the specific emails and specific dates """
  query = ""

  # Add to the query the specific emails to search for
  last_item = emails[-1]
  for email in emails:
    query += "from:"
    query += email
    query += " "
    if email == last_item:
      query += " "
    else:
      query += "OR"
      query += " "

  # Add to the query the specific dates to look for
  today = datetime.date.today()
  week = today - datetime.timedelta(days=7)
  query += "after:"
  query += week.strftime("%Y/%m/%d")
  query += " "

  query += "before:"
  query += today.strftime("%Y/%m/%d")
  query += " "
  return query


def read_email(service, message):
  """ Extract the body content, subject and sender from the email and activating the make_file function """
  try:
    # retrieve the specific email and its message
    msg_result = service.users().messages().get(userId="me", id=message["id"]).execute()

    # retrieve the various parts of the message
    payload = msg_result["payload"]
    parts = payload.get('parts')[0]
    data = parts["body"]["data"] # body text
    text = urlsafe_b64decode(data).decode()
    headers = payload["headers"] # sender and subject

    # retrieve the sender and subject if it exists
    for header in headers:
      if header["name"] == "From":
        sender = header["value"]

      if header["name"] == "Subject":
        subject = header["value"]
    make_file(sender, subject, text)
  except HttpError as error:
    print(f"An error occurred: {error}")

def get_emails(query):
  """Authentication of Gmail API and calling it with specified query to retrieve the emails needed and activating the read_email function
  """
  open("collectedemails.txt", 'w').close()
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me",q=query).execute()
    messages = []
    if 'messages' in results:
      messages.extend(results['messages'])
    while 'nextPageToken' in results:
      page_token = results['nextPageToken']
      results = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
      if 'messages' in results:
        messages.extend(results['messages'])
    for message in messages:
      read_email(service, message)

  except HttpError as error:
  # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")
