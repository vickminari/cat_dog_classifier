// script.js

const uploadForm = document.getElementById('uploadForm');
const imageUpload = document.getElementById('imageUpload');
const imagePreviewContainer = document.getElementById('imagePreview');
const imagePreview = document.querySelector('.image-preview__image');
const previewDefaultText = document.querySelector('.image-preview__default-text');
const resultDiv = document.getElementById('result');
const loader = document.getElementById('loader');

const API_ENDPOINT = 'http://127.0.0.1:8000/predict/';

// Evento para mostrar a pré-visualização da imagem
imageUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        previewDefaultText.style.display = 'none';
        imagePreview.style.display = 'block';

        reader.addEventListener('load', () => {
            imagePreview.setAttribute('src', reader.result);
        });

        reader.readAsDataURL(file);
    } else {
        previewDefaultText.style.display = 'block';
        imagePreview.style.display = 'none';
        imagePreview.setAttribute('src', "");
    }
});

// Evento para enviar a imagem para a API
uploadForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impede o envio padrão do formulário

    const file = imageUpload.files[0];
    if (!file) {
        resultDiv.innerHTML = 'Por favor, selecione uma imagem primeiro.';
        return;
    }

    // Mostrar o loader e limpar o resultado anterior
    loader.style.display = 'block';
    resultDiv.innerHTML = '';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            displayResult(data);
        } else {
            resultDiv.innerHTML = 'Erro ao classificar a imagem. Tente novamente.';
        }
    } catch (error) {
        console.error('Erro de rede:', error);
        resultDiv.innerHTML = 'Não foi possível conectar à API. Verifique se ela está em execução.';
    } finally {
        // Esconder o loader
        loader.style.display = 'none';
    }
});

function displayResult(data) {
    const prediction = data.prediction;
    const confidence = data.confidence;

    resultDiv.innerHTML = `Eu tenho ${confidence} de certeza que isso é um... <strong>${prediction}!</strong>`;
}
