from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from PIL import Image
from io import BytesIO
import easyocr
import schedule
from dotenv import load_dotenv
import os

load_dotenv()

def initialize_driver():
    """
    Khởi tạo trình duyệt Chrome và mở trang kiểm tra phương tiện vi phạm.
    
    Returns:
        webdriver.Chrome: Đối tượng trình duyệt đã được khởi tạo
    """
    driver = webdriver.Chrome()
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
    return driver

def input_license_plate(driver, bien_so):
    """
    Nhập biển số xe vào form.
    
    Args:
        driver (webdriver.Chrome): Đối tượng trình duyệt
        bien_so (str): Biển số xe cần tra cứu
    """
    ele_bs = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[1]/input')
    ele_bs.click()
    ele_bs.send_keys(bien_so)
    time.sleep(1)

def select_vehicle_type(driver, loai):
    """
    Chọn loại phương tiện (xe máy, ô tô,...).
    
    Args:
        driver (webdriver.Chrome): Đối tượng trình duyệt
        loai (str): Mã loại phương tiện
    """
    loai_xe = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[2]/select')
    select = Select(loai_xe)
    select.select_by_value(str(loai))
    time.sleep(1)

def solve_captcha(driver):
    """
    Giải mã captcha bằng OCR.
    
    Args:
        driver (webdriver.Chrome): Đối tượng trình duyệt
        
    Returns:
        str: Kết quả giải mã captcha
    """
    # Chụp ảnh captcha
    img_url = driver.find_element(By.ID, 'imgCaptcha')
    img_src = img_url.screenshot_as_png

    # Lưu ảnh để phân tích
    img = Image.open(BytesIO(img_src))
    img.save("captcha.png")

    # Giải mã captcha bằng easyocr
    time.sleep(5)
    reader = easyocr.Reader(['en'])
    result = reader.readtext('captcha.png', detail=0)
    
    return result[0]

def input_captcha_and_submit(driver, captcha_text):
    """
    Nhập mã captcha và gửi form tra cứu.
    
    Args:
        driver (webdriver.Chrome): Đối tượng trình duyệt
        captcha_text (str): Mã captcha đã giải
    """
    captcha_input = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[1]/form/div/div[2]/div[3]/div/input')
    captcha_input.click()
    captcha_input.send_keys(captcha_text)
    time.sleep(1)

    btn = driver.find_element(By.CLASS_NAME, 'btnTraCuu')
    btn.click()
    time.sleep(10)

def check_result(driver):
    """
    Kiểm tra kết quả tra cứu.
    
    Args:
        driver (webdriver.Chrome): Đối tượng trình duyệt
        
    Returns:
        bool: True nếu mã captcha đúng, False nếu sai
        str: Thông báo kết quả
    """
    check_code = driver.find_element(By.CLASS_NAME, 'xe_texterror').text
    if check_code != "":
        return False, "Giải mã thất bại"
    
    fin = driver.find_element(By.XPATH, '/html/body/center/div[3]/div/div[2]/div[2]/div/div/div[2]/div').text
    if fin == "Không tìm thấy kết quả !":
        return True, "Không tìm thấy phương tiện của bạn"
    else:
        return True, "Tìm kiếm thành công"

def main():
    """
    Hàm chính để thực hiện tra cứu phương tiện vi phạm.
    Đọc thông tin biển số và loại phương tiện từ file .env,
    sau đó thực hiện tra cứu tự động trên trang web.
    """
    bien_so = os.getenv("BIEN")
    loai = os.getenv("LOAI")

    driver = initialize_driver()
    
    # Nhập biển số và chọn loại xe
    input_license_plate(driver, bien_so)
    select_vehicle_type(driver, loai)
    
    # Giải mã captcha
    captcha_text = solve_captcha(driver)
    
    # Nhập captcha và gửi form
    input_captcha_and_submit(driver, captcha_text)
    
    # Kiểm tra kết quả
    success, message = check_result(driver)
    print(message)
    
    # Đóng trình duyệt hoặc thử lại nếu thất bại
    if not success:
        driver.close()
        main()  # Thử lại nếu giải mã thất bại
    else:
        driver.close()

# Lên lịch chạy tự động
schedule.every().day.at("06:00").do(main)
schedule.every().day.at("12:00").do(main)

if __name__ == "__main__":
    # Chạy lần đầu khi chương trình bắt đầu
    main()
    
    # Duy trì lịch chạy
    while True:
        schedule.run_pending()
        time.sleep(1)