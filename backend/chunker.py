def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks




# def chunk_text(text, chunk_size=800, overlap=100):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         chunk = text[start:end]

#         # Try not to cut mid sentence
#         if "." in chunk:
#             last_period = chunk.rfind(".")
#             chunk = chunk[:last_period + 1]

#         chunks.append(chunk.strip())
#         start = end - overlap

#     return chunks
