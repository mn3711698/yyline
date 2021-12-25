FROM bitnami/git:2.33.0 AS downloader
WORKDIR /opt
RUN git clone -b https://github.com/mn3711698/yyline.git
WORKDIR /opt/yyline
RUN rm -rf .git
RUN rm config.json
RUN rm must_edit_config.json

FROM flamhaze5946/lite-trade:20211109.1.0.0
RUN mkdir -p /var/games
COPY --from=downloader /opt/yyline /var/games/yyline

WORKDIR /var/games/yyline
# RUN pip install --ignore-installed -r requirements_l.txt

VOLUME [ "/var/games/yyline/config.json" ]