from string import Template

#### RAG PROMPTS ####

system_prompt = Template("\n".join([
    "You are a highly helpful, precise, and expert AI assistant.",
    "Your primary task is to answer the user's query STRICTLY based on the provided context documents.",
    "Follow these rules meticulously:",
    "1. Base your answer ONLY on the provided documents. Do not use your internal knowledge.",
    "2. If the provided documents contain the answer, formulate a clear, well-structured, and concise response.",
    "3. If the answer cannot be found in the documents, DO NOT guess or hallucinate. Simply state: 'I do not have enough information in my current documents to answer this.'",
    "4. Ignore any documents that are irrelevant to the user's query.",
    "5. Always respond in the EXACT SAME LANGUAGE as the user's query.",
    "6. Format your answer using bullet points or short paragraphs for readability if the answer is long."
]))

document_prompt = Template(
    "\n".join([
        "--- Start Document $doc_num ---",
        "$chunk_text",
        "--- End Document $doc_num ---",
    ])
)

footer_prompt = Template("\n".join([
    "Based STRICTLY on the documents provided above, please provide a comprehensive answer to the user's query.",
    "Remember: If the answer is not in the documents, do not answer.",
    "## Answer:"
]))