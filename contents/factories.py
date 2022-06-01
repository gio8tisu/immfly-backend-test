import factory

from .models import Author, Channel, ChannelLanguage, Content, ContentGenre


class ChannelLanguageFactory(factory.django.DjangoModelFactory):
    language = factory.Faker("language_name")
    code = factory.Faker("language_code")

    class Meta:
        model = ChannelLanguage


class ContentGenreFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

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


class ChannelFactory(factory.django.DjangoModelFactory):
    title = "TV Shows"
    language = factory.SubFactory(ChannelLanguageFactory)
    picture = factory.django.ImageField()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        contents = kwargs.pop("contents", None)
        subchannels = kwargs.pop("subchannels", None)

        manager = cls._get_manager(model_class)
        return manager.create_channel(
            contents=contents, subchannels=subchannels, **kwargs
        )

    class Meta:
        model = Channel
