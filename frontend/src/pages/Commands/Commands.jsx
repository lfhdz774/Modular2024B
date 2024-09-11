import React, { useState } from 'react';
import { PostCommands } from 'src/Services/command.service';

function Command() {
  const [comando, setComando] = useState('');
  const [respuesta, setRespuesta] = useState('');

  const enviarComando = async () => {
    try {
        // El nombre del campo debe ser exactamente 'comando' para que el backend lo reciba correctamente
        let Comando = {
            comando: comando  // Esto envía el valor del comando directamente
        }
        
        const response = await PostCommands(Comando);  // Envía el objeto correctamente
        console.log(response);
        if (response.status === 200) {
            console.log(response.data);  // Procesa la respuesta
        }
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
      />
      <button onClick={enviarComando}>Enviar Comando</button>
      {respuesta && <p>Respuesta: {respuesta}</p>}
    </div>
  );
}

export default Command;
