import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Task 1: Decision Tree
class DecisionTreeModel:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.model = DecisionTreeClassifier(max_depth=self.max_depth, random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, y_test, y_pred):
        acc = accuracy_score(y_test, y_pred)
        # Using pos_label='Y' since your target column is 'Y' and 'N'
        prec = precision_score(y_test, y_pred, pos_label='Y', zero_division=0)
        rec = recall_score(y_test, y_pred, pos_label='Y', zero_division=0)
        return acc, prec, rec

# Task 2: Random Forest
class RandomForestModel:
    def __init__(self, n_estimators=100):
        self.n_estimators = n_estimators
        self.model = RandomForestClassifier(n_estimators=self.n_estimators, random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, y_test, y_pred):
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, pos_label='Y', zero_division=0)
        rec = recall_score(y_test, y_pred, pos_label='Y', zero_division=0)
        return acc, prec, rec


def preprocess(df):
    if "Loan_ID" in df.columns:
        df = df.drop("Loan_ID", axis=1)

    df = df.fillna(df.mode().iloc[0])
    
    # FIX: Temporarily remove Loan_Status so it doesn't get ruined by get_dummies
    target = None
    if "Loan_Status" in df.columns:
        target = df["Loan_Status"]
        df = df.drop("Loan_Status", axis=1)

    df = pd.get_dummies(df)
    
    # Put Loan_Status back into the dataframe
    if target is not None:
        df["Loan_Status"] = target

    return df


def main():
    # LOCAL PATHS: Use the exact names of the files you uploaded 
    # Make sure these CSV files are in the SAME folder as this script.
    train_path = "train_u6lujuX_CVtuZ9i.csv"
    test_path  = "test_Y3wMUE5_7gLdaTN.csv"

    try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
    except FileNotFoundError:
        print("Error: Files not found. Ensure the CSV files are in the same directory as this code.")
        return

    train_df = preprocess(train_df)
    test_df = preprocess(test_df)

    # Align columns (VERY IMPORTANT)
    # We must align only the features, so we don't accidentally fill target columns with 0
    train_target = train_df["Loan_Status"]
    train_features = train_df.drop("Loan_Status", axis=1)
    
    # Check if test dataset actually has 'Loan_Status'. 
    # (Often in these datasets, the test.csv doesn't have the target column!)
    has_target = "Loan_Status" in test_df.columns
    if has_target:
        test_target = test_df["Loan_Status"]
        test_features = test_df.drop("Loan_Status", axis=1)
    else:
        test_features = test_df

    # Align
    train_features, test_features = train_features.align(test_features, join="left", axis=1, fill_value=0)

    X_train = train_features
    y_train = train_target
    X_test = test_features

    # If the test set doesn't have a target column, we can't evaluate accuracy
    if not has_target:
        print("\nNote: The 'test.csv' file does not contain a 'Loan_Status' column.")
        print("We can train the model and make predictions, but we cannot evaluate Accuracy/Precision/Recall.")
        return

    y_test = test_target

    print("\nDecision Tree Results\n")
    depths = [2, 5, None]

    for d in depths:
        model = DecisionTreeModel(max_depth=d)
        model.train(X_train, y_train)
        preds = model.predict(X_test)
        acc, prec, rec = model.evaluate(y_test, preds)

        print(f"Depth = {d}")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print("-------------------")

    print("\nRandom Forest Results\n")
    estimators = [10, 50, 100]

    for n in estimators:
        model = RandomForestModel(n_estimators=n)
        model.train(X_train, y_train)
        preds = model.predict(X_test)
        acc, prec, rec = model.evaluate(y_test, preds)

        print(f"n_estimators = {n}")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print("-------------------")

# Ensures main() runs when you execute the file
if __name__ == "__main__":
    main()