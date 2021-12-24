from app import writelog

class _VO:
    stx =0
    len =0
    val =''
    def __init__(self, stx, len):
        self.stx = stx
        self.len = len
        
    def getParam(self):
        return (self.stx, self.stx+self.len)
    
    def putValue(self, v):
        self.val = v
        
    def __str__(self) -> str:
        ret = 'stx:'+str(self.stx)+',len='+str(self.len)+",v="+str(self.val)        
        return str(self.val)
        
class Header:
    def __init__(self, header):
        self.doc = header
        self.등록번호 = _VO(9, 13)
        self.회사명 = _VO(134, 15)
        self.귀속연월 = _VO(31,6)
        self.지급연월 = _VO(37,6)
        self.제출연도 = _VO(43, 6)
    
        writelog('Header %s',self.doc, 'dev')
        self._extract()
        
    def _extract(self):
         lst = [_att for _att in self.__dict__ if isinstance(getattr(self, _att), _VO)]
         for _item in lst:
            __VO_obj = getattr(self, _item)
            s, e = __VO_obj.getParam()
            __VO_obj.putValue( self.doc[ s: e] )
            writelog(_item+':%s',__VO_obj, 'dev')
    
    def to_map(self):
         ret = {}
         try:
            lst = [{_att: [getattr(self, _att).val] for _att in self.__dict__ if isinstance(getattr(self, _att), _VO)}]         
            for el in lst:
                ret.update(el)
         except Exception as e:
            writelog('에러:%s',e, 'dev')
            pass
            
         return {'header': ret}
        
class Body:
    unit_list_map = dict()
    code_range = ['A01','A02','A03','A04','A05','A21','A22','A25','A40','A50','A60','A69','A70','A80','A90','A99']
    
    def __init__(self, file):
        for line in file.readlines():            
            u = _Unit(line)
            if u.getIncomeCode() in self.code_range:
                u.extract()
                self.unit_list_map.update({u.getIncomeCode(): u})
                writelog("Body :%s", line, 'dev')
                
        writelog("Body total map =%s",self.unit_list_map, 'dev')
    
    def to_map(self):        
        ret = {}
        for code, unit in self.unit_list_map.items():
            try:
                sub = {}        
                lst = [{_att: [getattr(unit, _att).val] for _att in unit.__dict__ if isinstance(getattr(unit, _att), _VO)}]         
                for el in lst:
                    del(el['원천징수소득코드'])
                    sub.update(el)
        
                ret.update({code:sub})
                        
            except Exception as e:
                writelog('에러:%s',e, 'dev')
                pass
        
        writelog("Body to map2 =%s", ret, 'dev')
                    
        return ret
                
class _Unit:    
    def __init__(self, text):
        self.doc = text
        self.원천징수소득코드 = _VO(9,3)
        self.인원 = _VO(12,15)
        self.총지급액 = _VO(27,15)
        self.징수세액_소득세등 = _VO(42,15)
        self.징수세액_농특세 = _VO(57,15)
        self.납부세액_소득세등 = _VO(102, 15)
    
    def getIncomeCode(self):
        s, e = self.원천징수소득코드.getParam()
        return self._convertInt(self.doc[ s: e])
            
    def extract(self):
         lst = [_att for _att in self.__dict__ if isinstance(getattr(self, _att), _VO)]
         for _item in lst:
            __VO_obj = getattr(self, _item)
            s, e = __VO_obj.getParam()
            __VO_obj.putValue( self._convertInt(self.doc[ s: e]) )
            writelog(_item+ ':%s', __VO_obj, 'dev')
    
    # 숫자이며 숫자로 변환해 반환    
    def _convertInt(self, t):        
        try:
            a = int(t)
            return a
        except Exception as e:
            return t     