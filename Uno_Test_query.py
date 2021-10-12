# 예측에 사용할 데이터 만들기
import pandas as pd
import pickle
# Import Oracle DB Package
import cx_Oracle
# Credentials
import _auth_config as auth
# Support Functions
pd.set_option('mode.chained_assignment',  None)

# 오라클 DB 접속 아이디 및 접속 주소 등 정보 입력
credentials = f"{auth.username}/{auth.password}@{auth.host}:{auth.port}/{auth.servicename}/"
connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")

pdFS = pd.DataFrame()  # Foot shape 정보 프레임
pdST = pd.DataFrame()  # Static 정보 프레임
pdFT = pd.DataFrame()  # Flattrac shape 정보 프레임

QueryStartdata = '2021-09-01'
# 쿼리문
query_FOOTSHAPE = "SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
            enoviaif.tr_item.*, enoviaif.tr_result_FOOTSHAPE.*, enoviaif.tr_result_FOOTSHAPE_DETAIL.*\
            FROM ENOVIAIF.tr_result_FOOTSHAPE_DETAIL \
            INNER JOIN ENOVIAIF.tr_result_FOOTSHAPE \
            ON tr_result_FOOTSHAPE_DETAIL.item_seq = tr_result_FOOTSHAPE.item_seq \
            INNER JOIN ENOVIAIF.tr_item \
            ON tr_result_FOOTSHAPE_DETAIL.item_seq = tr_item.item_seq \
            INNER JOIN ENOVIAIF.tr_spec \
            ON tr_spec.spec_seq = tr_result_FOOTSHAPE_DETAIL.spec_seq \
            LEFT JOIN ENOVIAIF.tr_plmspec_rcx \
            ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
            WHERE tr_item.result_date > TO_DATE('2021-09-01', 'YYYY-MM-DD')"

query_STATIC = "SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
            enoviaif.tr_item.*, enoviaif.tr_result_STATIC.*\
            FROM ENOVIAIF.tr_result_STATIC \
            INNER JOIN ENOVIAIF.tr_item \
            ON tr_result_STATIC.item_seq = tr_item.item_seq \
            INNER JOIN ENOVIAIF.tr_spec \
            ON tr_spec.spec_seq = tr_result_STATIC.spec_seq \
            LEFT JOIN ENOVIAIF.tr_plmspec_rcx \
            ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
            WHERE tr_item.result_date > TO_DATE('2021-09-01', 'YYYY-MM-DD')"

query_FLATTRAC = "SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
            enoviaif.tr_item.*, enoviaif.tr_result_FLATTRAC.*\
            FROM ENOVIAIF.tr_result_FLATTRAC \
            INNER JOIN ENOVIAIF.tr_item \
            ON tr_result_FLATTRAC.item_seq = tr_item.item_seq \
            INNER JOIN ENOVIAIF.tr_spec \
            ON tr_spec.spec_seq = tr_result_FLATTRAC.spec_seq \
            LEFT JOIN ENOVIAIF.tr_plmspec_rcx \
            ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
            WHERE tr_item.result_date > TO_DATE('2021-09-01', 'YYYY-MM-DD')"

# 쿼리 전송 및 데이터 저장
pdFS = pd.read_sql(query_FOOTSHAPE, connection)
pdST = pd.read_sql(query_STATIC, connection)
pdFT = pd.read_sql(query_FLATTRAC, connection)
connection.close()

# 데이터 저장 확인용
# ''''
pdFS.to_csv("D:\\workroom\\p_workroom\\_DATA_Traing\\FSData.csv", mode='w')
pdST.to_csv("D:\\workroom\\p_workroom\\_DATA_Traing\\STData.csv", mode='w')
pdFT.to_csv("D:\\workroom\\p_workroom\\_DATA_Traing\\FTData.csv", mode='w')
# '''


# 시간이 많이 걸리니 데이터 저장하고 불러서 작동 확인. Binary 파일로 저장
pickle.dump(pdFS, open('D:\\workroom\\p_workroom\\_DATA_Traing\\pdFS.pkl', 'wb'))
pickle.dump(pdST, open('D:\\workroom\\p_workroom\\_DATA_Traing\\pdST.pkl', 'wb'))
pickle.dump(pdFT, open('D:\\workroom\\p_workroom\\_DATA_Traing\\pdFT.pkl', 'wb'))




