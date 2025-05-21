# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports for Streamlit and FastAPI
EXPOSE 8000
#EXPOSE 8501

# Start both FastAPI and Streamlit using a script
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --server.address 0.0.0.0"]

