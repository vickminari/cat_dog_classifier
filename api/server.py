from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import io

# Inicializando API
app = FastAPI(title="API Classificadora de Cães e Gatos")

# Configuração do CORS (Cross-Origin Resource Sharing)
# Permite que o nosso front-end (em outra "origem") acesse esta API.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregamento do modelo
# O modelo precisa ter a mesma arquitetura de quando foi treinado.
model = models.resnet18()
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 2)

# Carregar os pesos salvos do modelo
try:
    model.load_state_dict(torch.load("cat_dog_classifier_model.pth", map_location=torch.device('cpu')))
except FileNotFoundError:
    print("Erro: Arquivo 'cat_dog_classifier_model.pth' não encontrado.")
    exit()

model.eval()  # Colocar o modelo em modo de avaliação (Importante)

# Nomes das classes
class_names = ['cat', 'dog'] 

# Transformações da imagem
# Devem ser as mesmas transformações usadas na VALIDAÇÃO durante o treinamento.
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Função de predição
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

# Definição do endpoint principal da API
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint que recebe um arquivo de imagem, faz a predição e retorna
    a classe (gato ou cachorro) e a confiança da previsão.
    """
    image_bytes = await file.read()
    predicted_class, confidence = predict_image(image_bytes)

    if predicted_class == 'dog':
        classe_traduzida = "Cachorro"
    else:
        classe_traduzida = "Gato"

    return {
        "prediction": classe_traduzida,
        "confidence": f"{confidence:.2%}"
    }

# Apenas para teste
@app.get("/test")
def read_root():
    return {"message": "Bem-vindo à API de Classificação de Cães e Gatos!"}