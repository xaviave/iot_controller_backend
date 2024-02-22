from django import forms


class AddProductForm(forms.Form):
    product_type = forms.ChoiceField(
        choices=[
            ("led_panel", "LedPanel"),
            # ("coffee_machine", "CoffeeMachine")
        ]
    )
    quantity = forms.IntegerField(min_value=1, initial=1)
