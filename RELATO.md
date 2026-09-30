# Relato — Experiment Tracker: prática com Spec-Driven Development

## 1. Contexto e problema

O projeto surgiu da dificuldade de manter organizadas as informações de experimentos com modelos pequenos de linguagem (SLMs), especialmente testes de geração de código Python. Cada experimento pode envolver modelos, datasets, configurações e hardwares diferentes, além de métricas como pass@1 e consumo de energia. Quando esses dados ficam espalhados ou são registrados sem um padrão, torna-se difícil recuperar e comparar os resultados.

O objetivo foi criar uma ferramenta gráfica local para centralizar esses registros, sem depender de serviços remotos nem executar os modelos.

## 2. Solução

O Experiment Tracker é uma aplicação desktop feita em Python com Tkinter. Ela permite cadastrar, consultar, editar e excluir experimentos, importar registros JSON e gerar relatórios TXT. As informações não disponíveis podem permanecer sem preenchimento, em vez de serem substituídas por valores inventados.

O projeto mantém duas implementações:

- **Versão original**, em `src/app/`: protótipo inicial com interface gráfica e armazenamento JSON local.
- **Tentativa 2**, em `tentativa2/`: versão corrigida e recomendada para demonstração. Ela gera IDs UUID automaticamente, aceita mais campos opcionais, organiza o formulário por seções e permite filtrar a lista por modelo, dataset e data.

As duas versões são locais e não incluem backend, autenticação, sincronização em nuvem, APIs de modelos ou execução de modelos. Como seus formatos de dados são diferentes, os arquivos JSON de uma versão não devem ser presumidos compatíveis com a outra.

## 3. Processo de Spec-Driven Development

O trabalho foi realizado com o GitHub Spec Kit e passou por duas rodadas. O fluxo apresentado na segunda rodada foi:

1. **Constitution**: estabelecer princípios e restrições para orientar o desenvolvimento.
2. **Specify**: definir problema, usuários, histórias, requisitos e critérios de aceitação.
3. **Clarify**: revisar ambiguidades e ajustar os requisitos antes de planejar.
4. **Plan**: decidir arquitetura e tecnologias e documentar a pesquisa e o modelo de dados.
5. **Tasks**: decompor o trabalho em tarefas executáveis.
6. **Implement**: desenvolver a aplicação seguindo as tarefas.
7. **Verify**: conferir a implementação contra os artefatos e executar testes.

Os artefatos da primeira implementação estão em `specs/001-experiment-tracker/`. A tentativa 2 mantém artefatos revisados em `tentativa2/.specify/specs/experiment-tracker/`.

## 4. O que aconteceu nas duas rodadas

Na primeira rodada, os artefatos e as tarefas foram considerados concluídos, mas a aplicação ainda não estava exposta como uma interface gráfica executável. A existência de código de interface e tarefas marcadas como completas não comprovava, por si só, que uma pessoa conseguiria iniciar e usar a aplicação.

A correção não foi apenas pedir novamente “faça a interface”. O pedido passou a orientar o agente a conferir o plano, as tarefas e a implementação existente, identificar a lacuna e então completar o ponto de entrada gráfico. Essa revisão tornou explícita a diferença entre **ter componentes de GUI no código** e **ter um programa realmente lançável**.

Na tentativa 2, os requisitos e o plano foram revistos para reduzir atrito no cadastro: somente ID, nome, data e modelo são obrigatórios; os demais dados podem ficar ausentes. O fluxo também passou a incluir as etapas de esclarecimento e verificação mostradas no material da prática.

## 5. Comparação das abordagens

O PDF compara três abordagens: processo sem verificação, processo com verificação e desenvolvimento sem SDD. O quadro registra os seguintes resultados:

| Abordagem | Tempo indicado | Considerada correta? | Qualidade indicada |
|---|---|---|---|
| 1. Sem verificação | 2h 20 min | Não | Bom |
| 2. Com verificação | Mínimo | Sim | Ótimo |
| 3. Sem SDD | Mínimo | Sim | Funcional |

Essa comparação sugere que gerar código não é suficiente para concluir uma tarefa: é necessário verificar se o resultado atende ao requisito e funciona no uso esperado. O material também registra que, para uma ideia simples e já clara, o processo completo pode parecer demorado; ao mesmo tempo, as etapas dão mais controle sobre o que está sendo produzido e alterado.

## 6. Reflexões

Especificar a ideia antes de implementar ajudou a visualizar o produto final e deu uma referência para avaliar o código. Quando a interface gráfica faltou na primeira rodada, a especificação e o plano permitiram apontar objetivamente a lacuna, em vez de depender de uma impressão vaga.

O principal aprendizado foi que os artefatos do SDD precisam ser usados durante a implementação e a verificação, não apenas criados no início. Uma lista de tarefas marcada como concluída não substitui uma checagem do comportamento. Para este projeto, a verificação prática da inicialização gráfica e dos fluxos foi tão importante quanto escrever os componentes.

O processo também tem custo. Para um projeto pequeno e com objetivo bem definido, produzir e revisar todos os artefatos pode parecer mais demorado do que pedir o código diretamente. Seu valor aparece especialmente quando os requisitos precisam ser acompanhados, quando há várias rodadas de correção ou quando é importante justificar decisões e demonstrar o que foi validado.

## 7. Resultado

O resultado é um Experiment Tracker local com interface gráfica, registro e organização de experimentos, importação JSON e exportação TXT. A segunda implementação corrige lacunas identificadas na primeira e permite deixar informações opcionais sem preenchimento. O projeto também conserva especificações, planos, tarefas e testes para tornar o processo e as decisões mais rastreáveis.