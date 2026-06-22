// Arquivo: static/script.js
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('enviarArquivo');
    const entradaArquivo = document.getElementById('arquivo');
    const entradaPergunta = document.getElementById('perguntaUpload'); // Puxa o texto do prompt
    const mensagem = document.getElementById('mensagem');
    const resultadoDiv = document.getElementById('resultado');
    const paginasSpan = document.getElementById('paginas');
    const resumoSpan = document.getElementById('resumo');

    function carregarHistoricoDoBanco() {
        fetch("/historico/")
            .then(response => response.json())
            .then(dadosDoBanco => {
                const painel = document.getElementById("historico");
                painel.innerHTML = ""; 

                if (dadosDoBanco.length === 0) {
                    painel.innerHTML = "<p style='text-align:center; color:#9aa4b2;'>O histórico está vazio.</p>";
                    return;
                }

                dadosDoBanco.forEach(doc => {
                    const item = document.createElement("div");
                    item.style.padding = "15px";
                    item.style.marginTop = "10px";
                    item.style.background = "#252b3b";
                    item.style.borderRadius = "10px";
                    item.style.borderLeft = "4px solid #3b82f6";
                    
                    item.innerHTML = `
                        <h3 style="color: #6ea8fe; margin-bottom:5px;">${doc.nome_arquivo}</h3>
                        <p style="font-size:0.9rem; color:#9aa4b2;"><strong>Páginas:</strong> ${doc.total_paginas}</p>
                        <p style="color:#d1d5db; margin-top:5px; white-space: pre-wrap;"><strong>Resposta da IA:</strong><br>${doc.resposta_ia}</p>
                    `;
                    painel.appendChild(item);
                });
            });
    }

    carregarHistoricoDoBanco();

    form.addEventListener('submit', (event) => {
        event.preventDefault(); 
        const arquivo = entradaArquivo.files[0];
        const perguntaDigitada = entradaPergunta.value; 
        
        if (arquivo && perguntaDigitada) {
            mensagem.textContent = 'Lendo PDF e processando seu prompt...';
            mensagem.style.color = '#7dd3fc';
            resultadoDiv.style.display = 'none';

            // Junta o arquivo e a pergunta no mesmo pacote
            const formData = new FormData();   
            formData.append('arquivo', arquivo); 
            formData.append('pergunta', perguntaDigitada); 

            fetch("/uploads/", {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.detail) { throw new Error(data.detail); }
                
                mensagem.textContent = 'Sucesso e salvo no banco de dados!';
                mensagem.style.color = '#10b981'; 
                
                paginasSpan.textContent = data.total_paginas;
                resumoSpan.textContent = data.resposta_ia;
                resultadoDiv.style.display = 'block'; 

                carregarHistoricoDoBanco();
            })
            .catch(error => {
                mensagem.textContent = 'Erro: ' + error.message;
                mensagem.style.color = '#ef4444';
            });
        }
    });
});

function limparHistorico() {
    if(confirm("Tem certeza que deseja apagar os dados do SQLite?")) {
        fetch("/limpar-historico/")
            .then(() => {
                window.location.reload(); 
            });
    }
}