# 🔐 PLANO DE TRABALHOS ATUALIZADO - GESTÃO DE SENHAS TECNIMPOR

**Status:** Em Produção com Funcionalidades Essenciais Implementadas  
**Última Atualização:** 12/12/2025 17:56 WET  
**Tempo Total Estimado para Conclusão:** ~43 horas  
**Responsividade:** 100% (PC, Tablet, Telemóvel)

---

## ✅ FASES CONCLUÍDAS

### ✅ FASE 1 - SETUP (CONCLUÍDA)
| # | Tarefa | Status |
|---|--------|--------|
| 1.1 | Estrutura Django + Apps | ✅ Concluído |
| 1.2 | Database (SQLite) | ✅ Concluído |
| 1.3 | Modelos (Cliente, Equipamento, Senha, Utilizador, etc.) | ✅ Concluído |
| 1.4 | Migrações | ✅ Concluído |

---

### ✅ FASE 2 - AUTENTICAÇÃO & PERMISSÕES (CONCLUÍDA)
| # | Tarefa | Status |
|---|--------|--------|
| 2.1 | Login com username/email | ✅ Concluído |
| 2.2 | Logout | ✅ Concluído |
| 2.3 | Perfis de utilizador (viewer, user, admin, superadmin) | ✅ Concluído |
| 2.4 | Decoradores @login_required | ✅ Concluído |
| 2.5 | Controlo de acesso por perfil | ✅ Concluído |
| 2.6 | Dashboard com stats por perfil | ✅ Concluído |

---

### ✅ FASE 3 - GESTÃO PRINCIPAL (CONCLUÍDA)
| # | Tarefa | Status |
|---|--------|--------|
| 3.1 | Clientes (CRUD) | ✅ Concluído |
| 3.2 | Utilizadores (CRUD) | ✅ Concluído |
| 3.3 | Marcas (CRUD) | ✅ Concluído |
| 3.4 | Tipos de Controlador (CRUD) | ✅ Concluído |
| 3.5 | Versões de Controlador (CRUD) | ✅ Concluído |
| 3.6 | Modelos (CRUD) | ✅ Concluído |
| 3.7 | Modelos + Controlador (CRUD) | ✅ Concluído |
| 3.8 | Equipamentos (CRUD) | ✅ Concluído |
| 3.9 | Países (CRUD) | ✅ Concluído |

---

### ✅ FASE 4 - GERADOR SHA-256 (CONCLUÍDA)
| # | Tarefa | Status |
|---|--------|--------|
| 4.1 | Algoritmo SHA-256 (NIF + Marca + Modelo + Série) | ✅ Concluído |
| 4.2 | Suporte para senhas alfanuméricas e numéricas | ✅ Concluído |
| 4.3 | Validação de comprimento (6-16 caracteres) | ✅ Concluído |
| 4.4 | Preview em tempo real (AJAX) | ✅ Concluído |
| 4.5 | Tipo de senha automático (conforme controlador) | ✅ Concluído |

---

### ✅ FASE 5 - SENHAS (CONCLUÍDA)
| # | Tarefa | Status |
|---|--------|--------|
| 5.1 | Criação de senhas (temporária/permanente) | ✅ Concluído |
| 5.2 | Validação: impedir sobrescrita de senhas ativas | ✅ Concluído |
| 5.3 | Listar senhas com filtros por perfil | ✅ Concluído |
| 5.4 | Soft delete (marcar como inativa) | ✅ Concluído |
| 5.5 | Datas de validade (temporárias) | ✅ Concluído |
| 5.6 | Histórico de senhas por equipamento | ✅ Concluído |

---

### ✅ FASE 6 - VERIFICAÇÃO ATIVA (CONCLUÍDA)
| # | Tarefa | Status | Data |
|---|--------|--------|------|
| 6.1 | Endpoint AJAX para verificar senha ativa ao selecionar equipamento | ✅ Concluído | 12/12/2025 |
| 6.2 | Mensagem clara com tipo (temporária/permanente) | ✅ Concluído | 12/12/2025 |
| 6.3 | Exibição de dados da senha ativa (valor, datas) | ✅ Concluído | 12/12/2025 |
| 6.4 | Atalho "Ver senhas" na mensagem de aviso | ✅ Concluído | 12/12/2025 |
| 6.5 | Validação de backend (proteção POST) | ✅ Concluído | 12/12/2025 |
| 6.6 | Testes em produção | ✅ Funcional | 12/12/2025 |

---

## 🚨 FASE 0: SEGURANÇA EM EMERGÊNCIA (FAZER HOJE) - 4.5h

> **⚠️ AVISO CRÍTICO:** O projeto tem 5 vulnerabilidades que podem permitir acesso não autorizado.

### 0.1 Settings.py - Correção Imediata (1.5h)
- [ ] DEBUG = True → DEBUG = False (config via .env)
- [ ] SECRET_KEY hardcoded → variável de ambiente
- [ ] ALLOWED_HOSTS = ['*'] → configurável
- [ ] AUTH_PASSWORD_VALIDATORS = [] → validação forte (min 10 chars)
- [ ] Adicionar HTTPS/SSL em produção

**Instalar:** `pip install python-decouple`

### 0.2 URLs.py - Correção de Rotas (1.5h)
- [ ] Verificar URLs com double slash (`//`)
- [ ] Adicionar validação <int:id> a todos os IDs
- [ ] Adicionar @require_http_methods aos endpoints AJAX
- [ ] Adicionar @csrf_protect obrigatório

### 0.3 .gitignore Completo (30m)
- [ ] Criar .gitignore com Python + Django + OS patterns
- [ ] Evitar commits acidentais de .env ou db.sqlite3

### 0.4 Logging Completo (1h)
- [ ] Criar pasta `logs/`
- [ ] Configurar RotatingFileHandler
- [ ] Logs separados: errors.log, auth.log, audit.log

---

## 📍 PRIORIDADE 1: SEGURANÇA CRÍTICA (Esta semana) - 6h

### 1.1 Validação de Inputs - XSS/SQL Injection (2.5h)
- [ ] Criar forms.py completo com validators
- [ ] ClienteForm com validação NIF (regex 9 dígitos)
- [ ] UtilizadorForm com password min 10 chars
- [ ] SenhaForm com validação
- [ ] Usar forms em todas as views (nunca request.POST direto)

### 1.2 Proteção Viewer - Isolamento de Dados (1.5h)
- [ ] Criar mixins.py com decorador @check_viewer_permission
- [ ] ViewerDataFilter para filtrar querysets
- [ ] Validators no model para garantir empresa_cliente

### 1.3 Rate Limiting para Login (1h)
- [ ] Instalar django-ratelimit
- [ ] Aplicar @ratelimit(key='ip', rate='5/m') ao login
- [ ] Prevenir brute force attacks

---

## ⚡ PRIORIDADE 2: CONFIGURAÇÃO PROFISSIONAL (Esta semana) - 5h

### 2.1 Separar Settings por Ambiente (1.5h)
- [ ] Criar pasta `settings/` com base.py, local.py, production.py, test.py
- [ ] base.py: configurações comuns
- [ ] local.py: DEBUG=True, SQLite, HTTPS desativado
- [ ] production.py: DEBUG=False, PostgreSQL, HTTPS obrigatório, Redis
- [ ] test.py: memoria DB, hash MD5 para testes rápidos
- [ ] Atualizar manage.py para usar DJANGO_SETTINGS_MODULE

### 2.2 Requirements.txt Organizado (30m)
- [ ] requirements/base.txt: dependências comuns
- [ ] requirements/dev.txt: debug-toolbar, black, flake8, pytest
- [ ] requirements/prod.txt: gunicorn, psycopg2, celery, redis

### 2.3 Docker para Produção (2h)
- [ ] Criar Dockerfile com Python 3.11-slim
- [ ] Criar docker-compose.yml com serviços: db (PostgreSQL), redis, web
- [ ] Adicionar healthchecks
- [ ] Volumes para persistência de dados

---

## 📄 PRIORIDADE 3: TEMPLATES FALTANTES (Semana 2) - 8h

### 3.1 Clientes Edit (1h)
- [ ] `templates/clientes/edit.html` com form de edição

### 3.2 Equipamentos Edit (1h)
- [ ] `templates/equipamentos/edit.html` com campos: cliente, tipo, marca, modelo, número_série

### 3.3 Senhas Edit, Disable & History (2h)
- [ ] `templates/senhas/edit.html` com edição de dados
- [ ] `templates/senhas/disable.html` para desativar senhas
- [ ] `templates/senhas/view_history.html` com histórico completo

### 3.4 Utilizadores Edit (1h)
- [ ] `templates/utilizadores/edit.html` com edição de username, email, perfil

### 3.5 Gestão - Edit Files (2h)
- [ ] `templates/gestao/modelo_edit.html`
- [ ] `templates/gestao/marca_edit.html`
- [ ] `templates/gestao/pais_edit.html`
- [ ] `templates/gestao/modelo_controlador_edit.html`
- [ ] `templates/gestao/versao_controlador_edit.html`
- [ ] `templates/gestao/tipo_controlador_edit.html`

---

## 🎨 PRIORIDADE 4: UI/UX RESPONSIVIDADE (Semana 2) - 8h

### 4.1 Integrar Bootstrap 5 (2h)
- [ ] Atualizar base.html com Bootstrap CDN
- [ ] Navbar moderna com logo e dropdown do utilizador
- [ ] Sidebar responsiva (desktop: fixo, mobile: toggle)
- [ ] Alert dismissible com Bootstrap classes
- [ ] Footer com links e copyright

### 4.2 jQuery para Interatividade (2h)
- [ ] Confirmação de delete
- [ ] Auto-hide alerts (5 segundos)
- [ ] Table search em tempo real
- [ ] Form validation client-side
- [ ] AJAX preview de senha
- [ ] Copy to clipboard
- [ ] Sidebar toggle em mobile

### 4.3 Responsividade Mobile-First (2h)
- [ ] Col-12 col-md-6 col-lg-4 em todos cards
- [ ] table-responsive para tabelas
- [ ] Bootstrap grid system em formulários
- [ ] Media queries para ajustes específicos

### 4.4 Melhorias Visuais (2h)
- [ ] Ícones Font Awesome em botões
- [ ] Badges para status (Ativo/Inativo)
- [ ] Loading spinners
- [ ] Tooltips
- [ ] Modals para confirmações
- [ ] Toast notifications

---

## 📊 PRIORIDADE 5: PERFORMANCE (Semana 3) - 8h

### 5.1 Adicionar Índices de BD (1h)
- [ ] Index em Cliente: nif, designacao_social, ativo
- [ ] Index em Senha: cliente, ativa, data_criacao
- [ ] Index em Equipamento: cliente, ativo
- [ ] Executar makemigrations + migrate

### 5.2 Pagination + Filtros (2h)
- [ ] Paginator com 10 itens por página
- [ ] Filtros por NIF, designação, ativo
- [ ] Ordenação configurável (order_by)
- [ ] Template com navegação de páginas

### 5.3 Otimização de Queries (2h)
- [ ] select_related() para ForeignKeys
- [ ] prefetch_related() para ManyToMany
- [ ] annotate() com Count para estatísticas
- [ ] Eliminar N+1 queries

### 5.4 Caching (2h)
- [ ] @cache_page(60*5) em views de lista
- [ ] Cache.delete() ao guardar dados
- [ ] Redis como backend (em produção)
- [ ] Cache timeout configurável

### 5.5 Query Profiling (1h)
- [ ] Usar django-debug-toolbar em dev
- [ ] Identificar queries lentas
- [ ] Testes de carga com Apache Bench

---

## 🚀 PRIORIDADE 6: DEPLOY (Semana 3-4) - 4h

### 6.1 Deploy em Docker (2h)
- [ ] Build image: `docker-compose build`
- [ ] Run containers: `docker-compose up`
- [ ] Migrations: `docker-compose exec web python manage.py migrate`
- [ ] Superuser: `docker-compose exec web python manage.py createsuperuser`
- [ ] Static files: `docker-compose exec web python manage.py collectstatic`

### 6.2 CI/CD Pipeline (2h)
- [ ] Criar `.github/workflows/deploy.yml`
- [ ] Testes automáticos (pytest)
- [ ] Deploy automático ao fazer push para main
- [ ] Notificações de sucesso/erro

---

## ⏳ FASE 7 - MELHORIAS FUTURAS (BACKLOG)

| # | Tarefa | Prioridade |
|---|--------|-----------|
| 7.1 | Exportar lista de senhas (PDF/CSV) | Média |
| 7.2 | Relatório de acessos a senhas | Baixa |
| 7.3 | Dashboard com gráficos (Chart.js) | Média |
| 7.4 | Integração com API de backup | Baixa |
| 7.5 | Notificações de senhas a expirar | Média |
| 7.6 | Auditoria detalhada de operações | Média |
| 7.7 | Dark mode | Baixa |
| 7.8 | Internacionalização (i18n) | Baixa |
| 7.9 | Autenticação 2FA (TOTP) | Média |
| 7.10 | API REST para integrações | Média |

---

## 📊 RESUMO POR MÓDULO

### Backend (Django)
- ✅ Modelos completos com relationships
- ✅ Views com permissões e filtros por perfil
- ✅ Endpoints AJAX (preview, verificação, criação)
- ✅ Validação duplicada (cliente + servidor)
- ✅ Histórico de operações
- ⏳ Forms com validators
- ⏳ Rate limiting no login

### Frontend (HTML/CSS/JS)
- ✅ Templates responsivos
- ✅ Formulários interativos
- ✅ Preview em tempo real
- ✅ Avisos de colisão de senhas
- ⏳ Bootstrap 5 completo
- ⏳ jQuery para interatividade
- ⏳ Mobile-first responsivo

### Base de Dados
- ✅ 11 tabelas normalizadas
- ✅ Soft delete para auditoria
- ⏳ Índices nas chaves
- ⏳ Pagination para listas grandes
- ⏳ Query optimization

### DevOps
- ⏳ Docker + Docker Compose
- ⏳ PostgreSQL (produção)
- ⏳ Redis (cache)
- ⏳ CI/CD GitHub Actions

---

## 🔐 SEGURANÇA IMPLEMENTADA

✅ Autenticação por login/email + password  
✅ Controlo de acesso por perfil  
✅ CSRF protection (Django)  
✅ Validação de dados no cliente + servidor  
✅ Sem armazenamento de senhas em plaintext  
✅ Soft delete para rastreabilidade  
✅ Histórico de todas as operações  
⏳ HTTPS/SSL em produção  
⏳ Rate limiting no login  
⏳ Password validators fortes  

---

## 📁 FICHEIROS PRINCIPAIS

```
gestao_senhas/
├── settings/
│   ├── __init__.py
│   ├── base.py           ⏳ NOVO
│   ├── local.py          ⏳ NOVO
│   ├── production.py     ⏳ NOVO
│   └── test.py           ⏳ NOVO
├── urls.py               ✅ ATUALIZADO (12/12)
└── wsgi.py

core/
├── models.py             ✅ Completo
├── views.py              ✅ ATUALIZADO (12/12)
├── urls.py               ✅ ATUALIZADO (12/12)
├── forms.py              ⏳ NOVO (validators)
├── mixins.py             ⏳ NOVO (decorators)
├── admin.py              ✅ Completo
└── utils.py              ✅ SHA-256

templates/
├── base.html             ⏳ ATUALIZAR (Bootstrap)
├── dashboard.html        ✅ Completo
├── login.html            ✅ Completo
├── clientes/
│   ├── add.html          ✅ Completo
│   ├── list.html         ✅ Completo
│   └── edit.html         ⏳ NOVO
├── equipamentos/
│   ├── add.html          ✅ Completo
│   ├── list.html         ✅ Completo
│   └── edit.html         ⏳ NOVO
├── senhas/
│   ├── add.html          ✅ ATUALIZADO (12/12)
│   ├── list.html         ✅ Completo
│   ├── edit.html         ⏳ NOVO
│   ├── disable.html      ⏳ NOVO
│   └── view_history.html ⏳ NOVO
├── utilizadores/
│   ├── add.html          ✅ Completo
│   ├── list.html         ✅ Completo
│   └── edit.html         ⏳ NOVO
└── gestao/
    ├── *_add.html        ✅ Completo
    ├── *_list.html       ✅ Completo
    └── *_edit.html       ⏳ NOVO (6 ficheiros)

static/
├── css/
│   └── style.css         ⏳ ATUALIZAR (Bootstrap)
└── js/
    ├── main.js           ⏳ ATUALIZAR (jQuery)
    └── equipamento_popups.js ✅ Completo

.env                      ⏳ NOVO
.gitignore                ⏳ NOVO
docker-compose.yml        ⏳ NOVO
Dockerfile                ⏳ NOVO
requirements.txt          ⏳ ATUALIZAR
```

---

## 🎯 PRÓXIMAS AÇÕES RECOMENDADAS

### Semana 1 (Esta semana):
```
Seg: Fase 0.1-0.2 (Settings + URLs + Logging)     = 3h
Ter-Qua: Fase 1.1 (Validação + Forms)             = 2.5h
Qui: Fase 1.2-1.3 (Viewer + Rate Limiting)        = 2.5h
Sex: Fase 2.1 (Settings por ambiente)             = 1.5h
Sab: Fase 2.2-2.3 (Requirements + Docker)         = 2.5h
TOTAL: ~12h
```

### Semana 2:
```
Seg-Ter: Fase 3 (Templates faltantes)             = 8h
Qua-Sex: Fase 4 (Bootstrap + jQuery + Mobile)     = 8h
TOTAL: ~16h
```

### Semana 3:
```
Seg-Ter: Fase 5 (Índices + Pagination + Cache)    = 8h
Qua-Sex: Fase 6 (Deploy + CI/CD)                  = 4h
TOTAL: ~12h
```

---

## 📈 ROADMAP VISUAL

```
[✅ Setup]
    ↓
[✅ Auth & Permissões]
    ↓
[✅ Gestão Principal]
    ↓
[✅ Gerador SHA-256]
    ↓
[✅ Senhas]
    ↓
[✅ Verificação Ativa]
    ↓
[⏳ Segurança Emergência]
    ↓
[⏳ Segurança Crítica]
    ↓
[⏳ Config Profissional]
    ↓
[⏳ Templates + UI/UX]
    ↓
[⏳ Performance]
    ↓
[⏳ Deploy]
    ↓
[🚀 Produção 100% Profissional]
```

---

## ✨ DEPOIS DE COMPLETAR

O projeto será:
- ✅ **Seguro** para produção
- ✅ **Escalável** com Docker
- ✅ **Performante** com cache + índices
- ✅ **Protegido** contra ataques
- ✅ **Auditável** com logs
- ✅ **Manutenível** com código limpo
- ✅ **Responsivo** (PC/Tablet/Mobile)
- ✅ **Moderno** (Bootstrap 5)

**Tempo Total Estimado:** ~43 horas  
**Status Atual:** 6 fases concluídas, 1 em progresso  
**Próxima Fase:** 0 (Segurança Emergência)

---

**Última Atualização:** 12/12/2025 às 17:56 WET  
**Status Geral:** ✅ FUNCIONAL E TESTADO (com melhorias futuras mapeadas)
