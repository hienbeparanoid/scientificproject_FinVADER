sentences = ["Naman is smart, boring, and creative.",  # base example
             "Naman is smart, boring, and creative!!!!!!",  # using punctuations
             "Naman is SMART, boring, and CREATIVE.",  # using CAPS
             "Naman is smart, boring, and super creative.",  # using degree modifiers (example 1)
             "Naman is smart, slightly boring, and creative.",  # using degree modifiers (example 2)
             "Naman is smart, boring, and creative but procrastinates a lot.",  # Polarity shift due to Conjunctions
             "Naman isn't smart at all.",  # Catching Polarity Negation
             ]

comments = ["  - base example",
           "  - using punctuations",
           "  - using CAPS",
           "  - using degree modifiers (example 1)",
           "  - using degree modifiers (example 2)",
           "  - Polarity shift due to Conjunctions",
           "  - Catching Polarity Negation"]

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

for i in range(len(sentences)):
    vs = analyzer.polarity_scores(sentences[i])
    print("{:-<65} {:-<65} {}".format(sentences[i], comments[i],  str(vs)))