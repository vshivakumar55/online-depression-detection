
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count

# Create your views here.
from Remote_User.models import tweets_Model,ClientRegister_Model,review_Model


def tweetserverlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('admin')
        password = request.POST.get('password')
        if admin == "Server" and password =="Server":
            return redirect('viewallusers')


    return render(request,'TServer/tweetserverlogin.html')

def viewtreandingquestions(request,chart_type):
    dd = {}
    pos,neu,neg =0,0,0
    poss=None
    topic = tweets_Model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics=t['ratings']
        pos_count=tweets_Model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss=pos_count
        for pp in pos_count:
            senti= pp['names']
            if senti == 'positive':
                pos= pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics]=[pos,neg,neu]
    return render(request,'TServer/viewtreandingquestions.html',{'object':topic,'dd':dd,'chart_type':chart_type})

def View_Positive_reviews(request):

    rtype='Positive'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'TServer/View_Positive_reviews.html',{'list_objects': obj})

def View_Negative_reviews(request):

    rtype='Negative'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'TServer/View_Negative_reviews.html',{'list_objects': obj})

def View_Depression_reviews(request):

    rtype='Depression'
    #obj = review_Model.objects.all()

    obj = review_Model.objects.all().filter(sanalysis=rtype)

    return render(request,'TServer/View_Depression_reviews.html',{'list_objects': obj})



def viewallusers(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'TServer/viewallusers.html',{'objects':obj})

def negativechart(request,chart_type):
    dd = {}
    pos, neu, neg = 0, 0, 0
    poss = None
    topic = tweets_Model.objects.values('ratings').annotate(dcount=Count('ratings')).order_by('-dcount')
    for t in topic:
        topics = t['ratings']
        pos_count = tweets_Model.objects.filter(topics=topics).values('names').annotate(topiccount=Count('ratings'))
        poss = pos_count
        for pp in pos_count:
            senti = pp['names']
            if senti == 'positive':
                pos = pp['topiccount']
            elif senti == 'negative':
                neg = pp['topiccount']
            elif senti == 'nutral':
                neu = pp['topiccount']
        dd[topics] = [pos, neg, neu]
    return render(request,'TServer/negativechart.html',{'object':topic,'dd':dd,'chart_type':chart_type})


def charts(request,chart_type):
    chart1 = tweets_Model.objects.values('names').annotate(dcount=Avg('ratings'))
    return render(request,"TServer/charts.html", {'form':chart1, 'chart_type':chart_type})

def dislikeschart(request,dislike_chart):
    charts = tweets_Model.objects.values('names').annotate(dcount=Avg('dislikes'))
    return render(request,"TServer/dislikeschart.html", {'form':charts, 'dislike_chart':dislike_chart})

def View_All_User_Tweets(request):
    chart = tweets_Model.objects.values('names','uname','ratings','dislikes','uses','sanalysis','tdesc').annotate(dcount=Avg('usefulcounts'))
    return render(request,'TServer/View_All_User_Tweets.html',{'objects':chart})

def View_Sentiment_Analysis(request):

    if request.method == "POST":
        kword = request.POST.get('type')
        obj = tweets_Model.objects.all().filter(sanalysis=kword)
        return render(request, 'TServer/View_Sentiment_Analysis.html', {'objs': obj})
    return render(request, 'TServer/View_Sentiment_Analysis.html')

def View_Depression_Posts(request):

    kword = 'Depression'
    obj = tweets_Model.objects.all().filter(sanalysis=kword)
    return render(request, 'TServer/View_Depression_Posts.html', {'objs': obj})
