import os
import time
from playwright.sync_api import sync_playwright

COOKIE_FILE = ".session_cookie"
LOGIN_URL = "https://adventofcode.com/2025/auth/login"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print(f"Opening {LOGIN_URL}...")
        page.goto(LOGIN_URL)
        
        print("Please log in via the browser window...")
        
        # Wait for the session cookie to be set
        while True:
            cookies = context.cookies()
            session_cookie = next((c for c in cookies if c["name"] == "session"), None)
            
            if session_cookie:
                print("Session cookie found!")
                with open(COOKIE_FILE, "w") as f:
                    f.write(f"session={session_cookie['value']}")
                print(f"Cookie saved to {COOKIE_FILE}")
                break
            
            time.sleep(1)
            
        browser.close()

if __name__ == "__main__":
    if os.path.exists(COOKIE_FILE):
        print(f"{COOKIE_FILE} already exists. Delete it if you want to re-login.")
    else:
        run()
