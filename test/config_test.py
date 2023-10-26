import sys
sys.path.append('.')

from utils.config import Config

if __name__ == '__main__':
    print(Config.openai_key)
