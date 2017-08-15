#coding:utf-8
import codecs
import pymysql
import json
import sys
conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='66666666',db='traintrain',charset='utf8')
cur=conn.cursor()
cur.execute("select * from train")
lines2=cur.fetchall()
alltrainnum=[]
allstation=[]
for i in range(0,len(lines2)):
    list=[]
    list.append(lines2[i][0])
    x=str(lines2[i][1]).split(' ')
    for j in range(0,len(x)):
        list.append(x[j])
    alltrainnum.append(list)
for i in range(0,len(alltrainnum)):
    for j in range(1,len(alltrainnum[i])):
        if alltrainnum[i][j] not in allstation:
            allstation.append(alltrainnum[i][j])
cur.execute("select * from time")
lines1=cur.fetchall()
data={}
for i in range(0,len(lines1)):
    x=str(lines1[i][0]).replace("b'",'').replace("'",'').split(' ')
    alltime=[]
    for j in range(0,len(x),4):
        list1=[x[j],x[j+1]]
        list2=[x[j+2],x[j+3]]
        list=[list1,list2]
        alltime.append(list)
    data[alltrainnum[i][0]]=[alltrainnum[i],alltime]
cur.execute("select * from direc")
lines3=cur.fetchall()
direc={}
for t in range(0,len(lines3)):
    x=str(lines3[t]).replace("('",'').split('-')
    y=x[1].replace("',)",'').split(',')
    li=[]
    for i in range(0,len(y)):
        list=y[i].split(' ')
        li.append(list)
    direc[x[0]]=li
cur.execute("select * from same")
lines4=cur.fetchall()
same={}
for i in range(0,len(lines4)):
    list=str(lines4[i]).replace("('",'').replace("',)",'').replace("(",'').replace(',','').replace("\\r",'').replace(")",'').split(' ')
    for li in list:
        same[li]=list
for i in range(0,len(allstation)):
    try:
        same[allstation[i]]
    except:
        same[allstation[i]]=[allstation[i]]
start=sys.argv[1]
end=sys.argv[2]
interval1=int(sys.argv[3])
interval2=int(sys.argv[4])
ottran={}
cur.execute("select * from timedata")
lines=cur.fetchall()
n=allstation.index(start)
x=str(lines[n]).replace("('",'').replace("',)",'').split('-')
for i in range(0,len(x)-1):
    y=x[i].split(' ')
    ottran[y[0]]=y[1]
ottran1={}
cur.execute("select * from timedata1")
lines5=cur.fetchall()
n=allstation.index(end)
x=str(lines5[n]).replace("('",'').replace("',)",'').split('-')
for i in range(0,len(x)-1):
    y=x[i].split(' ')
    ottran1[y[0]]=y[1]
conn.close()
def twotime(x,y,z):         #两个站点之间某趟车次的时间
    in1=data[z][0].index(x)
    in2=data[z][0].index(y)
    t=int(data[z][1][in1-1][1][0])
    t1=int(data[z][1][in1-1][1][1])
    m=int(data[z][1][in2-1][0][0])
    m1=int(data[z][1][in2-1][0][1])
    thetime=(m-t)*60+m1-m1
    return thetime
def twostation(x,y,h,m,interval):  #the shortest time between two stations from a certain time
    jiao=[i for i in direc[x] if i in direc[y]]
    mmin=2880*4
    route=''
    for i in range(0,len(jiao)):
        if jiao[i].index(x)<jiao[i].index(y):
            s1=data[jiao[i][0]][0].index(x)-1
            s2=data[jiao[i][0]][0].index(y)-1
            time=(int(data[jiao[i][0]][1][s2][0][0])-int(data[jiao[i][0]][1][s1][1][0]))*60+int(data[jiao[i][0]][1][s2][0][1])-int(data[jiao[i][0]][1][s1][1][1])
            hour=int(data[jiao[i][0]][1][s1][1][0])
            miut=int(data[jiao[i][0]][1][s1][1][1])
            while hour>=24:
                hour-=24
            middle=hour*60+miut-(h*60+m+interval)
            if middle<0:
                middle+=24*60
            minn=middle+time+120
            if minn<mmin:
                mmin=minn
                route=jiao[i][0]
    return str(mmin),route
def straight(x,y):
    jiao=[i for i in direc[x] if i in direc[y]]
    result=[]
    if jiao!=[]:
        jiao1=[]
        for i in range(0,len(jiao)):
            if jiao[i].index(x)<jiao[i].index(y):
                jiao1.append(jiao[i])
        if jiao1==[]:
            return []
        else:
            for i in range(0,len(jiao1)):
                result.append(jiao1[i][0])
            return result
    else:
        return []
def minimum(x,y):   #the shortest time between two stations
    jiao=[val for val in direc[x] if val in direc[y]]
    t=2880*10
    for i in range(0,len(jiao)):
        if jiao[i].index(x)<jiao[i].index(y):
            s1=data[jiao[i][0]][0].index(x)-1
            s2=data[jiao[i][0]][0].index(y)-1
            time=(int(data[jiao[i][0]][1][s2][0][0])-int(data[jiao[i][0]][1][s1][1][0]))*60+int(data[jiao[i][0]][1][s2][0][1])-int(data[jiao[i][0]][1][s1][1][1])
            if time<t:
                t=time
    return t
def transfer(x,y):    #the transfer stations
    result1=[]
    result2=[]
    for i in range(0,len(direc[x])):
        for j in range(1,len(direc[x][i])):
            if direc[x][i][j] not in result1 and direc[x][i][j]!=x:
                result1.append(direc[x][i][j])
    for i in range(0,len(direc[y])):
        for j in range(1,len(direc[y][i])):
            if direc[y][i][j] not in result2 and direc[y][i][j]!=y:
                result2.append(direc[y][i][j])
    result=[i for i in result1 if i in result2]
    return result,result1,result2
def primarytransfer(x,y,interval):    #the primary transfer  the same station
    transtation=transfer(x,y)[0]
    result=[]
    result1=[]
    result2=[]
    if transtation!=[]:
        for i in range(0,len(transtation)):
            route1=[value for value in direc[x] if value in direc[transtation[i]]]
            route2=[value for value in direc[transtation[i]] if value in direc[y]]
            for h in range(0,len(route1)):
                if route1[h].index(x)<route1[h].index(transtation[i]):
                    for H in range(0,len(route2)):
                        if route2[H].index(transtation[i])<route2[H].index(y):
                            if route1[h][0]!=route2[H][0]:
                                s1=data[route1[h][0]][0].index(x)-1
                                s2=data[route1[h][0]][0].index(transtation[i])-1
                                dmin=(int(data[route1[h][0]][1][s2][0][0])-int(data[route1[h][0]][1][s1][1][0]))*60+int(data[route1[h][0]][1][s2][0][1])-int(data[route1[h][0]][1][s1][1][1])
                                arrivetimehour=int(data[route1[h][0]][1][s2][0][0])
                                arrivetimeminu=int(data[route1[h][0]][1][s2][0][1])

                                s3=data[route2[H][0]][0].index(transtation[i])-1
                                s4=data[route2[H][0]][0].index(y)-1
                                dmin1=(int(data[route2[H][0]][1][s4][0][0])-int(data[route2[H][0]][1][s3][1][0]))*60+int(data[route2[H][0]][1][s4][0][1])-int(data[route2[H][0]][1][s3][1][1])
                                starttimehour=int(data[route2[H][0]][1][s3][1][0])
                                starttimeminu=int(data[route2[H][0]][1][s3][1][1])

                                while arrivetimehour>=24:
                                    arrivetimehour=arrivetimehour-24
                                while starttimehour>=24:
                                    starttimehour=starttimehour-24
                                if starttimehour>arrivetimehour and ((starttimehour-arrivetimehour)*60+starttimeminu-arrivetimeminu)>=interval:
                                    Min=dmin+dmin1+(starttimehour-arrivetimehour)*60+starttimeminu-arrivetimeminu
                                if starttimehour>arrivetimehour and ((starttimehour-arrivetimehour)*60+starttimeminu-arrivetimeminu)<interval:
                                    Min=dmin+dmin1+(24+starttimehour-arrivetimehour)*60+starttimeminu-arrivetimeminu
                                if starttimehour<arrivetimehour:
                                    Min=dmin+dmin1+(24+starttimehour-arrivetimehour)*60+starttimeminu-arrivetimeminu
                                if starttimehour==arrivetimehour and starttimeminu-arrivetimeminu>=interval:
                                    Min=dmin+dmin1+starttimeminu-arrivetimeminu
                                if starttimehour==arrivetimehour and starttimeminu-arrivetimeminu<interval:
                                    Min=dmin+dmin1+24*60+starttimeminu-arrivetimeminu

                                result1.append(Min)
                                result2.append([transtation[i],route1[h][0],route2[H][0],Min])
                            else:
                                continue
        try:
            minindex=result1.index(min(result1))
            result.append(result2[minindex])
            result1[minindex]=10000
            minindex1=result1.index(min(result1))
            if result2[minindex1] not in result:
                result.append(result2[minindex1])
            return result
        except:
            return []
    else:
        return []
def primarytransfer1(x,y,interval):    #the primary transfer  the differrent stations
    transtation=transfer(x,y)[0]
    result=[]
    result1=[]
    result2=[]
    if transtation!=[]:
        for i in range(0,len(transtation)):
            if len(same[transtation[i]])>1:
                route1=[value for value in direc[x] if value in direc[transtation[i]]]
                for h in range(0,len(route1)):
                    if route1[h].index(x)<route1[h].index(transtation[i]):
                        s1=data[route1[h][0]][0].index(x)-1
                        s2=data[route1[h][0]][0].index(transtation[i])-1
                        dmin=(int(data[route1[h][0]][1][s2][0][0])-int(data[route1[h][0]][1][s1][1][0]))*60+int(data[route1[h][0]][1][s2][0][1])-int(data[route1[h][0]][1][s1][1][1])
                        arrivetimehour=int(data[route1[h][0]][1][s2][0][0])
                        arrivetimeminu=int(data[route1[h][0]][1][s2][0][1])
                        while arrivetimehour>=24:
                            arrivetimehour-=24
                        for j in range(0,len(same[transtation[i]])):
                            if same[transtation[i]][j]!=transtation[i]:
                                dmin1=twostation(same[transtation[i]][j], y, arrivetimehour, arrivetimeminu,interval)
                                result1.append(dmin+int(dmin1[0]))
                                result2.append([transtation[i],same[transtation[i]][j],route1[h][0],dmin1[1],dmin+int(dmin1[0])])
            else:
                continue
        try:
            minindex=result1.index(min(result1))
            result.append(result2[minindex])
            result1[minindex]=10000
            minindex1=result1.index(min(result1))
            if result2[minindex1] not in result:
                result.append(result2[minindex1])
            return result
        except:
            return []
    else:
        return []
def twoTransfer(x,y,ottran,ottran1,interval):   #transfer once
    result=[]
    result1=[]
    result2=[]
    tr=transfer(x,y)[0]
    transtation1=transfer(x,y)[1]
    transtation2=transfer(x,y)[2]
    mmin=8880
    break_flag=0
    break_flag1=0
    duan=0
    for i in range(0,len(transtation1)):
        if transtation1[i]!=y:
            time1=minimum(x, transtation1[i])
            if (time1+int(ottran1[transtation1[i]+y]))>mmin:
                continue
            for j in range(0,len(transtation2)):
                if transtation2[j]!=transtation1[i] and transtation2[j]!=x:
                    time2=minimum(transtation2[j],y)
                    if (time2+int(ottran[x+transtation2[j]]))>mmin:
                        continue
                    junc=[val for val in direc[transtation1[i]] if val in direc[transtation2[j]]]
                    junction=[]
                    for v in range(0,len(junc)):
                        if junc[v].index(transtation1[i])<junc[v].index(transtation2[j]):
                            junction.append(junc[v])
                    if junction!=[]:
                        both1=[value1 for value1 in direc[x] if value1 in direc[transtation1[i]]]
                        both2=[value2 for value2 in direc[transtation1[i]] if value2 in direc[transtation2[j]]]
                        both3=[value3 for value3 in direc[transtation2[j]] if value3 in direc[y]]
                        for d in range(0,len(both1)):
                            if both1[d].index(x)<both1[d].index(transtation1[i]):
                                for f in range(0,len(both2)):
                                    if both2[f].index(transtation1[i])<both2[f].index(transtation2[j]):
                                        for l in range(0,len(both3)):
                                            if both3[l].index(transtation2[j])<both3[l].index(y):
                                                s1=data[both1[d][0]][0].index(transtation1[i])-1
                                                s2=data[both1[d][0]][0].index(x)-1
                                                nub1=int((int(data[both1[d][0]][1][s1][0][0])-int(data[both1[d][0]][1][s2][1][0]))*60+int(data[both1[d][0]][1][s1][0][1])-int(data[both1[d][0]][1][s2][1][1]))
                                                ath1=int(data[both1[d][0]][1][s1][0][0])
                                                atm1=int(data[both1[d][0]][1][s1][0][1])

                                                s3=data[both2[f][0]][0].index(transtation2[j])-1
                                                s4=data[both2[f][0]][0].index(transtation1[i])-1
                                                nub2=int((int(data[both2[f][0]][1][s3][0][0])-int(data[both2[f][0]][1][s4][1][0]))*60+int(data[both2[f][0]][1][s3][0][1])-int(data[both2[f][0]][1][s4][1][1]))
                                                ath2=int(data[both2[f][0]][1][s3][0][0])
                                                atm2=int(data[both2[f][0]][1][s3][0][1])
                                                sth1=int(data[both2[f][0]][1][s4][1][0])
                                                stm1=int(data[both2[f][0]][1][s4][1][1])

                                                s5=data[both3[l][0]][0].index(y)-1
                                                s6=data[both3[l][0]][0].index(transtation2[j])-1
                                                nub3=int((int(data[both3[l][0]][1][s5][0][0])-int(data[both3[l][0]][1][s6][1][0]))*60+int(data[both3[l][0]][1][s5][0][1])-int(data[both3[l][0]][1][s6][1][1]))
                                                sth2=int(data[both3[l][0]][1][s6][1][0])
                                                stm2=int(data[both3[l][0]][1][s6][1][1])

                                                while ath1>=24:
                                                    ath1-=24
                                                while ath2>=24:
                                                    ath2-=24
                                                while sth1>=24:
                                                    sth1-=24
                                                while sth2>=24:
                                                    sth2-=24
                                                t1=sth1-ath1
                                                t2=sth2-ath2
                                                if t1<=0:
                                                    t1+=24
                                                if t2<=0:
                                                    t2+=24
                                                if nub1>mmin:
                                                    break_flag=1
                                                if ath1==sth1 and (stm1-atm1)>=interval:
                                                    if ath2==sth2 and (stm2-atm2)>=interval:
                                                        MMin=nub1+nub2+nub3+stm1-atm1+stm2-atm2
                                                        duan=nub1+nub2+stm1-atm1
                                                    else:
                                                        MMin=nub1+nub2+nub3+stm1-atm1+t2*60+stm2-atm2
                                                        duan=nub1+nub2+stm1-atm1
                                                else:
                                                    if ath2==sth2 and (stm2-atm2)>=interval:
                                                        MMin=nub1+nub2+nub3+t1*60+stm1-atm1+stm2-atm2
                                                        duan=nub1+nub2+t1*60+stm1-atm1
                                                    else:
                                                        MMin=nub1+nub2+nub3+t1*60+stm1-atm1+t2*60+stm2-atm2
                                                        duan=nub1+nub2+t1*60+stm1-atm1
                                                if (sth1-ath1)==1 and (stm1-atm1)<interval:
                                                    MMin+=1440
                                                if (sth2-ath2)==1 and (sth2-atm2)<interval:
                                                    MMin+=1440
                                                if duan>mmin:
                                                    break_flag1=1
                                                if MMin<mmin and both1[d][0]!=both2[f][0] and both2[f][0]!=both3[l][0] and both1[d][0]!=both3[l][0]:
                                                    result1.append(MMin)
                                                    result2.append([transtation1[i],transtation2[j],both1[d][0],both2[f][0],both3[l][0],MMin])
                                                    mmin=MMin
                                            if break_flag==1 or break_flag1==1:
                                                break_flag1=0
                                                break
                                    if break_flag==1:
                                        break_flag=0
                                        break
                    else:
                        continue
    try:
        minindex=result1.index(min(result1))
        result.append(result2[minindex])
        result1[minindex]=20000
        minindex1=result1.index(min(result1))
        if result2[minindex1] not in result:
            result.append(result2[minindex1])
        return result
    except:
        return []
all={}
result1=straight(start,end)
nonstop=[]
if result1!=[]:
    timearray=[]
    timearray1=[]
    for i in range(0,len(result1)):
        timearray.append(twotime(start,end,result1[i]))
    w=min(timearray)
    for i in range(0,len(result1)):
        if twotime(start,end,result1[i])==w:
            timearray1.append(i)
    for i in range(0,len(result1)):
        inthree={}
        stations=[]
        x=data[result1[i]][0].index(start)
        y=data[result1[i]][0].index(end)+1
        for j in range(x,y):
            infour={}
            infour['name']=data[result1[i]][0][j]
            t=int(data[result1[i]][1][j-1][0][0])
            t1=int(data[result1[i]][1][j-1][1][0])
            m=data[result1[i]][1][j-1][0][1]
            m1=data[result1[i]][1][j-1][1][1]
            while t>=24:
                t-=24
            while t1>=24:
                t1-=24
            infour['arriveTime']=str(t)+':'+str(m)
            infour['startTime']=str(t1)+':'+str(m1)
            stations.append(infour)
        if i in timearray1:
            inthree['isFastest']='true'
        else:
            inthree['isFastest']='false'
        inthree['trainNumber']=result1[i]
        inthree['time']=str(twotime(start,end,result1[i]))
        inthree['stations']=[]
        inthree['stations'].append(stations)
        nonstop.append(inthree)
all['nonstop']=nonstop

result3=primarytransfer(start,end,interval1)
result31=primarytransfer1(start,end,interval2)
once=[]
result2=[]
bijiao=[]
bijiao1=[]
for i in range(0,len(result3)):
    bijiao.append(result3[i])
    bijiao1.append(int(result3[i][3]))
for i in range(0,len(result31)):
    bijiao.append(result31[i])
    bijiao1.append(int(result31[i][4]))
if bijiao!=[]:
    Minindex=bijiao1.index(min(bijiao1))
    result2.append(bijiao[Minindex])
    bijiao1[Minindex]=20000
    Minindex1=bijiao1.index(min(bijiao1))
    if Minindex1!=Minindex:
        result2.append(bijiao[Minindex1])
    for i in range(0,len(result2)):
        if len(result2[i])==4:
            d=1
        else:
            d=2
        inthree={}
        trainNum=[]
        station=[]
        for n in range(d,d+2):
            stations=[]
            if n==d:
                x=data[result2[i][d]][0].index(start)
                y=data[result2[i][d]][0].index(result2[i][0])+1
            else:
                x=data[result2[i][d+1]][0].index(result2[i][d-1])
                y=data[result2[i][d+1]][0].index(end)+1
            for j in range(x,y):
                infour={}
                if d==2 and n==(d+1):
                    rr=result2[i][1]
                else:
                    rr=result2[i][0]
                if data[result2[i][n]][0][j]==rr:
                    infour['isTransferStation']='true'
                else:
                    infour['isTransferStation']='false'
                infour['name']=data[result2[i][n]][0][j]
                t=int(data[result2[i][n]][1][j-1][0][0])
                t1=int(data[result2[i][n]][1][j-1][1][0])
                while t>=24:
                    t-=24
                while t1>=24:
                    t1-=24
                m=data[result2[i][n]][1][j-1][0][1]
                m1=data[result2[i][n]][1][j-1][1][1]
                infour['arriveTime']=str(t)+':'+str(m)
                infour['startTime']=str(t1)+':'+str(m1)
                stations.append(infour)
            station.append(stations)
            trainNum.append(result2[i][n])
        inthree['time']=result2[i][d+2]
        if i==0:
            inthree['isFastest']='true'
        else:
            inthree['isFastest']='false'
        inthree['trainNumber']=trainNum
        inthree['stations']=station
        once.append(inthree)
all['once']=once
result4=twoTransfer(start,end,ottran,ottran1,interval1)
twice=[]
if result4!=[]:
    for i in range(0,len(result4)):
        inthree={}
        trainNum=[]
        station=[]
        for n in range(2,5):
            stations=[]
            if n==2:
                x=data[result4[i][n]][0].index(start)
                y=data[result4[i][n]][0].index(result4[i][0])+1
            if n==3:
                x=data[result4[i][n]][0].index(result4[i][0])
                y=data[result4[i][n]][0].index(result4[i][1])+1
            if n==4:
                x=data[result4[i][n]][0].index(result4[i][1])
                y=data[result4[i][n]][0].index(end)+1
            for j in range(x,y):
                infour={}
                if (j==x and (n==3 or n==4)) or (j==(y-1) and (n==2 or n==3)):
                    infour['isTransferStation']='true'
                else:
                    infour['isTransferStation']='false'
                infour['name']=data[result4[i][n]][0][j]
                t=int(data[result4[i][n]][1][j-1][0][0])
                t1=int(data[result4[i][n]][1][j-1][1][0])
                while t>=24:
                    t-=24
                while t1>=24:
                    t1-=24
                m=data[result4[i][n]][1][j-1][0][1]
                m1=data[result4[i][n]][1][j-1][1][1]
                infour['arriveTime']=str(t)+':'+str(m)
                infour['startTime']=str(t1)+':'+str(m1)
                stations.append(infour)
            station.append(stations)
            trainNum.append(result4[i][n])
        inthree['time']=result4[i][5]
        if i==0:
            inthree['isFastest']='true'
        else:
            inthree['isFastest']='false'
        inthree['trainNumber']=trainNum
        inthree['stations']=station
        twice.append(inthree)
all['twice']=twice
with codecs.open("D:/workspace/traintrainserver/public/json/result.json","w","utf-8") as f:
    j1=json.dumps(all,ensure_ascii=False)
    f.write(j1)
