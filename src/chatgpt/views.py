from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from markdown import markdown

from accounts.models import Account
from lib.views import get_paginated_items, get_db_items
from lib.utils import markdown_item, markdown_items, export_history
from .models import ChatGPTDB
from .forms import ChatGPTForm
from .chains import get_conversation


@login_required
def get_chatgpt_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = ChatGPTForm(request.POST)
        if form.is_valid():
            user_message = form.data['input_message']
            ai_message = get_conversation(user, user_message)
            context['user_message'] = user_message
            ai_message_html = markdown(ai_message)
            context['ai_message'] = ai_message_html
            instance = form.save(commit=False)
            # author = Account.objects.filter(email=user.email).first()
            author = Account.objects.get(email=user.email)
            instance.author = author
            instance = ChatGPTDB(author=author, user_message=user_message, ai_message=ai_message)
            instance.save()
            # context['output_message'] = output_message
            return render(request, 'chatgpt/get_chatgpt.html', context)
    else:
        form = ChatGPTForm()
    context['form'] = form
    return render(request, 'chatgpt/get_chatgpt.html', context)


@login_required
def regen_chatgpt_view(request, *args, **kwargs):
    context = {}
    user = request.user
    author = Account.objects.get(email=user.email)
    form = ChatGPTForm()
    item = ChatGPTDB.objects.filter(author=author).last()
    user_message = f"Based on my query {item.user_message}, reflect on your output and find ways to improve on your output {item.ai_message}"
    ai_message = get_conversation(user, user_message)
    # reproduce a simple message for display and save
    user_message = f"Reflect on my query: {item.user_message}"
    context['user_message'] = user_message
    ai_message_html = markdown(ai_message)
    context['ai_message'] = ai_message_html
    instance = form.save(commit=False)
    instance.author = author
    instance = ChatGPTDB(author=author, user_message=user_message, ai_message=ai_message)
    instance.save()
    context['form'] = form
    return render(request, 'chatgpt/get_chatgpt.html', context)


@login_required
def get_chatgpt_detail_view(request, slug):
    context = {}
    item = get_object_or_404(ChatGPTDB, slug=slug)
    context['item'] = markdown_item(item)
    return render(request, 'chatgpt/get_chatgpt_detail.html', context)


@login_required
def chatgpt_list_view(request, *args, **kwargs):
    context = {}
    paginated_items = get_paginated_items(request, ChatGPTDB)
    if paginated_items:
        context['items'] = paginated_items
        return render(request, 'chatgpt/chatgpt_list.html', context)
    else:
        context['items'] = {}
        return render(request, 'chatgpt/chatgpt_list.html', context)


@login_required
def chatgpt_history_view(request, *args, **kwargs):
    context = {}
    paginated_items = get_paginated_items(request, ChatGPTDB)
    if paginated_items:
        context['items'] = markdown_items(paginated_items)
        return render(request, 'chatgpt/chatgpt_history.html', context)
    else:
        context['items'] = {}
        return render(request, 'chatgpt/chatgpt_history.html', context)


@login_required
def export_chatgpt_history_view(request, *args, **kwargs):
    context = {}
    user = request.user
    items = get_db_items(request, ChatGPTDB)
    if items:
        export_file = export_history(user, items)
        if export_file:
            context['status_message'] = f'Success! File ({export_file}) has been exported to {user.email}'
        else:
            context['status_message'] = f'Fail! No File has been exported to {user.email}'
        return render(request, 'chatgpt/export_chatgpt_history.html', context)
    else:
        context['status_message'] = f'No file has been exported'
        return render(request, 'chatgpt/export_chatgpt_history.html', context)


@login_required
def delete_chatgpt_list_view(request, slug):
    item = get_object_or_404(ChatGPTDB, slug=slug)
    item.delete()
    previous_page_url = request.META.get('HTTP_REFERER')
    if previous_page_url:
        return redirect(previous_page_url)
    else:
        # Redirect to a default page if there's no previous page URL available
        return redirect('chatgpt/chatgpt_list.html')


@login_required
def delete_chatgpt_history_view(request, slug):
    item = get_object_or_404(ChatGPTDB, slug=slug)
    item.delete()
    previous_page_url = request.META.get('HTTP_REFERER')
    if previous_page_url:
        return redirect(previous_page_url)
    else:
        # Redirect to a default page if there's no previous page URL available
        return redirect('chatgpt/chatgpt_history.html')


@login_required
def delete_chatgpt_list_view_org(request, slug):
    item = get_object_or_404(ChatGPTDB, slug=slug)
    item.delete()
    # reload item_view
    context = {}
    paginated_items = get_paginated_items(request, ChatGPTDB)
    if paginated_items:
        context['items'] = paginated_items
        return render(request, 'chatgpt/chatgpt_list.html', context)
    else:
        context['items'] = {}
        return render(request, 'chatgpt/chatgpt_list.html', context)


@login_required
def delete_chatgpt_history_view_org(request, slug):
    item = get_object_or_404(ChatGPTDB, slug=slug)
    item.delete()
    # reload item_view
    context = {}
    paginated_items = get_paginated_items(request, ChatGPTDB)
    if paginated_items:
        context['items'] = markdown_items(paginated_items)
        return render(request, 'chatgpt/chatgpt_history.html', context)
    else:
        context['items'] = {}
        return render(request, 'chatgpt/chatgpt_history.html', context)
