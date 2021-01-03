from googletrans import Translator

class TranslateArticle:
    def __init__(self, article):
        paragraph = article.split('\n')

        translator = Translator()
        eng_translation = []

        for text in paragraph:
            if text != "":
              eng_translation.append(translator.translate(text).text)

        self.merged_paragraph = list(zip(paragraph, eng_translation))

    def text(self):
        return self.construct_message('\n\n')

    def html(self):
        return self.construct_message('<br><br>')

    def construct_message(self, line_break):
        message = ''
        for org, tran in filter(None, self.merged_paragraph):
            message += org
            message += line_break
            message += tran

        return message
