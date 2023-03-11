FROM python:3.10-slim

WORKDIR /app

COPY bot.py /app

# Install required dependencies
RUN pip install -y pyTelegramBotAPI
RUN pip install -y certifi
RUN pip install -y jsonpickle
RUN pip install -y requests
RUN pip install -y telebot


# Expose the port the application will run on
EXPOSE 8080


CMD ["python3", "bot.py"]
