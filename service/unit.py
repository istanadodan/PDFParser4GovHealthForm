import os
from abc import ABCMeta, abstractmethod
from model import PDFModel

model=PDFModel()

class PDF_template(metaclass=ABCMeta):
    result={}
    basket=[]
    body=''
    html=''    
    filepath=''
    id=''

    def __init__(self, title=None):
        if title not in self.result:
            self.result[title] = dict()
        self.id = title

    @abstractmethod
    def execute(self):
        pass

    def add_result(self, account):
        field = self.result[self.id]
        if account not in field:
            field[account] = []
        
        field[account] += [self.basket[0]]
        self.result[self.id] = field

    def find_all(self, tag='div', text=False, recursive=True):
        self.tags = model.find_all(tag,text=text,recursive=recursive)

    def extract(self, keyword, nth=0):        
        self.basket = model.extract(self.tags, keyword, nth)
  
    @classmethod
    def clear(cls):
        cls.result = {k:{} for k in cls.result.keys()}
        cls.basket = []

    @classmethod
    def to_html(cls, filepath):
        cls.filepath = filepath
        model.to_html(filepath)
        cls.body = model.body
        cls.html = model.html

    @classmethod
    def get_result(cls):
        return cls.result
    
    @classmethod
    def initialize(cls):
        # #unit을 미리 만들어 놓는 것으로 변경하면서, 객체생성 시에 등록한 키값을 보존해야함.
        # if not cls.result:
        #     cls.result = OrderedDict()
        # else:
        #     for k in cls.result.keys():
        #         cls.result[k] = OrderedDict()

        # cls.result = {k:{} for k in cls.result.keys()}
        cls.result = {}
        cls.basket = []
        cls.body=''
        model.initialize()

    def addfilename(self):
        # if 'FILE' not in cls.result:
        #     cls.result['FILE'] = dict()
        #     cls.result['FILE']['FILENAME'] = list()
        # # 클래스초기화에서 키를 남겨두면서 하위키에 대해도 확인
        # elif 'FILENAME' not in cls.result['FILE']:
        #     cls.result['FILE']['FILENAME'] = list()
        _result = self.result[self.id]
        if 'FILENAME' not in _result:
            _result['FILENAME'] = list()

        _result['FILENAME'] += [os.path.basename(self.filepath)]
        self.result[self.id] = _result

class PDF_unit_check(PDF_template):

    def __init__(self):
        super().__init__('CHECK')

    def execute(self):
        self.find_all('div')

        self.extract('사업장 고지내역서',0)
        self.add_result('type')

class PDF_unit_file(PDF_template):

    def __init__(self):
        super().__init__('FILE')

    def execute(self):

        self.addfilename()

# 건강보험용
class PDF_unit1(PDF_template):

    def __init__(self):
        super().__init__('사업장(건강)')

    def execute(self):

        self.find_all('div')

        self.extract('사업장관리번호',0)
        self._amend("사업장관리번호")
        self.add_result('사업장관리번호')

        self.extract('고지년월 차수',0)
        self._amend("고지년월 차수")
        self.add_result('고지년월 차수')

    def _amend(self, rpl):
        self.basket[0] = self.basket[0].replace(rpl,'')


class PDF_unit2(PDF_template):

    def __init__(self):
        super().__init__('건강보험료')

    def execute(self):

        self.find_all('div')

        self.extract('장기요양보험료',1)
        self.add_result('산출보험료')

        self.extract('장기요양보험료',2)
        self.add_result("정산보험료")

        self.extract('장기요양보험료',3)
        self.add_result("가입자보험료")

        self.extract('장기요양보험료',8)
        self.add_result("고지보험료")

        self.extract('장기요양보험료',9)
        self.add_result("연체금")

class PDF_unit3(PDF_template):

    def __init__(self):
        super().__init__('장기요양보험료')

    def execute(self):

        self.find_all('div')

        self.extract('장기요양보험료',12)
        self.add_result('산출보험료')

        self.extract('장기요양보험료',13)
        self.add_result('정산보험료')

        self.extract('장기요양보험료',15)
        self.add_result('가입자보험료')

        self.extract('납 부 금 액',2)
        self.add_result('고지보험료')

        self.extract('장기요양보험료',23)
        self.add_result('연체금')

class PDF_unit4(PDF_template):

    def __init__(self):
        super().__init__('납부할보험료')

    def execute(self):

        self.find_all('div')

        self.extract('납부할보험료',1)
        self.add_result('납부할보험료')

# 연금용
class PDF_unit5(PDF_template):

    def __init__(self):
        super().__init__('사업장(연금)')

    def execute(self):

        self.find_all('div')
 
        self.extract('사업장관리번호',0)
        self._amend("사업장관리번호")
        self.add_result('사업장관리번호')

        self.extract('고지년월',1)
        self.add_result('고지년월')

    def _amend(self, rpl):
        self.basket[0] = self.basket[0].replace(rpl,'')

class PDF_unit6(PDF_template):

    def __init__(self):
        super().__init__('연금보험료')

    def execute(self):

        self.find_all('div')

        self.extract('⊙ 고지내역 ○ 자동이체',1)
        self.add_result('고 지 인 원')

        self.extract('납부 할 금액',1)
        self.add_result('당월분보험료')

        self.extract('납부 할 금액',2)
        self.add_result('소급분보험료')

        self.extract('체납기간(개월)',1)
        self.add_result('연체금')
