from controller.unit import PDF_template, PDF_unit_check
from app import SH_NAME, TASK_NAME, CLASS_NAME, GROUP1, GROUP2

_global_group = [GROUP1, GROUP2]
CHECK_KEY = '건강'

class Unit_Manage:
    KEYS = [0, 1]
    result = {}

    def __init__(self):
        self._register_units()
    
    def init(self):
        self.result={}
        PDF_template.initialize()

    def update_result(self):
        t_id = self.type
        
        if t_id in self.result:
            for key in self.result[t_id].keys():
                _acc = self.result[t_id][key]
                _add = PDF_template.result[key]
                for k in _acc.keys():
                    #배열간 병합
                    _acc[k] += _add[k]
        else:
            self.result[t_id] = PDF_template.result
        
    def file(self, filepath):
        PDF_template.to_html(filepath)
        
    def addfilename(self):
        self.create_unit('FILE').execute()

    def model(self, model):
        PDF_template.model(model)
    
    def html(self):
        return PDF_template.html

    def check_type(self, filter=None):
        task_name = "CHECK"
        # type값을 축출해옴.
        self.create_unit(task_name).execute()
        
        if CHECK_KEY in PDF_template.result[task_name]['type'][0]:
            self.type = self.KEYS[0]
        else:
            self.type = self.KEYS[1]

        del (PDF_template.result[task_name])

        if not (filter is None): return filter == int(self.type)
        
        return True
    
    def set_unit_list(self, ul=None):
        self._unit_list = ul

    def unit_list(self):
        if hasattr(self, '_unit_list') and getattr(self, '_unit_list') is not None:
            return self._unit_list
        else:
            return _global_group[self.type]

    def create_unit(self, unit_name):
        module = __import__('controller.unit')

        _class_name = self._get_class_name(unit_name)
        __class = getattr(module, _class_name)
        
        return __class()
    
    def clear(self):
        PDF_template.clear()

    def _register_units(self):
        # map {unit_name: class_name}
        _zip = zip(TASK_NAME, CLASS_NAME)
        self.class_map = {_task_name:_class_name for _task_name, _class_name in _zip}

        # for id in self.KEYS:
        #     _zip = zip(_global_group[id], _global_class[id])
        #     self.class_map.update({_unit_name:_class_name for _unit_name, _class_name in _zip})

    # 유닛의 인덱스에 대응되는 클래스명을 가져옴
    def _get_class_name(self, name):
        return self.class_map[name]