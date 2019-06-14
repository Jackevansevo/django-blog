from django.forms import ModelForm
from django.forms.widgets import TextInput
from django.contrib import admin

# Register your models here.
from posts.models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"

    exclude = ("author", "markdown")
    prepopulated_fields = {"slug": ("title",)}

    list_display = ("title", "author", "pub_date")
    list_filter = ("tags__name", "pub_date")
    autocomplete_fields = ("tags",)
    search_fields = ("title",)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class TagAdminForm(ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
        widgets = {"color_code": TextInput(attrs={"type": "color"})}


class PostInline(admin.TabularInline):
    model = Post.tags.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ("name", "colored_code")
    search_fields = ("name",)
    inlines = (PostInline,)
    prepopulated_fields = {"slug": ("name",)}
