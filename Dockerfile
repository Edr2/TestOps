# App that will send tests to Test Controller
FROM python:3.9-slim

# Install Chrome and Chrome Driver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_130.0.6723.91-1_amd64.deb \
    && apt install -y ./google-chrome-stable_130.0.6723.91-1_amd64.deb \
    && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.91/linux64/chrome-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . /app
WORKDIR /app

# Command to run tests
CMD ["python", "-m", "unittest", "tests/test_insider.py"]