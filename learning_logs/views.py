from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """Página principal do learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas."""
    topic = Topic.objects.get(id = topic_id)

    #Garante que o tópico do usuário seja protegido pela entrada de outros users.
    if topic.owner != request.user:
        return Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formúlário em branco
        form = TopicForm()
    else:
        #Dados de POST submetidos; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Acrescentando novas anotações para um assunto em particular."""
    topic = Topic.objects.get(id = topic_id)

    # Garante que o tópico do usuário seja protegido pela entrada de outros users.
    if topic.owner != request.user:
        return Http404

    if request.method != 'POST':
        # Nenhum dado submetido; cria um formúlário em branco
        form = EntryForm()

    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma anotação existente."""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    # Garante que o tópico do usuário seja protegido pela entrada de outros users.
    if topic.owner != request.user:
        return Http404

    if request.method != 'POST':
        #Requisição inicial; Preenche previamente o formulário com a anotação atual (antes de editar)
        form = EntryForm(instance=entry)

    else:
        #Atualiza os dados da anotação
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


