# python-video-integration
Projeto usado para cortar vídeos de forma escalável

Aplicativo com funcionalidades de integração http implementadas com Python, Flask, Socket.IO, FFMPEG, RabbitMQ

## Pré-requisitos
* Python 3.6
* FFmpeg (https://www.ffmpeg.org)
* VirtualEnv / VirtualEnvWrapper
* Docker (RabbitMQ)

## Características do projeto
O projeto possui 4 componentes principais:

|Componente|Descrição|
|----------|---------|
|WEB|Módulo usado como interface para usuário realizar upload e cortes em determinado vídeo através arquivos txt|
|WATCHER|Módulo que escuta diretório onde são gravados txt com as informações de corte de vídeo e envia para uma fila de corte|
|CONSUMER|Módulo escuta uma fila e consome as informações enviando para api de corte|
|API|Serviço usado para realizar o corte do video e gravação do vídeo no diretório de destino |

## Preparando o projeto

Para executar o projeto é necessário realizar o build e disponibilizar os binários para execução na raiz do projeto:
Criar uma VirtualEnv com as dependências:
```
mkvirtualenv -p python3.6 python-video-integration
workon python-video-integration
```
Realizar install das dependências e criar os binários para execução:
```
python setup.py install
```

## Criar uma instância no Docker para RabbitMQ
```
docker run -d --name rabbitmq -p 5672:5672 -p rabbitmq:3-management
```
Para executar a imagem:
```
docker start rabbitmq
```

## Para executar o projeto
Depois de executar o passo acima executar os seguintes comandos na raiz do projeto (diferentes terminais):
```
~/<CAMINHO DA ENV>/python-video-integration/bin/web
~/<CAMINHO DA ENV>/python-video-integration/bin/watcher
~/<CAMINHO DA ENV>/python-video-integration/bin/consumer
~/<CAMINHO DA ENV>/python-video-integration/bin/api
```
## Para testar o corte de vídeo
Foi incorporado swagger para testar requisições para a API, para acessar o Swagger digite o seguinte endereço:
```
http://localhost:5001/upload
```
Escolha um vídeo mp4 e realize o upload (Submit)
Selecione o seus cortes (Add cut)
Envie os cortes selecionados (Send cut)

## Diretório de destino
O diretório de destino tem o nome do vídeo cortado e dentro os cortes selecionados de acordo com os títulos.

## Serviços e urls disponíveis 

*web.py
|Metodo|URL|Descrição|
|------|---|-----------|
|GET|/upload/|Exibe a interface de upload e corte de vídeos|
|POST|/upload/|Envia o arquivo para o diretório de videos configurado na aplicação|
|XHR|/addfile/|Cria um arquivo que será processado pelo Watcher|

*api.py
|Metodo|URL|Descrição|
|------|---|-----------|
|POST|/cutvideo/|Recebe as informações do vídeo e executa os a criação de diretórios e os cortes em FFmpeg |
|XHR|//|Versão da API|