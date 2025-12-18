# 1. Ir para a localização do projeto
cd /d "caminho projeto"

# 2. Criar ambiente virtual
python -m venv venv
Python3 -m vens .venv

# 3. Ativar ambiente virtual
venv\Scripts\activate
source .venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

--- se não tiver requirements.txt
pip install django
pip install pillow


# 5. Aplicar migrations
python manage.py makemigrations
python manage.py migrate

# 6. Criar superusuário (admin) - se não tiver ainda feito 
python manage.py createsuperuser

# 7. Arrancar servidor
python manage.py runserver

# 8. Aceder ao projeto
http://localhost:8000/login/
http://127.0.0.0:8000/login/