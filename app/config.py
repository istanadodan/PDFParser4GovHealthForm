import os
import json
from configparser import ConfigParser

config = ConfigParser()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir,'config.ini')
properties = ''

config.read(file_path,encoding='utf-8')

with open('app/healthPensionConfig.json','r',encoding='utf-8') as f:    
    properties = json.load(f)    

def get_config2(name):    
    if name not in properties:
        return None
    return properties[name]
    
def get_config(path):
    section, item = path.split('/')
    data = config[section][item]
    return [v.strip() for v in data.split(',') if v]

if __name__=='__main__':
    rst = get_config('LISTBOX/group1')
    for r in rst:
        print(r)
        
    print(get_config2('group'))
    print(get_config2('class_map'))