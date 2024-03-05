FROM python:3.10



# Set the environment variable to unbuffered mode to see output logs in real-time
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the requirements file to leverage Docker cache
COPY ./api_fast_api/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy the application source code to the container
COPY ./api_fast_api /app


# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

# Healthcheck to monitor the application
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

# IMPORTANT
# This is the port that FastAPI will be listening on inside the container
EXPOSE 8000