# 스펙 데이터값을 정제하는 과정
import pandas as pd
df2 = pd.DataFrame()

def Change1(df2):
    # 불필요한 문자 제거하여 >> C01 list로 만들고 >> Dataflame의 열을 교체하는 작업
    temp1=[]
    for name1 in df2['C01_MATERIAL']:
        temp1.append(name1.split('(')[0])
    df2['C01_MATERIAL'] = temp1

    temp2 = []
    i = 0
    for name2 in df2['JLC_MATERIAL']:
        if name2 is not None:
            temp2.append(name2.split('(')[0])
        else:
            if df2['JEC_MATERIAL'][i] is not None:
                temp2.append(df2['JEC_MATERIAL'][i])
            else:
                temp2.append(df2['JFC_MATERIAL'][i])
        i = i + 1
    df2['JLC_MATERIAL'] = temp2

    temp3=[]
    temp4=[]
    for name3 in df2['TUH_1_2']:
        temp3.append(name3.split('-')[0])
        temp4.append(name3.split('-')[1])
    df2['TUH_1'] = temp3
    df2['TUH_2'] = temp4

    temp5=[]
    for name5 in df2['BT1_MATERIAL']:
        # temp5.append(name5.replace('?','by').replace('횞','by').replace('(','_').replace(')','_').replace('&OC',''))
        a1 = name5[1]
        a2 = name5.replace(a1, "by")
        temp5.append(a2.replace('(', '_').replace(')', '_').replace('&OC', ''))
    df2['BT1_MATERIAL'] = temp5

    temp6=[]
    for name6 in df2['SUT_STEP_GAUGE']:
        name6 = [v for v in name6.split('-') if v]
        temp6.append(sorted([float(x) for x in name6])[len(name6) // 2])
    df2['SUT_STEP_GAUGE2'] = temp6

    temp7=[]
    for name7 in df2['TRW_STEP_GAUGE']:
        if name7: #비어 있는지 여부를 확인
            name7 = [v for v in name7.split('-') if v]
            temp7.append(max([float(x) for x in name7]))
        else:
            temp7.append('')
    df2['TRW_STEP_GAUGE2'] = temp7

    temp8_top=[]
    temp8_bot=[]
    for name8 in df2['BSW_STEP_GAUGE']:
        name8 = [v for v in name8.split('-') if v]
        name8_1 = name8[:round(len(name8) * 0.5)]
        name8_2 = name8[round(len(name8) * 0.5):]
        temp8_top.append(max([float(x) for x in name8_1]))
        temp8_bot.append(max([float(x) for x in name8_2]))
    df2['BSW_STEP_GAUGE_TOP'] = temp8_top
    df2['BSW_STEP_GAUGE_BOT'] = temp8_bot

    temp9=[]
    for name9 in df2['RIC_STEP_GAUGE']:
        name9 = [v for v in name9.split('-') if v]
        temp9.append(max([float(x) for x in name9]))
    df2['RIC_STEP_GAUGE2'] = temp9

    temp10=[]
    for name10,name11,name12, name13 in zip(df2['BEAD_SINGLE_STRANDS'],df2['BEAD_LAY_UP'],df2['BEAD_STRAND'], df2['BEAD_LAYERS']):
        # print(name10)
        # print(name11)
        # print(name12)
        # print(name13)
        if name10.split('-')[0] == '0':
            if name11.split('-')[0] == '0':
                temp10.append(f"{name12}-{name13}")
                # print(f"{name12}-{name13}")
            else:
                temp10.append(f"{name11}")
                # print(name11)
        else:
            temp10.append(f"{name10}")
    df2['BEAD_SINGLE_STRANDS2'] = temp10

    temp11 = []
    for name11 in df2['FIL_EXTRUDED']:
        # print(name11[1])
        if name11 is None:
            temp11.append("")
        elif name11[1] == 'A':
            temp11.append("Regular")
        elif name11[1] == 'B':
            temp11.append("Regular")
        elif name11[1] == 'C':
            temp11.append("Thin")
        elif name11[1] == 'D':
            temp11.append("Thin")
        elif name11[1] == 'F':
            temp11.append("Thin")
        elif name11[1] == 'H':
            temp11.append("Regular")
        elif name11[1] == 'G':
            temp11.append("Thin")
        elif name11[1] == 'T':
            temp11.append("Thin")
        else:
            temp11.append("")
    df2['FIL_SHAPE'] = temp11

    temp12=[]
    for name12 in df2['CTB_STEP_GAUGE']:
        if name12: #비어 있는지 여부를 확인
            name12 = [v for v in name12.split('-') if v]
            temp12.append(max([float(x) for x in name12]))
        else:
            temp12.append('')
    df2['CTB_STEP_GAUGE2'] = temp12

    # temp13_1 = []
    # temp13_2 = []
    # for name13 in df2['JLC_MATERIAL']:
    #     if name13:  # 비어 있는지 여부를 확인
    #         name13 = [v for v in name13.split(' ') if v]
    #         temp13_1.append(name13[0])
    #         temp13_2.append(name13[1].split('D')[0])
    #     else:
    #         temp13_1.append('')
    #         temp13_2.append('')
    # df2['JLC_MATERIAL_1'] = temp13_1
    # df2['JLC_MATERIAL_2'] = temp13_2
    #
    # temp14_1 = []
    # temp14_2 = []
    # for name14 in df2['C01_MATERIAL']:
    #     if name14:  # 비어 있는지 여부를 확인
    #         name14 = [v for v in name14.split(' ') if v]
    #         print(name14)
    #         temp14_1.append(name14[0])
    #         temp14_2.append(name14[1].split('D')[0])
    #     else:
    #         temp14_1.append('')
    #         temp14_2.append('')
    # df2['C01_MATERIAL_1'] = temp14_1
    # df2['C01_MATERIAL_2'] = temp14_2

    return df2

#TEST LOAD가 없는 경우
def Change2(df2):
    # 불필요한 문자 제거하여 >> C01 list로 만들고 >> Dataflame의 열을 교체하는 작업
    temp1=[]
    for name1 in df2['C01_MATERIAL']:
        temp1.append(name1.split('(')[0])
    df2['C01_MATERIAL'] = temp1

    # 일부 에러가 발생 ? 일단 제외하고 사용
    temp2 = []
    i = 0
    for name2 in df2['JLC_MATERIAL']:
        if name2 is not None:
            temp2.append(name2.split('(')[0])
        else:
            if df2['JEC_MATERIAL'][i] is not None:
                temp2.append(df2['JEC_MATERIAL'][i])
            else:
                temp2.append(df2['JFC_MATERIAL'][i])
        i = i + 1
    df2['JLC_MATERIAL'] = temp2

    temp3=[]
    temp4=[]
    for name3 in df2['TUH_1_2']:
        temp3.append(name3.split('-')[0])
        temp4.append(name3.split('-')[1])
    df2['TUH_1'] = temp3
    df2['TUH_2'] = temp4

    temp5=[]
    for name5 in df2['BT1_MATERIAL']:
        # temp5.append(name5.replace('?','by').replace('횞','by').replace('(','_').replace(')','_').replace('&OC',''))
        a1 = name5[1]
        a2 = name5.replace(a1, "by")
        temp5.append(a2.replace('(', '_').replace(')', '_').replace('&OC', ''))
    df2['BT1_MATERIAL'] = temp5

    temp6=[]
    for name6 in df2['SUT_STEP_GAUGE']:
        name6 = [v for v in name6.split('-') if v]
        temp6.append(sorted([float(x) for x in name6])[len(name6) // 2])
    df2['SUT_STEP_GAUGE2'] = temp6

    temp7=[]
    for name7 in df2['TRW_STEP_GAUGE']:
        if name7: #비어 있는지 여부를 확인
            name7 = [v for v in name7.split('-') if v]
            temp7.append(max([float(x) for x in name7]))
        else:
            temp7.append('')
    df2['TRW_STEP_GAUGE2'] = temp7

    temp8_top=[]
    temp8_bot=[]
    for name8 in df2['BSW_STEP_GAUGE']:
        name8 = [v for v in name8.split('-') if v]
        name8_1 = name8[:round(len(name8) * 0.5)]
        name8_2 = name8[round(len(name8) * 0.5):]
        temp8_top.append(max([float(x) for x in name8_1]))
        temp8_bot.append(max([float(x) for x in name8_2]))
    df2['BSW_STEP_GAUGE_TOP'] = temp8_top
    df2['BSW_STEP_GAUGE_BOT'] = temp8_bot

    temp9=[]
    for name9 in df2['RIC_STEP_GAUGE']:
        name9 = [v for v in name9.split('-') if v]
        temp9.append(max([float(x) for x in name9]))
    df2['RIC_STEP_GAUGE2'] = temp9

    temp10=[]
    for name10,name11,name12, name13 in zip(df2['BEAD_SINGLE_STRANDS'],df2['BEAD_LAY_UP'],df2['BEAD_STRAND'], df2['BEAD_LAYERS']):
        if name10.split('-')[0] == '0':
            if name11.split('-')[0] == '0':
                temp10.append(f"{name12}-{name13}")
                # print(f"{name12}-{name13}")
            else:
                temp10.append(f"{name11}")
                # print(name11)
        else:
            temp10.append(f"{name10}")
    df2['BEAD_SINGLE_STRANDS2'] = temp10

    temp11 = []
    for name11 in df2['FIL_EXTRUDED']:
        # print(name11[1])
        if name11 is None:
            temp11.append("")
        elif name11[1] == 'A':
            temp11.append("Regular")
        elif name11[1] == 'B':
            temp11.append("Regular")
        elif name11[1] == 'C':
            temp11.append("Thin")
        elif name11[1] == 'D':
            temp11.append("Thin")
        elif name11[1] == 'F':
            temp11.append("Thin")
        elif name11[1] == 'H':
            temp11.append("Regular")
        elif name11[1] == 'G':
            temp11.append("Thin")
        elif name11[1] == 'T':
            temp11.append("Thin")
        else:
            temp11.append("")
    df2['FIL_SHAPE'] = temp11

    temp12=[]
    for name12 in df2['CTB_STEP_GAUGE']:
        if name12: #비어 있는지 여부를 확인
            name12 = [v for v in name12.split('-') if v]
            temp12.append(max( [float(x) for x in name12] ))
        else:
            temp12.append('')
    df2['CTB_STEP_GAUGE2'] = temp12
    #
    # temp13_1 = []
    # temp13_2 = []
    # for name13 in df2['JLC_MATERIAL']:
    #     if name13:  # 비어 있는지 여부를 확인
    #         name13 = [v for v in name13.split(' ') if v]
    #         temp13_1.append(name13[0])
    #         temp13_2.append(name13[1].split('D')[0])
    #     else:
    #         temp13_1.append('')
    #         temp13_2.append('')
    # df2['JLC_MATERIAL_1'] = temp13_1
    # df2['JLC_MATERIAL_2'] = temp13_2
    #
    # temp14_1 = []
    # temp14_2 = []
    # for name14 in df2['C01_MATERIAL']:
    #     if name14:  # 비어 있는지 여부를 확인
    #         name14 = [v for v in name14.split(' ') if v]
    #         temp14_1.append(name14[0])
    #         temp14_2.append(name14[1].split('D')[0])
    #     else:
    #         temp14_1.append('')
    #         temp14_2.append('')
    # df2['C01_MATERIAL_1'] = temp14_1
    # df2['C01_MATERIAL_2'] = temp14_2
    # return df2

# Modal 스펙 변환에 사용
def Change3(df2):
    # 불필요한 문자 제거하여 >> C01 list로 만들고 >> Dataflame의 열을 교체하는 작업
    temp1=[]
    for name1 in df2['C01_MATERIAL']:
        temp1.append(name1.split('(')[0])
    df2['C01_MATERIAL'] = temp1

    temp2 = []
    i = 0
    for name2 in df2['JLC_MATERIAL']:
        if name2 is not None:
            temp2.append(name2.split('(')[0])
        else:
            if df2['JEC_MATERIAL'][i] is not None:
                temp2.append(df2['JEC_MATERIAL'][i])
            else:
                temp2.append(df2['JFC_MATERIAL'][i])
        i = i + 1
    df2['JLC_MATERIAL'] = temp2

    temp3=[]
    temp4=[]
    for name3 in df2['TUH_1_2']:
        temp3.append(name3.split('-')[0])
        temp4.append(name3.split('-')[1])
    df2['TUH_1'] = temp3
    df2['TUH_2'] = temp4

    temp5=[]
    for name5 in df2['BT1_MATERIAL']:
        # temp5.append(name5.replace('?','by').replace('횞','by').replace('(','_').replace(')','_').replace('&OC',''))
        a1 = name5[1]
        a2 = name5.replace(a1, "by")
        temp5.append(a2.replace('(', '_').replace(')', '_').replace('&OC', ''))
    df2['BT1_MATERIAL'] = temp5

    temp6=[]
    for name6 in df2['SUT_STEP_GAUGE']:
        name6 = [v for v in name6.split('-') if v]
        temp6.append(sorted([float(x) for x in name6])[len(name6) // 2])
    df2['SUT_STEP_GAUGE2'] = temp6

    temp7=[]
    for name7 in df2['TRW_STEP_GAUGE']:
        if name7: #비어 있는지 여부를 확인
            name7 = [v for v in name7.split('-') if v]
            temp7.append(max([float(x) for x in name7]))
        else:
            temp7.append('')
    df2['TRW_STEP_GAUGE2'] = temp7

    temp8_top=[]
    temp8_bot=[]
    for name8 in df2['BSW_STEP_GAUGE']:
        name8 = [v for v in name8.split('-') if v]
        name8_1 = name8[:round(len(name8) * 0.5)]
        name8_2 = name8[round(len(name8) * 0.5):]
        temp8_top.append(max([float(x) for x in name8_1]))
        temp8_bot.append(max([float(x) for x in name8_2]))
    df2['BSW_STEP_GAUGE_TOP'] = temp8_top
    df2['BSW_STEP_GAUGE_BOT'] = temp8_bot

    temp9=[]
    for name9 in df2['RIC_STEP_GAUGE']:
        if name9: #비어 있는지 여부를 확인
            name9 = [v for v in name9.split('-') if v]
            temp9.append(max([float(x) for x in name9]))
        else:
            temp9.append('')
    df2['RIC_STEP_GAUGE2'] = temp9

    temp10=[]
    for name10,name11,name12, name13 in zip(df2['BEAD_SINGLE_STRANDS'],df2['BEAD_LAY_UP'],df2['BEAD_STRAND'], df2['BEAD_LAYERS']):
        # print(name10)
        # print(name11)
        # print(name12)
        # print(name13)
        if name10.split('-')[0] == '0':
            if name11.split('-')[0] == '0':
                temp10.append(f"{name12}-{name13}")
                # print(f"{name12}-{name13}")
            else:
                temp10.append(f"{name11}")
                # print(name11)
        else:
            temp10.append(f"{name10}")
    df2['BEAD_SINGLE_STRANDS2'] = temp10

    temp11 = []
    for name11 in df2['FIL_EXTRUDED']:
        # print(name11[1])
        if name11 is None:
            temp11.append("")
        elif name11[1] == 'A':
            temp11.append("Regular")
        elif name11[1] == 'B':
            temp11.append("Regular")
        elif name11[1] == 'C':
            temp11.append("Thin")
        elif name11[1] == 'D':
            temp11.append("Thin")
        elif name11[1] == 'F':
            temp11.append("Thin")
        elif name11[1] == 'H':
            temp11.append("Regular")
        elif name11[1] == 'G':
            temp11.append("Thin")
        elif name11[1] == 'T':
            temp11.append("Thin")
        else:
            temp11.append("")
    df2['FIL_SHAPE'] = temp11

    temp12=[]
    for name12 in df2['CTB_STEP_GAUGE']:
        if name12: #비어 있는지 여부를 확인
            name12 = [v for v in name12.split('-') if v]
            temp12.append(max([float(x) for x in name12]))
        else:
            temp12.append('')
    df2['CTB_STEP_GAUGE2'] = temp12
    #
    # temp13_1 = []
    # temp13_2 = []
    # for name13 in df2['JLC_MATERIAL']:
    #     if name13:  # 비어 있는지 여부를 확인
    #         name13 = [v for v in name13.split(' ') if v]
    #         temp13_1.append(name13[0])
    #         temp13_2.append(name13[1].split('D')[0])
    #     else:
    #         temp13_1.append('')
    #         temp13_2.append('')
    # df2['JLC_MATERIAL_1'] = temp13_1
    # df2['JLC_MATERIAL_2'] = temp13_2
    #
    # temp14_1 = []
    # temp14_2 = []
    # for name14 in df2['C01_MATERIAL']:
    #     if name14:  # 비어 있는지 여부를 확인
    #         name14 = [v for v in name14.split(' ') if v]
    #         temp14_1.append(name14[0])
    #         temp14_2.append(name14[1].split('D')[0])
    #     else:
    #         temp14_1.append('')
    #         temp14_2.append('')
    # df2['C01_MATERIAL_1'] = temp14_1
    # df2['C01_MATERIAL_2'] = temp14_2

    return df2

# FORD 스펙 변환에 사용
def Change4(df2):
    # 불필요한 문자 제거하여 >> C01 list로 만들고 >> Dataflame의 열을 교체하는 작업
    temp1=[]
    for name1 in df2['C01_MATERIAL']:
        temp1.append(name1.split('(')[0])
    df2['C01_MATERIAL'] = temp1

    temp2 = []
    i = 0
    for name2 in df2['JLC_MATERIAL']:
        if name2 is not None:
            temp2.append(name2)
        else:
            if df2['JEC_MATERIAL'][i] is not None:
                temp2.append(df2['JEC_MATERIAL'][i])
            else:
                temp2.append(df2['JFC_MATERIAL'][i])
                print(df2['JFC_MATERIAL'][i])
        i = i + 1
    df2['JLC_MATERIAL'] = temp2

    temp3=[]
    temp4=[]
    for name3 in df2['TUH_1_2']:
        temp3.append(name3.split('-')[0])
        temp4.append(name3.split('-')[1])
    df2['TUH_1'] = temp3
    df2['TUH_2'] = temp4

    temp5=[]
    for name5 in df2['BT1_MATERIAL']:
        # temp5.append(name5.replace('?','by').replace('횞','by').replace('(','_').replace(')','_').replace('&OC',''))
        a1 = name5[1]
        a2 = name5.replace(a1, "by")
        temp5.append(a2.replace('(', '_').replace(')', '_').replace('&OC', ''))
    df2['BT1_MATERIAL'] = temp5

    temp6=[]
    for name6 in df2['SUT_STEP_GAUGE']:
        name6 = [v for v in name6.split('-') if v]
        temp6.append(sorted([float(x) for x in name6])[len(name6) // 2])
    df2['SUT_STEP_GAUGE2'] = temp6

    # temp7=[]
    # for name7 in df2['TRW_STEP_GAUGE']:
    #     if name7: #비어 있는지 여부를 확인
    #         name7 = [v for v in name7.split('-') if v]
    #         temp7.append(max([float(x) for x in name7]))
    #     else:
    #         temp7.append('')
    # df2['TRW_STEP_GAUGE2'] = temp7

    temp8_top=[]
    temp8_bot=[]
    for name8 in df2['BSW_STEP_GAUGE']:
        name8 = [v for v in name8.split('-') if v]
        name8_1 = name8[:round(len(name8) * 0.5)]
        name8_2 = name8[round(len(name8) * 0.5):]
        temp8_top.append(max([float(x) for x in name8_1]))
        temp8_bot.append(max([float(x) for x in name8_2]))
    df2['BSW_STEP_GAUGE_TOP'] = temp8_top
    df2['BSW_STEP_GAUGE_BOT'] = temp8_bot

    temp9=[]
    for name9 in df2['RIC_STEP_GAUGE']:
        name9 = [v for v in name9.split('-') if v]
        temp9.append(max([float(x) for x in name9]))
    df2['RIC_STEP_GAUGE2'] = temp9

    temp10=[]
    for name10,name11,name12, name13 in zip(df2['BEAD_SINGLE_STRANDS'],df2['BEAD_LAY_UP'],df2['BEAD_STRAND'], df2['BEAD_LAYERS']):
        # print(name10)
        # print(name11)
        # print(name12)
        # print(name13)
        if name10.split('-')[0] == '0':
            if name11.split('-')[0] == '0':
                temp10.append(f"{name12}-{name13}")
                # print(f"{name12}-{name13}")
            else:
                temp10.append(f"{name11}")
                # print(name11)
        else:
            temp10.append(f"{name10}")
    df2['BEAD_SINGLE_STRANDS2'] = temp10

    temp11 = []
    for name11 in df2['FIL_EXTRUDED']:
        # print(name11[1])
        if name11 is None:
            temp11.append("")
        elif name11[1] == 'A':
            temp11.append("Regular")
        elif name11[1] == 'B':
            temp11.append("Regular")
        elif name11[1] == 'C':
            temp11.append("Thin")
        elif name11[1] == 'D':
            temp11.append("Thin")
        elif name11[1] == 'F':
            temp11.append("Thin")
        elif name11[1] == 'H':
            temp11.append("Regular")
        elif name11[1] == 'G':
            temp11.append("Thin")
        elif name11[1] == 'T':
            temp11.append("Thin")
        else:
            temp11.append("Regular")
    df2['FIL_SHAPE'] = temp11

    temp12=[]
    for name12 in df2['CTB_STEP_GAUGE']:
        if name12: #비어 있는지 여부를 확인
            name12 = [v for v in name12.split('-') if v]
            temp12.append(max([float(x) for x in name12]))
        else:
            temp12.append('')
    df2['CTB_STEP_GAUGE2'] = temp12

    # temp13_1 = []
    # temp13_2 = []
    # for name13 in df2['JLC_MATERIAL']:
    #     if name13:  # 비어 있는지 여부를 확인
    #         name13 = [v for v in name13.split(' ') if v]
    #         temp13_1.append(name13[0])
    #         temp13_2.append(name13[1].split('D')[0])
    #     else:
    #         temp13_1.append('')
    #         temp13_2.append('')
    # df2['JLC_MATERIAL_1'] = temp13_1
    # df2['JLC_MATERIAL_2'] = temp13_2
    #
    # temp14_1 = []
    # temp14_2 = []
    # for name14 in df2['C01_MATERIAL']:
    #     if name14:  # 비어 있는지 여부를 확인
    #         name14 = [v for v in name14.split(' ') if v]
    #         print(name14)
    #         temp14_1.append(name14[0])
    #         temp14_2.append(name14[1].split('D')[0])
    #     else:
    #         temp14_1.append('')
    #         temp14_2.append('')
    # df2['C01_MATERIAL_1'] = temp14_1
    # df2['C01_MATERIAL_2'] = temp14_2

    return df2


