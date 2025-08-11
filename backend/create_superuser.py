import asyncio
import sys
import os

# --- INÍCIO DO BLOCO DE CORREÇÃO ---
# Adiciona o diretório 'backend' (que é o diretório deste script)
# ao caminho de busca de módulos do Python.
# Isso garante que a importação 'from app...' funcione.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# --- FIM DO BLOCO DE CORREÇÃO ---

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select

from app.core.database import engine
from app.core.security import get_password_hash
from app.models.user_model import User

# ... (o resto do código permanece exatamente como estava) ...

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_superuser():
    async with async_session() as session:
        result = await session.execute(select(User))
        if result.scalars().first() is not None:
            print("Pelo menos um usuário já existe no banco de dados. Nenhum usuário foi criado.")
            return

        print("Nenhum usuário encontrado. Criando um novo superusuário...")
        email = input("Digite o email do superusuário: ")
        password = input("Digite a senha do superusuário: ")

        new_superuser = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_superuser=True,
        )

        session.add(new_superuser)
        await session.commit()

        print(f"Superusuário '{email}' criado com sucesso!")

if __name__ == "__main__":
    print("Iniciando script para criação de superusuário...")
    asyncio.run(create_superuser())
    print("Script finalizado.")
