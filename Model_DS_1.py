# 예측에 사용할 데이터 만들기
import pandas as pd
import pickle
# Import Oracle DB Package
import cx_Oracle
# Credentials
import _auth_config as auth
# Support Functions
pd.set_option('mode.chained_assignment',  None)

print('서버에 연결해서 DATA를 내려 받으려면 1을 입력하세요. (처음 모델 만들 때만 사용)')
print('저장된 데이터로 예측하려면 2을 입력하세요')
type_num = int(input('숫자를 입력해 주세요 : '))

if type_num == 1:
    # 오라클 DB 접속 아이디 및 접속 주소 등 정보 입력
    credentials = f"{auth.username}/{auth.password}@{auth.host}:{auth.port}/{auth.servicename}/"
    connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")
    df = pd.DataFrame()  # 모든 정보 추출
    df1 = pd.DataFrame()  # 정보만 추출
    query1 = "SELECT enoviaif.tr_spec.plm_spec_obj_id, enoviaif.tr_plmspec_rcx.*, \
            enoviaif.tr_spec.spec_seq, enoviaif.tr_item.*, enoviaif.tr_result_dyna_stiff.*\
            FROM ENOVIAIF.tr_result_dyna_stiff \
            INNER JOIN ENOVIAIF.tr_item \
            ON tr_result_dyna_stiff.item_seq = tr_item.item_seq \
            INNER JOIN ENOVIAIF.tr_spec \
            ON tr_spec.spec_seq = tr_result_dyna_stiff.spec_seq \
            INNER JOIN ENOVIAIF.tr_plmspec_rcx \
            ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
            WHERE tr_item.result_date > TO_DATE('2019-05-31', 'YYYY-MM-DD')"
    df1 = pd.read_sql(query1, connection)
    #
    # for item_seq in PLM_DATA['ITEM_SEQ']:
    #     ################# QUERY #################
    #     query2 = f"SELECT enoviaif.tr_spec.plm_spec_obj_id, enoviaif.tr_plmspec_rcx.*, \
    #             enoviaif.tr_spec.spec_seq, enoviaif.tr_item.*, enoviaif.tr_result_dyna_stiff.*\
    #             FROM ENOVIAIF.tr_result_dyna_stiff \
    #             INNER JOIN ENOVIAIF.tr_item \
    #             ON tr_result_dyna_stiff.item_seq = tr_item.item_seq \
    #             INNER JOIN ENOVIAIF.tr_spec \
    #             ON tr_spec.spec_seq = tr_result_dyna_stiff.spec_seq \
    #             INNER JOIN ENOVIAIF.tr_plmspec_rcx \
    #             ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
    #             WHERE tr_result_dyna_stiff.item_seq = '{item_seq}'"
    #     a1 = pd.read_sql(query2, connection)
    #     df1 = pd.concat([df1, a1])
    # Close Connection
    connection.close()

    df1["TEST_LOAD"] = df1["LOAD_100"]
    pickle.dump(df1, open('D:\\workroom\\p_workroom\\_DATA_Traing\\_df.pkl', 'wb'))
elif type_num == 2:
    df1 = pickle.load(open('D:\\workroom\\p_workroom\\_DATA_Traing\\_df.pkl', 'rb'))

# df1.to_csv('D:\\workroom\\p_workroom\\_DATA_Traing\\_df.csv')
df1 = df1.copy().drop_duplicates(subset=['SPEC_NO'], keep='last')
df = df1.dropna(subset=["RIC_STEP_GAUGE"])
df = df.reset_index()
del(df["index"])
# SPEC NO 를 사용하여, 정보를 읽어 오기
df2 = df.iloc[:,1:590]
df2["TEST_LOAD"] = df["LOAD_100"]
df2["RIM_WIDTH"] = df["RIM_WIDTH"]
df2["AIR"] = df["AIR"]

# 스펙을 변환하기
import _PLM_SPEC_CHANGE # 필요한 스펙으로 변환하는 함수 정의
df3 = _PLM_SPEC_CHANGE.Change2(df2)
# 사용할 cols를 정의하고, One - Hot Encoding 적용하기


import _use_cols
use_cols = _use_cols.cols_DS
df4 = df3[use_cols]
df4["SPEC_NO"]=df3["SPEC_NO"]
df4 = df4.dropna()

df5 = df[['SPEC_NO', 'STIFFNESS_DISP_1','STIFFNESS_DISP_2','STIFFNESS_DISP_3','STIFFNESS_DISP_4','STIFFNESS_DISP_5','STIFFNESS_DISP_6','DYNAMINC_STIFFNESS']]
df6 = pd.DataFrame()
df6 = df4.merge(df5)
# df6.to_csv("D:\\workroom\\p_workroom\\_DATA_Traing\\check_data.csv", index=None, encoding='UTF-8')

scale_cols = _use_cols.scale_cols_DS
# one hot encording을 적용하기 전에, 숫자 데이타를 지정하기
df7 = df6.copy().astype('object') #Data Type을 모두 object로 통일화 하기

temp1 = []
for name1 in df7['RIM_WIDTH']:
    # name1.replace('J','')
    temp1.append(name1.replace('J',''))
df7['RIM_WIDTH'] = temp1

df8 = df7
for col in scale_cols:
    print(col)
    df8 = df8.astype({col: 'float16'})

# targets = ['STIFFNESS_DISP_1','STIFFNESS_DISP_2','STIFFNESS_DISP_3','STIFFNESS_DISP_4','STIFFNESS_DISP_5','STIFFNESS_DISP_6','DYNAMINC_STIFFNESS']
targets = ['DYNAMINC_STIFFNESS']

for col in targets:
    df8=df8.astype({col: 'float16'})

JLC_MATERIAL_1 = ['A 1500D/1 + N66 1260D/1 Single End Cord',
                  'ARAMID 1500 D/1 + NYLON66 1260 D/1',
                  'Aramid 1500 D/2 + Nylon66 1260 D/1 21EPI',
                  'A1500D/2+N66 1260D/1 Single End Cord',
                  'N66 1260D/2 28EPI (28T)']
JLC_MATERIAL_2 = ['A 1500D/1 + N66 1260D/1 25.4EPI',
                    'A 1500D/1 + N66 1260D/1 25.4EPI',
                  'A 1500D/2 + N66 1260D/1 21EPI',
                  'A 1500 D/2 + N66 1260 D/1 21EPI',
                  'N66 1260D/2 28EPI']
df8['JLC_MATERIAL'] = df8.copy()['JLC_MATERIAL'].replace(JLC_MATERIAL_1, JLC_MATERIAL_2)

C01_MATERIAL_1 = ['RAYON 1650 D/2 26EPI']
C01_MATERIAL_2 = ['R 1650D/2 26EPI']
df8['C01_MATERIAL'] = df8.copy()['C01_MATERIAL'].replace(C01_MATERIAL_1, C01_MATERIAL_2)

compd_exclude = [] # 제거하고 싶은 컴파운드 선언  << CX, CF, CN
temp_lists = list(df8['CTB_COMPOUND'].unique())
for temp_list in temp_lists:
    if temp_list[:2] == 'CX':
        compd_exclude.append(temp_list)
    elif temp_list[:3] == 'CQF':
        compd_exclude.append(temp_list)
    elif temp_list[:3] == 'CQN':
        compd_exclude.append(temp_list)
    elif temp_list[:3] == 'CQK':
        compd_exclude.append(temp_list)

C01_exclude = ['DSP1000D/2 28EPI Low Shrinkage'] # 제거하고 싶은 선언
BT1_MATERIAL_exclude = ['Mbynby Wire 0.35mmUT'] # 제거하고 싶은 선언
FIL_SHAPE1 = ['Reglar','Thin'] # 선택하고 싶은 Fil 선언

df9 = df8[  (df8['AIR'] > 1.8) &
            (df8['AIR'] < 3.5) &
            (df8['TEST_LOAD'] > 310) &
            (df8['TEST_LOAD'] < 800) &
            (df8['FIL_SHAPE'].isin(FIL_SHAPE1)) &
            (~df8['C01_MATERIAL'].isin(C01_exclude)) &
            (~df8['BT1_MATERIAL'].isin(BT1_MATERIAL_exclude)) &
            (~df8['CTB_COMPOUND'].isin(compd_exclude))  ].reset_index(drop=True)

_DS_data = {}
_DS_data['1.Target list'] = targets
_DS_data['1.Input Properties list'] = use_cols
_DS_data['1.Input Properties list (number)'] = scale_cols
_DS_data['1.Input Data'] = df9

df9.to_csv("D:\\workroom\\p_workroom\\_DATA_Traing\\_DS_data.csv", index=None, encoding='UTF-8')
pickle.dump(_DS_data, open('D:\\workroom\\p_workroom\\_DATA_Traing\\_DS_data.pkl', 'wb'))
