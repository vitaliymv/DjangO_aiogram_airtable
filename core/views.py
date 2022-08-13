from django.views.generic import TemplateView, FormView
from pyairtable.formulas import match
from core.forms import LoginForm
from core.services import decrypt
from django_aiogram_airtable.settings import table


class IndexView(TemplateView):
    template_name = "index.html"


class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            "profile": table.get(kwargs.get("id"))
        })
        return context


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/profile"

    def get_success_url(self):
        formula = match(
            {
                "username": self.request.POST['username'],
            }
        )
        user = table.first(formula=formula)
        if decrypt(user.get("fields").get("password")) == self.request.POST["password"]:
            return f"/profile/{user.get('id')}"
