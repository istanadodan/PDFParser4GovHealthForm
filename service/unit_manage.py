import importlib
from service.unit import PDF_template
from app import get_config

CLASS_MAP = get_config('class_map')

# # module = __import__('service.unit') 와 동일.
# 'unit'를 뺼 경우, service.__init__에 from .unit import * 추가가 필요.        
module = importlib.import_module('service.unit', 'unit')

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
        check_unit_name = "CHECK"
        check_keyword = 'type'
        unit_obj = self.create_unit(check_unit_name)
        if not unit_obj: return None
        unit_obj.execute()
        return unit_obj.result[check_unit_name][check_keyword][0]
        
    # 유닛의 인덱스에 대응되는 클래스명을 가져옴        
    def create_unit(self, unit_name):
        if not self.class_map or not unit_name in self.class_map:
            return None
        class_name = self.class_map[unit_name]        
        _class = getattr(module, class_name) 
        return _class()
    
    def clear(self):
        PDF_template.clear()

    # 항목취득객체(유닛) 목록작성
    def _register_units(self):
        self.class_map = CLASS_MAP; 