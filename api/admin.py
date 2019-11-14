from django.contrib import admin

from .models import Word, Card, Session, Category, Pack


class WordInline(admin.TabularInline):
    model = Word
    extra = 0


class CardAdmin(admin.ModelAdmin):
    inlines = (WordInline,)


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ('started', 'last_activity',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = (WordInline,)


class PackAdmin(admin.ModelAdmin):
    inlines = (WordInline,)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Word)
admin.site.register(Pack, PackAdmin)
