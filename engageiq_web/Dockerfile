# 1. Use an official, lightweight Python blueprint as the base environment
FROM python:3.11-slim

# 2. Set environment variables to optimize Python inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establish the internal working directory layout
WORKDIR /app

# 4. Install system dependencies required for scientific computing packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy the requirements file and install the exact library versions
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy your entire Django project code into the container
COPY . /app/

# 7. Expose the communication port (Django default is 8000)
EXPOSE 8000

# 8. Start the application server inside the container environment
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]