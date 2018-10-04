# Using only a gmail to control criation many accounts in Happn

## How?
It is possible, because gmail [ignore dots](https://support.google.com/mail/answer/7436150?hl=en. However to Happn API are different emails.

## Flow
- Create a gmail with 30 caracteres.
- Turn on the [Gmail API to python](https://developers.google.com/gmail/api/quickstart/python). Execute just the Step 1.
- Export GAW_SCOPES, GAW_CLIENT_SECRET_FILE_PATH, GAW_USER_ID, GAW_APPLICATION_NAME
- Run quickstart.

### Example
```
export GAW_SCOPES="https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify"
export GAW_CLIENT_SECRET_FILE_PATH=credentials.json
export GAW_USER_ID=<email@gmail.com>
# Your preferred application name.
export GAW_APPLICATION_NAME=HappnBot
```

### Quickstart;
Run the sample using the following command:

```python pyhappn/quickstart.py```

- a. The sample will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser. If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

- b. Click the Accept button.

- c. The sample will proceed automatically, and you may close the window/tab.

Path where token is created: ~/.credentials/gmail-api-wrapper-py.json.<br>
To reset token just delete this file.
