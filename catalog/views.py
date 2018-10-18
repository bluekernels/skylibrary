from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
# importing the generic view 
from django.views import generic

# Create your views here.
from .models import Author, Book, BookInstance, Genre

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_instances_on_loan = BookInstance.objects.filter(status__exact='o').count()
    num_instances_on_maintenance = BookInstance.objects.filter(status__exact='m').count()
    num_authors = Author.objects.count()  # 'all()' is implied by default. 

    # Render the HTML template index.html with the data in the context variable 
    return render(
        request,
        'index.html',
        context={'num_books':num_books, 
        'num_instances':num_instances, 
        'num_instances_available':num_instances_available, 
        'num_instances_on_loan':num_instances_on_loan,
        'num_instances_on_maintenance':num_instances_on_maintenance,
        'num_authors':num_authors}
    )

# using the class-based generic list view 
class BookListView(generic.ListView): 
    """
    Generic class-based view for a list of books.
    You don't need to specify the file name , by default , django will be expecting a file name 
    structure like <model_name>_<generic_view_type>
    e.g. book_list 
        book : model name 
        list : the class-based generic view which is list  
    html page expected: book_list.html     
    """
    model = Book
    paginate_by = 3

class BookDetailView(generic.DetailView): 
    """
    Generic class-based view for a detail of books
    html page expected : book_detail.html 
    """
    model = Book
    paginate_by = 3

class AuthorListView(generic.ListView): 
    model = Author 
    paginate_by = 3 

class AuthorDetailView(generic.DetailView): 
    model = Author 
    paginate_by = 3 

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        
from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned' # required permission
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

       
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    #initial={'date_of_death':'05/01/2018',}
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
    

#Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'