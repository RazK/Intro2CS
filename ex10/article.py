#!/usr/bin/env python3
#############################################################
# FILE :        articles.py
# WRITER :      Raz Karl , razkarl , 311143127
# EXERCISE :    intro2cs ex10 2016-2017
# DESCRIPTION:  Defines the Article class.
#############################################################

class Article:
    """
    Represents an article with a title and links to other articles.
    """

    def __init__(self, article_title):
        """
        Initialize an article with the given title and no neighbors.
        :param article_title: string - title of the article
        """
        self.__title = article_title
        self.__neighbors = set()


    def get_title(self):
        """
        Return the article's title.
        :return: string - the article's title
        """
        return self.__title


    def add_neighbor(self, neighbor):
        """
        Add a link to the given neighbor article
        :param neighbor: Article - neighbor to link
        """
        self.__neighbors.add(neighbor)


    def get_neighbors(self):
        """
        Return a list of articles linked from this article.
        :return: list of Article objects - article neighbors
        """
        return list(self.__neighbors)


    def __len__(self):
        """
        Return the number of links from this article (neighbors)
        :return: int - number of neighbors
        """
        return len(self.__neighbors)


    def __contains__(self, article):
        """
        Returns if the given article is a neighbor of this article.
        :param article: Article - neighbor candidate
        :return:        True if given article is linked from this article,
                        otherwise False.
        """
        return article in self.__neighbors


    def __repr__(self):
        """
        Return a string representing this article.
        :return: string representation of the article
        :example:
            Article:
                title       "Cyber"
                neighbors   [Buzzwords, Money]
            return:     "('Cyber', ['Buzzwords', 'Money'])"
        """
        return "('{0}', {1})".format(self.__title,
                                   [neighbor.get_title() for neighbor in
                                    self.__neighbors])