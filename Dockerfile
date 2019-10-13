FROM ubuntu:18.04
RUN apt update -y && apt install -y python3 python3-pip iputils-ping nmap
RUN pip3 install requests feedparser docopt
RUN mkdir /root/node /token
COPY node.py /root/node.py
COPY node /root/node
WORKDIR /root
CMD ["python3", "node.py", "-a", "api.tagazoo.com:443", "-s", "https"]