#coding: utf-8

#author:yanbin_team
#date:2020-6-23
#此代码基于《普通话教材》将其数据化,实现了从书本到sqlite数据库的转化，主要实现了给汉字注音，然后入库便于用户查询相关字词及其拼音

#在运行此代码之前必须要在D盘创建code2020文件夹
#将您所要注音的csv文件放在code2020文件夹下即可
#运行完成之后，您可以在您的D盘code2020文件夹下找到word.sqlite的数据库，此数据库就是文字注音后的文件
##（注：csv文件的编码格式必须是UTF-8，ANSI的编码格式不可用）

import os,codecs,requests,re
from pony.orm import * 
dbpath = r"D:/code2020/word.sqlite"
csv_path = "D:/code2020/总词汇.csv"#地址可以替换成您要汉字注音的csv文件

db = Database()
class Word(db.Entity):
    id = PrimaryKey(int, auto=True)
    page = Optional(str, column='page')
    word_1 = Optional(str, column='word_1')
    pinyin_1 = Optional(str, column='pinyin_1')
    word_2 = Optional(str, column='word_2')
    pinyin_2 = Optional(str, column='pinyin_2')
    word_3 = Optional(str, column='word_3')
    pinyin_3 = Optional(str, column='pinyin_3')
    word_4 = Optional(str, column='word_4')
    pinyin_4 = Optional(str, column='pinyin_4')
    word_5 = Optional(str, column='word_5')
    pinyin_5 = Optional(str, column='pinyin_5')
    word_6 = Optional(str, column='word_6')
    pinyin_6 = Optional(str, column='pinyin_6')
    word_7 = Optional(str, column='word_7')
    pinyin_7 = Optional(str, column='pinyin_7')
    word_8 = Optional(str, column='word_8')
    pinyin_8 = Optional(str, column='pinyin_8')

def create_db():
	
	if os.path.exists(dbpath):
		os.remove(dbpath)
	f = open(dbpath,"w")
	f.close()
	db.bind(provider='sqlite', filename=dbpath)
	db.generate_mapping(create_tables=True)
	set_sql_debug(True)

# def _get_pinyin(word):
	"""
	拼音查询代码
	"""
def getpy(wd):
	"""获取汉字的拼音"""
	head={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
		'Cookie': 'BIDUPSID=4A4D0A44BEF185AD83D64CC2F573329D; PSTM=1588927792; BAIDUID=4A4D0A44BEF185AD6CFA3FFB933393D3:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=b6dbf84c7137aa4d916842a7fbaef4f85dfd00e1_1592291831_js; H_PS_PSSID=1447_31670_21083_31069_32045_30823_26350; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=3; H_PS_645EC=ea9eb5qDtAyHNnR4Hn8cXw%2FOrurPMlY3dBouixR08GGbIdC6iMpAzR2BDFg'}
		
	url='http://www.baidu.com/s?wd='  # 找到百度查找的规则，等号后面的即是查询的内容
	r=requests.get(url+wd+'拼音',headers=head)  # 构建百度查找拼音的链接
	r.encoding='utf-8'
	html=r.text
	py=re.findall(r'<span class="op_exactqa_detail_word_pronounce">\[([\d\D]*?)\]<',html)  #找到拼音
		
	#     data.append([(wd,),(','.join(py),)])
	#     data.append([(wd),(','.join(py))])
	return ','.join(py)
    

def insert2db():
	"""
	数据入库
	csv格式
	"""
	f = codecs.open(csv_path,"r","utf-8-sig")
	for line in f.readlines():
		li = line.strip().split(",")#一列的读取数据
	#     print(li)#一行中文列表
		pinyin=[]#一行拼音列表    
		for elem in li:#遍历每一个词，获取拼音
			p = getpy(elem) 
			pin=(''.join(p))#每一个词语的拼音
			pinyin.append(pin[0:20])
			print(pin)
	#     print(pinyin)
		if len(li)==6:
			w= Word(page=li[0],word_1=li[1],pinyin_1=pinyin[1],word_2=li[2],pinyin_2=pinyin[2],word_3=li[3],pinyin_3=pinyin[3],word_4=li[4],pinyin_4=pinyin[4],word_5=li[5],pinyin_5=pinyin[5],word_6=li[6],pinyin_6=pinyin[6])
		else:
			w= Word(page=li[0],word_1=li[1],pinyin_1=pinyin[1],word_2=li[2],pinyin_2=pinyin[2],word_3=li[3],pinyin_3=pinyin[3],word_4=li[4],pinyin_4=pinyin[4],word_5=li[5],pinyin_5=pinyin[5],word_6=li[6],pinyin_6=pinyin[6],word_7=li[7],pinyin_7=pinyin[7],word_8=li[8],pinyin_8=pinyin[8])

		db.commit()
	f.close()



if __name__ == "__main__":
	create_db()
	insert2db()