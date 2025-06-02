FROM python:latest

ENV TZ=Asia/Tokyo

RUN apt-get update
RUN apt-get install -y openjdk-17-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV CLASSPATH=/app/bin

RUN apt-get install -y tzdata
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

COPY ./app /app
WORKDIR /app

# RUN find . -name "*.class" -delete
RUN javac -source 17 -target 17 -d bin -encoding UTF-8 $(find . -name "*.java")

RUN python -m venv venv \
    && ./venv/bin/pip install --upgrade pip setuptools wheel \
    && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/python", "app.py"]