import pickle
import numpy as np
import sklearn

with open('models/ml_dnf.dat', 'rb') as f:
    model_dnf = pickle.load(f)

with open('models/ml_time.dat', 'rb') as f:
    model_time = pickle.load(f)

with open('models/ml_pos.dat', 'rb') as f:
    model = pickle.load(f)
def dnf(inputs):
    X_dnf = np.array([[inputs['rider_number'], inputs['air_temp'],
                       inputs['track_cond'], inputs['humidity'], inputs['season'], inputs['race_id']]])
    dnf_pred = model_dnf.predict(X_dnf)[0]
    return dnf_pred
def time(inputs):
    dnf_input = dnf(inputs)
    X_time = np.array([[inputs['rider_number'], inputs['air_temp'],
                        inputs['track_cond'], inputs['humidity'], inputs['season'], inputs['race_id'], dnf_input]])
    time_pred = model_time.predict(X_time)[0]
    return time_pred
def prediction(inputs):
    dnf_input = dnf(inputs)

    time_input = time(inputs)

    X_pos = np.array([[inputs['rider_number'], inputs['air_temp'],
                       inputs['track_cond'], inputs['humidity'], inputs['season'], inputs['race_id'],dnf_input,time_input]])
    position_pred = model.predict(X_pos)[0]

    return position_pred
x={
    'rider_number': 93,
    'air_temp': 35,
    'track_cond': 1,
    'humidity': 0.31,
    'season': 2025,
    'race_id': 1
}
dnf_i = dnf(x)
x["dnf"] = dnf_i
time_i = time(x)
x["time_pred"] = time_i
print(prediction(x))

