# Sistema de Gestión de Minimercado UPS

## Integrantes

* Robinson Redrovan
* Michael Franco
* Bryan Mejía

## Descripción

Backend desarrollado en FastAPI para la gestión de un minimercado.

El sistema permite:

* Gestión de productos
* Gestión de clientes
* Gestión de proveedores
* Registro de ventas
* Control de inventario
* Reportes básicos

## Tecnologías

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Swagger OpenAPI

## Ejecución

Instalar dependencias:

pip install -r requirements.txt

Ejecutar:

uvicorn app.main:app --reload

## Swagger

http://127.0.0.1:8000/docs

## Arquitectura

* Models
* Repositories
* Services
* Routes

## Funcionalidades

### Productos

* Listar productos
* Crear productos

### Clientes

* Listar clientes
* Crear clientes

### Proveedores

* Listar proveedores
* Crear proveedores

### Ventas

* Listar ventas
* Registrar ventas

### Inventario

* Consultar stock

### Reportes

* Resumen general del sistema
