from .models import Authors, Tags, Quotes, TagInQuote, AboutAuthor, db_connect, create_table
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


class AllDataPipeline:

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        quote = Quotes()
        author = Authors()
        tag = Tags()
        tag_in_q = TagInQuote()

        tags = item['keywords']
        authors = item['author']
        quote = item['quote']
        url = item['url']

        specialChars = '“”'
        for specialChar in specialChars:
            quote = quote.replace(specialChar, '')

        for author in authors:
            author_unique = session.execute(select(Authors).filter(Authors.name == author)).scalar()
            if author_unique:
                pass
            else:
                create_author = Authors(name=author, url=url)
                session.add(create_author)
                session.commit()

        author = session.execute(select(Authors).filter(Authors.name == authors[0])).scalar()
        create_quote = Quotes(quote=quote, author_id=author.id)
        session.add(create_quote)
        session.commit()

        for tag in tags:
            tag_unique = session.execute(select(Tags).filter(Tags.tag == tag)).scalar()
            if tag_unique:
                pass
            else:
                tag_unique = Tags(tag=tag)
                session.add(tag_unique)
                session.commit()

            tag_in_quote = TagInQuote(quotes_id=create_quote.id, tag_id=tag_unique.id)
            session.add(tag_in_quote)
            session.commit()
        session.close()

        return item


class AboutAuthorPipeline:

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        about = AboutAuthor()

        authors = item['author']
        birthday = item['birthday']
        description = item['description']

        create_about = AboutAuthor(name=authors, birthday=birthday, description=description)
        session.add(create_about)
        session.commit()
        session.close()

        return item