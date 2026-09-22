# Relato — LLM Experiment Tracker

## 1. Problema
Falta de praticidade para anotar os experimentos da pesquisa.
As informações de hardware, tempo e resultados precisam de organização siostemática.
A ideia foi criar uma ferramenta local simples para registrar, consultar e organizar essas informações.

## 2. Solução desenvolvida

Foi desenvolvido o Experiment Tracker, uma aplicação gráfica local
para gerenciamento de experimentos com modelos de linguagem.

A aplicação permite:

- cadastrar experimentos;
- registrar informações do modelo, dataset e configuração;
- registrar o hardware utilizado;
- registrar o uso de um harness orientado ao raciocínio;
- armazenar métricas como pass@1, tempo de execução e energia, quando disponíveis;
- visualizar, editar e excluir experimentos;
- importar experimentos a partir de JSON;
- gerar relatórios em formato TXT.

A aplicação utiliza armazenamento local em JSON e não possui backend,
autenticação ou sincronização remota.

## 3. Uso de SDD

O desenvolvimento foi conduzido utilizando o GitHub Spec Kit como
framework de Spec-Driven Development.

O processo foi organizado em etapas:

1. Constitution: definição dos princípios e restrições do projeto;
2. Specify: definição do problema, usuários, requisitos funcionais, histórias de usuário e critérios de aceitação;
3. Plan: definição da arquitetura, modelo de dados e decisões técnicas;
4. Tasks: decomposição da implementação em tarefas menores;
5. Implement: desenvolvimento da aplicação a partir dos artefatos especificados.

Os principais artefatos produzidos foram `constitution.md`, `spec.md`,
`plan.md` e `tasks.md`, além dos arquivos de implementação e testes.

## 4. Experiência com SDD

É bem mais fácil de visualizar a ideia final quando é preciso descrevê-la com tantas características, detalhes e exemplos. Começar pedindo o código diretamente exigiria muito mais mudanças no produto. Com as especificações, o código gerado foi direto ao ponto, sem devaneios extras.

Além disso, percebe-se a especificação como uma referência durante a implementação.
Quando surgiu uma dúvida sobre uma funcionalidade da interface, por exemplo, foi possível verificar se ela realmente fazia parte dos requisitos definidos.

Por outro lado, uma exigência bem explícita foi ignorada: a interface. Então, houve a necessidade de pedir para o agente verificar essa especificação e corrigir a implementação.

## 5. Resultado

Ao final, foi obtida uma aplicação funcional para registro e organização
local de experimentos de LLM, acompanhada dos artefatos de especificação,
planejamento, tarefas e testes.