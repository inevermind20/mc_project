// MODAIS POP-UP
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Fechar ao clicar fora
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ADICIONAR CLIENTE
function adicionarCliente() {
    const nif = document.getElementById('novo_cliente_nif').value;
    const designacao = document.getElementById('novo_cliente_designacao').value;
    const pais = document.getElementById('novo_cliente_pais').value;

    if (!nif || !designacao || !pais) {
        alert('Preencha todos os campos obrigatórios!');
        return;
    }

    fetch('/ajax/cliente/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ nif, designacao_social: designacao, pais })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const select = document.getElementById('cliente_select');
            const option = new Option(data.nome, data.id, true, true);
            select.add(option);
            closeModal('clienteModal');
            alert('✅ Cliente adicionado com sucesso!');
        } else {
            alert('❌ Erro: ' + data.error);
        }
    });
}

// ADICIONAR MARCA
function adicionarMarca() {
    const nome = document.getElementById('nova_marca_nome').value;

    if (!nome) {
        alert('Digite o nome da marca!');
        return;
    }

    fetch('/ajax/marca/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ nome })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const select = document.getElementById('marca_select');
            const option = new Option(data.nome, data.id, true, true);
            select.add(option);

            // Atualizar também no modal de modelo
            const selectModelo = document.getElementById('novo_modelo_marca');
            const optionModelo = new Option(data.nome, data.id);
            selectModelo.add(optionModelo);

            closeModal('marcaModal');
            carregarModelos();
            alert('✅ Marca adicionada com sucesso!');
        } else {
            alert('❌ Erro: ' + data.error);
        }
    });
}

// ADICIONAR MODELO
function adicionarModelo() {
    const marca_id = document.getElementById('novo_modelo_marca').value;
    const nome = document.getElementById('novo_modelo_nome').value;

    if (!marca_id || !nome) {
        alert('Preencha todos os campos!');
        return;
    }

    fetch('/ajax/modelo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ marca_id, nome })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            closeModal('modeloModal');
            carregarModelos();
            alert('✅ Modelo adicionado com sucesso!');
        } else {
            alert('❌ Erro: ' + data.error);
        }
    });
}

// ADICIONAR TIPO CONTROLADOR
function adicionarTipoControlador() {
    const nome = document.getElementById('novo_tipo_controlador_nome').value;

    if (!nome) {
        alert('Digite o nome do tipo de controlador!');
        return;
    }

    fetch('/ajax/tipo-controlador/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ nome })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const select = document.getElementById('tipo_controlador_select');
            const option = new Option(data.nome, data.id, true, true);
            select.add(option);

            // Atualizar também no modal de versão
            const selectVersao = document.getElementById('nova_versao_tipo');
            const optionVersao = new Option(data.nome, data.id);
            selectVersao.add(optionVersao);

            closeModal('tipoControladorModal');
            carregarVersoes();
            alert('✅ Tipo de Controlador adicionado!');
        } else {
            alert('❌ Erro: ' + data.error);
        }
    });
}

// ADICIONAR VERSÃO CONTROLADOR
function adicionarVersaoControlador() {
    const tipo_id = document.getElementById('nova_versao_tipo').value;
    const versao = document.getElementById('nova_versao_numero').value;

    if (!tipo_id || !versao) {
        alert('Preencha todos os campos!');
        return;
    }

    fetch('/ajax/versao-controlador/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ tipo_controlador_id: tipo_id, versao })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            closeModal('versaoControladorModal');
            carregarVersoes();
            alert('✅ Versão de Controlador adicionada!');
        } else {
            alert('❌ Erro: ' + data.error);
        }
    });
}

// CARREGAR MODELOS (quando marca muda)
function carregarModelos() {
    const marcaId = document.getElementById('marca_select').value;
    const modeloSelect = document.getElementById('modelo_select');

    if (!marcaId) {
        modeloSelect.innerHTML = '<option value="">Selecione a marca primeiro...</option>';
        return;
    }

    // Aqui você pode fazer um fetch para buscar modelos da marca
    // Por enquanto, mantém os modelos existentes (precisa endpoint no backend)
    modeloSelect.innerHTML = '<option value="">Carregando...</option>';

    fetch(`/ajax/modelos-por-marca/${marcaId}/`)
        .then(r => r.json())
        .then(data => {
            modeloSelect.innerHTML = '<option value="">Selecione o modelo...</option>';
            data.modelos.forEach(m => {
                const option = new Option(m.nome, m.id);
                modeloSelect.add(option);
            });
        })
        .catch(() => {
            modeloSelect.innerHTML = '<option value="">Erro ao carregar modelos</option>';
        });
}

// CARREGAR VERSÕES (quando tipo controlador muda)
function carregarVersoes() {
    const tipoId = document.getElementById('tipo_controlador_select').value;
    const versaoSelect = document.getElementById('versao_controlador_select');

    if (!tipoId) {
        versaoSelect.innerHTML = '<option value="">Selecione o tipo primeiro...</option>';
        return;
    }

    versaoSelect.innerHTML = '<option value="">Carregando...</option>';

    fetch(`/ajax/versoes-por-tipo/${tipoId}/`)
        .then(r => r.json())
        .then(data => {
            versaoSelect.innerHTML = '<option value="">Selecione a versão...</option>';
            data.versoes.forEach(v => {
                const option = new Option(v.versao, v.id);
                versaoSelect.add(option);
            });
        })
        .catch(() => {
            versaoSelect.innerHTML = '<option value="">Erro ao carregar versões</option>';
        });
}

// CARREGAR MODELO+CONTROLADOR (quando modelo e versão estão selecionados)
function carregarModeloControladores() {
    const modeloId = document.getElementById('modelo_select').value;
    const versaoId = document.getElementById('versao_controlador_select').value;
    const mcSelect = document.getElementById('modelo_controlador_select');

    if (!modeloId || !versaoId) {
        mcSelect.innerHTML = '<option value="">Selecione modelo e controlador primeiro...</option>';
        return;
    }

    mcSelect.innerHTML = '<option value="">Carregando...</option>';

    fetch(`/ajax/modelo-controlador/${modeloId}/${versaoId}/`)
        .then(r => r.json())
        .then(data => {
            if (data.exists) {
                mcSelect.innerHTML = `<option value="${data.id}" selected>${data.nome}</option>`;
            } else {
                mcSelect.innerHTML = '<option value="criar" selected>Será criado automaticamente</option>';
            }
        })
        .catch(() => {
            mcSelect.innerHTML = '<option value="">Erro ao verificar combinação</option>';
        });
}
