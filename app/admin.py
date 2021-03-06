"""Administration models"""

from django.contrib import admin

from .models import Message, MessageHistory

class MessageAdmin(admin.ModelAdmin):
    """
    Message administration model.
    Here, we intercept the soft deletion of messages to add an entry
    in the history.
    """

    def save_model(self, request, obj, form, change):
        """Actual place where we intercept the form"""

        super(MessageAdmin, self).save_model(request, obj, form, change)

        if not change or 'is_deleted' not in form.changed_data:
            return

        is_deleted = form.cleaned_data['is_deleted']

        # if just deleted: we add a delete history
        # is just recovered: we remove the delete history
        if is_deleted:
            MessageHistory(message=obj, is_addition=False).save()
        else:
            MessageHistory.objects.get(message=obj, is_addition=False).delete()

admin.site.register(Message, MessageAdmin)
