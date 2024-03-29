from django.contrib import messages
from django.core import mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            context = {
                "name": "Carlos Silva",
                "cpf": "12345678901",
                "email": "carlos.silva@mail.com",
                "phone": "61 99876-1018",
            }
            body = render_to_string("subscriptions/subscription_email.txt", form.cleaned_data)

            mail.send_mail(
                "Confirmação de inscrição",
                body,
                "contato@eventex.com.br",
                ["contato@eventex.com.br", form.cleaned_data["email"]],
            )
            messages.success(request, "Inscrição realizada com sucesso")
            return redirect("/inscricao/")
        else:
            return render(request, "subscriptions/subscription_form.html", {"form": form})
    else:
        context = {"form": SubscriptionForm()}
        return render(request, "subscriptions/subscription_form.html", context)
