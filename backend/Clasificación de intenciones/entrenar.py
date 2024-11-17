import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Cargar el archivo CSV con pandas
data = pd.read_csv('./intenciones.csv')
comandos = data['comando']
intenciones = data['intencion']

# Crear el pipeline
pipeline = Pipeline([
    ('vectorizer', CountVectorizer(ngram_range=(1, 2))),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Entrenar el modelo con los datos
pipeline.fit(comandos, intenciones)

# Guardar el modelo entrenado
joblib.dump(pipeline, 'modelo_intenciones.pkl')
print("Modelo de clasificación de intenciones guardado.")
