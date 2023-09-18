from django import forms
from .models import Purchase, Product

# .values_list("name", flat=True)
class PurchaseForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     label='Product', 
                                     widget=forms.Select(attrs={'class': 'ui selection dropdown field-with'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label_from_instance = self.get_product_display_name

    def get_product_display_name(self, obj):
        # 返回你想要用作显示名称的字段的值，这里使用 'name'
        return obj.name
    class Meta:
        model = Purchase
        fields = ['product', 'price', 'quantity']
     