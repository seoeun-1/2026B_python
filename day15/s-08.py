# 범주형(문자) 특성 갖는 학습 방법
# 1) 실습에 필요한 펭귄 계측 데이터
import seaborn as sns
df = sns.load_dataset('penguins')
df.info()
# 2) 전처리: 결측 행 제외
df = df.dropna().reset_index(drop=True)
df.info()

X = df.drop(columns=['species'])
Y = df['species'] # 3개 클래스: Adelie, Chinstrap, Gentoo

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)
num_features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
cat_features = ['island', 'sex']

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
# OneHotEncoder: 범주형 자료들을 0과 1 표현                         
preprocessor = ColumnTransformer(
  transformers=[
    ('num', StandardScaler(), num_features),
    ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_features)
  ]
)
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression


pipe = Pipeline([

  ('preprocessor', preprocessor),

  ('model', LogisticRegression(C=1.0, max_iter=1000, random_state=42))

])

pipe.fit(X_train, Y_train)
Y_pred = pipe.predict(X_test)
Y_pred_proba = pipe.predict_proba(X_test)

# 파이프라인 내부의 LogisticRegression 모델 객체에서 classes_ 속성 추출
classes = pipe.named_steps['model'].classes_

import numpy as np
print("--- [Step 3-1] 모델 기본 예측 결과 ---")
print("클래스 순서:", classes)
print("예측 품종(3개):", Y_pred[:3])
print("예측 확률 배열(3개):\n", np.round(Y_pred_proba[:3], decimals=3))
print(f"첫 번째 샘플 확정 품종: {classes[np.argmax(Y_pred_proba[0])]}")

from sklearn.metrics import f1_score
f1 = f1_score(Y_test, Y_pred, average='macro')
print(f"\nF1-Macro 점수: {f1:.4f}")