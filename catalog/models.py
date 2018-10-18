from django.db import models   

# Creating the "Genre" models here.
class Genre(models.Model): 
    """
    This Model represents a book genre (e.g. Science Fiction, Non Fiction, Military history, Romance)
    """
    name = models.CharField(max_length=30, blank=False, help_text="Enter a book genre (e.g. Science Fiction, None Fiction, Cybersecurity, Military history, Romance etc.")        
    
    def __str__(self): 
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Language(models.Model):
    """
    Model representing the Language that was used in the book (e.g. English, French, Japanese, etc.)
    """

    name = models.CharField(max_length=30, blank=False, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    
    def __str__(self):

        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
class Book(models.Model): 
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=100, help_text="The title of book")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=3000, help_text='Enter a brief description of the book with the maximum length of 3000 characters')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    number_of_pages = models.IntegerField('PAGE NUMBER', help_text='The number of pages of book', blank=False)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book', blank=True)
    BOOK_INNER_COLOR = (
        ('w', 'White'),
        ('m', 'Milk'),
        ('b', 'Black')
    )
    status = models.CharField('INNER COLOUR', max_length=1, choices=BOOK_INNER_COLOR, default='w', help_text='The inner color of the book which may either by white or milk color', blank=False)
   

    def __str__(self): 
        """
        String for representing the Model object
        """
        return self.title

    
    def get_absolute_url(self): 
        """
        Returns the url to access a detail record for this book. 
        """
        return reverse('book-detail', args=[str(self.id)])

    # function to display the genre in the list_diplay in the admin.py
    def display_genre(self): 
        """
        Creates a string for the Genre. This is required to display genre in Admin
        """
        return ', '.join([genre.name for genre in self.genre.all()])
    display_genre.short_description = 'Genre'

import uuid # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User #Required to assign User as a borrower

class BookInstance(models.Model): 
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=100, help_text="addition book details")
    due_back = models.DateField(null=True, blank=True) # date at which the book is expected to come available after being borrowed or in maintenance
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'), 
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=False, default='m', help_text='Book availability status')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),) 
    
    def __str__(self): 
        """
        String for representing the Model object 
        """
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    """
    Model representing an author 
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Date format : YYYY-MM-DD")
    date_of_death = models.DateField(null=True, blank=True)

    class Meta: 
        ordering = ["last_name", "first_name"]
        
    
    def get_absolute_url(self): 
        """
        Returns the url to access a particular author instance 
        """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self): 
        """
        String for representing the Model object.
        """
        return '{0}, {1}'. format(self.last_name, self.first_name)



