import json
import spacy
from spacy.tokens import DocBin
from spacy.util import minibatch, compounding
from pathlib import Path
import random

# Cargar los datos de entrenamiento desde 'training_data.json'
with open('training_data.json', 'r', encoding='utf-8') as f:
    TRAIN_DATA = json.load(f)

# Crear un modelo en blanco para español
nlp = spacy.blank("es")

# Añadir el componente NER al pipeline si no existe
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Añadir las etiquetas de entidad personalizadas
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

# Configurar el optimizador
optimizer = nlp.initialize()

# Número de iteraciones
n_iter = 30

for itn in range(n_iter):
    print(f"Iteración {itn + 1}")
    random.shuffle(TRAIN_DATA)
    losses = {}

    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        examples = []
        for text, annotation in zip(texts, annotations):
            doc = nlp.make_doc(text)
            example = spacy.training.Example.from_dict(doc, annotation)
            examples.append(example)
        nlp.update(examples, sgd=optimizer, drop=0.35, losses=losses)
    print("Pérdida:", losses)

# Guardar el modelo entrenado
output_dir = Path("modelo_ner")
nlp.to_disk(output_dir)
print("Modelo de NER guardado en", output_dir)
