import gensim
import gensim.corpora as corpora
import spacy


def tokenizer(texts):
    """
    https://spacy.io/api/annotation
    remove stopwords, punchtuation, wired word,
    only keep meaningfull words based on
    pos['NOUN', 'ADJ', 'VERB', 'ADV','INTJ'], lemmatization
    """
    words = []
    nlp = spacy.load('en', disable=['parser', 'ner'])
    for text in texts:
        doc = nlp(text)
        ws = [token.lemma_ for token in doc if
              (token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV', 'INTJ']) &
              (token.is_alpha) & (~token.is_stop)]
        words.append(ws)
    return words


def make_gram(words, num_gram=1):
    """
    Make unigram, bigram or trigram into account, the default is unigram
    """
    if num_gram == 1:
        grams = words
    elif num_gram == 2:
        bigram = gensim.models.Phrases(words, min_count=3, threshold=50)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        grams = [bigram_mod[ws] for ws in words]
    else:
        bigram = gensim.models.Phrases(words, min_count=3, threshold=50)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram = gensim.models.Phrases(bigram[words],
                                        min_count=3, threshold=50)
        trigram_mod = gensim.models.phrases.Phraser(trigram)
        grams = [trigram_mod[bigram_mod[ws]] for ws in words]
    return grams


def make_id_corpus(grams):
    """
    According to gram, get id2word dictionary
    and get corpus with format (id, freq) in each doc
    """
    id2word = corpora.Dictionary(grams)
    corpus = [id2word.doc2bow(gs) for gs in grams]
    return id2word, corpus


def text2corpus(texts, num_gram):
    words = tokenizer(texts)
    grams = make_gram(words, num_gram=num_gram)
    id2word, corpus = make_id_corpus(grams)
    return id2word, corpus


# id2text, corpus = text2corpus(texts, num_gram=3)
