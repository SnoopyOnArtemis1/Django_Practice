from django.shortcuts import render
from .models import Product, Purchase
import pandas as pd
from .utils import get_simple_plot, get_salesman_from_id, get_image
from .forms import PurchaseForm
from django.http import HttpResponse
import matplotlib.pyplot as plt
import seaborn as sns
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df["salesman_id"] = df["salesman_id"].apply(get_salesman_from_id)
    df.rename({'salesman_id':'salesman'}, axis=1, inplace=True) #更換表頭
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    #print(df)

    plt.switch_backend('Agg') #告诉 Matplotlib:使用 "Agg" 后端（backend）来渲染图表，而不是默认的图形用户界面（GUI）后端
    plt.xticks(rotation=45)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout()
    graph = get_image()

    #return HttpResponse("hello salesman")
    return render(request, 'products/sales.html', {'graph': graph})


    '''在数据科学和机器学习中，通常使用 Matplotlib 来绘制图表和图形。
       Matplotlib 有多个可用的后端，用于指定图表的输出方式。
       "Agg" 后端是一种非交互式后端，它将图表渲染为位图（bitmap）图像文件，而不是在图形用户界面中显示。
       这在一些应用场景中非常有用，特别是在生成图像文件或在服务器上自动化生成图表时。

       如果你执行了 plt.switch_backend('Agg')，你将不会看到 Matplotlib 图表的窗口显示，而是图表将被保存为图像文件或用于其他非交互式用途。
       这在一些自动化任务中很常见，例如生成报告、网站上的图表或批量处理数据可视化。'''

@login_required
def chart_select_view(request):
    graph = None
    error_message = None
    df = None
    price = None

    try:
        product_df = pd.DataFrame(Product.objects.all().values())
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id'] #?

        if purchase_df.shape[0] > 0:
            df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x': 'id', 'date_x': 'date'}, axis=1)
            #print(df['date'][0])
            #print(type(df['date'][0]))
            price = df['price']
            if request.method == 'POST':
                chart_type = request.POST['sales']
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                #print(request.POST)
                #print(chart_type)
                #print(date_from,date_to)

                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                # print(df)
                df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                #print(df2)

                if chart_type != "":
                    if date_from != "" and date_to !="":
                        df = df[ (df['date']>date_from) & (df['date']<date_to) ]
                        df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                        graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'], data=df)
                    else:
                        error_message = "Please select a chart type to continue"

                else:
                    error_message = "Please select a chart type to continue"

        else:
            error_message = 'No records in the database'
    except:
        product_df = None
        purchase_df = None
        error_message = 'No records in the database'

    context = {
        'graph':graph,
        'price':price,
        'error_message':error_message,
        # 'products': product_df.to_html(),
        # 'purchases': purchase_df.to_html(),
        # 'df': df,
    }
    
    return render(request, 'products/main.html', context)

@login_required
def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message = None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()

        form = PurchaseForm()
        added_message = 'The purchase has been added'

    context = {
        'form': form,
        'added_message': added_message,
    }
    return render(request, 'products/add.html', context)