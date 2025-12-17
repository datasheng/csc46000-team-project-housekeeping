FROM python:3.12

RUN apt update
RUN apt install -y python3 python3-pip dos2unix


WORKDIR /usr/app/src


COPY AllScripts ./AllScripts
COPY AllResults ./AllResults
COPY BackupData ./BackupData
COPY CSVs ./CSVs
COPY tableauData ./tableauData
COPY run_all.sh ./
COPY libraries.txt ./

RUN pip install -r libraries.txt
RUN dos2unix run_all.sh && chmod +x run_all.sh
CMD ["bash", "./run_all.sh"]
