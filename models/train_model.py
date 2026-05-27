from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

# ==========================================
# TRAIN MODEL
# ==========================================
def train_models(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    rf = RandomForestClassifier(
        n_estimators=50,
        max_depth=6
    )

    xgb = XGBClassifier(
        n_estimators=50,
        max_depth=4,
        eval_metric='logloss'
    )

    rf.fit(X_train_scaled, y_train)
    xgb.fit(X_train_scaled, y_train)

    return rf, xgb, scaler, X_test_scaled, y_test