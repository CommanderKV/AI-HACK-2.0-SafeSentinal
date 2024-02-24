def test_model(model, X, y):
    y_pred = model.predict(X)
    print(classification_report(y, y_pred))