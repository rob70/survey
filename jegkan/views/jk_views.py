from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseNotFound, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from ..models import Question, Evaluation, Topic
from ..forms import EvaluateForm, AnswerForm, BaseAnswerFormSet
from django.forms import inlineformset_factory, formset_factory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

# Create your views here.
""" Anonymous users' view """

def index(request):
    if request.user.is_authenticated:
        """ Landing page authenticated users """
        topic_list = Topic.objects.order_by('-pub_date')[:5]
        context = {'topic_list': topic_list}
    else:

        """ Landing page anonymous users """
        
        context = {}
    return render(request, 'jegkan/index.html', context)


"""
Teacher views

"""

#help function
def is_member(user):
    #return user.groups.filter(name='Member').exists()
    return user.is_staff


@login_required
@user_passes_test(is_member)
def teacher_page(request):
    pass
    

@login_required
def categorydetails(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        context = {
            'topic': topic,
        }
    except Topic.DoesNotExist:
        
        raise Http404("Kan ikke finne den siden")
    return render(request, 'jegkan/categorydetails.html', context,)

@login_required
#@user_passes_test(is_member, login_url='/jegkan/login/')
@permission_required('jegkan.add_question', raise_exception=True)
def manage_questions(request, topic_id):
    """ Legg til eller endre spørsmål """
    topic = Topic.objects.get(pk=topic_id)
    QuestionInlineFormSet = inlineformset_factory(Topic, Question, fields=('question_text',))
    if request.method == "POST":
        
        formset = QuestionInlineFormSet(request.POST, request.FILES, instance=topic)
        if formset.is_valid():
            
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(topic.get_absolute_url())
        else: 
            
    else:
        formset = QuestionInlineFormSet(instance=topic)
    return render(request, 'jegkan/managequestionswfields.html', {'formset': formset})

@login_required
def submit(request, topic_id):
    """Testing Survey-taker submit their completed survey."""
    
    category = Topic.objects.get(pk=topic_id)
    user = request.user
    try:
        survey = Topic.objects.prefetch_related("question_set__evaluation_set").get(
            pk=topic_id
        )
    except Topic.DoesNotExist:
        raise Http404()
    """
    try:
        sub = survey.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()  """

    questions = survey.question_set.all()
    # options is a QuerySet of Evaluation objects for each question
    options = [q.evaluation_set.filter(user=user) for q in questions]
    eva_obj = Evaluation.objects.filter(user=user)
    # Creating a list of dictionaries. This permits me to use the same
    # keyword in the keyword:value pairs.
    evaluation_data = [{'option': l.evaluation}
                    for l in eva_obj]
    
    
    
    form_kwargs = {"empty_permitted": False}
    
    
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions)-len(evaluation_data))
    content = []
    if request.method == "POST":
        
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            
            content.append("formset is valid")

            # with transaction.atomic():
            parent_child_merge = zip(questions, eva_obj)
            x = 0
            for form in formset:
                
                
                opt = form.cleaned_data.get("option")
                q = questions[x]
                
                try:
                    evaluation_object = eva_obj[x]
                    evaluation_object.evaluation = opt
                    evaluation_object.save()
                except IndexError:
                    e = Evaluation(question = q, user = user, evaluation = opt)
                    e.save()                
                x = x+1
            for q, e in parent_child_merge:
                
                content.append(q)
                content.append(e)
                
                
            return HttpResponseRedirect(reverse('jegkan:cat_results', args=(1, )))
            
            
    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs, initial = evaluation_data)
    
    for form in formset:
        
    question_forms = zip(questions, formset)
        
    return render(
        request,
        "jegkan/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset, 'category': category,},
    )

@login_required
def category_results(request, topic_id):
    
    topic = Topic.objects.get(pk=topic_id)
    user = request.user
    try:
        results = Topic.objects.prefetch_related("question_set__evaluation_set").get(
            pk=topic_id
        )
    except Topic.DoesNotExist:
        raise Http404()
    # look up the questions
    questions = results.question_set.all()
    # look up existing evaluations for the user
    options = [q.evaluation_set.filter(user=user) for q in questions]
    # Choosing first evaluation object from evaluation query set associated with the user
    #evaluation_object = question.evaluation_set.filter(user=user)[0]
    # The concrete evaluation from the object
    eva_obj = Evaluation.objects.filter(user=user)
    evaluation_data = [{'option': l.evaluation}
                    for l in eva_obj]
    q_and_e = zip(questions, evaluation_data)
    context = {'questions': questions, 
                'evaluation_data': evaluation_data,
                'q_and_e': q_and_e,
                'topic': topic,
                }
    return render(request, 'jegkan/category_results.html', context )

@login_required
def student_overview(request):
    # start or edit test
    question_categories = Topic.objects.all() 
    context = {'question_categories': question_categories}
    return render(request, 'jegkan/mypage.html', context)


