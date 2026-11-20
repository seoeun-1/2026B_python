# PythonML Practice5: 다중 분류
# 데이터셋: seaborn diamonds dataset (다이아몬드 세공 품질 'cut' 다중 분류)
#
# [단계 1] 데이터 로드 및 전처리, 독립/종속 변수 분리
# 1. seaborn의 'diamonds' 데이터셋을 로드하세요. (sns.load_dataset('diamonds'))
# 2. 실습 연산 효율성을 위해 5,000개 샘플을 무작위 추출하세요. (df = df.sample(n=5000, random_state=42).reset_index(drop=True))
# 3. 다이아몬드 커팅 품질('cut': Fair, Good, Very Good, Premium, Ideal)을 종속 변수 Y로, 나머지 컬럼을 독립 변수 X로 분리하세요.
#
# [단계 2] 훈련용 / 테스트용 데이터 분리
# train_test_split을 사용하여 8:2 비율(test_size=0.2)로 분리하고, 5개 클래스 비율 유지를 위해 stratify=Y, 재현성을 위해 random_state=42로 설정하세요.
#
# [단계 3] ColumnTransformer를 활용한 복합 전처리 구성
# 1. 수치형 피처: ['carat', 'depth', 'table', 'price', 'x', 'y', 'z'] -> StandardScaler를 적용하세요.
# 2. 범주형 피처: ['color', 'clarity'] -> OneHotEncoder(drop='first', sparse_output=False )를 적용하세요.
# 3. 위 두 변환기를 ColumnTransformer로 묶어 'preprocessor' 객체를 정의하세요.
#
# [단계 4] 파이프라인(Pipeline) 구축 및 기본 모델 학습
# 1. Pipeline을 생성하여 [단계 3]의 'preprocessor'와 LogisticRegression(max_iter=1000, random_state=42)을 단일 워크플로우로 연결하세요.
# 2. X_train 원본(DataFrame)과 Y_train을 파이프라인에 직접 투입하여 모델을 학습(fit)시키세요.
#
# [단계 5] 모델 다중 분류 지표 산출 및 혼동 행렬 시각화
# 1. 테스트 세트(X_test)에 대한 예측 레이블(Y_pred) 및 예측 확률(Y_pred_proba)을 생성하세요.
# 2. 파이프라인 내부 분류기의 클래스 순서(classes_)를 확인하고, 다중 분류 4대 평가 지표를 산출하세요:
#    - 정확도 (accuracy_score) 정밀도 (precision_score, average='macro') 재현율 (recall_score, average='macro') F1 점수 (f1_score, average='macro')
# 3. ConfusionMatrixDisplay.from_predictions를 활용해 혼동 행렬을 시각화하세요.
#
# [단계 6] GridSearchCV 기반 하이퍼파라미터 튜닝
# 1. 규제 강도 탐색 그리드를 정의하세요: {'model__C': [0.01, 0.1, 1.0, 10.0]}
# 2. StratifiedKFold(n_splits=5, shuffle=True, random_state=42) 교차 검증 객체를 생성하세요.
# 3. scoring='f1_macro'를 기준으로 GridSearchCV를 수행하여 최적 파라미터와 최고 점수를 출력하세요.
# 4. 최적 추정기(best_estimator_)로 X_test를 평가하고 classification_report를 출력하세요.
#
# [단계 7] 파이프라인 직렬화(저장/불러오기) 및 신규 원본 데이터 실시간 추론
# 1. joblib.dump를 사용하여 최적화된 파이프라인 전체를 './diamond_pipeline.pkl'로 저장하세요.
# 2. joblib.load로 저장된 파이프라인을 다시 불러오세요.
# 3. 스케일링/인코딩을 거치지 않은 원본 형태의 임의 다이아몬드 샘플(DataFrame)을 생성하세요: (예: carat=0.7, color='E', clarity='SI1', depth=61.5, table=55.0, price=3000, x=5.7, y=5.75, z=3.5)
# 4. 불러온 파이프라인의 predict() 및 predict_proba()에 직접 전달하여 예측 커팅 등급(cut)과 가장 높은 확신도(최대 확률 %)를 출력하세요.

import pandas as pd
import seaborn as sns
import numpy as np

df = sns.load_dataset('diamonds')
df = df.sample(n=5000, random_state=42).reset_index(drop=True)

X = df.drop(columns=['cut'])
Y = df['cut']

from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42, stratify=Y
)

num_features = ['carat', 'depth', 'table', 'price', 'x', 'y', 'z']
cat_features = ['color', 'clarity']

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
    ]
)

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', LogisticRegression(max_iter=1000, random_state=42))
])

pipeline.fit(X_train, Y_train)
Y_pred = pipeline.predict(X_test)
Y_pred_proba = pipeline.predict_proba(X_test)

print(Y_pred[:3])
print(pipeline.named_steps['model'].classes_)
print(np.round(Y_pred_proba[:3], 3))

from sklearn.metrics import accuracy_score

print('정확도:', accuracy_score(Y_test, Y_pred))

from sklearn.metrics import precision_score

print('정밀도:', precision_score(
    Y_test, Y_pred, average='macro', zero_division=0
))

from sklearn.metrics import recall_score

print('재현율:', recall_score(
    Y_test, Y_pred, average='macro', zero_division=0
))

from sklearn.metrics import f1_score

print('F1 점수:', f1_score(
    Y_test, Y_pred, average='macro', zero_division=0
))

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_predictions(
    Y_test, Y_pred, xticks_rotation=45
)
plt.tight_layout()
plt.show()

param_grid = {
    'model__C': [0.01, 0.1, 1.0, 10.0]
}

from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(
    n_splits=5, shuffle=True, random_state=42
)

from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(
    pipeline,
    param_grid,
    cv=cv,
    scoring='f1_macro',
    n_jobs=-1
)

grid.fit(X_train, Y_train)

print('최적 파라미터:', grid.best_params_)
print('최고 교차 검증 F1 점수:', grid.best_score_)

best_pipeline = grid.best_estimator_
Y_pred = best_pipeline.predict(X_test)

from sklearn.metrics import classification_report

print(classification_report(Y_test, Y_pred, zero_division=0))

import joblib

joblib.dump(best_pipeline, './diamond_pipeline.pkl')
loaded_pipeline = joblib.load('./diamond_pipeline.pkl')

X_new = pd.DataFrame({
    'carat': [0.7],
    'color': ['E'],
    'clarity': ['SI1'],
    'depth': [61.5],
    'table': [55.0],
    'price': [3000],
    'x': [5.7],
    'y': [5.75],
    'z': [3.5]
})

Y_new_pred = loaded_pipeline.predict(X_new)
Y_new_pred_proba = loaded_pipeline.predict_proba(X_new)

print('예측 커팅 등급:', Y_new_pred[0])
print(f'최대 예측 확률: {Y_new_pred_proba[0].max() * 100:.2f}%')