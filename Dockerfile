FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN set -ex;\
    apt-get update && \
    apt-get install -y --fix-missing \
    python3-opencv \
    aria2

RUN mkdir /is
WORKDIR /is

COPY requirements.txt /is/
RUN pip3 install --no-cache-dir -r /is/requirements.txt

COPY . /is/

RUN aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --header="Authorization: Bearer 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" https://huggingface.co/HCMUE-Research/eton-Image-Search-VIT/resolve/main/pytorch_model.bin -d models/VIT-Best-model -o pytorch_model.bin
RUN aria2c --console-log-level=error -c -x 16 -s 16 -k 1M --header="Authorization: Bearer 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" https://huggingface.co/HCMUE-Research/eton-Image-Search-VIT/resolve/main/optimizer.pt -d models/VIT-Best-model -o optimizer.pt

CMD ["gunicorn", "--timeout", "600", "--threads", "3", "--bind", "0.0.0.0:5000", "route:app"]
