import os
from IPython import get_ipython

ipython = get_ipython()

if ipython:
    print(" Conectando ao banco...")
    try:
        ipython.run_line_magic('load_ext', 'sql')
        
        db_url = os.environ.get('DATABASE_URL')
        
        if not db_url:
            raise ValueError("DATABASE_URL não definida")
        
        ipython.run_line_magic('sql', db_url)
        print("Conectado com sucesso!")
        
    except Exception as e:
        print(f"Erro na conexão: {e}")
        print("Verifique se DATABASE_URL está definida e o postgres está rodando")