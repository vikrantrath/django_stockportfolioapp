from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.
# API key for iex ---> pk_118d842c6f1e4f1eb47d13f6b7ecb5ea


def home(request):
    import requests
    import json
    
    if(request.method == 'POST'):
        ticker = request.POST['ticker']
        api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=pk_118d842c6f1e4f1eb47d13f6b7ecb5ea')
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            print(api_request)
            api = "Error"
        return render(request,'home.html',{'api':api})
    else:
        return render(request,'home.html',{'ticker': "Enter Ticker"})

def about(request):
    return render(request,'about.html',{})

def addStock(request):
    if(request.method == 'POST'):
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,("Stock has Been Added"))
            return redirect('addStock')
    else:
        import requests
        import json
        ticker = Stock.objects.all()
        queryString = ''
        for item in ticker:
            queryString+= (item.ticker+',')
        print(queryString)
        tickerResponse = requests.get(f'https://cloud.iexapis.com/stable/stock/market/batch?symbols={queryString}&types=quote&token=pk_118d842c6f1e4f1eb47d13f6b7ecb5ea')
        try:
            tickerData = json.loads(tickerResponse.content)
            tickerList = []
            for k,v in tickerData.items():
                tickerList.append(v['quote'])
        except Exception as e:
            tickerList = "Error"
        return render(request,'addStock.html',{'tickerData':tickerList})

def deleteStock(request, tickerName):
    print(tickerName)
    item = Stock.objects.get(ticker=tickerName.lower())
    item.delete()
    messages.success(request,("Stock has been Deleted!"))
    return redirect('addStock')