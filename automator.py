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
from config import Config
from datetime import datetime  # 确保正确导入
from concurrent.futures import ThreadPoolExecutor  # 导入 ThreadPoolExecutor
import signal
import sys
import subprocess

logger = Logger("Automator")

def signal_handler(sig, frame):
    """处理信号，确保日志写入磁盘"""
    logger.error("signal_handler execute")
    logger.stop()  # 停止日志记录
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)  # 捕获 Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # 捕获终止信号

class Automator:
    def __init__(self, config, device_config=None):
        self.config = config
        self.device_config = device_config
        server = self.config.get("server", "localhost")  # 默认服务器地址
        port = self.config.get("port", 4723)  # 默认端口

        logger.debug("Initializing Automator with config: {}".format(self.config.config_data))
        logger.debug("Initializing Automator with device config: {}".format(self.device_config))
        
        desired_capabilities = {
            "platformName": self.config.get("platformName", "Android"),  # 默认平台名称
            "appium:automationName": self.config.get("appium:automationName", "UiAutomator2"),  # 默认自动化名称
            "appium:appPackage": self.config.get("appium:appPackage", "com.xunmeng.pinduoduo"),  # 默认应用包名
            "appium:appActivity": self.config.get("appium:appActivity", ".ui.activity.MainFrameActivity"),  # 默认应用活动
            "appium:forceAppLaunch": self.config.get("appium:forceAppLaunch", True),  # 默认强制启动应用
            "appium:noReset": self.config.get("appium:noReset", True),  # 默认不重置应用
            "appium:printPageSourceOnFindFailure": self.config.get("appium:printPageSourceOnFindFailure", True),  # 默认打印页面源代码
            "appium:skipDeviceInitialization": self.config.get("appium:skipDeviceInitialization", True),  # 默认跳过设备初始化
            "appium:unicodeKeyBoard": self.config.get("appium:unicodeKeyBoard", True),  # 默认使用 Unicode 键盘
        }

        if device_config:
            desired_capabilities["appium:deviceName"] = device_config.get("device_name")
            desired_capabilities["appium:udid"] = device_config.get("udid")

        self.driver = webdriver.Remote(
            command_executor=f'http://{server}:{port}',
            desired_capabilities=desired_capabilities
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
        logger.stop()
        self.driver.quit()


    def process_whole_flow(self):
        """处理全流程的自动化流程"""        
        try:
            self.handle_popups_and_navigate() 
            keyword = self.device_config.get("keyword")
            if keyword is None:
                raise ValueError("Keyword is required but not provided in device_config.")
            self.search_keyword(keyword)
            self.handle_product_detail(True)
        except Exception as e:
            logger.error("Error occurred while process_whole_flow: {}".format(str(e)))
            self.screenshot('process_whole_flow')
        finally:
            self.close()

    def process_swip_flow(self):
        """处理单流程的自动化流程"""        
        try:
            self.handle_product_detail(True)
        except Exception as e:
            logger.error("Error occurred while process_whole_flow: {}".format(str(e)))
            self.screenshot('process_whole_flow')
        finally:
            self.close()


def process_whole_flow(device_config):
    """处理单个设备的自动化流程"""
    logger.debug("execute beigin")
    config = Config("config.json")  # 创建 Config 对象
    automator = Automator(config, device_config)  # 将 Config 对象传入 Automator
    
    try:
        automator.process_whole_flow()
    except Exception as e:
        logger.error("Error occurred while processing device {}: {}".format(device_config.get("device_name"), str(e)))
    finally:
        logger.debug("execute over")

def process_swip_flow(device_config):
    """处理单个设备的自动化流程"""
    logger.debug("execute beigin")
    config = Config("simple_config.json")  # 创建 Config 对象
    automator = Automator(config, device_config)  # 将 Config 对象传入 Automator

    try:
        automator.process_swip_flow()
    except Exception as e:
        logger.error("Error occurred while processing device {}: {}".format(device_config.get("device_name"), str(e)))
    finally:
        logger.debug("execute over")

def get_connected_devices():
    """通过 adb 获取所有连接的设备 ID"""
    try:
        # 执行 adb devices 命令
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip().split('\n')[1:]  # 跳过第一行
        devices = []
        for line in output:
            if line.strip():  # 确保行不为空
                device_id = line.split()[0]  # 获取设备 ID
                devices.append(device_id)
        return devices
    except Exception as e:
        logger.error(f"Failed to get connected devices: {str(e)}")
        return []

if __name__ == "__main__":
    # 获取所有连接的设备 ID
    connected_devices = get_connected_devices()

    # 生成设备配置示例
    device_configs = []
    for i, udid in enumerate(connected_devices):
        device_configs.append({
            "device_name": f"device{i + 1}",  # 设备名称为 device1, device2, ...
            "udid": udid
        })

    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=len(device_configs)) as executor:
        executor.map(process_swip_flow, device_configs)