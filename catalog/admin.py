from django.contrib import admin

# Register your models here.
from .models import Genre, Book, BookInstance, Language, Author
admin.site.register(Genre)
admin.site.register(Language)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin): 
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model 
admin.site.register(Author, AuthorAdmin)
# or @admin.register(Author)

class BooksInstanceInline(admin.TabularInline): 
    model = BookInstance

# Register the Admin classes for Book using the decorator 
@admin.register(Book)
class BookAdmin(admin.ModelAdmin): 
    """
        genre field cannot be directly specified because it is a ManyToManyFIeld (Django prevents this becuase 
        there would be a large database access "cost" in doing so) instead we'll define a display_genre function 
        to get the information as a string
    """
    list_display = ('title', 'author', 'display_genre')  
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator 
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin): 
    list_display = ('book','status','borrower','due_back','id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
  