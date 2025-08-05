
#coding=utf-8

from dataclasses import replace
import re


with open(r'output.txt','a',encoding='utf-8') as file:
    file.write("PSEUDOPILOT:ALL\n")
    file.write("\n")
    
    
    
RWNU=int(input("请输入跑道条数："))
for i in range(1,RWNU+1):
    NUM=input("请输入跑道{}编号:".format(i))
    NUM1=NUM
    if "L" in NUM:
        NU1=re.findall(r"\d+",NUM)
        NU2=int(",".join(NU1))+18
        if NU2>36:
            NU2=NU2-36
        if int(",".join(re.findall(r"\d+",NUM1)))<10:
            NUM1="0"+NUM1
        if NU2<10:
            NUM2="0"+str(NU2)+"R"
        else:
            NUM2=N2 
            
    elif "R" in NUM:
        NU1=re.findall(r"\d+",NUM)
        NU2=int(",".join(NU1))+18
        if NU2>36:
            NU2=NU2-36
        if int(",".join(re.findall(r"\d+",NUM1)))<10:
            NUM1="0"+NUM1
        if NU2<10:
            NUM2="0"+str(NU2)+"L" 
        else:
            NUM2=N2         
    elif "C" in NUM:
        NUM1=NUM
        NU1=re.findall(r"\d+",NUM)
        NU2=int(",".join(NU1))+18
        if NU2>36:
            NU2=NU2-36
        if int(",".join(re.findall(r"\d+",NUM1)))<10:
            NUM1="0"+NUM1
        if NU2<10:
            NUM2="0"+str(NU2)+"C"
        else:
            NUM2=N2 
    else:   
        NUM1=NUM
        NU1=re.findall(r"\d+",NUM)
        NU2=int(",".join(NU1))+18
        if NU2>36:
            N2=NU2-36
        else:
            N2=NU2  
        if int(",".join(re.findall(r"\d+",NUM1)))<10:
            NUM1="0"+NUM1
        if N2<10:
            NUM2="0"+str(N2) 
        else:
            NUM2=N2          
    RWY1=input("请输入{}号跑道头经纬度:".format(i))
    RWY2=input("请输入{}号跑道尾经纬度:".format(i))
    RW1=RWY1.replace(",",":")
    RW2=RWY2.replace(",",":")
    with open(r'output.txt','a',encoding='utf-8') as file:
        file.write("ILS{}:{}:{}\n".format(NUM1,RW1,RW2))
        file.write("ILS{}:{}:{}\n".format(NUM2,RW2,RW1))
        file.write("\n")
        
        
        
        
DEP=input("请输入起飞机场：")
ALT=input("请输入机场标高：")
INI=input("请输入控制权所有席位：")
while True:
    CALLSIGN=input("请输入呼号：")
    ARR=input("请输入落地机场：")
    TYP=input("请输入机型：")
    RFL=input("请输入巡航高度：")
    PPOS=input("请输入经纬度：")
    HEAD=int(input("请输入头朝向："))
    ROUTE1=input("请输入实际航路：")
    ROUTE2=input("请输入计划航路：")
    REM=input("请输入备注信息：")
    HDG=HEAD*2.88*4+2
    POS=PPOS.replace(",",":")
    with open(r'output.txt','a',encoding='utf-8') as file:
        file.write('PSEUDOPILOT:ALL\n')
        file.write("@N:{}:2000:1:{}:{}:0:{}:0\n".format(CALLSIGN,POS,ALT,HDG))
        file.write("$FP{}:*A:I:{}:420:{}:0000:0000:{}:{}:00:00:0:0::/v/{}:{}\n".format(CALLSIGN,TYP,DEP,RFL,ARR,REM,ROUTE1))
        file.write("$ROUTE:{}\n".format(ROUTE2))
        file.write("DELAY:1:8\n")
        file.write("REQALT::{}\n".format(ALT))
        file.write("INITIALPSEUDOPILOT:{}\n".format(INI))
        file.write("\n")
    YN=input(r"是否退出(Y:1/N:2):")
    if YN=="1":
        break
    elif YN=="2":
        continue
print("模拟机文本已生成至output.txt")






