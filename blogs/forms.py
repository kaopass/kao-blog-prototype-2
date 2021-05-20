from django import forms
from .models import Blog

class StyleForm(forms.ModelForm):
    favicon = forms.CharField(
        max_length=4,
        help_text="<a href='https://getemoji.com/' target='_blank'>Emoji cheatsheet</a>",
        required=True
    )

    external_stylesheet = forms.CharField(
        help_text="<br>List of <a href='https://www.cssbed.com/' target='_blank'>no-class css themes</a> (only paste the CDN link)",
        required=False,
    )

    custom_styles = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 40}),
        required=False,
    )

    class Meta:
        model = Blog
        fields = ('favicon', 'external_stylesheet', 'custom_styles',)