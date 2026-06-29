# Sistema de Gestión de Minimercado UPS

## Integrantes

* Robinson Redrovan
* Michael Franco
* Bryan Mejía

---

# Descripción General

El Sistema de Gestión de Minimercado UPS es una aplicación backend desarrollada para administrar las operaciones de un minimercado mediante una API REST construida con **FastAPI**.

El sistema permite gestionar:

* Productos
* Clientes
* Proveedores
* Usuarios
* Roles
* Ventas
* Inventario
* Caja
* Reportes
* Autenticación JWT

La aplicación fue desarrollada aplicando principios de Ingeniería de Software mediante una arquitectura por capas (Models, Repositories, Services y Routes), facilitando el mantenimiento, escalabilidad y reutilización del código.

---

# Objetivo General

Desarrollar una API REST para la administración integral de un minimercado utilizando FastAPI, SQLAlchemy y SQLite, aplicando buenas prácticas de desarrollo de software y pruebas automatizadas.

---

# Objetivos Específicos

* Implementar una API REST utilizando FastAPI.
* Gestionar productos, clientes, proveedores, ventas e inventario.
* Implementar autenticación mediante JWT.
* Aplicar una arquitectura basada en capas.
* Gestionar la persistencia mediante SQLAlchemy y SQLite.
* Documentar automáticamente la API mediante Swagger/OpenAPI.
* Implementar pruebas unitarias utilizando diferentes frameworks de testing.
* Medir la cobertura del código mediante Coverage.py.
* Utilizar Git y GitHub para el trabajo colaborativo.

---

# Tecnologías Utilizadas

| Tecnología      | Uso                    |
| --------------- | ---------------------- |
| Python 3        | Lenguaje principal     |
| FastAPI         | Framework Backend      |
| SQLAlchemy      | ORM                    |
| SQLite          | Base de datos          |
| Pydantic        | Validación de datos    |
| JWT             | Autenticación          |
| Swagger/OpenAPI | Documentación          |
| Git             | Control de versiones   |
| GitHub          | Repositorio remoto     |
| Pytest          | Pruebas unitarias      |
| Unittest        | Pruebas unitarias      |
| Doctest         | Validación de ejemplos |
| Mockito         | Mocking                |
| Coverage.py     | Cobertura de código    |

---

# Arquitectura del Proyecto

El proyecto sigue una arquitectura en capas.

```
Cliente

↓

Routes

↓

Services

↓

Repositories

↓

Models

↓

SQLite
```

Cada capa tiene responsabilidades claramente definidas.

## Models

Representan las entidades de la base de datos.

Ejemplos:

* Producto
* Cliente
* Usuario
* Rol
* Venta
* Caja
* Factura

---

## Repositories

Gestionan el acceso a la base de datos mediante SQLAlchemy.

Operaciones:

* Crear
* Consultar
* Actualizar
* Eliminar

---

## Services

Implementan toda la lógica de negocio.

Ejemplos:

* Validación de stock
* Validación de precios
* Validación de cédula
* Validación de RUC
* Registro de ventas
* Generación de facturas
* Movimientos de caja
* Inventario
* Autenticación

---

## Routes

Exponen los endpoints REST consumidos por el frontend o Swagger.

---

# Estructura del Proyecto

```text
minimercado-backend/

app/
│
├── database.py
├── exceptions.py
├── main.py
├── security.py
│
├── models/
│   └── models.py
│
├── repositories/
│
├── services/
│
├── routes/
│
├── schemas/
│   └── schemas.py
│
├── utils/
│   └── dependencies.py
│
└── tests/
```

---

# Funcionalidades Implementadas

## Autenticación

* Login JWT
* Refresh Token
* Usuario autenticado
* Protección de endpoints

---

## Gestión de Roles

* Crear
* Listar
* Actualizar
* Eliminar

---

## Gestión de Usuarios

* Crear
* Consultar
* Actualizar
* Eliminar

---

## Gestión de Productos

* Crear
* Consultar
* Actualizar
* Eliminar
* Validación de stock

---

## Gestión de Clientes

* Crear
* Consultar
* Actualizar
* Eliminar

---

## Gestión de Proveedores

* Crear
* Consultar
* Actualizar
* Eliminar

---

## Gestión de Ventas

* Registrar ventas
* Actualizar ventas
* Consultar ventas
* Eliminar ventas
* Generación automática de factura

---

## Gestión de Caja

* Apertura
* Cierre
* Movimientos

---

## Gestión de Inventario

* Consultar inventario
* Registrar ingresos
* Registrar salidas
* Actualización automática del stock

---

## Reportes

* Resumen general
* Productos más vendidos
* Stock bajo
* Ventas por mes
* Top clientes
* Inventario

---

# Validaciones

## Productos

* Precio mayor a cero.
* Costo mayor a cero.
* Stock no negativo.

## Clientes

* Cédula válida.
* Correo válido.

## Proveedores

* RUC válido.
* Correo válido.

## Usuarios

* Contraseña mínima de 8 caracteres.
* Correo válido.
* Rol obligatorio.

## Ventas

* Cliente existente.
* Producto existente.
* Stock suficiente.
* Caja abierta.

---

# Instalación

## Clonar repositorio

```bash
git clone https://github.com/Redrovan/minimercado-ups-backend.git
```

## Ingresar al proyecto

```bash
cd minimercado-backend
```

## Crear entorno virtual

```bash
python -m venv venv
```

## Activar entorno

Windows

```bash
.\venv\Scripts\Activate.ps1
```

Linux

```bash
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar servidor

```bash
uvicorn app.main:app --reload
```

---

# Documentación Swagger

Una vez iniciado el servidor:

```
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden consumir todos los endpoints implementados.

---

# Pruebas Unitarias

El proyecto incorpora pruebas automáticas utilizando:

* Pytest
* Unittest
* Doctest
* Mockito

Ejecutar:

```bash
python -m pytest -v
```

Resultado obtenido:

```
12 pruebas ejecutadas
12 pruebas aprobadas
```

---

# Cobertura del Código

Para ejecutar el análisis de cobertura:

```bash
coverage run -m pytest
```

Generar reporte:

```bash
coverage report
```

Generar reporte HTML:

```bash
coverage html
```

Cobertura alcanzada:

```
97%
```

---

# Ejemplo de Reporte

Endpoint

```
GET /reportes/resumen
```

Respuesta

```json
{
  "productos": 2,
  "clientes": 1,
  "proveedores": 1,
  "ventas": 1,
  "ingresos": 25.50
}
```

---

# Repositorio

GitHub

https://github.com/Redrovan/minimercado-ups-backend

---

# Conclusiones

El desarrollo del Sistema de Gestión de Minimercado UPS permitió aplicar los principales conceptos de Ingeniería de Software relacionados con el diseño de arquitecturas por capas, desarrollo de APIs REST, persistencia de datos y control de versiones. La implementación de FastAPI facilitó la construcción de una API moderna, documentada automáticamente mediante Swagger y protegida mediante autenticación JWT. Además, la incorporación de pruebas unitarias utilizando Pytest, Unittest, Doctest y Mockito permitió verificar el correcto funcionamiento de los diferentes módulos del sistema, alcanzando una cobertura del 97% mediante Coverage.py. Finalmente, el uso de Git y GitHub permitió llevar un adecuado control de versiones y un trabajo colaborativo entre los integrantes del proyecto, obteniendo una aplicación funcional, organizada y preparada para futuras ampliaciones.
