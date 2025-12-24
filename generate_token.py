from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

def main():
    # Scopes required for the application
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    creds_file = 'credentials.json'
    token_file = 'token.json'
    
    if not os.path.exists(creds_file):
        print(f"Error: '{creds_file}' not found.")
        print("Please download the OAuth Client ID JSON from Google Cloud Console,")
        print("rename it to 'credentials.json', and place it in this folder.")
        return

    print("Starting authentication flow...")
    print("A browser window should open. Please log in with your Google account.")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Save the credentials (including refresh token)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            
        print("\nAuthentication successful!")
        print(f"Token saved to: {os.path.abspath(token_file)}")
        print("\nNEXT STEP:")
        print("Open this 'token.json' file, copy ALL content, and paste it into")
        print("GitHub Secrets as 'GMX_DRIVE_TOKEN_JSON'.")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == '__main__':
    main()
