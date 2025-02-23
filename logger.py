import logging
import sys
from datetime import datetime

class Logger:
    def __init__(self, filename=None):
        # 默认以年月日的形式创建文件名
        if filename is None:
            filename = datetime.now().strftime('%Y-%m-%d') + '.log'
        
        # 设置日志格式
        self.logger = logging.getLogger('MyLogger')
        self.logger.setLevel(logging.DEBUG)

        # 创建控制台处理器
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        # 创建文件处理器
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)

        # 创建格式器并将其添加到处理器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 将处理器添加到日志器
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)
