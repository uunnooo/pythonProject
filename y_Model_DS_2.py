import pickle
import pandas as pd
import random
from sklearn.preprocessing import RobustScaler

class ohe():  # One Hot Encording (OHE)
    def __init__(self, dfs, use_cols):
        self.dfs = dfs
        self.use_cols = use_cols

    def scale_columns(self):
        return self.dfs[0][self.use_cols].select_dtypes(exclude='object').columns.tolist()

    def dummify(self, target):
        sizes = [df.shape[0] for df in self.dfs]

        df_dummies = self.dfs[0].copy()
        for df in self.dfs[1:]:
            df_dummies = df_dummies.append(df)
        df_dummies = pd.get_dummies(df_dummies[self.use_cols + [target]])

        dummy_dfs = []
        for i, size in enumerate(sizes):
            if -sum(sizes[i + 1:]) != 0:
                dummy_dfs.append(df_dummies.iloc[-sum(sizes[i:]):-sum(sizes[i + 1:]), :].reset_index(drop=True))
            else:
                dummy_dfs.append(df_dummies.iloc[-sum(sizes[i:]):, :].reset_index(drop=True))

        return dummy_dfs

_DS_data = pickle.load(open('Z:\\_DATA_Traing\\DS\\_DS_data.pkl', 'rb'))
targets = _DS_data['1.Target list']
use_cols = _DS_data['1.Input Properties list']
scale_cols = _DS_data['1.Input Properties list (number)']
df8 = _DS_data['1.Input Data']

# Training Set와 Test Set를 구분
test_samples = random.sample(df8['SPEC_NO'].unique().tolist(),int(df8.shape[0]*0.2))
train_samples = [s for s in df8['SPEC_NO'].unique().tolist() if s not in test_samples]

df_test = df8[df8['SPEC_NO'].isin(test_samples)].reset_index(drop = True).copy()
df_train = df8[df8['SPEC_NO'].isin(train_samples)].reset_index(drop = True).copy()

df_ohe = ohe([df_train, df_test],use_cols) #문자열은 one hot encording을 적용하고
target = targets[0]
[dummy_train, dummy_test] = df_ohe.dummify(target)  # one-hot-encording 이 적용된 dummy data를 만들고
Xtrain = dummy_train.drop(target, axis=1)  # dummy_train에서 target열 (axis=1이면 열을 제거) 을 제거한 후, Xtrain을 만들고
Xtest = dummy_test.drop(target, axis=1)

Xtrain1 = Xtrain.iloc[:2,:] # Xtrain1 : OHE이 적용된 Data Sample 형식

#############################################################################################
# Normalize하는 작업
xtrain = Xtrain.copy()
xtest = Xtest.copy()
scaler = RobustScaler()
xtrain[scale_cols] = scaler.fit_transform(Xtrain[scale_cols])
xtest[scale_cols] = scaler.transform(Xtest[scale_cols])

df9=df8[use_cols]
categoricals = {}
for col in df9.select_dtypes(include = 'object').columns:
    categoricals[col] = df9[col].unique().tolist()
df_categoricals = pd.DataFrame.from_dict(categoricals, orient='index')

_DS_data["2.df_test"] = df_test
_DS_data["2.df_train"] = df_train
_DS_data["2.Xtrain"] = Xtrain
_DS_data["2.Xtest"] = Xtest
_DS_data["2.xtrain"] = xtrain
_DS_data["2.xtest"] = xtest
_DS_data["2.Scaler"] = scaler
_DS_data["2.Category"] = categoricals
_DS_data["2.Input_Sample for New Prediction"] = Xtrain1

pickle.dump(_DS_data, open('Z:\_DATA_Traing\DS\_DS_data2.pkl', 'wb'))