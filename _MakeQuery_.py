def fnQuery(startDate, endDate, testItem) :
    '''
    Make Query to use Oracle DB

    :param startDate: Start Date to get DB Table
    :param endDate: End Date to get DB Table
    :param testItem: There are 3 items
     FS- Foot shape
     ST- Static
     FT- Flat trac

    :return: DB getted Server using Query
    '''

    import pandas as pd
    import cx_Oracle
    # Credentials
    import _AuthConfig as auth

    # 오라클 DB 접속 아이디 및 접속 주소 등 정보 입력
    credentials = f"{auth.username}/{auth.password}@{auth.host}:{auth.port}/{auth.servicename}/"
    connection = cx_Oracle.connect(credentials, encoding="UTF-8", nencoding="UTF-8")

    DF = pd.DataFrame()  # 서버에서 데이터를 받아올 데이터 프레임

    # QueryStartdate = "'2018-01-01'"
    # QueryEnddate = "'2019-01-01'"

    QueryStartdate = f"'{startDate}'"
    QueryEnddate = f"'{endDate}'"

    # 쿼리문
    if testItem == 'FS' :
        query = f"SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
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
                WHERE tr_item.result_date > TO_DATE({QueryStartdate}, 'YYYY-MM-DD') and tr_item.result_date < TO_DATE({QueryEnddate}, 'YYYY-MM-DD')"
        DF = pd.read_sql(query, connection)
        DF = DF.iloc[:,:-1]

    elif testItem == 'ST' :
        query = f"SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
                enoviaif.tr_item.*, enoviaif.tr_result_STATIC.*\
                FROM ENOVIAIF.tr_result_STATIC \
                INNER JOIN ENOVIAIF.tr_item \
                ON tr_result_STATIC.item_seq = tr_item.item_seq \
                INNER JOIN ENOVIAIF.tr_spec \
                ON tr_spec.spec_seq = tr_result_STATIC.spec_seq \
                LEFT JOIN ENOVIAIF.tr_plmspec_rcx \
                ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
                WHERE tr_item.result_date > TO_DATE({QueryStartdate}, 'YYYY-MM-DD') and tr_item.result_date < TO_DATE({QueryEnddate}, 'YYYY-MM-DD')"
        DF = pd.read_sql(query, connection)

    elif testItem == 'FT':
        query = f"SELECT enoviaif.tr_plmspec_rcx.*, enoviaif.tr_spec.*,\
                enoviaif.tr_item.*, enoviaif.tr_result_FLATTRAC.*\
                FROM ENOVIAIF.tr_result_FLATTRAC \
                INNER JOIN ENOVIAIF.tr_item \
                ON tr_result_FLATTRAC.item_seq = tr_item.item_seq \
                INNER JOIN ENOVIAIF.tr_spec \
                ON tr_spec.spec_seq = tr_result_FLATTRAC.spec_seq \
                LEFT JOIN ENOVIAIF.tr_plmspec_rcx \
                ON tr_plmspec_rcx.plm_spec_obj_id = tr_spec.plm_spec_obj_id \
                WHERE tr_item.result_date > TO_DATE({QueryStartdate}, 'YYYY-MM-DD') and tr_item.result_date < TO_DATE({QueryEnddate}, 'YYYY-MM-DD')"
        DF = pd.read_sql(query, connection)


    connection.close()
    return DF




