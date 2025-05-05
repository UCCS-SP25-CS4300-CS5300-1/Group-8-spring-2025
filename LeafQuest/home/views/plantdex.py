"""
Views for the PlantDex
"""
import threading

import openai
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from openai import OpenAI

from ..models import Profile
from ..models.captures import CapturedImage
from ..models.captures import GPTFacts
from identify_api.models import StatusChoices


def _get_gpt_facts(class_name):
    fact_entry, created = GPTFacts.objects.get_or_create(species=class_name)
    if created:
        if not settings.OPENAI_API_KEY:
            fact_entry.facts = "AI Facts unavailable, no API key provided."
            return

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert botanist. You are knowledgeable "
                            "about plant species and their fun facts. When given a "
                            "species of plant in a prompt, you will provide 4 fun facts "
                            "about this plant, each fact no longer than 2 sentences. "
                            "Use a helpful and friendly tone."
                            "Your response should be formatted as bullet points."
                            "Your response should not have any introduction or conclusion."
                            "You should not include any information about yourself."
                            "Your response should only contain the fact list."
                            "List the scientific name in the first fact, then every reference of the plant"
                            "for the rest of the response should be the common name."
                            "Do not include any markdown formatting in your response."
                        )
                    },
                    {"role": "user", "content": class_name}
                ],
                model="gpt-4o",
                temperature=0.7,
                max_tokens=512,
            )

            fact_entry.facts = chat_completion.choices[0].message.content
            fact_entry.completed = True
        except openai.RateLimitError:
            fact_entry.facts = ("AI Facts unavailable, RateLimitError\n"
                                "Funds exhausted or Rate Limit Exceeded")
        fact_entry.save()
    return


@login_required
def plantdex_view(request):
    context = {}

    captures = CapturedImage.objects.filter(user=request.user).order_by('-uploaded_at')
    context['captures'] = captures

    return render(request, 'plantdex/index.html', context)


@login_required
def plantdex_detail_view(request, pk):
    context = {}

    capture = get_object_or_404(CapturedImage, pk=pk)
    context['capture'] = capture

    context['user'] = capture.user
    context['profile'] = Profile.objects.get(user=capture.user)

    # Build page content
    ident_species = capture.ident_request.result
    if ident_species is None or ident_species == "":
        context['species'] = "Unknown"
        if capture.ident_request.req_status == StatusChoices.FAILED:
            if capture.ident_request.status_reason == "No Plant Identified":
                context['req_status'] = "bad plant"
            else:
                context['req_status'] = "failed"
        elif capture.ident_request.req_status == StatusChoices.PENDING:
            context['req_status'] = "pending"
        elif capture.ident_request.req_status == StatusChoices.CREATED:
            context['req_status'] = "created"

    # Get facts if the species is identified
    else:
        context['species'] = ident_species
        facts = GPTFacts.objects.filter(species=ident_species, completed=True)
        if len(facts) > 0:
            context['facts'] = facts[0].facts
        else:
            threading.Thread(target=_get_gpt_facts, args=(capture.ident_request.result,), daemon=True).start()
            context['facts'] = "Generating facts, please check back later."

    return render(request, 'plantdex/details.html', context)
