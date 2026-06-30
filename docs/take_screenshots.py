import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main():
    print("Initializing Selenium Chrome Driver...")
    options = Options()
    options.add_argument("--headless=new")  # ヘッドレスモード
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Chrome Web Driver の自動設定
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    output_dir = "/Users/macbook-projavlon/Desktop/JDU_bitiruv/cowork"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. メイン画面へのアクセス
        print("Navigating to http://localhost:5173/...")
        driver.get("http://localhost:5173/")
        time.sleep(3)  # 地図やリソースの読み込み待機
        
        main_path = os.path.join(output_dir, "screenshot_main.png")
        driver.save_screenshot(main_path)
        print(f"Saved main screenshot to {main_path}")
        
        # 2. チャットボットを開く
        print("Opening Mikka AI Assistant Chat Widget...")
        chat_btn = driver.find_element(By.ID, "chat-toggle-btn")
        chat_btn.click()
        time.sleep(1)
        
        chat_path = os.path.join(output_dir, "screenshot_chat.png")
        driver.save_screenshot(chat_path)
        print(f"Saved chat screenshot to {chat_path}")
        
        # チャットを閉じる
        close_chat = driver.find_element(By.ID, "chat-close-btn")
        close_chat.click()
        time.sleep(0.5)
        
        # 3. ログインモーダルを開く
        print("Opening Login Modal...")
        login_btn = driver.find_element(By.ID, "btn-show-login")
        login_btn.click()
        time.sleep(1)
        
        login_modal_path = os.path.join(output_dir, "screenshot_login.png")
        driver.save_screenshot(login_modal_path)
        print(f"Saved login modal screenshot to {login_modal_path}")
        
        # 4. ログイン実行 (Admin アカウント)
        print("Logging in as admin...")
        email_input = driver.find_element(By.ID, "login-email")
        password_input = driver.find_element(By.ID, "login-password")
        
        email_input.send_keys("admin@jdu.uz")
        password_input.send_keys("admin123")
        
        form_login = driver.find_element(By.ID, "form-login")
        form_login.submit()
        time.sleep(2)  # ログイン認証の待機
        
        # 5. 店舗登録モーダルを開く (ログイン後のみ表示されるボタン)
        print("Opening Add Restaurant Modal...")
        add_rest_btn = driver.find_element(By.ID, "btn-add-restaurant-trigger")
        add_rest_btn.click()
        time.sleep(1)
        
        add_modal_path = os.path.join(output_dir, "screenshot_add.png")
        driver.save_screenshot(add_modal_path)
        print(f"Saved add restaurant modal screenshot to {add_modal_path}")
        
    except Exception as e:
        print(f"An error occurred during screenshot generation: {e}")
    finally:
        driver.quit()
        print("Selenium execution finished.")

if __name__ == "__main__":
    main()
