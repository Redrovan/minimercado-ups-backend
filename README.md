# Sistema de Gestión de Minimercado UPS

## Integrantes

* Robinson Redrovan
* Michael Franco
* Bryan Mejía

# Sistema de Gestión de Minimercado UPS

## Descripción General

El Sistema de Gestión de Minimercado UPS es una aplicación backend desarrollada para administrar las operaciones básicas de un minimercado. El sistema permite gestionar productos, clientes, proveedores, ventas, inventario y reportes mediante una API REST construida con FastAPI.

La aplicación fue desarrollada aplicando conceptos de Ingeniería de Software, utilizando una arquitectura en capas que facilita el mantenimiento, escalabilidad y reutilización del código.

---

## Objetivos del Proyecto

### Objetivo General

Desarrollar una aplicación backend para la gestión de un minimercado utilizando herramientas y buenas prácticas de Ingeniería de Software.

### Objetivos Específicos

* Implementar una API REST utilizando FastAPI.
* Aplicar una arquitectura basada en modelos, repositorios, servicios y controladores.
* Gestionar la persistencia de datos mediante SQLite y SQLAlchemy.
* Documentar automáticamente los servicios mediante Swagger/OpenAPI.
* Utilizar Git y GitHub para el control de versiones y trabajo colaborativo.

---

## Tecnologías Utilizadas

| Tecnología      | Descripción                               |
| --------------- | ----------------------------------------- |
| Python 3        | Lenguaje de programación principal        |
| FastAPI         | Framework para el desarrollo de APIs REST |
| SQLAlchemy      | ORM para acceso a la base de datos        |
| SQLite          | Base de datos utilizada para persistencia |
| Swagger/OpenAPI | Documentación automática de la API        |
| Git             | Control de versiones                      |
| GitHub          | Repositorio remoto del proyecto           |

---

## Arquitectura del Proyecto

El proyecto implementa una arquitectura por capas para separar responsabilidades y mejorar la mantenibilidad del sistema.

### Model

Representa las entidades de la base de datos.

Ejemplos:

* Producto
* Cliente
* Proveedor
* Venta

### Repository

Encapsula las operaciones de acceso a datos.

Funciones principales:

* Consultar registros
* Crear registros
* Actualizar registros
* Eliminar registros

### Service

Contiene la lógica de negocio y validaciones.

Ejemplos:

* Validación de precios
* Validación de stock
* Validación de correo electrónico
* Validación de cédula y RUC

### Routes

Define los endpoints REST expuestos por la aplicación.

---

## Estructura del Proyecto

```text
minimercado-backend/

app/
│
├── database.py
├── main.py
│
├── models/
│   └── models.py
│
├── repositories/
│   ├── producto_repository.py
│   ├── cliente_repository.py
│   ├── proveedor_repository.py
│   └── venta_repository.py
│
├── services/
│   ├── producto_service.py
│   ├── cliente_service.py
│   ├── proveedor_service.py
│   └── venta_service.py
│
├── routes/
│   ├── productos.py
│   ├── clientes.py
│   ├── proveedores.py
│   ├── ventas.py
│   ├── inventario.py
│   └── reportes.py
│
├── schemas/
│   └── schemas.py
│
└── utils/
    └── dependencies.py
```

---

## Funcionalidades Implementadas

### Gestión de Productos

* Crear productos
* Listar productos
* Consultar producto por ID
* Actualizar productos
* Eliminar productos

### Gestión de Clientes

* Crear clientes
* Listar clientes
* Consultar cliente por ID
* Actualizar clientes
* Eliminar clientes

### Gestión de Proveedores

* Crear proveedores
* Listar proveedores
* Consultar proveedor por ID
* Actualizar proveedores
* Eliminar proveedores

### Gestión de Ventas

* Registrar ventas
* Listar ventas
* Consultar ventas por ID
* Actualizar ventas
* Eliminar ventas

### Gestión de Inventario

* Consultar stock disponible
* Identificar productos con stock bajo

### Reportes

* Total de productos
* Total de clientes
* Total de proveedores
* Total de ventas
* Total de ingresos generados

---

## Validaciones Implementadas

### Productos

* El precio debe ser mayor que cero.
* El costo no puede ser negativo.
* El stock no puede ser negativo.

### Clientes

* La cédula debe contener 10 dígitos.
* El correo electrónico debe tener formato válido.

### Proveedores

* El RUC debe contener 13 dígitos.
* El correo electrónico debe tener formato válido.

### Ventas

* El total de la venta debe ser mayor que cero.

---

## Instalación

### Clonar repositorio

```bash
git clone https://github.com/Redrovan/minimercado-ups-backend.git
```

### Ingresar al proyecto

```bash
cd minimercado-backend
```

### Crear entorno virtual

Windows:

```bash
python -m venv venv
```

### Activar entorno virtual

PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

---

## Documentación Swagger

Una vez iniciado el servidor:

```text
http://127.0.0.1:8000/docs
```

Swagger permite visualizar y probar todos los endpoints implementados en el sistema.

---

## Ejemplo de Reporte

Endpoint:

```http
GET /reportes/resumen
```

Respuesta:

```json
{
  "productos": 2,
  "clientes": 1,
  "proveedores": 1,
  "ventas": 1,
  "ingresos": 25.5
}
```

---

## Repositorio del Proyecto

Repositorio GitHub:

https://github.com/Redrovan/minimercado-ups-backend

---

## Integrantes

* Robinson Redrovan
* Michael Franco
* Bryan Mejía

---

## Conclusiones

El desarrollo de este proyecto permitió aplicar conceptos fundamentales de Ingeniería de Software relacionados con diseño arquitectónico, desarrollo de APIs REST, persistencia de datos y documentación de servicios. La utilización de FastAPI facilitó la construcción de una API moderna y documentada automáticamente mediante Swagger. Además, la implementación de una arquitectura basada en modelos, repositorios, servicios y controladores permitió mantener una adecuada separación de responsabilidades y una mejor organización del código. Finalmente, el uso de Git y GitHub proporcionó un adecuado control de versiones y seguimiento del desarrollo del proyecto.
