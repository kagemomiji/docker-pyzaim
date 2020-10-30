FROM python:3.7-buster

LABEL maintainer="@kagemomiji"

ENV CHROME_VERSION=86.0.4240.111-1_amd64

RUN  sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  apt update && \
  wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_$CHROME_VERSION.deb && \
  dpkg -i ./google-chrome-stable_$CHROME_VERSION.deb ; apt install -y -f  && \
  apt clean && \
  rm -rf /var/lib/apt/lists/* && \
  rm ./google-chrome-stable_$CHROME_VERSION.deb

RUN useradd -m -s /bin/bash zaim

COPY . /home/zaim/pyzaim

RUN chown -R zaim:zaim /home/zaim/pyzaim

USER zaim

WORKDIR /home/zaim/pyzaim

RUN pip install -r requirements.txt

ENTRYPOINT ["./main.py"]
