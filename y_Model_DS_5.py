import pickle
import pandas as pd
# from sklearn.preprocessing import RobustScaler
# import joblib
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler

_DS_data = pickle.load(open('Z:\\_DATA_Traing\\DS\\_DS_data4.pkl', 'rb'))
df_test = _DS_data["4.df_test"]
df_train = _DS_data["4.df_train"]
Xtrain = _DS_data["4.Xtrain"]
Xtest = _DS_data["4.Xtest"]
xtrain = _DS_data["4.xtrain"]
xtest = _DS_data["4.xtest"]
Xall = _DS_data["4.Xall"]
xall = _DS_data["4.xall"]
scaler = _DS_data["4.Scaler (with train set data)"]
scaler_alldata = _DS_data["4.Scaler (with all data)"]
categoricals = _DS_data["4.Category"]
Xtrain1 = _DS_data["4.Input_Sample for New Prediction"]
targets = _DS_data["1.Target list"]

# yall = pd.concat([df_test['DYNAMINC_STIFFNESS'], df_train['DYNAMINC_STIFFNESS']], axis=0).reset_index(drop=True)
yall = pd.concat([df_test[targets], df_train[targets]], axis=0).reset_index(drop=True)
df_all = pd.concat([df_test, df_train], axis=0).reset_index(drop=True)

score=[]
for target in targets:
    Ytrain = df_train[target]  # Ytrain << 예측 모델의 출력값
    reg_nn = MLPRegressor(activation='relu',
                          solver='adam',
                          hidden_layer_sizes=(1000,),
                          max_iter=1500,
                          batch_size=64,
                          alpha=0.0001,
                          tol=0.0001).fit(xtrain, Ytrain)
    reg_XGV = XGBRegressor(booster='gbtree',
                           min_child_weight = 5,
                           max_depth = 6,
                           nthread = 4,
                           colsample_bytree = 0.5,
                           colsample_bylevel = 0.9).fit(Xtrain, Ytrain)
    reg_RandF = RandomForestRegressor(  max_depth = 6,
                                        n_estimators = 800,
                                        min_samples_split = 3,
                                        n_jobs=-1).fit(Xtrain, Ytrain)

    # df_train[f"{target}_PRED"] = reg_nn.predict(xtrain) * 0.5 + reg_RandF.predict(Xtrain) * 0.5
    df_train[f"{target}_PRED_NN"] = reg_nn.predict(xtrain)
    df_train[f"{target}_PRED_XGV"] = reg_XGV.predict(Xtrain)
    df_train[f"{target}_PRED_Rand"] = reg_RandF.predict(Xtrain)
    # joblib.dump(reg_nn, 'Z:\\_DATA_Traing\\DS\\saved_model_nn' + target + '.pkl')  # 모델을 파일로 저장하는 방법
    # joblib.dump(reg_XGV, 'Z:\\_DATA_Traing\\DS\\saved_model_nn' + target + '.pkl')  # 모델을 파일로 저장하는 방법
    # joblib.dump(reg_RandF, 'Z:\\_DATA_Traing\\DS\\saved_model_RandF' + target + '.pkl')

    Ytest = df_test[target]
    # df_test[f"{target}_PRED"] = reg_nn.predict(xtest) * 0.5 + reg_RandF.predict(Xtest) * 0.5
    df_test[f"{target}_PRED_NN"] = reg_nn.predict(xtest)
    df_test[f"{target}_PRED_XGV"] = reg_XGV.predict(Xtest)
    df_test[f"{target}_PRED_Rand"] = reg_RandF.predict(Xtest)

    score.append(format(reg_nn.score(xtrain, Ytrain),"10.2f"))
    score.append(format(reg_nn.score(xtest, Ytest), "10.2f"))
    score.append(format(reg_XGV.score(Xtrain, Ytrain), "10.2f"))
    score.append(format(reg_XGV.score(Xtest, Ytest), "10.2f"))
    score.append(format(reg_RandF.score(Xtrain, Ytrain), "10.2f"))
    score.append(format(reg_RandF.score(Xtest, Ytest), "10.2f"))

    print(f"R^2 Score of {target}:")
    print("NN:     train         test    XGV:  train         test  RandF: train         test")
    print(score)
    score=[]

df_train.to_csv("Z:\\_DATA_Traing\\DS\\Prediction_Train_Set.csv", mode='w')
df_test.to_csv("Z:\\_DATA_Traing\\DS\\Prediction_Test_Set.csv", mode='w')


print('최종 모델을 만들려면 1을 입력하세요')
print('Fitting을 더 하려면 0을 입력하세요')
decision_num = int(input('최종 모델을 만들건가요? : '))
if decision_num == 1:
    for target in targets:
        reg_nn1 = MLPRegressor(activation='relu',
                              solver='adam',
                              hidden_layer_sizes=(1000,),
                              max_iter=1500,
                              batch_size=64,
                              alpha=0.0001,
                              tol=0.0001).fit(xall,yall[target])
        reg_XGV1 = XGBRegressor(booster='gbtree',
                               min_child_weight=5,
                               max_depth=6,
                               nthread=4,
                               colsample_bytree=0.5,
                               colsample_bylevel=0.9).fit(Xall, yall[target])
        reg_RandF1 = RandomForestRegressor(max_depth=6,
                                          n_estimators=800,
                                          min_samples_split=3,
                                          n_jobs=-1).fit(Xall, yall[target])

        df_all[f"{target}_PRED_NN"] = reg_nn1.predict(xall)
        df_all[f"{target}_PRED_XGV"] = reg_XGV1.predict(Xall)
        df_all[f"{target}_PRED_RandF"] = reg_RandF1.predict(Xall)
        df_all.to_csv("Z:\\_DATA_Traing\\DS\\Prediction_Final.csv", mode='w')

        _DS_data[f"5.FinalModel for MLP(NN)_{target}"] = reg_nn1
        _DS_data[f"5.FinalModel for XGV_{target}"] = reg_XGV1
        _DS_data[f"5.FinalModel for RandF_{target}"] = reg_RandF1
        pickle.dump(_DS_data, open('Z:\_DATA_Traing\DS\_DS_data5.pkl', 'wb'))
    print('Training Finished!')
else:
    print('Training Again - more Fitting needs')

samples = _DS_data['4.Input_Sample for New Prediction']
samples = samples.drop(1,0)
df_feat_imp = pd.DataFrame()
for target in targets:
    df_feat_imp[f"XGV_{target}"] = _DS_data[f"5.FinalModel for XGV_{target}"].feature_importances_.tolist()
    df_feat_imp[f"RandF_{target}"] = _DS_data[f"5.FinalModel for RandF_{target}"].feature_importances_.tolist()
df_feat_imp.index = samples.columns.values.tolist()
df_feat_imp.to_csv("Z:\\_DATA_Traing\\DS\\Feature_Importances_.csv", mode='w')

df_all2 = pd.concat([_DS_data["4.df_train"], _DS_data["4.df_test"]], axis=0).reset_index(drop=True)
_DS_data["5.Input Data"] = df_all2
pickle.dump(_DS_data, open('Z:\_DATA_Traing\DS\_DS_data5.pkl', 'wb'))