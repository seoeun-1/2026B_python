import pandas as pd
df = pd.read_csv('./project/Student_Performance.csv', encoding='utf-8-sig')
df.columns = ['study_hours', 'previous_score', 'extracurricular', 'sleep_hours', 'papers_practiced', 'performance_index']
df['extracurricular'] = df['extracurricular'].map({'Yes':1, 'No':0})
feature = ['study_hours', 'previous_score', 'extracurricular', 'sleep_hours', 'papers_practiced']
target = 'performance_index'
X = df[feature]
Y = df[target]

# 분할
from sklearn.model_selection import train_test_split, GridSearchCV
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

# 다항 특성 확장 표준화
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
poly = PolynomialFeatures(include_bias=False, degree=2)
poly.fit(X_train)
X_train_poly = poly.transform(X_train)
X_test_poly = poly.transform(X_test)

ss = StandardScaler()
ss.fit(X_train_poly)
X_train_scaled = ss.transform(X_train_poly)
X_test_scaled = ss.transform(X_test_poly)

# 결정계수, 학습
from sklearn.linear_model import LinearRegression, Ridge
model = LinearRegression()
model.fit(X_train_scaled, Y_train)

ridge = Ridge(alpha=1.0, random_state=42)
ridge.fit(X_train_scaled, Y_train)
print("Train R2:", ridge.score(X_train_scaled, Y_train))
print("Test R2:", ridge.score(X_test_scaled, Y_test))

from sklearn.pipeline import Pipeline
pipe_model = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge', Ridge(random_state=42))
])
pipe_model.fit(X_train, Y_train)

param_grid = {
    'poly__degree': [1, 2],
    'ridge__alpha': [0.01, 0.1, 1.0, 10.0, 100.0]
}

grid = GridSearchCV(
    estimator=pipe_model,
    param_grid=param_grid,
    scoring='r2',
    n_jobs=-1
)
grid.fit(X_train, Y_train)
best_model = grid.best_estimator_

from sklearn.metrics import r2_score
Y_pred = best_model.predict(X_test)
r2 = r2_score(Y_test, Y_pred)

# 저장 경로 수정: project.py와 같은 폴더의 artifacts
import joblib
from pathlib import Path

output = Path(__file__).resolve().parent / "artifacts"
output.mkdir(parents=True, exist_ok=True)

joblib.dump(best_model, output / "Student_Performance_pipe.pkl")
joblib.dump(r2, output / "Student_Performance_r2.pkl")