import pandas as pd
import joblib

class Service:
    def __init__(self):
        self.model = joblib.load('./project/artifacts/Student_Performance_pipe.pkl')
        self.r2 = joblib.load('./project/artifacts/Student_Performance_r2.pkl')

    def predict(self, data):
        sample = pd.DataFrame([{
            'study_hours': int(data['study_hours']),
            'previous_score': int(data['previous_score']),
            'extracurricular': int(data['extracurricular']),
            'sleep_hours': int(data['sleep_hours']),
            'papers_practiced': int(data['papers_practiced'])
        }])

        pred = self.model.predict(sample)[0]

        return {
            'prediction': round(float(pred), 2),
            'r2': round(float(self.r2), 4)
        }

service = Service()