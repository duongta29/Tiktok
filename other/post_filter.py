import re

def preprocess(text):
    return re.findall(r'\w+', text.lower())

def create_index(documents):
    index = {}
    for doc_id, text in enumerate(documents):
        for word in preprocess(text):
            if word not in index:
                index[word] = []
            index[word].append(doc_id)
    return index

def search(index, query):
    query_words = preprocess(query)
    print(query_words)
    results = set()
    for word in query_words:
        if word in index:
            results.update(index[word])
    return results

def check(key, content):
    index = create_index(content)
    results = search(index, key)
    return results

def filter_post(key, content):
    pass


# # Example usage
# documents = [
#     "The quick brown fox jumps over the lazy dog.",
#     "The rain in Spain falls mainly on the plain.",
#     "In the desert, you can remember your name."
# ]

# index = create_index(documents)
# query = "the quick"
# results = search(index, query)

# for doc_id in results:
#     print(f"Document {doc_id}: {documents[doc_id]}")



def main():
    documents = [
        "Bùi Hải An và Mai Phương đi ô tô.",
        "Hiếu thứ hai đi xe máy",
        "In the desert, you can remember your name."
    ]
    # content = "T A D"
    # content = preprocess(content)
    # print(content)

    # index = create_index(documents)
    # print(index)

    # query = input("Please enter your search query: ")
    # results = search(index, query)


    # if results:
    #     print("Documents containing the query:")
    #     for doc_id in results:
    #         print(f"Document {doc_id}: {documents[doc_id]}")
    # else:
    #     print("No documents contain the query.")

if __name__ == '__main__':
    main()