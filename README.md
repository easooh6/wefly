# 🎬 Cinema Ticket Booking System# 🎬 Cinema Ticket Booking System




![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)

![React](https://img.shields.io/badge/React-18.2+-61DAFB?style=flat-square&logo=react&logoColor=black)![React](https://img.shields.io/badge/React-18.2+-61DAFB?style=flat-square&logo=react&logoColor=black)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192?style=flat-square&logo=postgresql&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-316192?style=flat-square&logo=postgresql&logoColor=white)

![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat-square&logo=redis&logoColor=white)![Redis](https://img.shields.io/badge/Redis-6+-DC382D?style=flat-square&logo=redis&logoColor=white)

## About## About



Web application for automated cinema ticket booking. Users can browse movies, select showtimes, book seats through an interactive hall layout, and manage their cart. Admins have full control over movies, halls, seats, and sessions through a dedicated panel.Web application for automated cinema ticket booking. Users can browse movies, select showtimes, book seats through an interactive hall layout, and manage their cart. Admins have full control over movies, halls, seats, and sessions through a dedicated panel.



## Tech Stack## Tech Stack



**Backend:****Backend:**

- FastAPI - async web framework- FastAPI - async web framework

- SQLAlchemy - async ORM for PostgreSQL- SQLAlchemy - async ORM for PostgreSQL

- PostgreSQL - relational database- PostgreSQL - relational database

- Redis - caching system- Redis - caching system

- JWT - token-based authentication- JWT - token-based authentication

- Alembic - database migrations- Alembic - database migrations

- Pytest - testing framework- Pytest - testing framework



**Frontend:****Frontend:**

- React - UI library- React - UI library

- Axios - HTTP client with interceptors- Axios - HTTP client with interceptors

- CSS3 - responsive design- CSS3 - responsive design



## Key Features## Key Features



- Real-time seat selection with interactive hall layout- Real-time seat selection with interactive hall layout

- JWT authentication with automatic token refresh- JWT authentication with automatic token refresh

- Redis caching (20x performance improvement)- Redis caching (20x performance improvement)

- Role-based access control (admin/user)- Role-based access control (admin/user)

- Async architecture for high concurrency- Async architecture for high concurrency

- 3NF database normalization- 3NF database normalization

- 80%+ test coverage- 80%+ test coverage



## Quick Start## Quick Start



```bash```bash

# Clone# Clone

git clone https://github.com/easooh6/movie_full.gitgit clone https://github.com/easooh6/movie_full.git

cd movie_fullcd movie_full



# Backend# Backend

cd pythonproject/backcd pythonproject/back

python -m venv venvpython -m venv venv

source venv/bin/activatesource venv/bin/activate

pip install -r requirements.txtpip install -r requirements.txt

alembic upgrade headalembic upgrade head

uvicorn src.main:app --reloaduvicorn src.main:app --reload



# Frontend# Frontend

cd ../frontcd ../front

npm installnpm install

npm startnpm start

``````



**Access:****Access:**

- Frontend: http://localhost:3000- Frontend: http://localhost:3000

- API: http://localhost:8000- API: http://localhost:8000

- Docs: http://localhost:8000/docs- Docs: http://localhost:8000/docs

