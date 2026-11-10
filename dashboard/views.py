from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.conf import settings
from openai import OpenAI

from applications.models import Application
from jobs.models import Job


# ============================================================
# MAIN DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    if request.user.role == "client":
        return redirect("client_dashboard")

    return redirect("student_dashboard")


# ============================================================
# STUDENT DASHBOARD
# ============================================================

@login_required
def student_dashboard(request):

    applications = Application.objects.filter(
        student=request.user
    ).select_related("job")

    context = {
        "total_applications": applications.count(),

        "pending_applications": applications.filter(
            status="Pending"
        ).count(),

        "accepted_applications": applications.filter(
            status="Accepted"
        ).count(),

        "rejected_applications": applications.filter(
            status="Rejected"
        ).count(),

        "recent_applications": applications.order_by(
            "-applied_at"
        )[:5],
    }

    return render(
        request,
        "dashboard/student_dashboard.html",
        context
    )


# ============================================================
# CLIENT DASHBOARD
# ============================================================

@login_required
def client_dashboard(request):

    jobs = Job.objects.filter(
        client=request.user
    ).order_by("-id")

    applications = Application.objects.filter(
        job__client=request.user
    ).select_related(
        "job",
        "student"
    ).order_by(
        "-applied_at"
    )

    context = {
        "jobs": jobs,

        "applications": applications,

        "total_jobs": jobs.count(),

        "total_applications": applications.count(),

        "pending_applications": applications.filter(
            status="Pending"
        ).count(),

        "accepted_applications": applications.filter(
            status="Accepted"
        ).count(),
    }

    return render(
        request,
        "dashboard/client_dashboard.html",
        context
    )


# ============================================================
# AI CAREER ASSISTANT - GROQ
# ============================================================

@login_required
def ai_assistant(request):

    # ========================================================
    # GET EXISTING CHAT HISTORY
    # ========================================================

    chat_history = request.session.get(
        "ai_chat_history",
        []
    )


    # ========================================================
    # CLEAR CHAT
    #
    # Supports BOTH:
    #
    # /dashboard/ai-assistant/?clear=1
    #
    # and POST:
    #
    # clear_chat=1
    # ========================================================

    if (
        request.GET.get("clear") == "1"
        or request.POST.get("clear_chat") == "1"
    ):

        request.session["ai_chat_history"] = []

        request.session.modified = True

        return redirect("ai_assistant")


    # ========================================================
    # SEND MESSAGE
    # ========================================================

    if request.method == "POST":

        question = request.POST.get(
            "message",
            ""
        ).strip()


        if question:

            try:

                if not settings.GROQ_API_KEY:
                    raise RuntimeError(
                        "GROQ_API_KEY is not configured."
                    )

                # =================================================
                # CREATE GROQ CLIENT
                # =================================================

                client = OpenAI(
                    api_key=settings.GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1"
                )


                # =================================================
                # SYSTEM INSTRUCTION
                # =================================================

                system_instruction = (

                    "You are the CampusLance AI Assistant. "

                    "CampusLance is a platform where college "
                    "students can find freelance jobs and clients "
                    "can hire students. "

                    "Help users with freelancing, jobs, skills, "
                    "resumes, proposals, interviews, career "
                    "development and professional communication. "

                    "Give practical, accurate and useful answers. "

                    "IMPORTANT PLANNING RULES: "

                    "When the user asks for a learning plan, "
                    "career plan, study plan, roadmap, preparation "
                    "plan, or schedule, follow the exact duration "
                    "requested by the user. "

                    "If the user asks for a 3-month plan, create "
                    "a complete 3-month plan covering approximately "
                    "12 weeks. Do NOT replace it with a 1-week, "
                    "2-week, or shorter plan. "

                    "For a 3-month plan, organize the answer into "
                    "Month 1, Month 2, and Month 3, with weekly "
                    "goals where appropriate. "

                    "For a 6-month plan, cover all 6 months. "

                    "For a 1-year plan, cover the full year. "

                    "Never silently shorten the requested duration. "

                    "If the user specifies a number of weeks or "
                    "months, make sure the final answer actually "
                    "covers that number of weeks or months. "

                    "For learning plans, include practical topics, "
                    "skills, projects, exercises, and milestones "
                    "when appropriate. "

                    "Remember previous messages in the conversation "
                    "and use them when they are relevant. "

                    "Do not unnecessarily repeat the user's question. "

                    "Use headings, numbered lists, tables, or bullet "
                    "points when they improve readability. "

                    "Keep simple answers concise, but provide "
                    "sufficient detail for detailed plans and "
                    "roadmaps."
                )


                # =================================================
                # BUILD GROQ MESSAGE HISTORY
                # =================================================

                messages = [

                    {
                        "role": "system",
                        "content": system_instruction
                    }

                ]


                # =================================================
                # ADD PREVIOUS CHAT HISTORY
                # =================================================

                for chat_message in chat_history:

                    role = chat_message.get("role")

                    text = chat_message.get(
                        "text",
                        ""
                    )

                    if not text:
                        continue


                    # Only allow valid Groq roles
                    if role not in [
                        "user",
                        "assistant"
                    ]:
                        continue


                    messages.append({

                        "role": role,

                        "content": text

                    })


                # =================================================
                # ADD CURRENT USER MESSAGE
                # =================================================

                messages.append({

                    "role": "user",

                    "content": question

                })


                # =================================================
                # SEND REQUEST TO GROQ
                # =================================================

                response = client.chat.completions.create(

                    model="openai/gpt-oss-20b",

                    messages=messages,

                    temperature=0.7,

                    max_tokens=1200

                )


                # =================================================
                # GET AI RESPONSE
                # =================================================

                answer = response.choices[0].message.content


                if not answer:

                    answer = (
                        "Sorry, I couldn't generate a response. "
                        "Please try again."
                    )


                # =================================================
                # SAVE USER MESSAGE
                # =================================================

                chat_history.append({

                    "role": "user",

                    "text": question

                })


                # =================================================
                # SAVE AI MESSAGE
                # =================================================

                chat_history.append({

                    "role": "assistant",

                    "text": answer

                })


                # =================================================
                # KEEP LAST 20 CHAT MESSAGES
                # =================================================

                chat_history = chat_history[-20:]


                # =================================================
                # SAVE TO SESSION
                # =================================================

                request.session["ai_chat_history"] = chat_history

                request.session.modified = True


            except Exception as e:

                print("Groq Error:", e)


                # =================================================
                # SAVE ERROR MESSAGE TO CHAT
                # =================================================

                chat_history.append({

                    "role": "user",

                    "text": question

                })


                chat_history.append({

                    "role": "assistant",

                    "text": (
                        "Sorry, I couldn't connect to the AI "
                        "service right now. Please try again."
                    )

                })


                # =================================================
                # KEEP LAST 20 MESSAGES
                # =================================================

                chat_history = chat_history[-20:]


                # =================================================
                # SAVE SESSION
                # =================================================

                request.session["ai_chat_history"] = chat_history

                request.session.modified = True


    # ============================================================
    # RENDER AI ASSISTANT
    # ============================================================

    return render(

        request,

        "dashboard/ai_assistant.html",

        {
            "chat_history": chat_history,
        }

    )