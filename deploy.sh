# Deploy the bot to Koyeb
# Make sure you have the Koyeb CLI installed and configured

# Create a Dockerfile
echo 'FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]' > Dockerfile

# Create requirements.txt
echo 'python-telegram-bot==13.7
mega.py==1.0.8' > requirements.txt

# Build the Docker image
docker build -t telegram-mega-rename-bot .

# Push the image to a container registry (e.g., Docker Hub)
docker tag telegram-mega-rename-bot your-dockerhub-username/telegram-mega-rename-bot
docker push your-dockerhub-username/telegram-mega-rename-bot

# Deploy to Koyeb
koyeb service create telegram-mega-rename-bot --git github.com/your-username/your-repo --port 8080 --instance-type nano