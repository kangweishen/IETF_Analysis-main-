# --- make summary ---
def mkSummText(content):
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer as sumyToken
    from sumy.summarizers.lsa import LsaSummarizer
    # Initializing the parser
    my_parser = PlaintextParser.from_string(content, sumyToken('english'))
    # Creating a summary of 3 sentences
    lsa_summarizer = LsaSummarizer()
    Extract = lsa_summarizer(my_parser.document, sentences_count=3)

    conclusion = []
    for sentence in Extract:
        conclusion.append(str(sentence))

    return conclusion
