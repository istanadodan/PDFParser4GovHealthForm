from service.unit import PDF_template
from app import TASK_NAME, CLASS_NAME

class Unit_Manage:
    def __init__(self):
        self._register_units()
    
    def initialize(self):
        self.result={}
        PDF_template.initialize()

    def update_result(self):
        #'0'건강, '1'연금
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
    
    def html(self):
        return PDF_template.html

    def doc_type(self, type):
        self.type= type
        
    # 보고서종류 확인 키워드 축출
    def get_check_keyword(self):
        _TASK_UNIT = "CHECK"
        self.create_unit(_TASK_UNIT).execute()
        return PDF_template.result[_TASK_UNIT]['type'][0]
        
    # 유닛의 인덱스에 대응되는 클래스명을 가져옴        
    def create_unit(self, unit_name):
        if not self.class_map: return

        module = __import__('service.unit')        
        _class_name = self.class_map[unit_name]
        __class = getattr(module, _class_name)        
        return __class()
    
    def clear(self):
        PDF_template.clear()

    # 항목취득객체(유닛) 목록작성
    def _register_units(self):
        # map {unit_name: class_name}
        _zip = zip(TASK_NAME, CLASS_NAME)
        self.class_map = {_task_name:_class_name for _task_name, _class_name in _zip}