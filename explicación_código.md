## 📁 Estructura del Proyecto

Este backend está construido con FastAPI, organizado de forma modular para mantener el código limpio, escalable y fácil de mantener.
A continuación se describe cada carpeta y archivo principal:
```bash
app.
├── models/
├── routers/
├── schemas/
├── services/
├── data/
├── structures/
├── utils/
├── database.py
├── main.py
├── .env
├── app.db
├── requirements.txt
```

### 🧩 models/

Contiene los modelos de base de datos usando [SQLAlchemy](https://www.sqlalchemy.org).
Representan las tablas y sus relaciones (producto, order, order_item).

### 🔌 routers/

Incluye los endpoints de la API.
Cada archivo maneja un conjunto de rutas (por ejemplo: /orders, /products).

### 📦 schemas/

Define los Pydantic Schemas, utilizados para validar y estructurar la información enviada.

### ⚙️ services/

Acá vive la lógica de la aplicación:
Manejo del árbol, creación, actualización y lectura. También maneja el listado de órdenes, inserción y actualización de datos
Los routers llaman a estos servicios para mantener el código ordenado.

### 🛠️ utils/

Funciones auxiliares y utilidades comunes.

### 🗄️ database.py

Configura la conexión a la base de datos, los motores de SQLAlchemy y la sesión.

### 🌲 strutures/

Clase contenedora del árbol y manejo de la lista enlazada con Nodos

### 🗂️ data/

Data mock para no iniciar la aplicación sin datos

### 🚀 main.py

Punto de entrada de la aplicación.
Aquí se crean las instancias de FastAPI y se incluyen los routers.

### 🔑 .env

Archivo con variables de entorno (credenciales, etc.).
No se sube al repositorio.

### 💾 app.db

Base de datos SQLite (solo para desarrollo local).

### 📦 requirements.txt

Dependencias del proyecto para instalar con pip.

---

## 📦 Proyecto: Productos + Órdenes con Árbol Binario y Lista Enlazada

Backend desarrollado con FastAPI, SQLAlchemy, Pydantic y persistencia en SQLite.

### 🧭 Recorrido del Código (Cómo funciona todo junto)

El punto de entrada es **main.py**, donde se inicializa la aplicación FastAPI y se cargan las rutas definidas en **routers/**.

Cada ruta delega su lógica a un archivo dentro de **services/**, donde se implementan las operaciones principales:

- Gestión del árbol binario (lectura, inserción, búsqueda)
- POST, GETs de productos 
- CRUD de órdenes enlazadas
- Conversión y mapeo de datos SQL → JSON → Pydantic → Response

Los datos se validan y tipan utilizando los Schemas de Pydantic, ubicados en la carpeta **schemas/**.

La persistencia se maneja con SQLAlchemy ORM, mediante modelos definidos en la carpeta **models/**, lo que permite:

- No escribir SQL manual
- Cambiar de motor de base de datos con facilidad (SQLite → PostgreSQL)
- Manejar relaciones complejas (en este caso, una lista enlazada almacenada en SQL)

Esta estructura separa responsabilidades:

- **Routers** manejan las solicitudes HTTP
- **Services** contienen la lógica de negocio
- **Schemas** tipan y validan los datos
- **Models** representan las tablas y la lógica relacional en la base de datos
