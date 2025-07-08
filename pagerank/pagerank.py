import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    num_pages = len(corpus)
    probabilities = dict()

    links = corpus[page]
    if links:
        for p in corpus:
            probabilities[p] = (1 - damping_factor) / num_pages
            if p in links:
                probabilities[p] += damping_factor / len(links)
    else:
        for p in corpus:
            probabilities[p] = 1/num_pages

    return probabilities


    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    


def sample_pagerank(corpus, damping_factor, n):
    pagerank = dict()
    for page in corpus:
        pagerank[page] = 0

    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[current_page] += 1
        model = transition_model(corpus , current_page, damping_factor)
        current_page = random.choices(list(model.keys()), weights=model.values())[0]

    for page in pagerank:
        pagerank[page] /= n

    return pagerank

    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
   


def iterate_pagerank(corpus, damping_factor):
    n = len(corpus)
    pagerank = {page: 1 / n for page in corpus}

    converged = False
    while not converged:
        new_rank = dict()
        for page in corpus:
            total = 0
            for possible_page in corpus:
                if page in corpus[possible_page]:
                    total += pagerank[possible_page / n]
                if not corpus[possible_page]:
                    total += pagerank[possible_page] / n
            new_rank[page] = (1 - damping_factor) / n + damping_factor
        converged = all(abs(new_rank[page] - pagerank[page]) < 0.001 for page in corpus)
        pagerank = new_rank

    return pagerank



    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values areac
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
