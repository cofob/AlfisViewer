FROM		python

LABEL		author="cofob" maintainer="c@cofob.ru"

LABEL		org.opencontainers.image.source="https://git.sr.ht/~cofob/AlfisViewer"
LABEL		org.opencontainers.image.licenses=MIT

RUN			mkdir /alfisviewer
COPY		. /alfisviewer
COPY		entrypoint.sh /entrypoint.sh
RUN 		apt update && apt install libmariadb-dev -y
RUN			pip3 install -r /alfisviewer/requirements.txt

EXPOSE		8000/tcp

ENV			ALFIS_DB=blockchain.db

WORKDIR		/alfisviewer

VOLUME		["/alfisviewer"]

CMD			[ "/bin/bash", "/entrypoint.sh" ]