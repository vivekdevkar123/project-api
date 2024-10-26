import os
import json
from flask import Flask, Request, jsonify, request, redirect, session, url_for
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import secrets
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

# Replace with your client secret JSON file path
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
REDIRECT_URI = "http://localhost:5000/callback"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Create OAuth 2.0 flow
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
flow.redirect_uri = REDIRECT_URI

@app.route('/')
def index():
    return "Google Meet Integration!"

# Route to start the OAuth flow
@app.route('/authorize')
def authorize():
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true')
    session['state'] = state
    print(f"Authorization URL: {authorization_url}")
    print(f"State stored in session: {session['state']}")
    return redirect(authorization_url)

@app.route('/check-auth')
def check_auth():
    if 'credentials' in session:
        return {'is_authorized': True}
    return {'is_authorized': False}


# Route to handle the OAuth callback
@app.route('/callback')
def callback():
    print(f"Request state: {request.args.get('state')}")
    print(f"Session state: {session.get('state')}")
    
    if 'state' not in session:
        return "Session state not found", 400
    
    if session['state'] != request.args['state']:
        return "State mismatch error", 400

    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    return """
        <html>
        <head>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f0f8ff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    max-width: 400px;
                    text-align: center;
                }
                h2 {
                    color: #4CAF50;
                }
                p {
                    color: #333333;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    font-size: 16px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Authentication Successful</h2>
                <p>You can now safely close this page.</p>
                <button onclick="window.close()">Close Page</button>
            </div>
        </body>
        </html>
    """

# Route to create a Google Meet event
@app.route('/create-meet', methods=['GET', 'POST'])
def create_meet():
    # if 'credentials' not in session:
    #     # Redirect to Google OAuth
    #     return redirect(url_for('authorize'))

    credentials = Credentials(**session['credentials'])

    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            session['credentials'] = credentials_to_dict(credentials)
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return redirect(url_for('authorize'))

    service = build('calendar', 'v3', credentials=credentials)

    # Create a new Google Meet event
    event = {
        'summary': 'Test Meeting',
        'description': 'A test meeting for Google Meet',
        'start': {
            'dateTime': '2024-10-15T10:00:00Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': '2024-10-15T11:00:00Z',
            'timeZone': 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'conferenceSolutionKey': {'type': 'hangoutsMeet'},
                'requestId': 'test123',
            },
        },
        'attendees': [{'email': 'paaraspethe6277@gmail.com'}],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        meet_link = event.get('hangoutLink')
        return jsonify({'meet_link': meet_link})
    except Exception as e:
        print(f"Error creating meeting: {e}")
        return jsonify({'error': 'Failed to create meeting'}), 500



def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    app.run(port=5000, debug=True)
