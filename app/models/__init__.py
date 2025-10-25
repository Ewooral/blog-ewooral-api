from .author import Author, AuthorReadWithArticles
from .tag import Tag, TagReadWithArticles
from .article import Article, ArticleRead, ArticleReadWithDetails
from .link import ArticleTagLink

AuthorReadWithArticles.model_rebuild()
ArticleReadWithDetails.model_rebuild()
TagReadWithArticles.model_rebuild()