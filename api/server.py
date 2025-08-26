from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io

# 1. INICIALIZAÇÃO DA API
app = FastAPI(title="API Classificadora de Cães e Gatos")

# Configuração do CORS (Cross-Origin Resource Sharing)
# Permite que o nosso front-end (em outra "origem") acesse esta API.
origins = ["*"]  # Para desenvolvimento. Em produção, restrinja para o domínio do seu site.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CARREGAMENTO DO MODELO
# O modelo precisa ter a mesma arquitetura de quando foi treinado.
model = models.resnet18()
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)  # 2 classes: Gato e Cão

# Carregar os pesos salvos do modelo
# Certifique-se que o arquivo .pth está na mesma pasta que este script.
try:
    model.load_state_dict(torch.load("cat_dog_classifier_model.pth", map_location=torch.device('cpu')))
except FileNotFoundError:
    print("Erro: Arquivo 'cat_dog_classifier_model.pth' não encontrado.")
    print("Certifique-se de copiá-lo para a pasta 'api/'.")
    exit()

model.eval()  # !! IMPORTANTE: Colocar o modelo em modo de avaliação

# Nomes das classes (precisa ser na mesma ordem do treinamento, geralmente alfabética)
class_names = ['cat', 'dog'] 

# 3. TRANSFORMAÇÕES DA IMAGEM
# Devem ser as mesmas transformações usadas na VALIDAÇÃO durante o treinamento.
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 4. FUNÇÃO DE PREDIÇÃO
def predict_image(image_bytes: bytes):
    """Função para receber bytes de uma imagem e retornar a previsão."""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image_tensor = transform(image).unsqueeze(0)  # Adiciona dimensão de batch

    with torch.no_grad():
        outputs = model(image_tensor)
        # Aplica softmax para obter probabilidades
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
        
    predicted_class = class_names[predicted_idx.item()]
    confidence_score = confidence.item()

    return predicted_class, confidence_score

# 5. DEFINIÇÃO DO ENDPOINT DA API
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint que recebe um arquivo de imagem, faz a predição e retorna
    a classe (gato ou cachorro) e a confiança da previsão.
    """
    image_bytes = await file.read()
    predicted_class, confidence = predict_image(image_bytes)

    # Traduzindo para português para o front-end
    if predicted_class == 'dog':
        classe_traduzida = "Cachorro"
    else:
        classe_traduzida = "Gato"

    return {
        "prediction": classe_traduzida,
        "confidence": f"{confidence:.2%}" # Formata como porcentagem
    }

@app.get("/test")
def read_root():
    return {"message": "Bem-vindo à API de Classificação de Cães e Gatos!"}