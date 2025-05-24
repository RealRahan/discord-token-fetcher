import requests
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    print('\u001b[36m' + '=' * 60 + '\u001b[0m')
    print('\u001b[36m| \u001b[37mDiscord Token 2fa/non-2fa Fetcher \u001b[36m|\u001b[0m github.com/RealRahan')
    print('\u001b[36m' + '=' * 60 + '\u001b[0m')
    print()

def get_headers():
    return {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjQ5MDA1LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'Referer': 'https://discord.com/login'
    }

def login(email, password):
    session = requests.Session()  # Use session to maintain cookies
    headers = get_headers()
    data = {'login': email, 'password': password, 'undelete': False}
    
    # Initial login request
    r = session.post('https://discord.com/api/v9/auth/login', json=data, headers=headers)

    if r.status_code == 200 and r.json().get('mfa', False):
        ticket = r.json().get('ticket')
        if not ticket:
            print('\u001b[31m>\u001b[37m Error: No 2FA ticket received\u001b[0m')
            return

        print('\u001b[33m>\u001b[37m 2FA Required - Check your authenticator app\u001b[0m')
        
        # Get code with timeout
        code = input('\u001b[33m>\u001b[37m Enter 6-digit 2FA code: \u001b[0m').strip()
        
        # Prepare MFA data with proper formatting
        mfa_data = {
            'code': code,
            'ticket': ticket,
            'login_source': None,
            'gift_code_sku_id': None
        }
        
        # Additional headers that might be needed for MFA
        mfa_headers = headers.copy()
        mfa_headers.update({
            'X-Discord-Timezone': 'America/New_York',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
        })
        
        mfa_r = session.post('https://discord.com/api/v9/auth/mfa/totp', 
                           json=mfa_data, 
                           headers=mfa_headers)
        
        if mfa_r.status_code == 200:
            token = mfa_r.json().get('token')
            if token:
                print(f'\u001b[32m>\u001b[37m Token: {token}\u001b[0m')
                print('\n\u001b[32m>\u001b[37m Login successful!\u001b[0m')
            else:
                print('\u001b[31m>\u001b[37m Error: Token missing in 2FA response\u001b[0m')
                print(f'Response: {mfa_r.text}')
        else:
            print(f'\u001b[31m>\u001b[37m 2FA verification failed (Status: {mfa_r.status_code})\u001b[0m')
            print(f'Response: {mfa_r.text}')
    
    elif r.status_code == 200:
        token = r.json().get('token')
        if token:
            print(f'\u001b[32m>\u001b[37m Token: {token}\u001b[0m')
            print('\n\u001b[32m>\u001b[37m Login successful!\u001b[0m')
        else:
            print('\u001b[31m>\u001b[37m Error: No token in response\u001b[0m')
    
    elif "PASSWORD_DOES_NOT_MATCH" in r.text:
        print('\u001b[31m>\u001b[37m Incorrect password\u001b[0m')
    
    elif "captcha-required" in r.text:
        print('\u001b[31m>\u001b[37m Discord gave us captcha. Try again later\u001b[0m')
        print(f'Response: {r.text}')
    
    else:
        print(f'\u001b[31m>\u001b[37m Login failed (Status: {r.status_code})\u001b[0m')
        print(f'Response: {r.text}')

if __name__ == "__main__":
    clear_screen()
    display_title()
    email = input('\u001b[36m>\u001b[37m Email: \u001b[0m').strip()
    password = input('\u001b[36m>\u001b[37m Password: \u001b[0m').strip()
    login(email, password)
    input('\n\u001b[37mPress Enter to exit...\u001b[0m')
