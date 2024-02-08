from django.db import connection


def get_table_app(request, app_name):
    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        app_table_names = [
            name for name in all_table_names if name.startswith(app_name + "_")
        ]
        table_columns = {
            table: connection.introspection.get_table_description(cursor, table)
            for table in app_table_names
        }
        # print("table_columns: ", table_columns.values())
        return table_columns


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}


def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in text)


def get_dj_code_generate(app_name, model_name):

    prefix = app_name.__len__() + 1
    model_name = model_name[prefix:]

    # for urls.py
    urls_gen = ""
    urls_gen += f"\npath('{model_name}/', include('{app_name}.urls'))"
    urls_gen += (
        f"\npath('{model_name}/', views.{model_name}_list, name='{model_name}-list')"
    )
    urls_gen += f"\npath('{model_name}/create/', views.{model_name}_create, name='{model_name}-create')"
    urls_gen += f"\npath('{model_name}/<int:pk>', views.{model_name}_detail, name='{model_name}-detail')"
    urls_gen += f"\npath('{model_name}/<int:pk>/update', views.{model_name}_update, name='{model_name}-edit')"
    urls_gen += f"\npath('{model_name}/<int:pk>/delete', views.{model_name}_delete, name='{model_name}-delete')"
    urls_gen = html_escape(urls_gen).strip()

    # # for views.py
    views_gen = f"def {model_name}_list(request):"
    views_gen += f"\n    {model_name}s = {model_name}.objects.all()"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_list.html', '{model_name}s': {model_name}s)"
    views_gen += f"\n\ndef {model_name}_detail(request, pk):"
    views_gen += f"\n    {model_name} = {model_name}.objects.get(pk=pk)"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_detail.html', '{model_name}': {model_name})"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_detail.html', '{model_name}': {model_name})"
    views_gen += f"\n\ndef {model_name}_create(request):"
    views_gen += f"\n    form = {model_name}Form()"
    views_gen += (
        f"\n    return render(request, '{app_name}/{model_name}_create.html', )"
    )
    views_gen += f"\n\ndef {model_name}_update(request, pk):"
    views_gen += f"\n    {model_name} = {model_name}.objects.get(pk=pk)"
    views_gen += f"\n    form = {model_name}Form(instance={model_name})"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_edit.html', 'form': 'form')"
    views_gen += f"\n\ndef {model_name}_delete(request, pk):"
    views_gen += f"\n    {model_name} = {model_name}.objects.get(pk=pk)"
    views_gen += f"\n    return render(request, '{app_name}/{model_name}_delete.html', '{model_name}': {model_name})"
    views_gen = html_escape(views_gen)

    # for forms.py
    forms_gen = f"class {model_name}Form(forms.ModelForm):"
    forms_gen += f"\n    class Meta:"
    forms_gen += f"\n        model = {model_name}"
    forms_gen += f"\n        fields = '__all__'"
    forms_gen = html_escape(forms_gen)

    # for html
    html_gen = f"<h1>{model_name} </h1>"
    html_gen += f"\n<p>Hello world!</p>"
    html_gen = html_escape(html_gen)

    context_gen = {
        "urls_gen": urls_gen,
        "views_gen": views_gen,
        "forms_gen": forms_gen,
        "html_gen": html_gen,
    }

    return context_gen
