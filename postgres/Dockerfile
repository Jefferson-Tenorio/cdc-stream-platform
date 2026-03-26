FROM postgres:18.3

# Copia o script de verificação
COPY init-check.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init-check.sh

# Copia sua configuração customizada
COPY postgresql.conf /etc/postgresql/postgresql.conf

# Define o entrypoint customizado
ENTRYPOINT ["init-check.sh"]

# Único CMD com todos os argumentos necessários
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]   