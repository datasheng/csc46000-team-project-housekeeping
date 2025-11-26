FROM python:3.12

RUN apt update
RUN apt install -y python3 python3-pip


WORKDIR /usr/app/src


COPY AllScripts ./AllScripts
COPY AllResults ./AllResults
COPY BackupData ./BackupData
COPY CSVs ./CSVs
COPY run_all.sh ./
COPY libraries.txt ./

RUN pip install -r libraries.txt
RUN chmod +x run_all.sh
CMD ["./run_all.sh"]