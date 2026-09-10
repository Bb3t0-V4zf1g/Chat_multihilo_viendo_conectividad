# Chat multihilo TCP

Aplicacion de chat sencilla desarrollada en Python. El servidor usa TCP y crea un hilo independiente para atender a cada cliente conectado.

## Requisitos

- Python 3 instalado.
- Acceso a una terminal.
- No se necesitan paquetes externos; el proyecto utiliza solo la biblioteca estandar de Python.

## Estructura

```text
server/
  server_multithread_tcp.py   # Servidor TCP multihilo
clients/
  client_example.py            # Cliente del chat
```

## Como ejecutar el proyecto

Los comandos siguientes deben ejecutarse desde la carpeta raiz del proyecto:

### 1. Iniciar el servidor

En una terminal, ejecuta:

```powershell
python server/server_multithread_tcp.py
```

Si tu instalacion de Python usa el comando `py`, tambien puedes ejecutar:

```powershell
py server/server_multithread_tcp.py
```

El servidor quedara escuchando en `localhost`, puerto `6000`.

### 2. Conectar un cliente

Abre otra terminal, en la misma carpeta raiz, y ejecuta:

```powershell
python clients/client_example.py
```

Escribe un apodo cuando el programa lo solicite. Para probar el chat entre varias personas, abre una terminal adicional por cada cliente y ejecuta el mismo comando.

### 3. Usar el chat

- Escribe cualquier texto para enviarlo a los demas clientes conectados.
- Escribe `/quienes` para solicitar la lista de clientes conectados.
- Escribe `/exit` para salir del chat.
- Tambien puedes presionar `Ctrl+C` para interrumpir el cliente.

Para detener el servidor, vuelve a su terminal y presiona `Ctrl+C`.

## Explicacion sencilla

1. El servidor crea un socket TCP y lo enlaza con `localhost:6000`.
2. Cuando un cliente se conecta, el servidor crea un hilo para atenderlo sin bloquear a los demas clientes.
3. El cliente envia su apodo en formato JSON para registrarse.
4. El cliente mantiene un hilo que recibe mensajes mientras el hilo principal lee lo que escribe el usuario.
5. Cuando un cliente envia un mensaje, el servidor lo reenvia a los otros clientes conectados.

Este ejemplo esta pensado para ejecutarse en la misma computadora. Para conectar equipos distintos habria que cambiar `localhost` por la direccion IP del equipo donde se ejecuta el servidor y permitir el puerto `6000` en la red o firewall.

## Notas

- El servidor debe iniciarse antes que los clientes.
- El puerto `6000` debe estar disponible.
- La aplicacion no guarda el historial del chat: los mensajes solo se envian a los clientes conectados en ese momento.