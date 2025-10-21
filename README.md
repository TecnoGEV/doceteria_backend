# Doceteria Backend

Backend para a Doceteria.

## Instalação

Este projeto utiliza `uv` para gerenciamento de pacotes e ambiente virtual.

### 1. Instale o `uv`

Você pode instalar o `uv` usando um dos seguintes métodos:

**macOS e Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Após a instalação, verifique se o `uv` foi instalado corretamente com o comando:

```bash
uv --version
```

### 2. Crie o ambiente virtual e instale as dependências

Com o `uv` instalado, utilize o seguinte comando para criar o ambiente virtual e instalar as dependências do projeto:

```bash
uv sync
```

## Como Executar

Para executar o projeto, utilize o seguinte comando:

```bash
uv run uvicorn src.main:app --reload
```

ou

```bash
uv run task server
```

Isso iniciará o servidor de desenvolvimento.
O servidor estara escutando na porta padrao: 8000
Para acessar o swagger va ate a rota  **/docs**

## Como Rodar os Testes

Para rodar os testes, utilize o seguinte comando:

```bash
uv run pytest
```
