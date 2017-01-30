from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.db.models import Q
# Create your views here.


def home(request):
    games = Game.objects.all().order_by('-released_date')[:6]
    reviews = Game_Review.objects.all().order_by('-published_date')[:6]
    return render(request, 'main/home.html', {'games': games, 'reviews': reviews})


def games(request, filter):
    games = Game.objects.all().order_by('-released_date')

    if filter[1] == ' ':
        games = Game.objects.none()
    elif filter == 'All':
        games = Game.objects.all()
    elif filter[0] == 'c':
        games = Game.objects.filter(console=filter[1:])
    elif filter[0] == 'y':
        games = Game.objects.filter(released_date__year=filter[1:])
    elif filter[0] == 'g':
        games = Game.objects.filter(category__name=filter[1:])
    elif filter[0] == 't':
        games = Game.objects.filter(title__contains=filter[1:])
    elif filter[0] == 's':
        if filter[1:] == 'Date':
            games = Game.objects.all().order_by('-released_date')
        elif filter[1:] == 'Title':
            games = Game.objects.all().order_by('title')


    # show 6 games per page
    paginator = Paginator(games, 6)

    page = request.GET.get('page')
    try:
        games = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        games = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        games = paginator.page(paginator.num_pages)

    return render(request, 'main/games.html', {'games': games})


def reviews(request):
    reviews = Game_Review.objects.all()

    author = request.GET.get('author','')
    try :
        author = int(author)

    except:
        author=False


    title=request.GET.get('title','')
    year=request.GET.get('year','')
    platform=request.GET.get('platform','')

    if author == False :
        if title == ' ':
            latest_reviews = Game_Review.objects.none()
        elif title == '' and (year == '') and (platform == ''):
            latest_reviews = Game_Review.objects.all().order_by('-published_date')[:4]
        elif title == '' and (year == 'All') and (platform == 'All'):
            latest_reviews = Game_Review.objects.all().order_by('-published_date')
        elif year == 'All' and platform == 'All':
            latest_reviews = Game_Review.objects.all().filter(Q(game__title__icontains=title) | Q(title__icontains=title)).order_by('-published_date')
        elif year == 'All':
            latest_reviews = Game_Review.objects.filter(Q(game__title__icontains=title) & Q(game__console__icontains=platform)).order_by('-published_date')
        elif platform == 'All':
            latest_reviews = Game_Review.objects.filter(Q(game__title__icontains=title) & Q(game__released_date__year=year)).order_by('-published_date')
        else:
            latest_reviews = Game_Review.objects.filter(Q(game__title__icontains=title) & Q(game__released_date__year=year) & Q(game__console__icontains=platform)).order_by('-published_date')
    else:
        latest_reviews = Game_Review.objects.filter(author=author).order_by('-published_date')

    return render(request, 'main/reviews.html', {'reviews': reviews, 'latest_reviews': latest_reviews})


def videos(request, filter):
    games = Game.objects.all().order_by('-released_date')
    videos = Video.objects.all()

    if filter == ' ':
        videos = Video.objects.none()
    elif filter == 'All':
        videos = Video.objects.all()
    else:
        videos = Video.objects.filter(title__contains=filter)
    # show 4 games per page
    paginator = Paginator(videos, 8)

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        videos = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'main/videos.html', {'videos': videos, 'games': games})


def gallery(request):
    games = Game.objects.all()
    return render(request, 'main/gallery.html', {'games': games})


def contact(request):
    return render(request, 'main/contact.html', {})


def error404(request):
    return render(request, 'main/404.html', {})


def search_results(request, filter):
    if filter == ' ':
        games = Game.objects.none()
        reviews = Game_Review.objects.none()
        videos = Video.objects.none()
    else:
        games = Game.objects.filter(title__icontains=filter)
        reviews = Game_Review.objects.filter(Q(game__title__icontains=filter) | Q(title__icontains=filter))
        videos = Video.objects.filter(title__icontains=filter)

    # show 3 games per page
    paginator = Paginator(games, 3)

    page = request.GET.get('page')
    try:
        games = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        games = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        games = paginator.page(paginator.num_pages)

    # show 3 reviews per page
    paginator = Paginator(reviews, 3)

    page = request.GET.get('page1')
    try:
        reviews = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        reviews = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reviews = paginator.page(paginator.num_pages)

    # show 4 videos per page
    paginator = Paginator(videos, 4)

    page = request.GET.get('page2')
    try:
        videos = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        videos = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'main/search-results.html', {'games': games, 'reviews': reviews, 'videos': videos})

def game_single(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'main/games-single.html', {'game': game})


def review_single(request, rev):
    review = get_object_or_404(Game_Review, game_id=rev)
    return render(request, 'main/reviews-single.html', {'review': review})


def video_single(request, vid):
    review = get_object_or_404(Game_Review, game_id=vid)
    videos = Video.objects.filter(game_id=vid)
    return render(request, 'main/videos-single.html', {'videos': videos, 'review': review})


