from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .forms import CustomUserCreationForm, UserProfileUpdateForm, PostForm, CommentForm
from .models import Post, Comment
from django.db.models import Count

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Use prefetch_related to fetch tags and comments in fewer queries
        queryset = queryset.prefetch_related('tags')
        # Use annotate with Count to get the comment count for each post
        queryset = queryset.annotate(comment_count=Count('comments'))
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        # Fetch the post and prefetch its comments
        return super().get_queryset().prefetch_related('comments')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        # The comments are already prefetched, so accessing them won't cause new queries
        context['comments'] = self.object.comments.order_by('-created_at')
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', pk=pk)

@login_required
def edit_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, author=request.user, post__pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, author=request.user, post__pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})