	// Aguarda o HTML inteiro carregar antes de rodar o JS
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('enviarArquivo');
    const entradaArquivo = document.getElementById('arquivo');
    const mensagem = document.getElementById('mensagem');
    const resultadoDiv = document.getElementById('resultado');
    const paginasSpan = document.getElementById('paginas');
    const resumoSpan = document.getElementById('resumo');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); 
        const arquivo = entradaArquivo.files[0];
        
        if (arquivo) {
            // Mensagem de loading
            mensagem.textContent = 'Lendo PDF e consultando a IA...';
            mensagem.style.color = 'blue';
            resultadoDiv.style.display = 'none';

            const formData = new FormData();   
            formData.append('arquivo', arquivo); 

            fetch("/uploads/", {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.detail) { throw new Error(data.detail); }
                
                mensagem.textContent = 'Sucesso!';
                mensagem.style.color = 'green'; 
                
                // Pega os dados do Python e joga na tela
                paginasSpan.textContent = data.total_paginas;
                resumoSpan.textContent = data.resposta_ia;
                resultadoDiv.style.display = 'block'; // Deixa o bloco visível
            })
            .catch(error => {
                console.error("Erro:", error);
                mensagem.textContent = 'Erro: ' + error.message;
                mensagem.style.color = 'red';
            });
        }
    });
});