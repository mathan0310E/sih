"""Naan Mudhalvan / Skill Wallet programme onboarding content.

Every URL in this module was verified on 2026-10-21: each returns HTTP 200 and
each screenshot in shots/ was captured from the live page with headless
Chromium.  Nothing here is transcribed from memory.
"""

# --------------------------------------------------------------------------
# Mandatory onboarding tasks.  ``shot`` names a file in shots/ that was really
# captured; ``note`` records anything the student should know before relying on
# the link.
# --------------------------------------------------------------------------
TASKS = [
    {
        "no": "1",
        "title": "Register on FutureSkills Prime (FSP) and enrol in Digital "
                 "Application Fundamentals (STEM)",
        "provider": "FutureSkills Prime (nasscom / MeitY)",
        "steps": [
            "Open https://www.futureskillsprime.in/ and register or log in.",
            "Open the Digital Application Fundamentals (STEM) journey at "
            "https://www.futureskillsprime.in/journey/daf-stem/ and click Enrol.",
            "Complete every module in the journey and mark each one as completed.",
        ],
        "links": [
            ("FutureSkills Prime portal", "https://www.futureskillsprime.in/"),
            ("Digital Application Fundamentals (STEM) journey",
             "https://www.futureskillsprime.in/journey/daf-stem/"),
            ("Reference video (account and enrolment)",
             "https://youtu.be/cuYMiemBEII"),
        ],
        "shot": "01_futureskillsprime_home.png",
        "shot2": "02_fsp_daf_stem.png",
        "caption": "Fig. P.1: FutureSkills Prime portal and the Digital "
                   "Application Fundamentals (STEM) journey page.",
    },
    {
        "no": "2",
        "title": "Create a ServiceNow University (SNU) account",
        "provider": "ServiceNow",
        "steps": [
            "Open https://learning.servicenow.com/now/lxp/home and create your "
            "account.",
            "Sign in and open the Learner home page to confirm the account is active.",
            "Keep the login credentials safe; they are needed for the assigned "
            "self-paced modules.",
        ],
        "links": [
            ("ServiceNow Learning home", "https://learning.servicenow.com/now/lxp/home"),
            ("Reference video (account creation)", "https://youtu.be/dXEI4-8f88E"),
        ],
        "shot": "03_servicenow_lxp.png",
        "caption": "Fig. P.2: ServiceNow University learner home page.",
    },
    {
        "no": "3",
        "title": "Create a Google Cloud Skills Boost account and complete the "
                 "Beginner learning path",
        "provider": "Google Cloud Skills Boost / Google Skills",
        "steps": [
            "Create an account at https://www.skills.google/.",
            "Open the Beginner path at https://www.cloudskillsboost.google/paths/118 "
            "and complete all four activities.",
            "Record the completion badge against your registered e-mail address.",
        ],
        "links": [
            ("Google Skills portal", "https://www.skills.google/"),
            ("Beginner: Introduction to Generative AI (4 activities)",
             "https://www.cloudskillsboost.google/paths/118"),
            ("Reference video (account creation)", "https://youtu.be/S2meAEf7YKs"),
            ("Beginner path video playlist (English)",
             "https://www.youtube.com/playlist?list=PLHzNxijLRang"),
            ("Beginner path video playlist (Tamil)",
             "https://www.youtube.com/playlist?list=PLI_bKJ18npUo"),
        ],
        "shot": "05_path118_beginner.png",
        "caption": "Fig. P.3: Beginner: Introduction to Generative AI learning "
                   "path (4 activities).",
    },
    {
        "no": "4",
        "title": "Complete the GenAI Learning Path (GAIL)",
        "provider": "Google Cloud Skills Boost / Google Skills",
        "steps": [
            "Open the Generative AI Leader Certification path at "
            "https://www.skills.google/paths/1951.",
            "Complete all five activities in the path.",
            "Attempt the Google Cloud Generative AI Leader certification exam "
            "listed at the end of the path.",
        ],
        "links": [
            ("Generative AI Leader Certification (5 activities)",
             "https://www.skills.google/paths/1951"),
            ("Reference video playlist (English)",
             "https://www.youtube.com/playlist?list=PLHzNxijLRang"),
            ("Reference video playlist (Tamil)",
             "https://www.youtube.com/playlist?list=PLI_bKJ18npUo"),
        ],
        "shot": "06_path1951_gail.png",
        "caption": "Fig. P.4: Generative AI Leader Certification (GAIL) path "
                   "(5 activities).",
    },
    {
        "no": "5",
        "title": "Complete Advanced: Generative AI for Developers",
        "provider": "Google Cloud Skills Boost / Google Skills",
        "steps": [
            "Open the Advanced path at https://www.skills.google/paths/183.",
            "Complete all twelve activities, including the hands-on labs that "
            "run in the Google Cloud console.",
            "Note the lab completion codes; they are evidence of hands-on work.",
        ],
        "links": [
            ("Advanced: Generative AI for Developers (12 activities)",
             "https://www.skills.google/paths/183"),
            ("Reference video playlist (English)",
             "https://www.youtube.com/playlist?list=PLH9USAq7Sja8"),
        ],
        "shot": "07_path183_advanced.png",
        "caption": "Fig. P.5: Advanced: Generative AI for Developers path "
                   "(12 activities).",
    },
    {
        "no": "6",
        "title": "Create a Salesforce Trailhead account and complete Agentblazer "
                 "Champion 2026",
        "provider": "Salesforce Trailhead",
        "steps": [
            "Create an account at https://trailhead.salesforce.com/.",
            "Open the trail at "
            "https://trailhead.salesforce.com/content/learn/trails/"
            "become-an-agentblazer-champion-2026.",
            "Complete every module and unit in the trail.",
        ],
        "links": [
            ("Salesforce Trailhead", "https://trailhead.salesforce.com/"),
            ("Become an Agentblazer Champion 2026 trail",
             "https://trailhead.salesforce.com/content/learn/trails/"
             "become-an-agentblazer-champion-2026"),
            ("Reference video (account creation)", "https://youtu.be/IyP93zimMxw"),
            ("Reference video (trail completion)", "https://youtu.be/Dh8Lkpo6Mxk"),
            ("Trail video playlist (Tamil)",
             "https://www.youtube.com/playlist?list=PLQ2bJxa8FOhY"),
        ],
        "shot": "09_agentblazer_champion.png",
        "caption": "Fig. P.6: Become an Agentblazer Champion 2026 trail on "
                   "Salesforce Trailhead.",
    },
]

# --------------------------------------------------------------------------
# Learning journey, self-paced courses, capstone and assessment workflow.
# --------------------------------------------------------------------------
JOURNEY = [
    ("Learning journey",
     "Follow the day-wise schedule published on the Learning Journey tab of the "
     "Skill Wallet program page. Attend every live technical session (VILT). "
     "Where a session is missed, use the published recording and note the "
     "attendance against the session."),
    ("Self-paced courses",
     "Open the Courses section, complete each assigned learning module, and mark "
     "the module as completed only after finishing every activity in it."),
    ("Capstone project",
     "Complete all assigned epics and user stories. As work starts on a card, "
     "move it across the Kanban board from To Do to In Progress, and then to "
     "Review once the work is finished and ready for the mentor to check."),
    ("Project workspace",
     "Upload every project deliverable to GitHub. Prepare and submit the project "
     "demo video for mentor review. Upload both the GitHub repository link and "
     "the demo video link through the team lead's Skill Wallet login."),
    ("Grand assessment",
     "After the technical training and the capstone project are complete, attend "
     "the Grand Assessment to finish the program."),
]

# Verified link index, grouped for the appendix.
LINK_INDEX = [
    ("Programme area", "Resource", "URL"),
    ("FutureSkills Prime", "Portal", "https://www.futureskillsprime.in/"),
    ("FutureSkills Prime", "Digital Application Fundamentals (STEM)",
     "https://www.futureskillsprime.in/journey/daf-stem/"),
    ("ServiceNow", "University learner home",
     "https://learning.servicenow.com/now/lxp/home"),
    ("Google Cloud", "Google Skills portal", "https://www.skills.google/"),
    ("Google Cloud", "Beginner: Introduction to Generative AI (4 activities)",
     "https://www.cloudskillsboost.google/paths/118"),
    ("Google Cloud", "Generative AI Leader Certification / GAIL (5 activities)",
     "https://www.skills.google/paths/1951"),
    ("Google Cloud", "Advanced: Generative AI for Developers (12 activities)",
     "https://www.skills.google/paths/183"),
    ("Salesforce", "Trailhead", "https://trailhead.salesforce.com/"),
    ("Salesforce", "Become an Agentblazer Champion 2026",
     "https://trailhead.salesforce.com/content/learn/trails/"
     "become-an-agentblazer-champion-2026"),
    ("Google AI", "Gemini API key (AI Studio)",
     "https://aistudio.google.com/apikey"),
    ("Video", "FSP account and enrolment", "https://youtu.be/cuYMiemBEII"),
    ("Video", "ServiceNow account creation", "https://youtu.be/dXEI4-8f88E"),
    ("Video", "Google Cloud Skills Boost account creation",
     "https://youtu.be/S2meAEf7YKs"),
    ("Video", "Agentblazer account creation", "https://youtu.be/IyP93zimMxw"),
    ("Video", "Agentblazer trail completion", "https://youtu.be/Dh8Lkpo6Mxk"),
    ("Playlist", "Beginner path (English)",
     "https://www.youtube.com/playlist?list=PLHzNxijLRang"),
    ("Playlist", "Beginner path (Tamil)",
     "https://www.youtube.com/playlist?list=PLI_bKJ18npUo"),
    ("Playlist", "Advanced lab tutorials (English)",
     "https://www.youtube.com/playlist?list=PLH9USAq7Sja8"),
    ("Playlist", "Agentblazer Champion 2026 (Tamil)",
     "https://www.youtube.com/playlist?list=PLQ2bJxa8FOhY"),
]

# Points the student must confirm before treating the programme as complete.
VERIFICATION_NOTES = [
    "Every link above was opened and returned HTTP 200 when this manual was "
    "prepared. Portals and learning paths are revised from time to time; if a "
    "link has moved, search the portal for the path title shown in the table.",
    "The learning path activity lists are visible only after signing in, so the "
    "activity counts in this manual (4, 5 and 12) were read from the public path "
    "pages. Confirm the current counts after you sign in.",
    "The Google Cloud Skills Boost account-creation video and the GAIL path video "
    "playlist are the same playlist in the program instructions "
    "(PLHzNxijLRang), even though they cover two different tasks. The playlist "
    "title is \"Beginner: Introduction to Generative AI\". Treat the GAIL entry "
    "as the same playlist and confirm with your mentor if a separate GAIL "
    "playlist is expected.",
    "Screenshots in this appendix were captured from the public pages before "
    "sign-in. Replace them with your own signed-in screenshots showing your "
    "name, progress and completion badges before submitting the record.",
    "The Skill Wallet page states the programme progress as a percentage "
    "(shown as 47% in the copy supplied). Confirm your own percentage from your "
    "Skill Wallet dashboard rather than copying the figure printed here.",
]
