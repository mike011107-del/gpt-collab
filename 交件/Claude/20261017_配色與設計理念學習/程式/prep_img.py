from PIL import Image
import os
P="/mnt/user-data/uploads/崧淳環保科技股份有限公司/國外同業CIS素材_20261017/_報告原始檔/v3/"
O="/tmp/claude-0/report/img/"
photos="""Biffa_c13 Biffa_c02 Biffa_c01 Kanal-Tuerpe_c29 Kanal-Tuerpe_c31 Lanes_Group_c31 Lanes_Group_c01 Lanes_Group_c21 Metro_Rod_c26 Metro_Rod_c19 Metro_Rod_c16
Roto-Rooter_c04 Roto-Rooter_c01 Republic_Services_c06 Republic_Services_c19 Cleanaway_c01 Kaiser_c03 Rioned_c29 Thames_Water_c01 Thames_Water_c08 iPEK_c12
Uisce_Eireann_c20 Tideway_c11 Tideway_c05 Kier_c08 SUEZ_c01 Clancy_c31 Clancy_c12 Toa_Grout_c06 Metawater_c09 Vactor_c14 Remondis_c04 Dyno-Rod_c01 Dyno-Rod_c03 PUB_Singapore_c08 Sekisui_SPR_c31 Ventia_c11 Murphy_c01""".split()
for f in photos:
    im=Image.open(P+'photos/'+f+'.jpg').convert('RGB'); im.thumbnail((1000,1000)); im.save(O+f+'.jpg',quality=82)
for p in ['p3','p5','p7']:
    im=Image.open(P+'veolia/'+p+'.jpg').convert('RGB'); im.save(O+'veolia_'+p+'.jpg',quality=85)
A="/mnt/project-files/崧淳CI/研究/23_LOGO與CIS美感學習_20261017/"
f1=Image.open(A+'01_標誌造形三件事.png').convert('RGB'); f2=Image.open(A+'02_整套識別與版面習慣.png').convert('RGB')
print(f1.size,f2.size)
crops={'aes1_one':(f1,(0,320,1080,1490)),'aes1_frame':(f1,(0,1536,1080,2000)),'aes1_thin':(f1,(0,2024,1080,2864)),
       'aes2_nasa':(f2,(0,222,1080,1240)),'aes2_br':(f2,(0,1277,1080,1980)),'aes2_rebrand':(f2,(0,2017,1080,3034)),'aes2_ai':(f2,(0,3053,1080,3682))}
for k,(im,box) in crops.items():
    im.crop(box).save(O+k+'.png')
print(len(os.listdir(O)))
