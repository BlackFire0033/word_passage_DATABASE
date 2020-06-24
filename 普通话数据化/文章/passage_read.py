# coding: utf-8

##在运行此代码前，您需要在您的D盘创建code2020文件夹
#此代码基于《普通话教材》将其数据化,实现了从书本到sqlite数据库的转化，主要实现了给文章每一个字注音，SQL入库便于用户查询相关字词及其拼音
#将您所要注音的txt文件路径填入fetch后即可
#运行完成之后，您可以在您的D盘code2020文件夹下找到passage.sqlite的数据库，此数据库就是文字注音后的文件
#（注：txt文件的编码格式必须是UTF-8，ANSI的编码格式不可用）

import os,requests,re
from pony.orm import *
chuang_jian = r"D:/code2020/passage.sqlite"
fetch = r"D:\code2020\001"#可以替换您需要读取注音的文章，文件为UTF-8的TXT文件

db = Database()
class Passage(db.Entity):
	id = PrimaryKey(int, auto=True)
	tittle = Optional(str, column='tittle')
	zhengwen = Optional(str, column='zhengwen')
	pinyin = Optional(str, column='pinyin')

def chuangjian():
    dbpath = chuang_jian
    if os.path.exists(dbpath):
        os.remove(dbpath)
    f = open(dbpath,"w")
    f.close()
    db.bind(provider='sqlite', filename=dbpath)
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)

def _getpy(wd):
    """获取汉字的拼音"""
    head={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
         'Cookie': 'BIDUPSID=4A4D0A44BEF185AD83D64CC2F573329D; PSTM=1588927792; BAIDUID=4A4D0A44BEF185AD6CFA3FFB933393D3:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=b6dbf84c7137aa4d916842a7fbaef4f85dfd00e1_1592291831_js; H_PS_PSSID=1447_31670_21083_31069_32045_30823_26350; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=ea9eb5qDtAyHNnR4Hn8cXw%2FOrurPMlY3dBouixR08GGbIdC6iMpAzR2BDFg'}    
    url='http://www.baidu.com/s?wd='  # 找到百度查找的规则，等号后面的即是查询的内容
    r=requests.get(url+wd+'拼音',headers=head)  # 构建百度查找拼音的链接
    r.encoding='utf-8'
    html=r.text
    py=re.findall(r'<span class="op_exactqa_detail_word_pronounce">\[([\d\D]*?)\]<',html)  #找到拼音
    return ','.join(py)
    
def wenzhang():
    filePath = fetch
    fileList = os.listdir(filePath)
    for file in fileList:
        f = open(os.path.join(filePath,file),'r',encoding= 'ANSI')
        F=str(file)
        filename=F.replace(".txt"," ")
        print(filename) # 文件名
        for i in f.readlines():
    #         print(i)
            for zi in i:
                print(zi)
                pinyin=[]
                p=_getpy(zi)
                pin=(''.join(p))#每一个词语的拼音
                a=pin[0:10]
   #             print(a)
                p=Passage(tittle=filename,zhengwen=zi,pinyin=a)
                db.commit()
            
if __name__ == '__main__':
    chuangjian()
    wengzhang()
