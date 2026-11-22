# ✦ Meeting Intelligence

Assistente de inteligência artificial para transformar transcrições de reuniões em **resumos, decisões, tarefas, responsáveis, prazos e pendências rastreáveis**.

A solução utiliza a Cohere para analisar a transcrição, Pydantic para validar a estrutura dos resultados e uma camada adicional para verificar se todas as evidências apresentadas pela IA realmente existem no texto original.

> **Status:** MVP funcional, avaliado e pronto para publicação.

---

## Aplicação publicada

O link da aplicação será adicionado após a publicação no Render.

> A aplicação utiliza uma instância gratuita e pode levar aproximadamente um minuto para iniciar após um período sem acessos.

---

## Problema de negócio

Reuniões costumam gerar decisões, tarefas e pendências que nem sempre são registradas de maneira estruturada.

Isso pode causar:

- perda de decisões importantes;
- tarefas sem acompanhamento;
- responsáveis e prazos pouco claros;
- dificuldade para preparar atas;
- divergências sobre o que foi efetivamente acordado;
- retrabalho após a reunião;
- ausência de rastreabilidade entre o registro e a fala original.

---

## Solução

O Meeting Intelligence recebe uma transcrição em TXT ou texto colado e transforma o conteúdo em uma análise estruturada.

A aplicação identifica:

- resumo da reunião;
- assuntos principais;
- decisões explicitamente tomadas;
- tarefas e encaminhamentos;
- responsáveis explicitamente associados;
- prazos explicitamente associados;
- pendências;
- sugestões ainda não aprovadas;
- evidências literais da transcrição.

Antes da exportação, a pessoa usuária pode revisar as tarefas, corrigir responsáveis e prazos ou remover itens da ata final.

---

## Diferenciais

- Responsáveis não são inferidos apenas porque um nome foi mencionado.
- Prazos não são preenchidos quando não aparecem explicitamente.
- Sugestões não são automaticamente tratadas como decisões.
- Assuntos discutidos não são automaticamente transformados em tarefas.
- Cada item extraído apresenta uma evidência literal.
- As evidências são verificadas automaticamente contra a transcrição.
- A análise da IA é validada por um schema Pydantic.
- A versão final permanece sob revisão humana.
- Campos ausentes são apresentados como `Não informado`.

---

## Funcionalidades

### Entrada da reunião

- Seleção de transcrição fictícia do projeto.
- Upload de arquivo TXT.
- Colagem direta de texto.
- Validação de arquivos vazios ou muito curtos.
- Leitura de UTF-8, UTF-8 com BOM e Latin-1.

### Análise com IA

- Resumo factual.
- Identificação dos assuntos principais.
- Extração de decisões.
- Extração de tarefas.
- Extração de responsáveis e prazos explícitos.
- Identificação de pendências.
- Separação de sugestões não aprovadas.
- Saída estruturada em JSON.

### Validação

- Schema Pydantic com campos obrigatórios.
- Rejeição de campos inesperados.
- Preservação de valores ausentes como `null`.
- Verificação literal das evidências.
- Sinalização de evidências não encontradas.

### Revisão humana

- Edição da descrição das tarefas.
- Correção ou inclusão de responsáveis.
- Correção ou inclusão de prazos.
- Exclusão de tarefas da versão final.
- Preservação da evidência original.
- Prévia das tarefas revisadas.

### Exportações

- Ata em Markdown.
- Tarefas em CSV compatível com Excel.
- Análise completa em JSON.

---

## Como funciona

```text
Transcrição TXT ou texto colado
        ↓
Leitura e validação
        ↓
Cohere Chat API
        ↓
Resposta estruturada em JSON
        ↓
Validação com Pydantic
        ↓
Verificação das evidências
        ↓
Exibição dos resultados
        ↓
Revisão humana das tarefas
        ↓
Ata em Markdown
Tarefas em CSV
Análise em JSON
```

---

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python 3.12 | Linguagem principal |
| Streamlit | Interface |
| Cohere API | Análise estruturada da reunião |
| Pydantic | Validação do schema |
| python-dotenv | Variáveis de ambiente |
| CSV e JSON | Exportação dos resultados |
| Git e GitHub | Versionamento |
| GitHub Codespaces | Ambiente de desenvolvimento |
| Render | Hospedagem pública |

---

## Estrutura do projeto

```text
meeting-intelligence/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   └── styles.css
├── data/
│   └── sample/
│       ├── reuniao_ficticia.txt
│       ├── reuniao_avaliacao.txt
│       ├── ata_ficticia.md
│       ├── ata_exportada.md
│       ├── tarefas_exportadas.csv
│       └── analise_exportada.json
├── docs/
├── evaluation/
├── src/
│   ├── __init__.py
│   ├── evidence_checker.py
│   ├── exporters.py
│   ├── meeting_analyzer.py
│   ├── minutes_generator.py
│   ├── review.py
│   ├── schemas.py
│   └── transcript_loader.py
└── tests/
    ├── test_evidence_checker.py
    ├── test_exporters.py
    ├── test_meeting_evaluation.py
    ├── test_minutes_generator.py
    ├── test_review.py
    └── test_schemas.py
```

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Nandsbeltrao/meeting-intelligence.git
cd meeting-intelligence
```

### 2. Criar o ambiente virtual

```bash
python3.12 -m venv .venv
```

### 3. Ativar o ambiente

Linux ou macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configurar a Cohere

Crie um arquivo `.env`:

```env
COHERE_API_KEY=sua_chave_aqui
COHERE_CHAT_MODEL=command-a-plus-05-2026
```

Nunca publique a chave real no GitHub.

A aplicação também permite informar uma chave durante a sessão.

### 6. Executar

```bash
streamlit run app.py
```

A aplicação estará disponível em:

```text
http://localhost:8501
```

---

## Exemplo de reunião

A transcrição fictícia possui:

- decisão explícita sobre divulgação;
- tarefa com responsável e prazo;
- tarefa sem responsável;
- tarefa sem prazo;
- pendência sobre escolha de plataforma;
- sugestão ainda não aprovada;
- nome mencionado em outro contexto.

Exemplo:

```text
Bruno: Eu vou revisar o regulamento até 30 de novembro.
```

Resultado esperado:

```json
{
  "task": "Revisar o regulamento",
  "owner": "Bruno",
  "deadline": "30 de novembro",
  "explicitly_mentioned": true
}
```

Quando não há responsável:

```json
{
  "owner": null
}
```

Na ata e no CSV, o valor é apresentado como:

```text
Não informado
```

---

## Validação das evidências

Cada decisão, tarefa, pendência e sugestão contém um trecho literal da transcrição.

A aplicação normaliza:

- letras maiúsculas e minúsculas;
- acentos;
- espaços repetidos;
- quebras de linha.

Depois verifica se a evidência existe no texto original.

Se uma evidência não for localizada, o item é sinalizado para revisão humana.

---

## Revisão humana

A extração da IA não é tratada automaticamente como registro oficial.

Antes dos downloads, a pessoa usuária pode:

- editar a tarefa;
- preencher ou corrigir o responsável;
- preencher ou corrigir o prazo;
- remover a tarefa da versão final;
- consultar a evidência original.

A evidência permanece bloqueada para edição, preservando a rastreabilidade da extração.

---

## Avaliação

O sistema foi avaliado com oito comportamentos críticos:

| ID | Caso avaliado | Resultado |
|---:|---|---|
| 1 | Decisão explícita identificada | Aprovado |
| 2 | Tarefa com responsável e prazo | Aprovado |
| 3 | Ausência de responsável preservada | Aprovado |
| 4 | Ausência de prazo preservada | Aprovado |
| 5 | Pendência identificada | Aprovado |
| 6 | Sugestão não aprovada preservada | Aprovado |
| 7 | Nome citado não virou responsável | Aprovado |
| 8 | Evidências localizadas na transcrição | Aprovado |

### Resultado final

```text
8 testes executados
8 testes aprovados
```

O resultado se aplica ao conjunto fictício avaliado e não representa uma métrica estatística geral de precisão.

---

## Segurança e privacidade

- A chave da API não fica no código.
- O arquivo `.env` não é versionado.
- O ambiente `.venv` não é versionado.
- As transcrições demonstrativas são fictícias.
- Reuniões reais não devem ser publicadas sem autorização.
- Dados pessoais e confidenciais devem ser tratados conforme as políticas aplicáveis.
- A chave de avaliação da Cohere é destinada a desenvolvimento e demonstração.

---

## Limitações

- O MVP processa transcrições textuais, não arquivos de áudio.
- A qualidade depende da clareza da transcrição.
- Uma identificação incorreta de quem está falando pode afetar a análise.
- A IA pode interpretar frases ambíguas de forma inesperada.
- A validação literal da evidência não comprova, sozinha, que toda interpretação está correta.
- A avaliação utiliza uma reunião fictícia e um conjunto pequeno de testes.
- A aplicação ainda não possui autenticação.
- A chave de avaliação possui limites de utilização.
- A revisão humana continua necessária antes do uso oficial da ata.

---

## Possíveis evoluções

- Transcrição de MP3, WAV e M4A com Whisper.
- Importação de transcrições do Microsoft Teams.
- Importação de transcrições do Zoom e Google Meet.
- Identificação de participantes.
- Histórico de reuniões.
- Acompanhamento do status das tarefas.
- Integração com Microsoft Planner.
- Integração com Outlook.
- Integração com SharePoint.
- Envio de tarefas para planilhas.
- Autenticação e controle de acesso.
- Avaliação automatizada em conjuntos maiores.
- Monitoramento de custos e qualidade.

---

## Status

### Concluído

- [x] Leitura de TXT.
- [x] Entrada por texto colado.
- [x] Análise com IA real.
- [x] Saída estruturada.
- [x] Validação Pydantic.
- [x] Responsáveis e prazos ausentes como `null`.
- [x] Decisões, tarefas, pendências e sugestões.
- [x] Verificação de evidências.
- [x] Ata em Markdown.
- [x] Tarefas em CSV.
- [x] Análise em JSON.
- [x] Revisão humana.
- [x] Interface em Streamlit.
- [x] Avaliação formal 8/8.
- [x] Identidade visual.

### Pendente

- [ ] Publicação no Render.
- [ ] Validação pública do upload e dos downloads.
- [ ] Inclusão do link público neste README.

---

## Autora

Desenvolvido por **Fernanda Leite** como projeto de portfólio para demonstrar o uso de inteligência artificial generativa na transformação de reuniões em registros estruturados, rastreáveis e revisáveis.

---

## Aviso

Este é um projeto de demonstração.

As transcrições incluídas no repositório são fictícias. O uso em reuniões reais exige autorização, revisão de privacidade, segurança, retenção de dados e controle de acesso.