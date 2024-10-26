from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Function to get LinkedIn user profile
def get_linkedin_user_id(access_token):
    try:
        # LinkedIn API URL for fetching user profile
        url = 'https://api.linkedin.com/v2/me'

        # Set up headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Send request to LinkedIn API
        response = requests.get(url, headers=headers, timeout=5)  # 5 seconds timeout

        # Handle LinkedIn API response
        if response.status_code == 200:
            data = response.json()
            # Return LinkedIn user ID or any other required information
            return data.get('id'), None
        else:
            error_data = response.json()
            return None, error_data.get('message', 'Unknown error')

    except requests.exceptions.Timeout:
        return None, 'Request timed out'
    except Exception as e:
        return None, str(e)

# Function to create a post on LinkedIn
@app.route('/api/linkedin/post', methods=['POST'])
def linkedin_post():
    try:
        # Extract access token and post content from request body
        data = request.get_json()
        access_token = data.get('accessToken')
        content = data.get('content')

        # Fetch user ID dynamically
        user_id, error = get_linkedin_user_id(access_token)
        if error:
            return jsonify({
                'error': 'Failed to fetch LinkedIn user ID',
                'details': error
            }), 400

        # LinkedIn API endpoint for UGC posts
        url = 'https://api.linkedin.com/v2/ugcPosts'

        # Post body data
        body = {
            "author": f"urn:li:person:{user_id}",  # Dynamically fetched user ID
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": content,  # Text for your LinkedIn post
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        # Send POST request to LinkedIn API
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))

        # Check for successful response
        if response.status_code == 201 or response.status_code == 200:
            return jsonify({
                'message': 'Post created successfully!',
                'data': response.json()
            }), 200
        else:
            return jsonify({
                'error': 'Failed to create post',
                'details': response.json()
            }), response.status_code

    except Exception as e:
        return jsonify({
            'error': 'An error occurred',
            'details': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
