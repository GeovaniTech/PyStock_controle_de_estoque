# Como rodar o PyStock

## Passos Iniciais

1# Instalar o Python: https://www.python.org/

2# Adicionar o arquivo pip do python nas variáveis de Ambiente do Windows

3# ☢️ATENÇÃO! O projeto não está rodando pelo vscode

- Instalar o PyCharm: https://www.jetbrains.com/pycharm/

#4 Instalar WampServer: https://www.wampserver.com/en/

- 1. Abrir phpMyAdmin

![image](https://user-images.githubusercontent.com/84943777/236705219-c8c76ede-f48a-4de5-9a07-09325f894551.png)

- 2. Importar Base de dados

![image](https://user-images.githubusercontent.com/84943777/236705282-cd02f5d4-0ee8-4a11-8ae1-e40861f7eeb6.png)

4# Configurar porta que está rodando o banco de dados do WampServer (Geralmente 3306/3307)
![image](https://user-images.githubusercontent.com/84943777/236705354-46c358f9-2224-4c9a-baf4-ecb39e522c0c.png)

5# Importar todas as dependências
- Ex: <code>pip install openpyxl</code>

![image](https://user-images.githubusercontent.com/84943777/236705419-d2c67590-b888-4b9c-a4bb-dd07dbd5fbd0.png)

6# Agora resta rodar o projeto!

## Gerando o Build/Executável

1# Instalar o Cx_Freeze

<code>pip install Cx_Freeze</code>

2# Abrir CMD/PowerShell na pasta onde está o arquivo setup.py

3# Rodar o comando <code>py setup.py build</code>

4# Abrir pasta build e rodar o executável.
