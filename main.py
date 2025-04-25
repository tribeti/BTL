from selenium import webdriver
from selenium.webdriver. common . by import By
from selenium.webdriver.support.ui import Select
import time
from PIL import Image
from io import BytesIO
import easyocr
import schedule
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    bien_so = os.getenv("BIEN")
    loai = os.getenv("LOAI")

    # init
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")

    # bien so xe
    ele_bs = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[1]/input')
    ele_bs.click()
    ele_bs.send_keys(bien_so)
    time.sleep(1) 

    # loai xe (xe may, o to, ...)
    loai_xe = driver.find_element(By.XPATH,'/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[2]/select')
    select = Select(loai_xe)
    select.select_by_value(str(loai))
    time.sleep(1)

    # ma catpcha
    img_url = driver.find_element(By.ID, 'imgCaptcha')
    img_src = img_url.screenshot_as_png

    img = Image.open(BytesIO(img_src))
    img.save("captcha.png")

    time.sleep(5)
    reader = easyocr.Reader(['en'])
    result = reader.readtext('captcha.png',detail=0)

    captcha_input = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[3]/div/input')
    captcha_input.click()
    captcha_input.send_keys(result[0])
    time.sleep(1)

    btn = driver.find_element(By.CLASS_NAME,'btnTraCuu')
    btn.click()
    time.sleep(10)
    check_code = driver.find_element(By.CLASS_NAME,'xe_texterror').text
    if check_code != "":
        print('Giải mã thất bại')
        driver.close()
        main()
    else :
        fin = driver.find_element(By.XPATH,'/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[2]/div').text
        # print(fin)
        if fin == "Không tìm thấy kết quả !":
            print('Không tìm thấy phương tiện của bạn')
        else :
            print('Tìm kiếm thành công')
        driver.close()

schedule.every().day.at("6:00").do(main)
schedule.every().day.at("12:00").do(main)