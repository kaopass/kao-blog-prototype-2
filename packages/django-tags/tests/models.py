import uuid

from django.db import models
from tags.managers import TaggableManager
from tags.models import (
    CommonGenericTaggedItemBase,
    GenericTaggedItemBase,
    GenericUUIDTaggedItemBase,
    ItemBase,
    Tag,
    TagBase,
    TaggedItem,
    TaggedItemBase,
)


# Ensure that tow Taggable Manager with custom through model are allowed.
class Through1(TaggedItemBase):
    content_object = models.ForeignKey("MultipleTags", on_delete=models.CASCADE)


class Through2(TaggedItemBase):
    content_object = models.ForeignKey("MultipleTags", on_delete=models.CASCADE)


class MutipleTags(models.Model):
    tags1 = TaggableManager(through=Through1, related_name="tags1")
    tags2 = TaggableManager(through=Through2, related_name="tags2")


# Ensure that two TaggableManagers with GFK via different through models are allowed.
class ThroughGFK(GenericTaggedItemBase):
    tag = models.ForeignKey(Tag, related_name="tagged_items", on_delete=models.CASCADE)


class MultipleTagsGFK(models.Model):
    tags1 = TaggableManager(related_name="tagsgfk1")
    tags2 = TaggableManager(through=ThroughGFK, related_name="tagsgfk2")


class BlankTagModel(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class BaseFood(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MultiInheritanceLazyResolutionFoodTag(TaggedItemBase):
    content_object = models.ForeignKey(
        "MultiInheritanceFood", related_name="tagged_items", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = [["content_object", "tag"]]


class MultiInheritanceFood(BaseFood):
    tags = TaggableManager(through=MultiInheritanceLazyResolutionFoodTag)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=50)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class HousePet(Pet):
    trained = models.BooleanField(default=False)

# Test direct-tagging with custom through model
