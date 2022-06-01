import factory

from .models import Author, Channel, ChannelLanguage, Content, ContentGenre


class ChannelLanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChannelLanguage


class ChannelFactory(factory.django.DjangoModelFactory):
    title = "TV Shows"
    language = factory.SubFactory(ChannelLanguageFactory)

    class Meta:
        model = Channel


class ContentGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContentGenre


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author


class ContentFactory(factory.django.DjangoModelFactory):
    file = factory.django.FileField()
    rating = 5
    genre = factory.SubFactory(ContentGenreFactory)
    description = "description"

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.add(author)

    class Meta:
        model = Content
