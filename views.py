from django.shortcuts import render


MAJORS = [
    "Computer Science",
    "Information Technology",
    "Software Development",
    "Cybersecurity",
    "Data Analytics",
]

CLASS_STANDINGS = ["Freshman", "Sophomore", "Junior", "Senior"]

PROGRAMMING_LANGUAGES = ["Python", "Java", "JavaScript", "C++", "C#"]


def registration_form(request):
    errors = {}
    form_data = {
        "student_name": "",
        "student_id": "",
        "major": MAJORS[0],
        "class_standing": CLASS_STANDINGS[0],
        "programming_languages": [],
        "graduation_year": "",
        "comments": "",
    }

    if request.method == "POST":
        form_data = {
            "student_name": request.POST.get("student_name", "").strip(),
            "student_id": request.POST.get("student_id", "").strip(),
            "major": request.POST.get("major", ""),
            "class_standing": request.POST.get("class_standing", ""),
            "programming_languages": request.POST.getlist("programming_languages"),
            "graduation_year": request.POST.get("graduation_year", "").strip(),
            "comments": request.POST.get("comments", "").strip(),
        }

        if not form_data["student_name"]:
            errors["student_name"] = "Student Name is required."

        if not form_data["student_id"]:
            errors["student_id"] = "Student ID is required."

        if not errors:
            return render(
                request,
                "registration/results.html",
                {
                    "student": form_data,
                    "programming_languages": ", ".join(
                        form_data["programming_languages"]
                    )
                    or "None selected",
                },
            )

    return render(
        request,
        "registration/form.html",
        {
            "errors": errors,
            "form_data": form_data,
            "majors": MAJORS,
            "class_standings": CLASS_STANDINGS,
            "programming_languages": PROGRAMMING_LANGUAGES,
        },
    )
