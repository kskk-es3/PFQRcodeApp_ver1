FROM python:latest

ENV TZ=Asia/Tokyo \
    LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8

RUN apt-get update
RUN apt-get install -y openjdk-17-jdk tzdata locales

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"
ENV CLASSPATH=/app/bin

RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone
RUN sed -i '/ja_JP.UTF-8/s/^# //g' /etc/locale.gen
RUN locale-gen
RUN dpkg-reconfigure -f noninteractive tzdata

COPY ./app /app
WORKDIR /app

RUN find . -name "*.class" -delete
RUN javac -d bin -encoding UTF-8 $(find . -name "*.java")

RUN python -m venv venv \
    && ./venv/bin/pip install --upgrade pip setuptools wheel \
    && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/python", "app.py"]