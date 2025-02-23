import datetime
import hashlib
import time
import random
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from logger import Logger
import os

global_config = {
    "server": "localhost",  # 替换为默认服务器地址
    "port": 4723  # 替换为默认端口
}

logger = Logger()

class Automator:
    def __init__(self, device_config):
        logger.debug("Initializing Automator with device config: {}".format(device_config))
        server = device_config.get("server", global_config["server"])
        port = device_config.get("port", global_config["port"])
        self.driver = webdriver.Remote(
            command_executor=f'http://{server}:{port}',
            desired_capabilities={
                "platformName": "Android",
                "appium:automationName": "UiAutomator2",
                "appium:appPackage": "com.xunmeng.pinduoduo",
                "appium:appActivity": ".ui.activity.MainFrameActivity",
                "appium:forceAppLaunch": True,
                "appium:noReset": True,
                "appium:printPageSourceOnFindFailure": True,
                "appium:skipDeviceInitialization": True,
                "appium:unicodeKeyBoard": True
                # "appium:deviceName": device_config["device_name"],
                # "appium:udid": device_config["udid"],
            }
        )
        logger.debug("WebDriver initialized successfully.")
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(lambda x:x.find_element(By.XPATH, "//android.widget.RelativeLayout[@content-desc=\"首页\"]"))
        except Exception as e:
            logger.error("Failed to open 首页: {}".format(str(e)))
            self.screenshot("WebDriverWait")

    def simulate_human_delay(self, min_delay=0.5, max_delay=2.5):
        """模拟人类操作间隔"""
        time.sleep(random.uniform(min_delay, max_delay))

    def simulate_human_click_and_return(self, element):
        """模拟人类行为点击进入页面并返回页面"""
        element.click()  # 点击进入页面
        self.simulate_human_delay()  # 停顿
        self.driver.back()  # 返回页面
        self.simulate_human_delay()  # 停顿

    def swipe_down_quickly(self):
        """模拟缓慢下滑"""
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-20, 20)
        actions.w3c_actions.pointer_action.move_to_location(531 + offset_x, 2110 + offset_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(544 + offset_x, 754 + offset_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_down_slowly(self):
        """模拟缓慢下滑"""
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-20, 20)
        actions.w3c_actions.pointer_action.move_to_location(539 + offset_x, 1866 + offset_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(539 + offset_x, 1133 + offset_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_up(self):
        """模拟缓慢上滑"""
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-20, 20)
        actions.w3c_actions.pointer_action.move_to_location(544 + offset_x, 905 + offset_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(537 + offset_x, 1413 + offset_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def screenshot(self, identifier="default"):
        """截取当前屏幕并保存为文件，文件名格式为：年月日+传入的字符串+hash"""
        try:
            # 获取当前日期
            date_str = datetime.now().strftime('%Y-%m-%d')
            # 生成哈希值
            hash_object = hashlib.md5(identifier.encode())
            hash_str = hash_object.hexdigest()[:8]  # 取前8位作为文件名的一部分
            filename = f"{date_str}_{identifier}_{hash_str}.png"
            screenshot_path = os.path.join(os.getcwd(), filename)
            self.driver.save_screenshot(screenshot_path)
            logger.debug("Screenshot saved to: {}".format(screenshot_path))
        except Exception as e:
            logger.error("Failed to take screenshot: {}".format(str(e)))

    def handle_product_detail(self, quick=False):
        """处理商品详情页操作"""
        logger.debug("Handling product detail with quick mode: {}".format(quick))
        self.simulate_human_delay(3, 4)
        if quick:
            min_delay = 0.5
            max_delay = 1.5
        else:
            min_delay = 2
            max_delay = 4
        while True:
            try:
                self.swipe_down_quickly()
                self.simulate_human_delay(min_delay, max_delay)
                if random.random() > 0.6:
                    self.swipe_up()
                else:
                    self.swipe_down_slowly()
                self.simulate_human_delay()
            except Exception as e:
                logger.error("Error occurred while handling product detail: {}".format(str(e)))
                self.screenshot('handle_product_detail')  # 截图并保存

    def handle_popups_and_navigate(self):
        """处理弹窗并导航到首页"""
        logger.debug("Handling popups and navigating to home.")
        # 1. 扫描当前页面是否有弹窗
        # try:
        #     popup_close_button = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"popup_close_button_id")]')  # 替换为实际的关闭按钮资源ID
        #     if popup_close_button.is_displayed():
        #         popup_close_button.click()  # 点击关闭弹窗
        #         self.simulate_human_delay()
        # except Exception as e:
        #     print("没有找到弹窗或关闭按钮:", str(e))

        # 2. 判断首页图标是否为选中状态
        try:
            home = self.driver.find_element(By.XPATH, "//android.widget.RelativeLayout[@content-desc=\"首页\"]")
            home.click()  # 点击首页图标
            logger.debug("Navigated to home successfully.")
            self.simulate_human_delay(3, 4)
        except Exception as e:
            logger.error("Failed to find home icon: {}".format(str(e)))
            self.screenshot('handle_popups_and_navigate')

        try:
            # 3. 上下滑动页面
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-20, 20)
            actions.w3c_actions.pointer_action.move_to_location(500 + offset_x, 1690 + offset_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(500 + offset_x, 829 + offset_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-20, 20)
            actions.w3c_actions.pointer_action.move_to_location(594 + offset_x, 695 + offset_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(482 + offset_x, 1446 + offset_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-20, 20)
            actions.w3c_actions.pointer_action.move_to_location(609 + offset_x, 975 + offset_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(485 + offset_x, 1822 + offset_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            self.simulate_human_delay(5, 6)
        except Exception as e:
            logger.error("Error occurred while handling popups and navigate: {}".format(str(e)))
            self.screenshot('handle_popups_and_navigate')

    def search_keyword(self, keyword):
        try:
            logger.debug("Searching for keyword: {}".format(keyword))
            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(508, 150)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            self.simulate_human_delay(4, 5)

            el1 = self.driver.find_element(by=AppiumBy.XPATH, value="//android.widget.EditText[@content-desc=\"搜索\"]")
            el1.send_keys(keyword)
            self.simulate_human_delay()

            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1003, 156)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            self.simulate_human_delay()
        except Exception as e:
            logger.error("Error occurred while searching keyword: {}".format(str(e)))
            self.screenshot('search_keyword')

    def handle_popups_and_captcha(self):
        """处理弹窗和滑动验证码"""
        # try:
        #     # 检测并关闭弹窗
        #     try:
        #         popup_close_button = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"popup_close_button_id")]')  # 替换为实际的关闭按钮资源ID
        #         if popup_close_button.is_displayed():
        #             popup_close_button.click()  # 点击关闭弹窗
        #             self.simulate_human_delay()
        #     except Exception as e:
        #         print("没有找到弹窗或关闭按钮:", str(e))
        #
        #     # 检测滑动验证码
        #     try:
        #         captcha_slider = self.driver.find_element(By.XPATH, '//*[contains(@resource-id,"captcha_slider_id")]')  # 替换为实际的滑动验证码资源ID
        #         if captcha_slider.is_displayed():
        #             # 执行滑动操作
        #             self.solve_captcha(captcha_slider)
        #     except Exception as e:
        #         print("没有找到滑动验证码:", str(e))
        #
        # except Exception as e:
        #     print(f"处理弹窗或验证码时发生错误: {str(e)}")  # 可以替换为国际化的错误信息

    def solve_captcha(self, slider):
        """解决滑动验证码"""
        pass

    def close(self):
        """关闭驱动"""
        logger.debug("Closing the WebDriver.")
        self.driver.quit()


def process_device(device_config):
    """处理单个设备的自动化流程"""
    automator = Automator(device_config)
    
    try:
        automator.handle_popups_and_navigate()
        automator.search_keyword("hello")
        automator.handle_product_detail(True)
    finally:
        automator.close()

if __name__ == "__main__":
    # 设备配置示例
    devices_config = [
        {
            "device_name": "device1",
            "udid": "ABCD1234"
        },
        {
            "device_name": "device2",
            "udid": "EFGH5678"
        }
    ]
    
    process_device(devices_config[0])
    # 使用线程池并行执行
    # with ThreadPoolExecutor(max_workers=len(devices_config)) as executor:
    #     executor.map(process_device, devices_config)