Catraca Inteligente

Sistema acadêmico de demonstração de uma catraca inteligente, desenvolvido com Raspberry Pi, Arduino e tecnologias web.

O projeto tem como objetivo integrar hardware e software para demonstrar um sistema de controle de acesso, com registro de eventos, monitoramento e visualização em um dashboard web.

🛠️ Tecnologias utilizadas

Python – linguagem principal do backend.

FastAPI – criação da API.

RabbitMQ – comunicação e processamento de eventos.

SQLite – armazenamento do histórico de acessos.

HTML, CSS e JavaScript – desenvolvimento da interface web.

Raspberry Pi – servidor principal do sistema.

Arduino Uno – integração com o hardware.

Câmera CSI – captura de imagens.

✨ Funcionalidades

Dashboard para monitoramento do sistema.

Simulação de acessos autorizados e negados.

Registro e consulta do histórico de eventos.

Integração entre FastAPI e RabbitMQ.

Armazenamento dos eventos em banco de dados SQLite.

Comunicação serial com Arduino.

Verificação do status dos componentes.

Captura e visualização de imagens pela câmera.

🏗️ Arquitetura do projeto

O sistema é dividido em três partes principais:

Frontend: interface web desenvolvida com HTML, CSS e JavaScript.

Backend: servidor FastAPI responsável por receber solicitações, processar eventos e integrar os serviços.

Hardware: Raspberry Pi, Arduino Uno e câmera, utilizados na integração física e demonstração do sistema.
