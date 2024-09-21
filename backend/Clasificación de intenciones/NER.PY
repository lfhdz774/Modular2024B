import spacy
from spacy.tokens import DocBin
from spacy.util import minibatch, compounding
import random

TRAIN_DATA = [
    # Comandos de "crear_usuario"
    ("Necesito crear un usuario nuevo", {"entities": []}),
    ("Agregar acceso para Pedro", {"entities": [(18, 23, "USERNAME")]}),
    ("Registrar un nuevo usuario llamado Luis", {"entities": [(34, 38, "USERNAME")]}),
    ("Crear cuenta para Ana María", {"entities": [(17, 26, "USERNAME")]}),
    ("Crea un usuario llamado Raul", {"entities": [(27, 31, "USERNAME")]}),
    ("Genera un usuario que se llame Diego", {"entities": [(35, 40, "USERNAME")]}),
    ("Ayúdame generando un nuevo usuario", {"entities": []}),
    ("Necesito que crees un nuevo acceso", {"entities": []}),
    ("Genera un nuevo acceso", {"entities": []}),
    ("acceso nuevo", {"entities": []}),
    ("nuevo acceso", {"entities": []}),
    ("crea un nuevo usuario llamado Pedro", {"entities": [(30, 35, "USERNAME")]}),
    ("Genera un acceso", {"entities": []}),
    ("Registra un nuevo acceso llamado XxotakuxX", {"entities": [(33, 42, "USERNAME")]}),
    ("NECESITO CREAR UN NUEVO ACCESO", {"entities": []}),
    ("Ayúdame a crear un nuevo usuario", {"entities": []}),
    ("ayúdame generando una nueva cuenta", {"entities": []}),
    ("crea un nuevo acceso para Pedro", {"entities": [(25, 30, "USERNAME")]}),
    ("crea un nuevo usuario llamado Pedro en el servidor 4", {"entities": [(30, 35, "USERNAME")]}),
    ("Genera un nuevo usuario para el servidor de pruebas", {"entities": []}),
    ("ACCESO nuevo para el servidor pro", {"entities": []}),
    ("Por favor crea un nuevo acceso en el servidor 2", {"entities": []}),
    ("Añade un nuevo usuario al servidor 3", {"entities": []}),
    ("ayúdame creando un nuevo acceso en el servidor server_pro33", {"entities": []}),
    ("crear nuevo usuario", {"entities": []}),
    ("crear un acceso nuevo", {"entities": []}),
    ("genera un usuario en el servidor server_portal", {"entities": []}),
    ("crea un usuario llamado ruravi en el servidor servidor4", {"entities": [(24, 30, "USERNAME")]}),
    ("Genera un usuario en el servidor 6 que se llame Krizia", {"entities": [(50, 56, "USERNAME")]}),
    ("por favor añade un nuevo acceso en el servidor servidorprron con un nombre de usuario Felipe", {"entities": [(89, 95, "USERNAME")]}),
    ("¿Me podrías ayudar creando un nuevo usuario en el servidor ffmax que se llame Blanca?", {"entities": [(82, 88, "USERNAME")]}),
    ("me ayudarías creando un nuevo acceso", {"entities": []}),
    ("¿me podrías ayudar a generar un nuevo acceso llamado Hilda en el servidor vvmax?", {"entities": [(52, 57, "USERNAME")]}),
    ("Añade un acceso al servidor de pruebas", {"entities": []}),
    ("podrías añadir un usuario al servidor ddtech", {"entities": []}),
    # Comandos de "modificar_usuario"
    ("Actualizar los permisos de María en el servidor de pruebas", {"entities": [(24, 29, "USERNAME")]}),
    ("Modifica el grupo del usuario Ruravi", {"entities": [(31, 37, "USERNAME")]}),
    ("Cambia los permisos del usuario Pedro en el servidor 5", {"entities": [(33, 38, "USERNAME")]}),
    ("Cambia el grupo al que pertenece el acceso de Ruravi en el servidor 2", {"entities": [(49, 55, "USERNAME")]}),
    ("Elimina el acceso de la cuenta de Hilda del servidor 5", {"entities": [(36, 41, "USERNAME")]}),
    ("Necesito actualizar la cuenta de Pedro", {"entities": [(31, 36, "USERNAME")]}),
    ("Por favor, edita los detalles de Juan", {"entities": [(31, 35, "USERNAME")]}),
    ("Modificar usuario", {"entities": []}),
    ("Edita los datos de la cuenta de Rafael", {"entities": [(34, 40, "USERNAME")]}),
    ("me ayudarías editando la cuenta de Krizia", {"entities": [(35, 41, "USERNAME")]}),
    ("por favor edita la cuenta de Diego", {"entities": [(29, 34, "USERNAME")]}),
    ("necesito que cambies unos datos de la cuenta de Pedro", {"entities": [(49, 54, "USERNAME")]}),
    ("me podrías ayudar a cambiar datos de la cuenta de Luis?", {"entities": [(54, 58, "USERNAME")]}),
    ("modifica la cuenta de Aida", {"entities": [(22, 26, "USERNAME")]}),
    ("edita los datos de la cuenta de Federico", {"entities": [(34, 42, "USERNAME")]}),
    ("necesito modificar una cuenta", {"entities": []}),
    ("editar usuario", {"entities": []}),
    ("modificar usuario", {"entities": []}),
    ("editar acceso", {"entities": []}),
    ("modificar acceso", {"entities": []}),
    ("me ayudarías editando un acceso?", {"entities": []}),
    ("necesito que edites una cuenta", {"entities": []}),
    ("edita un acceso llamado Pedrito", {"entities": [(24, 31, "USERNAME")]}),
    ("cambia los datos de una cuenta", {"entities": []}),
    ("podrías editar una cuenta por mí?", {"entities": []}),
    ("cambia los permisos de un acceso en el servidor server_portal", {"entities": []}),
    ("Cambia el grupo al que pertenece el usuario Alfredo en el servidor 6", {"entities": [(49, 56, "USERNAME")]}),
    ("modifica el grupo de Raúl en el servidor 3", {"entities": [(21, 25, "USERNAME")]}),
    ("en el servidor server_portal modifica los permisos de Rebeca", {"entities": [(55, 61, "USERNAME")]}),
    ("cambia de grupo del acceso Fernando en el servidor de pruebas", {"entities": [(28, 36, "USERNAME")]}),
    ("edita el acceso de XxOtakiXx", {"entities": [(18, 27, "USERNAME")]}),
    ("ayúdame a modificar un usuario", {"entities": []}),
    ("ayúdame a cambiar los datos de una cuenta", {"entities": []}),
]


def entrenar_modelo_ner():
    nlp = spacy.blank("es")  # Crear un modelo en blanco para español

    # Crear el componente NER y añadirlo al pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # Añadir las etiquetas de entidad
    ner.add_label("USERNAME")

    # Evitar el entrenamiento de otros componentes
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        # Entrenar el modelo
        optimizer = nlp.begin_training()
        for itn in range(30):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.5))
            for batch in batches:
                texts, annotations = zip(*batch)
                examples = []
                for i in range(len(texts)):
                    doc = nlp.make_doc(texts[i])
                    example = spacy.training.Example.from_dict(doc, annotations[i])
                    examples.append(example)
                nlp.update(examples, sgd=optimizer, losses=losses)
            print(f"Iteración {itn + 1}, pérdidas: {losses}")

    # Guardar el modelo entrenado
    nlp.to_disk(r'Clasificación de intenciones\modelo_ner_personalizado')
    print("Modelo NER personalizado entrenado y guardado.")

# Llamar a la función para entrenar el modelo
entrenar_modelo_ner()
