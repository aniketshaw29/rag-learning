# What is RAG?

**RAG** stands for **Retrieval-Augmented Generation**. It is a technique that
gives Large Language Models (LLMs) access to external knowledge at query time,
so they can answer questions using your data instead of relying only on their
training data.

## The Problem

LLMs like Gemini, GPT, and Claude are trained on large amounts of public text.
They are great at general knowledge, but they have two big limitations:

1. **No access to your private data** - They cannot know about your company
   docs, personal notes, or internal wiki.
2. **Knowledge cutoff** - They only know things up to the date they were
   trained. Ask about something recent and they will either guess or say
   "I don't know."

## The RAG Solution

Instead of asking the LLM to memorize everything, RAG does this:

```
Your Question  -->  Search your documents  -->  Find relevant passages
                                                        |
                                                        v
                          LLM generates answer  <--  Pass them as context
```

The LLM gets a prompt like:

```
Answer the question below using ONLY the provided context.
If the context does not contain the answer, say so.

Context:
[relevant passages from your documents]

Question:
[what the user asked]
```

This dramatically reduces hallucination (making things up) because the model
is grounded in real, retrieved text.

## Why RAG Over Fine-Tuning?

| Approach        | Cost     | Speed to Update | Accuracy        |
|----------------|----------|-----------------|-----------------|
| Fine-tuning    | High     | Days/weeks      | Can still hallucinate |
| RAG            | Low      | Seconds (just add docs) | Answers cite real sources |

RAG is the go-to choice when:
- Your data changes frequently
- You need answers to cite their sources
- You want a fast, cheap way to add knowledge to an LLM

## Summary

RAG = **Retrieve** relevant chunks from your data, **Augment** the prompt with
them, then **Generate** an answer. Simple idea, powerful results.
