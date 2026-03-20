# Vivi - TP Individual - Ingenieria de Software II

## Tabla de contenido

- [Introduccion](#introduccion)
- [Lo mas desafiante](#lo-mas-desafiante)
- [Pre-requisitos](#pre-requisitos)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Comandos](#comandos)

## Introduccion

Vivi es un servicio backend para una plataforma de eCommerce, implementado como una API REST con Python y FastAPI. Permite gestionar el ciclo de vida de productos (crear, consultar, actualizar, eliminar) y el carrito de compras de los usuarios (agregar items, visualizar, vaciar). Utiliza PostgreSQL como base de datos y corre en contenedores Docker.

## Lo mas desafiante

La parte mas desafiante del proyecto fue la configuracion del entorno de testing E2E. La combinacion de pytest con SQLAlchemy async y PostgreSQL generó problemas a la hora de testear algunas partes. La solucion fue usar el TestClient sincrono de FastAPI junto con psycopg2 para la limpieza de datos entre tests, y una base de datos de test separada para no interferir con los datos de desarrollo.

## Pre-requisitos

- Docker (>= 20.10) y Docker Compose
- Python 3.12 (solo si se quiere correr fuera de Docker)
- Make

## Testing

Los tests E2E se ejecutan contra una instancia separada de PostgreSQL definida en el compose. Se utiliza pytest como framework de testing.

- [pytest - documentacion oficial](https://docs.pytest.org/)

## CI/CD

El proyecto usa GitHub Actions para ejecutar los tests automaticamente en cada push o pull request a la rama `main`. El workflow se encuentra en `.github/workflows/test.yml`.

### Como funciona

1. Clona el repositorio
2. Copia `.env.example` a `.env` para configurar las variables de entorno
3. Construye las imagenes de Docker con `make build`
4. Levanta los servicios (app, base de datos y base de datos de test) con `make up`
5. Espera a que los servicios esten listos
6. Ejecuta los tests con `make test`
7. Baja los servicios con `make down`

### Adaptacion a produccion

Para usar este workflow en prod se podrian hacer los siguientes cambios:

- Usar secrets de GitHub para las credenciales de la base de datos en vez del `.env.example` con valores por defecto.
- Agregar un step de linting con `make lint` antes de correr los tests.
- Agregar un step de build y push de la imagen Docker a un registry (como Docker Hub o GitHub Container Registry) si los tests pasan.
- Configurar deploy automatico a un servicio de hosting despues del push al registry.

## Comandos

### Construir la imagen de Docker
```bash
make build
```

### Correr la base de datos
```bash
docker compose up -d db
```

### Correr la imagen del servicio
```bash
make up
```

### Reinicio rapido
```bash
make restart
```

Esto levanta tanto la base de datos como el servicio. El servicio queda disponible en `http://localhost:8080`.

### Correr los tests
#### Todos
```bash
make test
```

#### Test de Products
```bash
make test-products
```

#### Los de Cart
```bash
make test-cart
```