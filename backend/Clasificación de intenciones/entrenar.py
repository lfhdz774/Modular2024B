import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# Carga el archivo CSV con pandas
data = pd.read_csv(r'Clasificación de intenciones\intents.csv')
comandos = data['comando']
intenciones = data['intencion']


# Crear el pipeline
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(ngram_range=(1, 2))),
    ('classifier', LogisticRegression())
])


# Entrenar el modelo con los datos
pipeline.fit(comandos, intenciones)


# Guardar el modelo entrenado
joblib.dump(pipeline, r'Clasificación de intenciones\modelo_intenciones.pkl')
