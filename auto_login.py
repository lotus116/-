import requests
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 自动配置信息 --------------------------------
# cclear116
LOGIN_PAGE_URL = 'http://100.64.13.17/a79.htm?wlanacip=100%2e64%2e13%2e18'
USER_ACCOUNT = '22251109xxx' # 你的账号
USER_PASSWORD = 'xxxxxx' # 你的密码
# ------------------------------------------------

# 检查网络连接 (requests)
def check_connection(timeout=3):
    check_url = 'http://connectivitycheck.gstatic.com/generate_204'
    try:
        response = requests.get(check_url, timeout=timeout, allow_redirects=False)
        return response.status_code == 204
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return False
    except Exception as e:
        return False


# 登录 (使用 Selenium 驱动 Edge) 这里不能用requests,因为登录页面有JS验证，加密了
def login():
    print(f"[{time.ctime()}] 侦测到掉线，正在启动 Selenium (Edge) 尝试登录...")
    
    edge_options = Options()
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--log-level=3")
    edge_options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.39'")
    
    # ！！关键改动：手动指定 msedgedriver.exe 的路径
    driver = None
    try:
        # __file__ 是指本脚本文件(auto_login.py)
        # os.path.dirname(__file__) 是指本脚本所在的文件夹 (C:\校园网自动登录)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        driver_path = os.path.join(script_dir, "msedgedriver.exe")
        
        if not os.path.exists(driver_path):
            print(f"错误：msedgedriver.exe 未找到！")
            print(f"请从微软官网下载后放在 {script_dir} 文件夹中。")
            return

        edge_service = Service(driver_path) # <-- 告诉 Selenium 使用这个驱动
        
        driver = webdriver.Edge(service=edge_service, options=edge_options)
        wait = WebDriverWait(driver, 10) # 10秒等待
        
        driver.get(LOGIN_PAGE_URL)
        
        # 1. 账号
        user_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='DDDDD'][type='text']"))
        )
        user_input.send_keys(USER_ACCOUNT)
        
        # 2. 密码
        pass_input = driver.find_element(By.CSS_SELECTOR, "input[name='upass'][type='password']")
        pass_input.send_keys(USER_PASSWORD)
        
        # 3. 登录
        login_btn = driver.find_element(By.CSS_SELECTOR, "input[name='0MKKey'][type='button']")
        login_btn.click()
        
        print("...登录操作已执行。")
        print("...等待 10 秒让网络充分连接...")
        time.sleep(10) 
        
        if check_connection():
            print("登录成功！网络已连接。")
        else:
            print("...登录似乎未成功，脚本将在下次循环时重试。")

    except Exception as e:
        print(f"Selenium (Edge) 登录时发生异常: {e}")
        
    finally:
        if driver:
            driver.quit()
# --- 主循环 ---
def main_loop(check_interval_seconds=30):
    print("校园网自动重连脚本已启动")
    print(f"将每隔 {check_interval_seconds} 秒检测一次网络状态。")
    
    if not check_connection():
        login()

    while True:
        time.sleep(check_interval_seconds)
        if not check_connection():
            login()
        else:
            pass 

if __name__ == "__main__":
    # 确保你安装了: pip install --upgrade requests selenium
    
    print("开始自动登录...")
    print("现在是: ", time.ctime())
    main_loop(check_interval_seconds=30)
