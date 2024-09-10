
# API Bookstore

Este é um projeto Django criado para simular uma livraria online. Abaixo segue o passo a passo para clonar, instalar e executar o projeto em sua máquina local.

## Instalação e execução

### 1. Clonar o repositório

Crie uma pasta em sua máquina onde deseja clonar o projeto. Depois, execute o comando abaixo para clonar o repositório:

```bash
git clone https://github.com/Opalucas/bookstore.git .
```

### 2. Criar um ambiente virtual

Navegue até a pasta onde o projeto foi clonado e crie um ambiente virtual:

- **Windows:**

```bash
python -m venv venv
```

- **Linux:**

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

Ative o ambiente virtual recém-criado:

- **Windows:**

```bash
venv\Scripts\activate
```

- **Linux:**

```bash
source venv/bin/activate
```

### 4. Instalar as dependências

Com o ambiente virtual ativado, instale as dependências necessárias utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configurar o PostgreSQL

Verifique se o PostgreSQL está instalado e rodando. Caso não esteja, instale e configure o PostgreSQL conforme necessário.

Crie um banco de dados para o projeto ou atualize a configuração no arquivo `settings.py` (localizado em `bookstore/bookstore/settings.py`):

Esse é um ponto muito importante para garantir o funcionamento do projeto.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bookstore',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### 6. Configurar variáveis de ambiente

Navegue para a pasta `books` e crie um arquivo `.env` com a seguinte chave:

```bash
cd books/
```

No arquivo `.env`, adicione a seguinte linha:

```bash
API_URL=https://www.googleapis.com/books/v1/
```

### 7. Criar um superusuário

Crie um superusuário para acessar o admin do Django:

```bash
python manage.py createsuperuser
```

### 8. Executar migrações

Após configurar o banco de dados e o ambiente, aplique as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 9. Executar o servidor

Se todas as configurações foram realizadas corretamente, você pode iniciar o servidor Django com o seguinte comando:

```bash
python manage.py runserver
```

A aplicação estará disponível em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
