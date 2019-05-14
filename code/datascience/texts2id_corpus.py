import gensim
import gensim.corpora as corpora
import spacy

nlp = spacy.load('en', disable=['parser', 'ner'])
additional_stopwords = ['day', 'today', 'week', 'year', 'time',
                        'make', 'times', 'weeks', 'days',
                        'made', 'makes', 'people', 'good',
                        'feel', 'felt', 'feels',
                        'lot', 'thing',
                        'things', 'life', 'live', 'lives',
                        'woman', 'women', 'man',
                        'men', 'well',
                        'great', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday',
                        'Saturday', 'Sunday', 'linkedin',
                        'share', 'Forbes',
                        'NEWSWIRE', 'Fox',
                        'CNBC', 'Insider', 'Reuters', 'Embed',
                        'Getty', 'AP',
                        'AFP', 'copyright',
                        'pm', 'image', 'images', 'Image',
                        'Images', 'express',
                        'Bloomberg', 'CNN', 'BBC', 'NBCUniversal',
                        'Newsday',
                        'Bleacher', 'Highlights', 'highlights',
                        'Enlarge', 'people', 'thing', 'time', 'NPR',
                        'place', 'ET',
                        'et', 'PM', 'message',
                        'EMT', 'EST', 'video', 'photo', 'videos', 'photos',
                        'Photo', 'Photos',
                        'caption', 'Beast', 'Good', 'News',
                        'Council', 'Analysis', 'LLC', 'Global',
                        'April', 'Quotes',
                        'contributor', 'group']

for i in additional_stopwords:
    nlp.Defaults.stop_words.add(i)
    nlp.vocab[i].is_stop = True


def tokenizer(texts):
    """
    https://spacy.io/api/annotation
    removes stopwords, punchtuation, abnormal words, etc;
    only keep meaningfull words based on
        pos['NOUN', 'ADJ', 'VERB', 'ADV','INTJ'] lemmatization.
    """
    words = []
    for text in texts:
        doc = nlp(text)
        ws = [token.lemma_ if ((
                               token.pos_ in
                               ['NOUN', 'ADJ', 'VERB', 'ADV', 'INTJ']) &
                               token.is_alpha & ~token.is_stop &
                               (token.lemma_ != '-PRON-'))
              else token.text if ((token.pos_ == 'PROPN') &
                                  token.is_alpha & ~token.is_stop)
              else None for token in doc]
        ws = [token for token in ws if token]
        words.append(ws)
    return words


def make_gram(words, num_gram=1):
    """
    Decides which of unigram, bigram or trigram to take into account. The default is unigram.
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
    According to num-gram, gets id2word dictionary and
    corpus with format (id,req) in each doc.
    """
    id2word = corpora.Dictionary(grams)
    corpus = [id2word.doc2bow(gs) for gs in grams]
    return id2word, corpus


def text2corpus(texts, num_gram):
    """Preprocessing for IDA."""
    words = tokenizer(texts)
    grams = make_gram(words, num_gram=num_gram)
    id2word, corpus = make_id_corpus(grams)
    return id2word, corpus, grams
