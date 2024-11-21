import random
import json
import csv
import string

plantillas_crear_usuario  = [
    "Necesito crear un usuario nuevo para {codigo_empleado} ",
    "Agregar acceso al usuario {codigo_empleado} ",
    "Registrar un nuevo acceso para {codigo_empleado} ",
    "Crear cuenta para {codigo_empleado} en el {servidor}",
    "Generar un nuevo usuario para {servidor} con el código {codigo_empleado}",
    "Crear un usuario con el código {codigo_empleado} en el {servidor}",
    "Agregar un nuevo usuario con el código {codigo_empleado} en el {servidor}",
    "Crea un usuario nuevo para el {servidor} con el código {codigo_empleado}",
    "Generar un usuario nuevo para el {servidor} con el código {codigo_empleado}",
    "Porfavor crea un nuevo usuario para {codigo_empleado} en el {servidor}",
    "crear nuevo usuario para {codigo_empleado} en el {servidor}",
    "nuevo acceso para {codigo_empleado} en el {servidor}",
    "Añade un nuevo acceso en  {servidor} para el usuario {codigo_empleado}",
    "me ayudarias a crear un usuario para el {servidor} con el código {codigo_empleado}",
    "me ayudarias añadieno un acceso para el usuario {codigo_empleado} en el {servidor}",
    "necesito crear un usuario para el {servidor} con el código {codigo_empleado}",
    "Acceso nuevo en el {servidor} para el usuario {codigo_empleado}",
    "Acceso nuevo para el usuario {codigo_empleado} en el {servidor}",
    "Crear un usuario en el {servidor} para el usuario {codigo_empleado}",
    "ayudame a crear un usuario en el {servidor} para el usuario {codigo_empleado}",
    "porfavor crea un usuario en el {servidor} para el usuario {codigo_empleado}",
    "porfavor crea un acceso para el usuario {codigo_empleado} en el {servidor}",
    "podrias crear un usuario en el {servidor} para el usuario {codigo_empleado}",
    "podrias crear un acceso para el usuario {codigo_empleado} en el {servidor}",
    "ayudame a crewar un usuario en el {servidor} para el usuario {codigo_empleado}",
    "ayudame a crear un acceso para el usuario {codigo_empleado} en el {servidor}",
    "crear un acceso del {servidor} para el usuario {codigo_empleado}",
    "crear una cceso para el usuario {codigo_empleado} en el {servidor}",
    "añadir un acceso para el usuario {codigo_empleado} en el {servidor}",
    "añadir un usuario en el {servidor} para el usuario {codigo_empleado}",
    "registrar un usuario en el {servidor} para el usuario {codigo_empleado}",
    "registrar un acceso para el usuario {codigo_empleado} en el {servidor}",
    "Necesito crear un acceso nuevo para {servidor}",
    "Agregar acceso al acceso {codigo_empleado} ",
    "Registrar un nuevo acceso para {codigo_empleado} ",
    "Crear cuenta para {codigo_empleado} en el {servidor}",
    "Generar un nuevo acceso para {servidor} con el código {codigo_empleado}",
    "Crear un acceso con el código {codigo_empleado} en el {servidor}",
    "Agregar un nuevo acceso con el código {codigo_empleado} en el {servidor}",
    "Crea un acceso nuevo para el {servidor} con el código {codigo_empleado}",
    "Generar un acceso nuevo para el {servidor} con el código {codigo_empleado}",
    "Porfavor crea un nuevo acceso para {codigo_empleado} en el {servidor}",
    "crear nuevo acceso para {codigo_empleado} en el {servidor}",
    "nuevo acceso para {codigo_empleado} en el {servidor}",
    "Añade un nuevo acceso en  {servidor} para el acceso {codigo_empleado}",
    "me ayudarias a crear un acceso para el {servidor} con el código {codigo_empleado}",
    "me ayudarias añadieno un acceso para el acceso {codigo_empleado} en el {servidor}",
    "necesito crear un acceso para el {servidor} con el código {codigo_empleado}",
    "Acceso nuevo en el {servidor} para el acceso {codigo_empleado}",
    "Acceso nuevo para el acceso {codigo_empleado} en el {servidor}",
    "Crear un acceso en el {servidor} para el acceso {codigo_empleado}",
    "ayudame a crear un acceso en el {servidor} para el acceso {codigo_empleado}",
    "porfavor crea un acceso en el {servidor} para el acceso {codigo_empleado}",
    "porfavor crea un acceso para el acceso {codigo_empleado} en el {servidor}",
    "podrias crear un acceso en el {servidor} para el acceso {codigo_empleado}",
    "podrias crear un acceso para el acceso {codigo_empleado} en el {servidor}",
    "ayudame a crewar un acceso en el {servidor} para el acceso {codigo_empleado}",
    "ayudame a crear un acceso para el acceso {codigo_empleado} en el {servidor}",
    "crear un acceso del {servidor} para el acceso {codigo_empleado}",
    "crear una cceso para el acceso {codigo_empleado} en el {servidor}",
    "añadir un acceso para el acceso {codigo_empleado} en el {servidor}",
    "añadir un acceso en el {servidor} para el acceso {codigo_empleado}",
    "registrar un acceso en el {servidor} para el acceso {codigo_empleado}",
    "registrar un acceso para el acceso {codigo_empleado} en el {servidor}"
]

plantillas_solicitar_info  = [
    "Necesito información del usuario {codigo_empleado}",
    "Dame los datos del usuario {codigo_empleado} ",
    "Información del usuario {codigo_empleado} ",
    "Datos del usuario {codigo_empleado} ",
    "Necesito información del empleado {codigo_empleado} ",
    "Dame los datos del empleado {codigo_empleado} ",
    "Información del empleado {codigo_empleado} ",
    "Datos del empleado {codigo_empleado} ",
    "Necesito información del usuario {codigo_empleado}",
    "Dame los datos del usuario {codigo_empleado}",
    "Información del usuario {codigo_empleado}",
    "Datos del usuario {codigo_empleado}",
    "Necesito información del empleado {codigo_empleado}",
    "Dame los datos del empleado {codigo_empleado}",
    "Información del empleado {codigo_empleado}",
    "Datos del empleado {codigo_empleado}",
    "Lista los accesos del usuario {codigo_empleado}",
    "Listar los accesos del usuario {codigo_empleado}",
    "que accesos tiene el usuario {codigo_empleado}",
    "cuales son los accesos del usuario {codigo_empleado}",
    "por favor lista los accesos del usuario {codigo_empleado}",
    "por favor listar los accesos del usuario {codigo_empleado}",
    "muestrame los accesos del usuario {codigo_empleado}",
    "mostrar los accesos del usuario {codigo_empleado}",
    "me podrias mostrar los accesos del usuario {codigo_empleado}",
    "porfavor muestrame los accesos del usuario {codigo_empleado}",
    "porfavor mostrar los accesos del usuario {codigo_empleado}",
    "datos del usuario {codigo_empleado}",
    "información del usuario {codigo_empleado}",
    "Necesito información del emeplado {codigo_empleado} ",
    "Dame los datos del emeplado {codigo_empleado} ",
    "Información del emeplado {codigo_empleado} ",
    "Datos del emeplado {codigo_empleado} ",
    "Necesito información del empleado {codigo_empleado} ",
    "Dame los datos del empleado {codigo_empleado} ",
    "Información del empleado {codigo_empleado} ",
    "Datos del empleado {codigo_empleado} ",
    "Necesito información del emeplado {codigo_empleado}",
    "Dame los datos del emeplado {codigo_empleado}",
    "Información del emeplado {codigo_empleado}",
    "Datos del emeplado {codigo_empleado}",
    "Necesito información del empleado {codigo_empleado}",
    "Dame los datos del empleado {codigo_empleado}",
    "Información del empleado {codigo_empleado}",
    "Datos del empleado {codigo_empleado}",
    "Lista los accesos del emeplado {codigo_empleado}",
    "Listar los accesos del emeplado {codigo_empleado}",
    "que accesos tiene el emeplado {codigo_empleado}",
    "cuales son los accesos del emeplado {codigo_empleado}",
    "por favor lista los accesos del emeplado {codigo_empleado}",
    "por favor listar los accesos del emeplado {codigo_empleado}",
    "muestrame los accesos del emeplado {codigo_empleado}",
    "mostrar los accesos del emeplado {codigo_empleado}",
    "me podrias mostrar los accesos del emeplado {codigo_empleado}",
    "porfavor muestrame los accesos del emeplado {codigo_empleado}",
    "porfavor mostrar los accesos del emeplado {codigo_empleado}",
    "datos del emeplado {codigo_empleado}",
    "información del emeplado {codigo_empleado}",
]

Resetear_contraseña = [
    "Resetea la contraseña del acceso {codigo_de_acceso}",
    "Reinicia la contraseña del acceso {codigo_de_acceso}",
    "Cambia la contraseña del acceso {codigo_de_acceso}",
    "Olvidé la contraseña del acceso {codigo_de_acceso}",
    "Ayudame a recuperar la contraseña del acceso {codigo_de_acceso}",
    "Necesito cambiar la contraseña del acceso {codigo_de_acceso}",
    "No puedo acceder al sistema con el acceso {codigo_de_acceso}",
    "No puedo iniciar sesión con el acceso {codigo_de_acceso}",
    "se perdió la contraseña del acceso {codigo_de_acceso}",
    "Reinicio de contraseña del acceso {codigo_de_acceso}",
    "me podrias ayudar a recuperar la contraseña del acceso {codigo_de_acceso}",
    "me podrias ayudar a cambiar la contraseña del acceso {codigo_de_acceso}",
    "necesito que me ayudes a recuperar la contraseña del acceso {codigo_de_acceso}",
    "necesito que me ayudes a cambiar la contraseña del acceso {codigo_de_acceso}",
    "RESTAURO LA CONTRASEÑA DEL ACCESO {codigo_de_acceso}",
    "ayudame a restaurar la contraseña del acceso {codigo_de_acceso}",
    "ayudame a cambiar la contraseña del acceso {codigo_de_acceso}",
    "ayudame a recuperar la contraseña del acceso {codigo_de_acceso}"
]

plantillas_por_intencion = {
    "crear_usuario": plantillas_crear_usuario,
    "info_usuario": plantillas_solicitar_info,
    "resetear_contraseña": Resetear_contraseña
}

servidores = [["servidor de ventas", "SRVTAS"], ["servidor principal", "SRVPRAL"], ["servidor de desarrollo", "SRVDLLO"], ["servidor de pruebas", "SRVPRBS"], ["Servidor Demo", "SRVDMO"],["Server 1 Prod","SRVPRD"],["Server Test1","SRVTST"],["Server Dev1","SRVDEV"]]
codigos_empleado = [str(i).zfill(4) for i in range(1000, 9999)]
codigos_de_acceso = []
for _ in range(300):
    codigo_empleado = random.choice(codigos_empleado)  # Seleccionar un código de empleado aleatorio
    codigo_servidor = random.choice([servidor[1] for servidor in servidores])  # Seleccionar un servidor aleatorio
    numero_aleatorio = str(random.randint(10, 99))  # Generar un número aleatorio de dos dígitos
    codigo = f"{codigo_empleado}{codigo_servidor}{numero_aleatorio}"  # Combinar todos los elementos
    codigos_de_acceso.append(codigo)

datos_entrenamiento_intenciones = []
TRAIN_DATA = []

for intencion, plantillas in plantillas_por_intencion.items():
    for plantilla in plantillas:
        for _ in range(50):  # Número de ejemplos a generar por plantilla
            codigo_empleado = random.choice(codigos_empleado)
            servidor = random.choice(servidores[0])
            codigo_de_acceso = random.choice(codigos_de_acceso)
            
            # Determinar qué entidades están en la plantilla
            entities_in_template = []
            params = {}
            if "{codigo_empleado}" in plantilla:
                entities_in_template.append("codigo_empleado")
                params["codigo_empleado"] = codigo_empleado
            if "{servidor}" in plantilla:
                entities_in_template.append("servidor")
                params["servidor"] = servidor
            if "{codigo_de_acceso}" in plantilla:
                entities_in_template.append("codigo_de_acceso")
                params["codigo_de_acceso"] = codigo_de_acceso
            
            # Generar el comando
            comando = plantilla.format(**params)
            
            # Añadir al conjunto de datos de intenciones
            datos_entrenamiento_intenciones.append([comando, intencion])
            
            # Inicializar la lista de entidades
            entities = []
            
            # Encontrar las posiciones de las entidades en el comando
            if "codigo_empleado" in entities_in_template:
                start_codigo = comando.find(codigo_empleado)
                end_codigo = start_codigo + len(codigo_empleado)
                if start_codigo != -1:
                    entities.append((start_codigo, end_codigo, "EMPLOYEE_CODE"))
                else:
                    print(f"Advertencia: No se encontró 'codigo_empleado' en el comando: '{comando}'")
                    continue  # Saltar este ejemplo si falta una entidad obligatoria

            if "servidor" in entities_in_template:
                start_servidor = comando.find(servidor)
                end_servidor = start_servidor + len(servidor)
                if start_servidor != -1:
                    entities.append((start_servidor, end_servidor, "SERVER"))
                else:
                    print(f"Advertencia: No se encontró 'servidor' en el comando: '{comando}'")
                    continue  # Opcional: Puedes decidir si saltar o no el ejemplo

            if "codigo_de_acceso" in entities_in_template:
                start_acceso = comando.find(codigo_de_acceso)
                end_acceso = start_acceso + len(codigo_de_acceso)
                if start_acceso != -1:
                    entities.append((start_acceso, end_acceso, "ACCESS_CODE"))
                else:
                    print(f"Advertencia: No se encontró 'codigo_de_acceso' en el comando: '{comando}'")
                    continue  # Opcional: Puedes decidir si saltar o no el ejemplo

            # Añadir al conjunto de datos de NER
            TRAIN_DATA.append((comando, {"entities": entities}))

# Guardar los datos de entrenamiento para clasificación de intenciones
with open('intenciones.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['comando', 'intencion'])
    writer.writerows(datos_entrenamiento_intenciones)

# Guardar los datos de entrenamiento para NER
with open('training_data.json', 'w', encoding='utf-8') as f:
    json.dump(TRAIN_DATA, f, ensure_ascii=False, indent=4)