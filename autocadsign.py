#coding:utf-8

from pyautocad import Autocad, APoint
import os.path



NAMETABLE_REVERSE={}
file=open('.\\name.cfg','r')
for line in file.readlines():
    line=line.rstrip().split(' ')
    if line[0]:
        NAMETABLE_REVERSE[line[1]]=line[0]
file.close()


def autocadsign(atype,filedirection,linedata,datedata=None,atype_date=None,Height=None):
    if atype_date==None:
        atype_date=' '

    if Height==None:
        Height=[400,300]

    # linedata[0]=[[x1,x2],[y1,y2]]
    movesize=[int(linedata[0][0][0]),int(linedata[0][1][0])]   #1:100 move toward right is positive
    atype_movesize=[int(linedata[0][0][1]),int(linedata[0][1][1])]
    signloc=[]
    for i in linedata[1]:
        signloc.append(int(i)-1)

    # 标准1:100图框，五个模式分别对应五个位置
    if datedata:
        mode1={'A3':(30150,3420),'A2':(47080,3920),'A1':(71560,3920),'A0':(106580,3920)}
        mode2={'A3':(25460,1320),'A2':(42580,1820),'A1':(67060,1820),'A0':(101850,1820)}
        mode3={'A3':(25460,2020),'A2':(42580,2520),'A1':(67060,2520),'A0':(101850,2520)}
        mode4={'A3':(25460,2720),'A2':(42580,3220),'A1':(67060,3220),'A0':(101850,3220)}
        mode5={'A3':(25460,3420),'A2':(42580,3920),'A1':(67060,3920),'A0':(101850,3920)}
    else:
        mode1={'A3':(30450,3420),'A2':(47380,3920),'A1':(71860,3920),'A0':(106880,3920)}
        mode2={'A3':(25760,1320),'A2':(42880,1820),'A1':(67360,1820),'A0':(102150,1820)}
        mode3={'A3':(25760,2020),'A2':(42880,2520),'A1':(67360,2520),'A0':(102150,2520)}
        mode4={'A3':(25760,2720),'A2':(42880,3220),'A1':(67360,3220),'A0':(102150,3220)}
        mode5={'A3':(25760,3420),'A2':(42880,3920),'A1':(67360,3920),'A0':(102150,3920)}
    atype_mode1 = {'A3': (34000, 8150), 'A2': (50900, 8650), 'A1': (75600, 8650), 'A0': (110400, 8650)}
    atype_mode2 = {'A3': (35500, 8150), 'A2': (52400, 8650), 'A1': (77100, 8650), 'A0': (111900, 8650)}
    atype_mode3 = {'A3': (37000, 8150), 'A2': (53900, 8650), 'A1': (78600, 8650), 'A0': (113400, 8650)}
    atype_mode4 = {'A3': (38500, 8150), 'A2': (55400, 8650), 'A1': (80100, 8650), 'A0': (114900, 8650)}
    atype_mode5 = {'A3': (40000, 8150), 'A2': (56900, 8650), 'A1': (81600, 8650), 'A0': (116400, 8650)}
    middlemode=[mode1,mode2,mode3,mode4,mode5]
    atype_middlemode=[atype_mode1,atype_mode2,atype_mode3,atype_mode4,atype_mode5]
    number=len(signloc)
    mode=[]
    atype_mode=[]
    filepath=[]
    for i in range(number):
        filepathloc=os.path.join(filedirection,'signfile\\'+linedata[2][i]+".dwg")
        filepath.append(filepathloc)
        mode.append(middlemode[signloc[i]])
        atype_mode.append(atype_middlemode[signloc[i]])

    acad = Autocad(create_if_not_exists=False)
    acad.prompt("Hello, Autocad\n")
    # print(acad.doc.Name)

    Layerobj = acad.ActiveDocument.Layers.Add("CADSIGN")
    if atype:
        acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item('standard')
    acad.ActiveDocument.ActiveLayer = Layerobj
    data=[]
    for block in acad.iter_objects('Block'):
        blockname=block.name[0:2]
        if blockname in ['A0','A1','A2','A3']:
            data.append((blockname,block.InsertionPoint[0],block.InsertionPoint[1],block.XScaleFactor))


    cadnumber=len(data)
    for i in range(number):
        for j in range(cadnumber):
                block=data[j][0]
                scale=data[j][3]/100
                # data[j]是图框的左下角坐标
                # mode[i]是哪个位置的签名，block是每个图框下需要移动的位置
                x=data[j][1]+(mode[i][block][0]+movesize[0])*scale
                y=data[j][2]+(mode[i][block][1]+movesize[1])*scale
                p1=APoint(x,y)
                acad.model.InsertBlock(p1, filepath[i], scale,scale,scale, 0)
                if datedata:
                    x2=x+1200*scale
                    p2=APoint(x2,y)
                    acad.model.AddText(datedata[i],p2,200*scale)
                if atype:
                    x3=data[j][1]+(atype_mode[i][block][0]+400+atype_movesize[0])*scale
                    y3=data[j][2]+(atype_mode[i][block][1]+atype_movesize[1])*scale
                    p3=APoint(x3,y3)
                    x4=x3-100*scale
                    y4=y3-400*scale
                    p4=APoint(x4,y4)
                    # linedata[2]是需要签名的名字
                    acad.model.AddText(NAMETABLE_REVERSE[linedata[2][i]], p3, Height[0]* scale)
                    acad.model.AddText(atype_date, p4, Height[1] * scale)

    acad.prompt("Autosign Successfully\n")

if __name__=='__main__':
    datedata=['2020.02.13','2020.02.14','2020.02.15','2020.02.16']
    atype_date='2019.03'
    linedata=[[['0', '0'],['0', '0']], ['1', '2', '4', '5'], ['wangzhenyu', 'wangzhenyu', 'wangzhenyu', 'wangzhenyu']]
    autocadsign(1,'D:\\autosign',linedata,datedata,atype_date)
