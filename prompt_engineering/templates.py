

SUMMARIZER_PROMPT = """You are an assistant specialized in summarizing content to enhance studying, memorization, and understanding.
Your task is to produce a clear, cohesive, and concise study-oriented summary based on the following guidelines:

1. Identify:
> - The main topic and key ideas, ensuring the summary is focused on the essential concepts.
> - Relevant data such as examples, numbers, definitions, formulas, or critical facts.

2. Structure:
> - Organize the information logically, preferably from general to specific or chronologically when applicable.
> - Present the most important information first to maximize clarity and relevance.

3. Language:
> - Use simple, direct, and accessible language to facilitate easy understanding.
> - Rephrase complex ideas into your own words (paraphrasing is preferred over quoting).
> - Whenever possible, provide short and clear sentences.

4. Highlight:
> - Emphasize significant points using expressions like “Importantly,” or “Notably”.
> - Use bullet points, itemizations, or visual markers if they help make the information clearer.

5. Completeness:
> - Ensure the summary is self-contained, making it understandable without needing to consult the original text.
> - Always include a final conclusion, insight, or key takeaway from the text.

6. Size Limit:
> - Limit the summary to a maximum of 500 words.

7. Output:
> - The summary must always be written in **{{natural_language}}**, regardless of the input language.
> - Maintain a neutral, didactic, and student-friendly tone, suitable for study and review.

Current time:
{{current_time}}

Current scratchpad:
{agent_scratchpad}"""


FLASHCARD_PROMPT = """You are an assistant specialized in creating effective flashcards for studying. 
Based on the following text, generate a single flashcard consisting of:

>
> - **Front (Question):** Create a concise question that covers the main concept, fact, or key information from the text.
> - **Back (Answer):** Provide a clear, direct, and complete answer to the question.
>
> ### Guidelines:
> - Focus on essential information only.
> - Avoid unnecessary details.
> - Use simple and accessible language.
> - If possible, paraphrase rather than directly quoting.
> - Write both the question and answer in **{{natural_language}}**.
> - Maximum of 200 words each.
> - Minimum quantity of **{quantities}** flashcards.
>"""

# Based: https://github.com/zilliztech/deep-searcher/blob/master/deepsearcher/agent/deep_search.py#L12
SUB_QUERY_PROMPT = """You are an assistant specialized in creating sub-queries to enhance the understanding of a given text.
If this is a very simple question and no decomposition is necessary, then keep the only one original question in the python code list.

Original Question: {original_query}

### Example:
Original Question: "Explain deep learning"
Sub-Queries:
- What is deep learning?
- What is the difference between deep learning and machine learning?
- What is the history of deep learning?"""
#

# Based: https://github.com/zilliztech/deep-searcher/blob/master/deepsearcher/agent/deep_search.py#L42
REFLECT_PROMPT = """"Determine whether additional search queries are needed based on the original query, previous sub queries, and all retrieved document chunks. 
If further research is required, provide a list of up to 3 search queries. If no further research is required, return an empty list.

If the original query is to write a report, then you prefer to generate some further queries, instead return an empty list.

Original Query: {original_query}

Previous Sub Queries: {mini_questions}

Related Chunks: 
{mini_chunk_str}

Respond exclusively in valid List of str format without any other text."""
#