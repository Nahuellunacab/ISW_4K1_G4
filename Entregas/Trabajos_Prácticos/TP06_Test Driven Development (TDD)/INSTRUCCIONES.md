## Para levantar el Backend
1. Dirigirse a ./backend y crear un entorno virtual:
```
python -m venv venv
```
2. Ejecutar entorno virtual:
```
.\venv\Scripts\activate
```
3. En el caso de que no se pueda activar por tema de permisos, ejecutar lo siguiente: 
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
4. Instalamos las dependencias necesarias:
```
pip install -r requirements.txt
```
5. Corremos el backend:
```
python app.py
```
## Para levantar el Frontend
1. Nos dirigimos a la carpeta /frontend e instalamos las dependencias:
```
npm install
```
2. Corremos el frontend:
```
npm run dev
```
3. Nos dirigimos a la url que nos expone la terminal:
```link
http://localhost:3000/
```
## Para ejecutar los tests
Las pruebas se pueden correr de dos maneras:
1. Desde la consola, ubicándose en la carpeta backend, con el comando:
```
python -m unittest tests.test_inscribirse_actividad.TestInscripcionActividad
```
2. Desde Visual Studio Code presionando el botón de play que aparece en la parte superior derecha del archivo con los tests.
