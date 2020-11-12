class News:
    def __init__(self,news):
        # source,author,title,description,url,urlToImage,publishedAt,content
        self.name = news['source']['name']
        self.author = news['author']
        self.title = news['title']
        self.description = news['description']
        self.url = news['url']
        self.urlToImage = news['urlToImage']
        self.publishedAt = news['publishedAt']
        self.content = news['content']
