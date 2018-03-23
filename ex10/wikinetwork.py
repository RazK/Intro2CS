#!/usr/bin/env python3
#############################################################
# FILE :        wikinetwork.py
# WRITER :      Raz Karl , razkarl , 311143127
# EXERCISE :    intro2cs ex10 2016-2017
# DESCRIPTION:  Defines the WikiNetwork class and helper
#               methods.
#############################################################
from article import *


# Article Links File Constants
ARTICLE_LINKS_FILENAME  = "links.txt"
ARTICLE_LINKS_SEPARATOR = "\t"


# Page Rank Algorithm Constants
PAGE_RANK_DEFAULT_D     = 0.9
PAGE_RANK_INITIAL_RANK  = 1


def read_article_links(file_name):
    """
    Parse article links from file and create a list of all links between
    articles.
    :param file_name:   string - path to articles file.
    :return:            list of tuples [(article_title, neighbor_title),
                        ...]
    :example:
        articles file:
            articleA    articleB
            articleA    articleC
            articleB    articleA
            (notice: Articles names separated by \t, lines end with \n)

        return:
            [(articleA, ArticleB), (ArticleA, ArticleC), (ArticleB, ArticleA)]
    """
    with open(file_name, 'r') as file:
        article_links = [tuple(line.split(ARTICLE_LINKS_SEPARATOR))
                         for line in file.read().splitlines()]

    # BODEK - Notice: closing the file here is unnecessary!!! You took off
    # points for neglecting this on ex5, but I argue this is done implicitly
    # by the interpreter! see:
    # http://tinyurl.com/ex5-points-taken-off-in-vain
    file.close()

    return article_links


class WikiNetwork:
    """
    Represents a network of Articles.
    See articles.py for Article class description.
    """

    def __init__(self, links_list):
        """
        Creates a network of Articles and links from the given list.
        :param links_list:  list of tuples [(article_title, neighbor_title),
                            ...]
        """
        self.__articles = dict()
        self.update_network(links_list)


    def update_network(self, links_list):
        """
        Update the articles network according to the given list.
        :param links_list:  list of tuples [(article_title, neighbor_title),
                            ...]
        """
        for article, neighbor in links_list:
            # Create new article if doesn't exist
            if article not in self:
                self[article] = Article(article)
            # Create the neighbor if doesn't exist
            if neighbor not in self:
                self[neighbor] = Article(neighbor)
            # Add neighbor to the article
            self[article].add_neighbor(self[neighbor])


    def get_articles(self):
        """
        Returns a list of all the articles in the network.
        :return: list of Article objects
        """
        return list(self.__articles.values())


    def get_titles(self):
        """
        Returns a list of titles of all the articles in the network.
        :return: list of strings - article titles
        """
        return list(self.__articles.keys())


    def __len__(self):
        """
        Return the number of articles in the network.
        :return: int - number of articles in the network
        """
        return len(self.__articles)


    def __contains__(self, title):
        """
        Returns if an article with the given title exists in the network.
        :param title:   string - article title
        :return:        True of an article with the given title exists in
                        the network, otherwise False.
        """
        return title in self.__articles


    def __repr__(self):
        """
        Return a string representing the articles network.
        :return: string representation of the articles network
        :example:
            Article Cyber:
                title       "Cyber"
                neighbors   [Buzzwords, Money]

            Article Buzzwords:
                title       "Buzzwords"
                neighbors   [Cyber, BigData]

            Article BigData:
                title       "BigData"
                neighbors   []

            return:     "{'Cyber': ('Cyber', ['Buzzwords', 'Money']),
                          'Buzzwords': ('Buzzwords', ['Cyber', 'BigData']),
                          'BigData': ('BigData', [])}"
            (no newlines in actual string)
        """
        return str(self.__articles)


    def __getitem__(self, title):
        """
        Returns the Article object matching the given title.
        Raises KeyError if the given title matches no article in the network.
        :param title:   string - an article title
        :return:        Article object - the article with the given title
        """
        if title not in self:
            # BODEK - Notice: This behavior is achieved anyway, since the
            # dictionary self.__articles will raise KeyError(title) for
            # unregistered titles.
            # Doing this explicitly since directed to do so in the guidelines
            # document.
            raise KeyError(title)
        else:
            return  self.__articles[title]


    def __setitem__(self, title, article):
        """
        Sets an Article object for the given title in the network.
        :param title:   string - title of the article
        :param article: Article object - article to set
        """
        self.__articles[title] = article


    def page_rank(self, iters, d=PAGE_RANK_DEFAULT_D):
        """
        Returns a list of titles of all articles in the network sorted by their
        Page Rank score.
        Lexicographic sort determines order of articles with the same rank.
        :param iters:   int - number of Page Rank iterations to perform
        :param d:       float - Page Rank distribution constant
        :return:        list of strings - titles of articles, sorted by Page
                        Rank score (then lexicographically)
        """
        # Holds the current rank of every article in each Page Rank iteration
        ranks = {title : PAGE_RANK_INITIAL_RANK for title in self.get_titles()}

        # Quick method for calculating the rank donation from an article
        # to it's neighbors
        def rank_donation(article):
            num_of_neighbors = len(article)
            if num_of_neighbors != 0:
                return d * ranks[article.get_title()] / num_of_neighbors
            return 0

        # Quick method for donating ranking to an article
        def donate(article, donation):
            donations[article.get_title()] += donation

        # Quick method for collecting all donations to an article's rank
        def collect_donations(article):
            ranks[article.get_title()] = donations[article.get_title()]

        # Rank pages with Page Rank
        for i in range(iters):
            # Holds the current rank donations (ranks given to an article by
            # other articles) in each Page Rank iteration
            donations = {title : 0 for title in self.get_titles()}

            # Step 1: Ranks distribution
            for article in self.get_articles():
                # distribute current article's rank between all his neighbors
                donation = rank_donation(article)
                for neighbor in article.get_neighbors():
                    donate(neighbor, donation)

                # In the actual Page Rank algorithm - every article in the
                # network now distributes the remainder of it's rank between
                # all other articles in the network.
                # This results in every article gaining another (1-d) by the
                # end of the iteration.
                # Let's skip this ceremony and just take our (1-d) home :-)
                donate(article, (1-d))

            # Step 2: Ranks collection
            for article in self.get_articles():
                collect_donations(article)

        # Return a list of articles sorted by their ranks, then
        # lexicographically in case of same rank.
        return sorted(sorted(ranks, key=str.lower),
                      key=lambda title: ranks[title],
                      reverse=True)


    def jaccard_index(self, article_title):
        """
        Returns a list of titles of all articles in the network sorted by their
        Jaccard Index with the given title.
        Lexicographic sort determines order of articles with the same index.
        Returns None if the article is not in the network or has no neighbors.
        :param article_title:   string - title of article to calculate
                                jaccard indexes from.
        :return:                list of strings - titles of articles, sorted by
                                Jaccard Indexes (then lexicographically)
        """
        # Articles not in the network return None
        if article_title not in self:
            return  None

        article   = self[article_title]
        neighbors = article.get_neighbors()

        # Articles with no neighbors return None
        if len(neighbors) == 0:
            return  None

        # Quick method for calculating the jaccard index of the given
        # article with another article
        def jaccard(other):
            # BODEK - Notice: I used Sets for holding neighbors in the
            # Article class exactly for this purpose - so that I can check
            # if a neighbor is contained or calculate intersections as fast
            # as possible.
            # Unfortunately, the public API does not allow me
            # to return the neighbors as Sets, rather only as lists - so I
            # had to cast them back to sets for the calculation (Stack
            # Overflow argues this is still the fastest way).
            # If I had the option for adding a *public* method to the Article
            # class, I would add 'get_neighbors_set' and use it here to make
            # this method even more efficient.
            intersection = len(set(neighbors) & set(other.get_neighbors()))
            union        = len(article) + len(other) - intersection
            return intersection / union

        # Build a dictionary of Jaccard indexes for all articles in the network
        indexes = {title:jaccard(self[title]) for title in self.get_titles()}

        # Return a list of articles sorted by their Jaccard Indexes, then
        # lexicographically in case of same index.
        return sorted(sorted(indexes.keys(), key=str.lower),
                      key=lambda title: indexes[title],
                      reverse=True)


    def travel_path_iterator(self, article_title):
        """
        Returns a generator that iterates over the network through the most
        popular neighbor of each article.
        The generator starts at the given article_title, and moves to the
        neighbor with the highest number of ingoing links in every iteration.
        If more than one neighbor has the highest amount of ingoing links,
        moves to the first neighbor in lexicographic order.
        If an article with no neighbors is reached, the iteration is stopped.
        :param article_title:   string - title of article to begin iterating
                                from.
        :return:                generator object - yields article
                                title and iterates to it's most popular
                                neighbor.
                                (lexicographic order breaks ties).
        """
        # Don't start iterating if the article doesn't exist
        if article_title not in self:
            raise StopIteration

        # Count the number of ingoing links for each article
        ingoing = {title : 0 for title in self.get_titles()}
        for article in self.get_articles():
            for neighbor in article.get_neighbors():
                ingoing[neighbor.get_title()] += 1

        # Start traveling from the given article
        traveler = self[article_title]

        # Lambdas for sorting by popularity and lexicographically
        popularity    = lambda neighbor: ingoing[neighbor.get_title()]
        lexicographic = lambda neighbor: str.lower(neighbor.get_title())

        # Travel to the most popular neighbor (lexicographic order breaks ties)
        while True:
            # Yield the current article
            yield traveler.get_title()

            # Stop iteration if article has no neighbors
            neighbors = traveler.get_neighbors()
            if not neighbors:
                raise StopIteration

            # Choose next neighbor by popularity
            traveler = max(sorted(neighbors, key=lexicographic),
                           key=popularity)


    def friends_by_depth(self, article_title, depth):
        """
        Returns a list of titles of articles that can be reached from the
        given article by following links until the given depth.
        Returns None if the article is not in the network.
        :param article_title:   string - article title to search from
        :param depth:           int - maximal number of links to follow.
        :return:                list of strings - titles of articles linked to
                                the given article by links up to the given
                                depth.
        """
        # Articles not in the network return None
        if article_title not in self:
            return None

        # Return recursive collection of friends
        friends = set()
        self.__collect_friends_by_depth(article_title, depth, friends)
        return list(friends)


    def __collect_friends_by_depth(self, article_title, depth, collection):
        """
        Add neighbors of neighbors to a collection recursively, up
        to the given depth.
        :param article_title:   string - article to collect friends from
        :param depth:           int - maximal friend distance (recursion depth)
        :param collection:      set - combined collection of friends
        """
        # Add the article itself
        collection.add(article_title)

        # Collect neighbors of neighbors recursively
        if depth >= 1:
            neighbors = self[article_title].get_neighbors()
            for neighbor in neighbors:
                collection.add(neighbor.get_title())
                self.__collect_friends_by_depth(neighbor.get_title(),
                                                depth-1,
                                                collection)