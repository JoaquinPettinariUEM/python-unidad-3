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

## 🌳 Árbol Binario de Productos

Los productos se almacenan en un árbol binario de búsqueda.

### 🔹 Inserción y búsqueda

El árbol usa el id del producto como valor para ordenar nodos.
Esto implica que, como los ids suelen ser crecientes, el árbol puede quedar sesgado hacia la derecha (no balanceado).

### 🔹 Persistencia

Manejamos un archivo JSON con productos.
Al iniciar la aplicación se ejecuta el **preload_products** que toma unos datos mocks a través de un archivo JSON, los inserta en a base de datos y en un árbol nuevo.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        preload_products(db)
        yield
    finally:
        db.close()
```

Como esto está hecho por sesión, al reiniciar la aplicación el árbol se va a volver a crear.

## 🧩 Lista Enlazada de Ordenes

Las órdenes están implementadas con una lista enlazada simple, donde cada nodo representa un producto dentro de la orden.

### 🔹 Modelos relacionados

```python
class Order(Base):
    id = Column(Integer, primary_key=True)
    head_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)

    head = relationship("OrderItem", foreign_keys=[head_id], post_update=True)
```

```python
class OrderItem(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer)
    quantity = Column(Integer)

    next_id = Column(Integer, ForeignKey("order_items.id"))
    next = relationship("OrderItem", remote_side=[id], uselist=False)
```

🔹 Explicación de la estructura

- **Order.head_id** apunta al primer OrderItem de la lista
- Cada **OrderItem.next_id** apunta al siguiente nodo
- De esa forma, SQLAlchemy reconstruye la lista enlazada automáticamente
- La relación remote_side=[id] es importante porque indica que el modelo se relaciona consigo mismo

Esto permite recorrer la orden así:
```python
current = order.head
while current:
    current = current.next
```

## 📚 Endpoints
### 🛒 Productos (/products)

- **GET /products/** Retorna todos los productos persistidos en la base.
- **GET /products/{product_id}** Retorna un producto individual.
- **POST /products/** Crea un producto nuevo y lo inserta en:
  - La base de datos
  - El árbol binario

### 📦 Órdenes (/orders)

Aquí es donde entra en juego la lista enlazada.

- **GET /orders/** Retorna todas las órdenes.
- **GET /orders/{order_id}** Recorre la lista enlazada desde el head y devuelve los productos con nombre y precio mapeados.
- **POST /orders/** Crea una nueva orden, armando la lista enlazada desde cero:
- **PUT /orders/{order_id}** Sobrescribe completamente los nodos de la orden.
- **DELETE /orders/{order_id}** Elimina la orden completa, junto con todos los nodos asociados.


## 🚧 Limitaciones y Posibles Mejoras

- El BST no está balanceado → podría degenerar en lista
- Las órdenes sobrescriben nodo por nodo, aunque funciona, podría optimizarse
- No existen validaciones avanzadas (existencia de producto, cantidad > 0, etc.)
- No hay manejo de transacciones en operaciones complejas
- No hay tests automatizados (muy recomendado agregarlos)
- El manejo de persistencia con un archivo JSON no es lo mejor.
- Actualmente combina el guardado de productos de forma redundante, tanto en el archivo JSON como en la base. No es lo mas óptimo

  
