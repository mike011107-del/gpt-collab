import sys,json,os
S='/tmp/claude-0/-home-claude/f822ab78-49b8-5e2f-8fbe-8111b065c404/scratchpad'
sys.path.insert(0,S+'/r19')
from tools import *
_c=os.getcwd(); os.chdir(S); sys.path.insert(0,S+'/r15')
import ev15
os.chdir(_c)
COMP=ev15.COMP; BAN=ev15.BAN; OLD=list(ev15.OLD)
# 18_ 第十五輪（純冷色 19 組）用過的顏色
p17=json.load(open(S+'/r17/pal17_all.json'))
for k,v in p17.items():
    for key in ('tank','cab','line','low'):
        x=v.get(key)
        if isinstance(x,list): x=x[0]
        if x and x.upper() not in ('#F4F1E8','#F2F1EC','#F3F2EE','#F1ECE1','#F2EEE3','#F4F5F0','#F2F1EA','#EEE7DB','#F6ECDD','#1E1F1E','#2B2D2F','#3C3A38','#3A3C3B','#1E2422','#3A3E3D','#34302D','#2B2826','#E2DCD2','#C9CEC4','#D2CFC8'):
            OLD.append(('18_'+k,x))
# 工地與公共車輛已經有主人的顏色（近似值；公會色樣沒有公開數值，用 RAL 或照片近似）
SITE=[('交維橙(公會64近似RAL2009)','#DA530A'),('交通錐(照片)','#F82F22'),('污水警示帶紅字(近似)','#C8102E'),
      ('業主告示牌藍(近似RAL5017)','#005E83'),('交通標誌藍(近似RAL5005)','#005187'),('中華電信藍','#0069AA'),
      ('新北圍籬綠(近似RAL6024)','#308446'),('台南垃圾車綠(近似)','#2E8B57'),('基隆垃圾車藍(近似)','#1F6FB2'),
      ('警車藍(近似)','#1B3F8B'),('消防紅(近似RAL3000)','#A42821'),('污水PVC管橘紅(近似RAL2001)','#B6481C'),
      ('交通指揮鉻黃衣(近似)','#FFD200'),('反光背心螢光黃綠','#C8E000')]
