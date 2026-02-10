from django import forms

class ImageDetectForm(forms.Form):
    image = forms.ImageField(
        label="تصویر را آپلود کنید",
        help_text="حداکثر حجم: ۱۰ مگابایت - فرمت: jpg, png, webp"
    )
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'مثال: این عکس چی هست؟ اشیا رو مشخص کن یا مشکلش چیه؟ (اختیاری)'
        }),
        label="دستور یا سوال (اختیاری)",
        required=False,
        max_length=500
    )