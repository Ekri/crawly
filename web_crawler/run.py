from RetrieverCache import RetrieverCache

if __name__ == "__main__":
    reader = RetrieverCache("dbs/faith/retrieved.db")
    list1 = reader.get_all()
    for url in list1:
        print url
