# Aplicação Web: Classificador de Cães e Gatos

Este projeto é uma aplicação web que utiliza um modelo de Deep Learning pré-treinado para classificar imagens de cães e gatos em tempo real. O sistema é composto por uma API backend (FastAPI) que serve o modelo e uma interface frontend interativa (HTML, CSS, JS) para a interação do usuário.

## Visão Geral

A aplicação permite que um usuário faça o upload de uma imagem a partir de seu dispositivo. A imagem é enviada para uma API RESTful, que utiliza um modelo PyTorch (ResNet18) pré-treinado para prever se a imagem contém um cão ou um gato. O resultado, junto com um score de confiança, é então exibido de volta para o usuário na interface web.

## Estrutura do Projeto

O repositório está organizado com uma clara separação entre o backend e o frontend.

```
.
├── api/
│   ├── server.py                     # Lógica da API com FastAPI
│   ├── cat_dog_classifier_model.pth  # Modelo pré-treinado
│   └── requirements_api.txt          # Dependências do backend
│
├── web/
│   ├── index.html                    # Estrutura do front-end
│   ├── style.css                     # Estilos do front-end
│   └── script.js                     # Lógica de interatividade do front-end
│
└── README.md                         # Este arquivo
```

## Tecnologias Utilizadas

**Backend e Modelo:**
- Python 3.8+
- FastAPI
- PyTorch
- Uvicorn
- Pillow

**Frontend:**
- HTML5
- CSS3
- JavaScript (Fetch API)

## Instalação

Siga os passos abaixo para configurar o ambiente e instalar as dependências necessárias para rodar a API.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/vickminari/cat_dog_classifier.git
    cd cat_dog_classifier
    ```

2.  **Navegue até o diretório da API:**
    ```bash
    cd api
    ```

3.  **Crie e ative um ambiente virtual:**
    É uma forte recomendação usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate    # No Windows
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements_api.txt
    ```

## Como Executar

Após a instalação, siga estes passos para iniciar a aplicação.

1.  **Inicie o Servidor da API:**
    Certifique-se de que você está no diretório `api/` com o ambiente virtual ativado.
    ```bash
    uvicorn main:app --reload
    ```
    O servidor será iniciado e estará escutando por requisições no endereço `http://127.0.0.1:8000`. Mantenha este terminal em execução.

2.  **Abra a Interface Web:**
    Navegue até a pasta `web/` no seu explorador de arquivos e abra o arquivo `index.html`.

A aplicação agora está pronta para uso. Selecione uma imagem e clique no botão para obter a classificação.

## Endpoint da API

A API expõe um único endpoint para classificação de imagens.

- **URL:** `http://127.0.0.1:8000/predict/`
- **Método:** `POST`
- **Corpo da Requisição:** `multipart/form-data`
  - **Chave:** `file`
  - **Valor:** O arquivo de imagem (ex: `my_dog.jpg`)

- **Resposta de Sucesso (Código 200):**
  ```json
  {
    "prediction": "Cachorro",
    "confidence": "99.87%"
  }
  ```

## Licença

Este projeto está licenciado sob a Licença MIT.