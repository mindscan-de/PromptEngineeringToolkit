# TLDR;

This project aims to implement a LLM-workflow engine. Single long prompts are non-deterministic and often yield in lower quality outputs when a threshold of 4-8 K tokens is exceeded and the LLM starts to *fabulate* things.

A way to improve the output quality of models is by allowing the output to self correct e.g. by using different prompts with different stated goals. Which are optimized for LLM output quality. Instead of writing lengthy prompt preambles, rules and reminders, we can run multiple simple prompts and refactor the prompts into smaller ones, with less cognitive complexity.

This helps to switch between models and also to avoid a possible vendor lock-in, because rewriting all your prompts to break away from a certain model can still be expensive. So why not simplify your queries to a degree beforehand, such you can use the models interchangeably.

## Cognitive Complexity of a Prompt

## Cognitive Capacity of a Model

Every LLM has a point, where the cognitive complexity of a prompt exceeds the cognitive capacity
to output tokens coherent with the prompt. I would put that point, where the reliability of the
LLM output drops below the 90% mark.

By refactoring the prompts into smaller ones, we can reduce the cognitive complexity of a prompt
into multiple smaller ones for each step. Each step or subtask can be joined into a workflow, which
connects multiple smaller task into a bigger one. Either by executing the transitions between 
tasks with or without logic.

## About this project

This project aims to explore how to implement a workflow engine allowing to combine deterministic workflows with non-deterministic LLM outputs, to optmimize for quality of work while minimizing input and output tokens (which are a proxy metric for runtime and costs).

It somehow similar to agentic behavior, but this is currently not my primary goal. I don't need and want any of the tool capabilities as for August 2025 speaking. I don't want to automate workflows across different domains. My goal is optimizing for the quality of the output by using more or less competent models. And I want to understand, what can and should be parameterized, when invoking the language models.

Instead of invoking tools, this project aims for implementing a text to text transformation, but with the ability to make decisions and to improve and self-correct, by executing basic to simple tasks.

I won't give any kind of support. It is a private project, which I just happen to share publicly so people can have a look into it.

This code doesn't support API tokens or whatsoever - the current implementation implements a basic support for Huggingface-TGI and early versions of oobabooga_webui. 