import pandas as pd
import pickle
from sklearn.neural_network import MLPRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import KFold, GridSearchCV

_DS_data = pickle.load(open('Z:\\_DATA_Traing\\DS\\_DS_data2.pkl', 'rb'))
df_test = _DS_data["2.df_test"]
df_train = _DS_data["2.df_train"]
Xtrain = _DS_data["2.Xtrain"]
Xtest = _DS_data["2.Xtest"]
xtrain = _DS_data["2.xtrain"]
xtest = _DS_data["2.xtest"]
target = _DS_data["1.Target list"][0]


xall = pd.concat([xtest, xtrain], axis=0).reset_index(drop=True)
Xall = pd.concat([Xtest, Xtrain], axis=0).reset_index(drop=True)
yall = pd.concat([df_test[target], df_train[target]], axis=0).reset_index(drop=True)
df_all = pd.concat([df_test, df_train], axis=0).reset_index(drop=True)


################################### 2021 / 5/6 추가 내용
df_all_X = df_all.iloc[:,:-8]
df_all_Y = df_all[_DS_data["1.Target list"]]
######################################################

# NN 방법
model=MLPRegressor()
param_grid = {}
param_grid['hidden_layer_sizes'] = [1000]
param_grid['activation'] = ['relu']
param_grid['solver'] = ['adam']
param_grid['alpha'] = [0.0001] # 기본값 0.0001
param_grid['max_iter'] = [1500] # 기본값 200
param_grid['tol'] = [0.001] #기본값 0.0001
param_grid['batch_size'] = ['auto', 64] # 기본값 ’auto’
# param_grid['learning_rate_init'] = [0.001, 0.0001] # default=’constant’
cv=KFold(n_splits=5, shuffle=True, random_state=0)
met_grid= ['r2', 'neg_mean_absolute_error'] #The metric codes from sklearn
# gcv=GridSearchCV(model, param_grid=param_grid, cv=cv, scoring=met_grid, refit='r2', n_jobs=-1)
gcv=GridSearchCV(model, param_grid=param_grid, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1)
gcv.fit(xall,yall)
print('final params', gcv.best_params_)   # 최적의 파라미터 값 출력
# 예측방법 결과 확인
mlp_bestmodel = gcv.best_estimator_  # 최적의 파라미터로 모델 생성
df_all["_PRED(NN)"] = mlp_bestmodel.predict(xall)
df_all.to_csv("Z:\\_DATA_Traing\\DS\\Prediction.csv", mode='w')

# XGB 방법
model2=XGBRegressor()
param_grid2 = {}
param_grid2['booster'] = ['gbtree']
param_grid2['min_child_weight'] = [5, 10]
param_grid2['max_depth'] = [6]
# param_grid2['gamma '] = [0,1,2]
param_grid2['nthread'] = [4]
param_grid2['colsample_bytree'] = [0.5, 0.8]
param_grid2['colsample_bylevel'] = [0.9]
# param_grid2['objective'] = ['reg']
# param_grid2['random_state '] = [0]
gcv2=GridSearchCV(model2, param_grid=param_grid2, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1)
gcv2.fit(Xall,yall)
print('final params', gcv2.best_params_)   # 최적의 파라미터 값 출력
# 예측방법 결과 확인
xgv_bestmodel = gcv2.best_estimator_  # 최적의 파라미터로 모델 생성
df_all["_PRED(XGB)"] = xgv_bestmodel.predict(Xall)
df_all.to_csv("Z:\\_DATA_Traing\\DS\\Prediction.csv", mode='w')

##########################################################################################
outlier_limit = int(input('Prediction.csv를 확인하고 Outlier를 제거할 abs_error값 을 적어 주세요 : '))
# 에러 5 이하를 filter 했음.
# 예측 결과를 확인하고, outlier 제거
df_all["abs_error"] = (df_all["_PRED(NN)"]
                       + df_all["_PRED(XGB)"]
                       - df_all["DYNAMINC_STIFFNESS"]*2).abs()
df_all_removed_outlier = df_all[df_all["abs_error"] < outlier_limit]

del(df_all_removed_outlier["abs_error"])
del(df_all_removed_outlier["_PRED(NN)"])
del(df_all_removed_outlier["_PRED(XGB)"])

_DS_data['3.MLP_Best_Model'] = mlp_bestmodel
_DS_data['3.MLP_Best_Model_params'] = gcv.best_params_
_DS_data['3.XGV_Best_Model'] = xgv_bestmodel
_DS_data['3.XGV_Best_Model_params'] = gcv2.best_params_
_DS_data['3.Input Data (Removed Outlier)'] = df_all_removed_outlier

pickle.dump(_DS_data, open('Z:\_DATA_Traing\DS\_DS_data3.pkl', 'wb'))
