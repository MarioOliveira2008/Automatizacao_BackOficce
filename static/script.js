
	// Aguarda o HTML inteiro carregar antes de rodar o JS
document.addEventListener("DOMContentLoaded", function() {

    function carregarHistorico() {
    fetch("/historico/")
        .then(response => response.json())
        .then(documentos => {

            const historico = document.getElementById("historico");
            historico.innerHTML = "";

            documentos.forEach(doc => {

                const item = document.createElement("div");

                item.innerHTML = `
                    <h3>${doc.nome_documento}</h3>
                    <p><strong>Data:</strong> ${doc.data}</p>
                    <p><strong>Resumo:</strong> ${doc.resumo}</p>
                    <hr>
                `;

                historico.appendChild(item);
            });
        })
        .catch(error => {
            console.error("Erro ao carregar histórico:", error);
        });
}

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

                carregarHistorico();
            })
            .catch(error => {
                console.error("Erro:", error);
                mensagem.textContent = 'Erro: ' + error.message;
                mensagem.style.color = 'red';
            });
        }
    });
});

window.onload = function() {
    mostrarHistorico();
}
function salvarHistorico(){
    var contagem = localStorage.length;
    if(contagem != 7){
        /* INICIAR LISTAGEM EM BRANCO */
        localStorage.setItem('URL_0',window.location.toString());
        localStorage.setItem('URL_1',"");
        localStorage.setItem('URL_2',"");
        localStorage.setItem('URL_3',"");
        localStorage.setItem('URL_4',"");
        localStorage.setItem('URL_5',"");
        localStorage.setItem('URL_6',"");
    }else{
        /* Subir ITEM atual e abaixar mais antigos */
        for( j=0; j<6; j++){
            var salvar = true;
            if(window.location.toString() == localStorage.getItem("URL_"+j)){
                save = false;
                break;
            }
        }

        if(salvar == true){
            localStorage.setItem('URL_6',localStorage.getItem("URL_5"));
            localStorage.setItem('URL_5',localStorage.getItem("URL_4"));
            localStorage.setItem('URL_4',localStorage.getItem("URL_3"));
            localStorage.setItem('URL_3',localStorage.getItem("URL_2"));
            localStorage.setItem('URL_2',localStorage.getItem("URL_1"));
            localStorage.setItem('URL_1',localStorage.getItem("URL_0"));
            localStorage.setItem('URL_0',window.location.toString());

        }
    }
}

var vazia;
function mostrarHistorico(){
    salvarHistorico();
    var lista = document.getElementById('historico');
    vazia = lista.innerHTML;
    var contagem = localStorage.length;
    lista.innerHTML = "";
    for (i = 0; i < contagem; i++) {
        var chave = localStorage.getItem(localStorage.key(i));
        console.log(chave);
        if(chave != ""){
            lista.innerHTML += "<li>"+chave+"</li>";
        }
    }
}

function limparHistorico(){
    document.getElementById('historico').innerHTML = vazia;
    localStorage.clear();
    localStorage.setItem('URL_0',window.location.toString());
}


