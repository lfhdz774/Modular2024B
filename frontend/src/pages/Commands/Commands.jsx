import { set } from 'lodash';
import React, { useState } from 'react';
import { PostCommands } from 'src/Services/command.service';

function Command() {
  const [comando, setComando] = useState('');
  const [respuesta, setRespuesta] = useState('');
  const [link, setLink] = useState('');

  const enviarComando = async () => {
    try {
        // El nombre del campo debe ser exactamente 'comando' para que el backend lo reciba correctamente
        let Comando = {
            comando: comando  // Esto envía el valor del comando directamente
        }
        
        const response = await PostCommands(Comando);  // Envía el objeto correctamente
        console.log(response);
        //alert(response.respuesta);
        setRespuesta(response.respuesta.message);
        setLink(response.respuesta.link);

    } catch (error) {
        console.error("Error al enviar el comando:", error);
    }
};

  return (
    <div className="App">
      <h1>Procesador de Comandos</h1>
      <input
        type="text"
        value={comando}
        onChange={(e) => setComando(e.target.value)}
        placeholder="Escribe un comando"
        style={{ width: '700px' }}
      />
      <button onClick={enviarComando}>Enviar Comando</button>
      <p>Respuesta: {respuesta}</p>
      <a href={link}>{link}</a>
    </div>
  );
}

export default Command;
