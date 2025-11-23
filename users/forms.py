from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Le decimos al formulario que use nuestro modelo personalizado
        model = User
        # Lista de campos a mostrar en el formulario
        fields = UserCreationForm.Meta.fields