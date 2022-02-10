from .appcontext import Appcontext
appcontext = Appcontext()

def get_config(name):
    _config = appcontext.get('config')
    if not _config:
        return None
    return _config.get(name, None)

def load_setting():
    with open('app/setting.json','r',encoding='utf-8') as f:
        import json
        appcontext.put(config=json.load(f))
        