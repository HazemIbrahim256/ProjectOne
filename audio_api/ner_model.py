import spacy
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

ENTITY_TYPES = ['PERSON', 'ORG', 'LOC', 'DATE', 'TIME', 'MONEY', 'PER', 'MISC', 'ORDINAL', 'GPE']
language = 'en'

# Load the pre-trained models for English, Spanish, Italian, and Arabic
if language == 'en':
    nlp = spacy.load('en_core_web_sm')
elif language == 'es':
    nlp = spacy.load('es_core_news_sm')
elif language == 'it':
    nlp = spacy.load('it_core_news_sm')
elif language == 'ar':
    tokenizer = AutoTokenizer.from_pretrained("hatmimoha/arabic-ner")
    model = AutoModelForTokenClassification.from_pretrained("hatmimoha/arabic-ner")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
else:
    raise ValueError(f"Language '{language}' not supported.")

def perform_ner(text):
    if language == 'ar':
        text = split_sentences(text)
        doc = nlp(text)
        entities = []
        tags = []
        for sentence in doc:
            for item in sentence:
                if item["word"].startswith("##"):
                    entities[-1] = entities[-1] + item["word"].replace("##", "")
                else:
                    entities.append(item["word"])
                tags.append(item["entity"])
        return entities, tags

    elif language in ['en', 'es', 'it']:
        doc = nlp(text)
        entities = []
        numbers = []

        for ent in doc.ents:
            entities.append((ent.text, ent.label_))

        for token in doc:
            if token.like_num:
                numbers.append(token.text)

        entity2 = []
        entity2_type = []

        for ent in entities:
            entity2.append(ent[0])
            entity2_type.append(ent[1])

        for i in numbers:
            if i in entity2:
                numbers.remove(i)

        return entity2, entity2_type, numbers



# text = "Barack Obama was born on August 4, 1961, in Honolulu, Hawaii. He served as the 44th President of the United States."
# entity2, entity2_type, numbers = perform_ner(text)

# print("English Entities:", entity2)
# print("English Entitie types:", entity2)
# print("English Numbers:", numbers)


def split_sentences(text):
    """ Simple Arabic tokenizer and sentencizer. It is a space-based tokenizer. I use some rules to handle
    tokenition exception like words containing the preposition 'و'. For example 'ووالدته' is tokenized to 'و والدته'

    :param text: Arabic text to handle
    :return: list of tokenized sentences
    """
    try:
        text = text.decode('utf-8')
    except(UnicodeDecodeError, AttributeError):
        pass
    text = text.strip()
    tokenizer_exceptions = ["وظف", "وضعها", "وضعه", "وقفنا", "وضع", "وصفوها", "وجهوا", "وجهتها", "وول", "وطننا",
                            "وكالته", "وجع", "والدته", "والده", "وطره", "وادي", "وضعية", "وعدوا",
                            "واجهات", "وفرتها", "وقاية", "وفا", "وزيرنا", "وزارتي", "وجهاها", "واردة", "وضعته",
                            "وزارية",
                            "وضعتها", "وافته", "وجاهة", "وهمية", "واجهة", "واضعاً", "واقعي", "ودائع", "واعدا", "واع",
                            "واسعا", "ولاة",
                            "ورائها", "وحدها", "وزارتي", "وزارتي", "والدة", "وزرائها", "وسطاء", "وليامز", "وافق",
                            "والدها", "واضعين", "وسم", "وافق", "وجهها", "واسعة", "واسع", "وزنها", "وزنه", "وصايته",
                            "وصلوا", "والدها", "وصولاً", "وضوحاً", "وجّهته", "وضعته", "ويكيليكس", "وحدها", "وزيراً",
                            "والي",
                            "وقفات", "وعر", "واقيًا", "وقوف", "وصولهم", "وارسو", "واجهت", "وقائية", "وضعهم",
                            "وسطاء", "وظيفته", "ورائه", "واسع", "ورط", "وظفت", "وقوف", "وافقت", "وفدًا", "وصلتها",
                            "وثائقي", "ويليان", "وساط", "وُقّع", "وَقّع", "وخيمة", "ويست", "والتر", "وهران", "ولاعة",
                            "ولايت", "والي", "واجب", "وظيفتها", "ولايات", "واشنطن", "واصف",
                            "وقح", "وعد", "وقود", "وزن", "وقوع", "ورشة", "وقائع", "وتيرة", "وساطة", "وفود", "وفات",
                            "وصاية", "وشيك", "وثائق", "وطنية", "وجهات", "وجهت", "وعود", "وضعهم", "وون", "وسعها", "وسعه",
                            "ولاية", "واصفاً", "واصلت", "وليان", "وجدتها", "وجدته", "وديتي", "وطأت", "وطأ", "وعودها",
                            "وجوه", "وضوح", "وجيز", "ورثنا", "ورث", "واقع", "وهم", "واسعاً", "وراثية", "وراثي", "والاس",
                            "واجهنا", "وابل", "ويكيميديا", "واضحا", "واقف", "واضح", "وصفته", "واتساب", "وحدات", "ون",
                            "وورلد", "والد", "وكلاء", "وتر", "وثيق", "وكالة", "وكالات", "و احدة", "واحد", "وصيته",
                            "وصيه", "ويلمينغتون", "ولد", "وزر", "وعي", "وفد", "وصول", "وقف", "وفاة", "ووتش", "وسط",
                            "وزراء", "وزارة", "ودي", "وصيف", "ويمبلدون", "وست", "وهمي", "وهج", "وهميا", "والد", "وليد",
                            "وثار",
                            "وجد", "وجه", "وقت", "ويلز", "وجود", "وجيه", "وحد", "وحيد", "ودا", "وداد", "ودرو",
                            "ودى", "وديع", "وراء", "ورانس", "ورث", "ورَّث", "ورد", "وردة", "ورق", "ورم", "وزير",
                            "وسام", "وسائل", "وستون", "وسط", "وسن", "وسيط", "وسيلة", "وسيم", "وصاف", "وصف", "وصْفَ",
                            "وصل", "وضع", "وطن", "وعاء", "وفاء", "وفق", "وفيق", "وقت", "وقع", "وكال", "وكيل",
                            "ولاء", "ولف", "وهب", "وصفها", "وباء", "ونستون", "وضح", "وجب", "وقّع", "ولنغتون", "وحش",
                            "وفر", "وساطته", "ولادة", "ولي", "وفيات", "وزار", "وجّه", "وهماً", "وجَّه", "ويب", "وظيفة",
                            "وظائف", "وقائي"]

    sentence_splitter_exceptions = ["د.", "كي.", "في.", "آر.", "بى.", "جى.", "دى.", "جيه.", "ان.", "ال.", "سى.", "اس.",
                                    "اتش.", "اف."]
    token_split_exceptions = ["،", "*", "’", "‘", ",", "(", ")", "/", "[", "]", "|", "؛", "«", "»", "!", "-", "“", "”",
                                '"', "؟", ":", "…", "..", "...", "\\", "\n"]
    sentence_splitters = ['.', '!', '؟', '\n']
    for token_split_exception in token_split_exceptions:
        text = text.replace(token_split_exception, " " + token_split_exception + " ")
    text = text.replace('  ', ' ')
    tokens = text.split()
    for i, token in enumerate(tokens):
        if token[-1] in sentence_splitters:
            is_exceptions = token in sentence_splitter_exceptions
            if not is_exceptions:
                tokens[i] = token[:-1] + ' ' + token[-1] + 'SENT_SPLITTER'
    tokens = ' '.join(tokens).split()
    for i, token in enumerate(tokens):
        if token.startswith('و'):
            is_exceptions = [token.startswith(exception) and len(token) <= len(exception) + 1 for exception in
                                tokenizer_exceptions]
            if True not in is_exceptions:
                tokens[i] = token[0] + ' ' + token[1:]
    text = (' '.join(tokens))
    text = text.replace(' وال', ' و ال')
    text = text.replace(' لل', ' ل ل')
    text = text.replace(' لإ', ' ل إ')
    text = text.replace(' بالأ', ' ب الأ')
    text = text.replace('وفقا ل', 'وفقا ل ')
    text = text.replace('نسبة ل', 'نسبة ل ')
    sentences = text.split('SENT_SPLITTER')
    return sentences