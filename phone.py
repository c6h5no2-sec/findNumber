from contextlib import nullcontext
from tkinter.messagebox import askretrycancel
import requests
import re
import time

def phoneNum(i):
    time.sleep(1)
    url = 'http://www.1234i.com/p.php'    
    data = {
        "ok3" : "20220810-09..48.31-194.233.64.10",
        "haomas" : i
        }

    proxy = {
        "http" : "127.0.0.1:8080",
        "https" : "127.0.0.1:8080"
    }    
    #print(i)

    try:
        content = requests.post(url,data,timeout = 10).content.decode('gb2312')

    except requests.exceptions.RequestException as e:
        tryTime = 3
        timeNum = 1
        while timeNum < tryTime :
            #print(timeNum)
            try:
                content = requests.post(url,data,timeout = 10).content.decode('gb2312')
                time.sleep(1)
                break
            except requests.exceptions.RequestException as e:
                if timeNum == 3:
                    print("超时")
                    file = open ('overtime.txt','a+')
                    file.write ( i + '\r\n')
                    file.close ()
                timeNum += 1

                continue
    
    return content
def reg(content,i):
        area = re.findall(r"<font color=blue>(.*?)</font>",content)
        area = ''.join(area)
        print(area + i)
        return area

def main():
    phone = ['123123','123123']
    for i in phone:
        content = phoneNum(i)
        #print(content)
        area = reg (content,i)

    
        if ',' not in area:
            content = phoneNum(i)
            area = reg (content,i)
            if ',' not in area: 
                print(i + "返回空")
                file = open('NULLuser.txt','a+')
                file.write( i + "\r\n")
                file.close()
            continue

        if "云南昆明" in area:
            print("***昆明用户：" + i + "***")
            file = open('KMuser.txt','a+')
            file.write( i + "\r\n")
            file.close()
            continue

        if "请不要反复刷新" in area:
            exit("请求过多，请稍后重试")

'''
设置超时后重新访问3次，如果仍然失败，则写入日志
返回空的用户建议手动访问，写入txt中
将昆明用户存入txt，在统计一下云南的用户

如有余力建议干一个统计
'''

if __name__ == "__main__":
    main()
    print('查询完毕')
