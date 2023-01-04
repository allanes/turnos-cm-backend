# turnos-cm-backend

cd turnos-cm-backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
pip install -r requirements.txt
   

Borrar el contenido de sql_app/alembic/revision

cd sql_app
alembic revision
cd ..
uvicorn main:app

Para cargar datos a la db:
localhost:8000/docs/init_db