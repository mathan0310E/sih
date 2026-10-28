"""Anticipated audience questions with concise, sourced answers.

Answers cite only the works listed in refs.py, all of which were verified.
Where a question cannot be settled from the sources used, the answer says so
rather than speculating.
"""

QA = [
 ("If philosophy never reaches final answers, how can it be useful to education?",
  "Because usefulness does not require finality. Philosophy's contribution is to make "
  "the reasons for educational decisions explicit and open to criticism, rather than to "
  "settle them once and for all. Dewey argued that education is the process of forming "
  "fundamental dispositions of inquiry, and Peters that education is inseparable from "
  "questions of value and justification. On this view philosophy's value lies in the "
  "quality of the reasoning it forces into the open, not in a guaranteed verdict. "
  "Biesta's critique of evidence-based practice in educational research makes a parallel "
  "point: what counts as evidence, and what counts as a good outcome, are themselves "
  "normative questions that no measurement can answer on its own.",
  "Dewey (1916); Peters (1966); Biesta (2007)"),

 ("What is the difference between philosophy of education and educational policy or theory?",
  "Philosophy of education is the second-order study of the concepts and assumptions that "
  "policy and theory take for granted: what education is for, what knowledge is, what "
  "counts as learning, and who has authority to decide. Policy and theory make claims "
  "within those assumptions; philosophy examines the assumptions themselves. Curren's "
  "anthology and Siegel's handbook both present the field this way, as conceptual "
  "analysis applied to educational practice rather than as empirical research or "
  "administrative design.",
  "Curren (2007); Siegel (2009)"),

 ("Are the five educational philosophies mutually exclusive, or can a teacher combine them?",
  "They are not mutually exclusive in practice, but they are not fully compatible either. "
  "Each rests on a different account of reality and knowledge, and those accounts generate "
  "different aims, so combining them involves a genuine tension rather than a simple blend. "
  "This presentation treats them as analytical perspectives that clarify commitments, in "
  "the way Gutek presents the traditions. Combining them is defensible, but the teacher "
  "should be able to say which commitment governs when they conflict — for example, "
  "whether discovery or mastery has priority in a particular lesson.",
  "Gutek (2013); Curren (2007)"),

 ("You said you claim no effect sizes. So how do we know any of this matters?",
  "This presentation does not claim that any tradition produces better outcomes, and it "
  "should not be read as doing so. The comparison is conceptual: it identifies what each "
  "tradition commits a teacher to. Where empirical claims do appear they are attributed to "
  "the studies that made them — for example, the Open Science Collaboration's replication "
  "findings, and Nosek and colleagues on open research practice. Testing whether a "
  "particular pedagogy works would require a controlled design with defined outcomes, "
  "which is a separate study and is identified on the limitations slide as further work.",
  "Open Science Collaboration (2015); Nosek et al. (2015)"),

 ("Is critical thinking a general skill that transfers, or is it tied to subject knowledge?",
  "Siegel argues in Educating Reason that critical thinking consists in acting on the basis "
  "of reasons and should be an explicit aim of education, not a by-product of subject "
  "teaching. Whether the thinking so developed transfers across different domains is a "
  "separate empirical question, and this presentation does not settle it. What the "
  "philosophical literature does establish is that the aim itself is defensible and can be "
  "stated, which is why the implications slide recommends teaching reasoning explicitly "
  "rather than incidentally.",
  "Siegel (1988)"),

 ("How is the Tuskegee case relevant to a computer science student?",
  "It establishes the principle that data about people may not be collected or withheld "
  "without informed consent, and that principle applies directly to software systems that "
  "process personal data. The Belmont Report, which followed from Tuskegee, sets out "
  "respect for persons, beneficence and justice as the governing principles. UNESCO's "
  "Recommendation on the Ethics of Artificial Intelligence extends that reasoning to "
  "algorithmic systems, which is why research and professional ethics are not confined to "
  "medicine or the social sciences.",
  "National Commission (1979); UNESCO (2021)"),

 ("Is research ethics anything more than a bureaucratic form-filling exercise?",
  "The philosophical answer is that it is applied ethics, and the form is a trace of the "
  "reasoning rather than a substitute for it. Consent, confidentiality, attribution and "
  "integrity each express an obligation owed to particular people: participants, readers "
  "and fellow researchers. The Belmont Report, the Declaration of Helsinki and the "
  "Singapore Statement all state these as principles first and procedures second. ALLEA's "
  "European Code of Conduct and the ICMJE recommendations then translate the principles "
  "into practice, which is the point at which the reasoning becomes procedural.",
  "National Commission (1979); World Medical Association (2013); Singapore Statement (2010); "
  "ALLEA (2023); ICMJE (2024)"),

 ("What is the difference between fabrication, falsification and plagiarism?",
  "These are the three standard categories of research misconduct. Fabrication is "
  "inventing data or results. Falsification is manipulating, changing or omitting data so "
  "that the record no longer represents what was observed. Plagiarism is misappropriating "
  "another person's words, data or images without attribution. Shamoo and Resnik set out "
  "the categories in this form, and ALLEA's code of conduct states them as the core "
  "prohibitions of research integrity. All three are distinguished from honest error, "
  "which is not misconduct.",
  "Shamoo & Resnik (2015); ALLEA (2023)"),

 ("Why has reproducibility become such a prominent issue?",
  "Because replication is the mechanism by which empirical claims are tested, and large "
  "collaborative replication found substantially lower reproducibility than the field "
  "expected. The Open Science Collaboration's 2015 study of psychological science is the "
  "widely cited instance. Ioannidis had argued a decade earlier that most published "
  "research findings could be false, on the basis of study design and publication "
  "incentives. Nosek and colleagues responded by setting out the open research practices — "
  "preregistration, data sharing and reporting standards — that are now the mainstream "
  "reform programme.",
  "Open Science Collaboration (2015); Ioannidis (2005); Nosek et al. (2015)"),

 ("Does philosophy have a legitimate place in a technical curriculum such as computer science?",
  "Yes, on two grounds. First, the technical foundations are themselves philosophical: "
  "logic and epistemology underlie the design of algorithms and the evaluation of machine "
  "learning, and questions about what a model can be said to know are epistemological. "
  "Second, the social consequences of technical work are normative and require ethical "
  "reasoning — UNESCO's Recommendation on the Ethics of Artificial Intelligence addresses "
  "technical practitioners directly. On this view philosophy is not a rival to technical "
  "training but part of what makes it accountable.",
  "UNESCO (2021); Popper (1959)"),

 ("Your examples are mainly from Western philosophy. Is that a limitation?",
  "It is, and it is stated as one on the limitations slide. The five branches and the five "
  "educational traditions presented here are drawn from a predominantly Western tradition, "
  "although comparable traditions of systematic reflection exist in Indian, Chinese and "
  "Islamic thought and are not represented. The scope of this presentation is therefore "
  "bounded, and a comparative treatment would be a substantive extension rather than a "
  "footnote.",
  "Stated as a limitation; no comparative sources cited in this presentation"),
]

INTRO = ("These questions were anticipated for the research seminar on "
         "\u201cPhilosophy and Its Role in Education and Society\u201d. Each answer is "
         "kept short, is spoken in the same order as the presentation, and cites the "
         "verified sources listed in the deck's reference slides. Where the presentation "
         "cannot settle a question from the sources it uses, the answer says so rather "
         "than speculating. All citations follow APA 7th edition.")
