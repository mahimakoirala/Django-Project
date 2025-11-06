from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required #everything related to auth is in contrib.
# Create your views here.
def index(request):
  return render(request, 'index.html')

def tweet_list(request):
  tweets = Tweet.objects.all().order_by('-created_at')
  return render(request, 'tweet_list.html', {'tweets': tweets} )

@login_required   #decorator
def tweet_create(request):
  if request.method == "POST":
    form = TweetForm(request.POST, request.FILES)
    if form.is_valid():
      tweet = form.save(commit = False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')
  else:
    form = TweetForm()
  return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)  #we need to get tweet so we used this .we will pass parameters tweet, tweet_id and user. the user can only edit the tweet if it is their tweet.
  if request.method == 'POST': 
    form = TweetForm(request.POST, request.FILES, instance=tweet) #for edit tweet, we also need to pass instance to know that we are editing the old tweet. 
    if form.is_valid():
      tweet = form.save(commit=False) # commit = False meaning dont save this object in memory, just create it in memory.
      tweet.user = request.user #add extra data before saving
      tweet.save() # now save to db
      return redirect('tweet_list')
  else:
    form = TweetForm(instance= tweet)
  return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
  tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user) #pk:primary key, request.user means the same user who posted the tweet. 
  if request.method == 'POST':
    tweet.delete()
    return redirect('tweet_list')
  return render(request, 'tweet_confirm_delete.html',{'tweet': tweet} ) #renders a html confirmation page(template) when user first requests to delete a tweet. this line also passes the tweet to the template. 

def register(request):
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      user = form.save(commit = False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      login(request, user)
      return redirect('tweet_list')
  else:
    form = UserRegistrationForm()
  return render(request, 'registration/register.html', {'form': form})