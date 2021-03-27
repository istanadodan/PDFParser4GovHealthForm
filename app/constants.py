from configparser import ConfigParser
import os

config = ConfigParser()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir,'config.ini')

config.read(file_path,encoding='utf-8')

def get_config(path):
    section, item = path.split('/')
    data = config[section][item]
    return [v.strip() for v in data.split(',') if v]

if __name__=='__main__':
    rst = get_config('LISTBOX/group1')
    for r in rst:
        print(r)