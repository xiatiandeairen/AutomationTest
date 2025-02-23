import json
import os

class Config:
    def __init__(self, file_path='config.json'):
        self.file_path = file_path
        self.config_data = self.load_config()

    def load_config(self):
        """从指定的 JSON 文件加载配置"""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Configuration file not found: {self.file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def get(self, key, default=None):
        """获取配置项的值，如果不存在则返回默认值"""
        return self.config_data.get(key, default)


if __name__ == "__main__":  
    config = Config()
    print(config.get("platformName"))

