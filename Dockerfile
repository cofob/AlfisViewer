FROM		python:slim

LABEL		author="cofob" maintainer="c@cofob.ru"

LABEL		org.opencontainers.image.source="https://git.sr.ht/~cofob/AlfisViewer"
LABEL		org.opencontainers.image.licenses=MIT

ARG			CACHEBUST=1
RUN			mkdir /alfisviewer
COPY		. /alfisviewer
COPY		entrypoint.sh /entrypoint.sh
RUN 		apt update && apt install libmariadb-dev gettext -y
RUN			pip3 install -r /alfisviewer/requirements.txt

EXPOSE		80/tcp

ENV			ALFIS_DB=blockchain.db

WORKDIR		/alfisviewer

VOLUME		[ "/alfisviewer" ]

CMD			[ "/bin/bash", "/entrypoint.sh" ]
