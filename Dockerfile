# Utilise une image Python officielle comme base
FROM python:3.12

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt et installe les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste de ton code
COPY . .

# Expose le port que l'application utilisera
EXPOSE 8000

# Commande pour exécuter l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]