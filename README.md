# turnos-cm-backend

cd turnos-cm-backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
pip install -r requirements.txt
   
cd sql_app
alembic revision

uvicorn main:app