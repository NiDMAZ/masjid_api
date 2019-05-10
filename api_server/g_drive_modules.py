from __future__ import print_function
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd
import logging

logger = logging.getLogger(__name__)


class GoogleSheetReader(object):
    def __init__(self, sheet_id=None, client_secret=None, token_cache='token.pickle'):
        self.SHEET_ID = sheet_id
        self.CLIENT_SECRET = client_secret
        self.TOKEN_CACHE = token_cache

        # If modifying these scopes, delete the file self.TOKEN_CACHE.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        self._creds = None
        self._service = None
        self._sheets_api = None

        logger.info('{} Initialised...'.format(self.__class__.__name__))

    def authenticate(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.TOKEN_CACHE):
            with open(self.TOKEN_CACHE, 'rb') as token:
                self._creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRET, self.SCOPES)
                self._creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(self.TOKEN_CACHE, 'wb') as token:
                pickle.dump(self._creds, token)

        logger.info('{} Authenticated'.format(self.__class__.__name__))

    def use_sheets_api(self):
        self.authenticate()
        self._service = build('sheets', 'v4', credentials=self._creds)

        # Call the Sheets API
        self._sheets_api = self._service.spreadsheets()
        logger.info('Created sheets service...')

    def read_data(self, sheet_name):
        logger.info('{} Reading: [{}]'.format(self.__class__.__name__, sheet_name))
        self.use_sheets_api()

        # Call the Sheets API
        result = self._sheets_api.values().get(spreadsheetId=self.SHEET_ID,
                                               range=sheet_name).execute()
        return result.get('values', [])

    def read_data_as_pd(self, sheet_name):
        results = self.read_data(sheet_name=sheet_name)
        columns = results.pop(0)
        df = pd.DataFrame(results, columns=columns)

        return df
