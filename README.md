# 📖 Backend – Setup desde cero (Los comandos pueden cambiar dependiendo el sistema operativo)

Este documento explica cómo levantar el proyecto desde cero después de clonar el repositorio.  
Los pasos están pensados para un usuario externo que no conoce el entorno.

---

## ✅ 1. Requisitos previos

Antes de empezar, asegurate de tener instalado:

- **Python 3.10+**
- **Git**
- **pip** (incluido con Python)
- **Virtualenv** (opcional, pero recomendado)

## 📥 2. Clonar el repositorio

```bash
git clone https://github.com/JoaquinPettinariUEM/python-unidad-3.git

cd python-unidad-3
```

## 🐢 3. Crear y activar un entorno virtual (venv, sin Docker Compose)

Crear el entorno virtual:
```bash
python -m venv venv

// Activar el entorno virtual (Windows):
venv\Scripts\activate
// En mac
source venv/bin/activate
```

Si todo va bien, deberías ver algo así al inicio de tu consola:
```bash
(venv) C:\ruta\proyecto/uem-be-py-unidad2
```

## 📦 4. Instalar dependencias

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 🧩 5.1. Configuración del archivo .env

Para que la aplicación pueda conectarse correctamente a Spotify y a la base de datos, necesitás configurar tus variables de entorno.
En este repositorio vas a encontrar un archivo llamado: 

```bash
.env.copy
```

### 🎧 5.2 ¿De dónde sacar las credenciales de Spotify?

1. Entrá a https://developer.spotify.com/dashboard
2. Creá una app nueva.
3. Copiá el Client ID y el Client Secret.
4. Pegalos en tu archivo .env **(Si optaste por la opción de Docker Compose tenes que pegar tus credenciales en docker-compose.yml)**

### 🔧 Cómo crear tu archivo .env
Copiá el archivo de ejemplo:
```bash
cp .env.copy .env
```

## ▶️ 6. Levantar el servidor
Ejecutá uvicorn en modo desarrollo:
```bash
uvicorn app.main:app --reload
```


## 📚 7. El servidor estará disponible en:

  - http://localhost:8000
  - Documentación automática OpenAPI: http://localhost:8000/docs
  - Documentación ReDoc: http://localhost:8000/redoc

## Entrega del proyecto:

[Explicación del código, estructura del proyecto y conclusiones](https://github.com/JoaquinPettinari/python-unidad-3/blob/main/explicación_código.md)










