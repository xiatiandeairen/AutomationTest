import logging
import logging.handlers
import sys
from datetime import datetime
from queue import Queue
import threading
import time

class Logger:
    def __init__(self, name, filename=None):
        self.log_queue = Queue()
        self.queue_handler = logging.handlers.QueueHandler(self.log_queue)
        
        # 默认以年月日的形式创建文件名
        if filename is None:
            filename = datetime.now().strftime('%Y-%m-%d') + '.log'
        
        # 设置日志格式，包含线程名
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.queue_handler)

        # 创建控制台处理器
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)

        # 创建文件处理器
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)

        # 创建格式器并将其添加到处理器
        formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 创建监听器
        self.listener = logging.handlers.QueueListener(self.log_queue, ch, fh)
        self.listener.start()

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def stop(self):
        """停止日志监听器"""
        self.listener.stop()  # 停止监听器
        self.logger.handlers[0].flush()
        self.logger.handlers[0].close()

# 创建 Logger 实例
# logger = Logger()
#
# def log_messages(thread_name):
#     """线程函数，用于记录日志信息"""
#     for i in range(5):
#         logger.debug(f"{thread_name} - Debug message {i}")
#         logger.error(f"{thread_name} - Error message {i}")
#         logger.warning(f"{thread_name} - Warning message {i}")
#         time.sleep(0.1)  # 模拟一些工作

# if __name__ == "__main__":
#     threads = []
#     num_threads = 5  # 创建5个线程
#
#     # 启动多个线程
#     for i in range(num_threads):
#         thread_name = f"Thread-{i+1}"
#         thread = threading.Thread(target=log_messages, args=(thread_name,), name=thread_name)
#         threads.append(thread)
#         thread.start()
#
#     # 等待所有线程完成
#     for thread in threads:
#         thread.join()
#
#     # 停止日志监听器
#     logger.stop()
