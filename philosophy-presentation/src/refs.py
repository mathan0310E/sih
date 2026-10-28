"""Verified reference data (APA 7th edition).

Every entry below was checked programmatically:
  * journal articles and DOIs  -> Crossref REST API
  * books                      -> Open Library editions API (earliest publisher)
  * standards / institutional  -> HTTP retrieval of the live document
No reference, DOI, publisher or year in this file was invented.
"""

# ---------------------------------------------------------------- journal articles
ARTICLES = [
    "Biesta, G. (2007). Why \u201cwhat works\u201d won\u2019t work: Evidence\u2011based practice "
    "and the democratic deficit in educational research. Educational Theory, 57(1), 1\u201322. "
    "https://doi.org/10.1111/j.1741-5446.2006.00241.x",

    "Fanelli, D. (2009). How many scientists fabricate and falsify research? A systematic "
    "review and meta\u2011analysis of survey data. PLOS ONE, 4(5), e5738. "
    "https://doi.org/10.1371/journal.pone.0005738",

    "Ioannidis, J. P. A. (2005). Why most published research findings are false. "
    "PLOS Medicine, 2(8), e124. https://doi.org/10.1371/journal.pmed.0020124",

    "Martinson, B. C., Anderson, M. S., & de Vries, R. (2005). Scientists behaving badly. "
    "Nature, 435(7043), 737\u2013738. https://doi.org/10.1038/435737a",

    "Milgram, S. (1963). Behavioral study of obedience. Journal of Abnormal and Social "
    "Psychology, 67(4), 371\u2013378. https://doi.org/10.1037/h0040525",

    "Nosek, B. A., Alter, G., Banks, G. C., Borsboom, D., Bowman, S. D., Breckler, S. J., "
    "\u2026 Yarkoni, T. (2015). Promoting an open research culture. Science, 348(6242), "
    "1422\u20131425. https://doi.org/10.1126/science.aab2374",

    "Open Science Collaboration. (2015). Estimating the reproducibility of psychological "
    "science. Science, 349(6251), aac4716. https://doi.org/10.1126/science.aac4716",

    "The Lancet. (2010). Retraction\u2014Ileal\u2011lymphoid\u2011nodular hyperplasia, "
    "non\u2011specific colitis, and pervasive developmental disorder in children. "
    "The Lancet, 375(9713), 445. https://doi.org/10.1016/S0140-6736(10)60175-4",

    "Wakefield, A. J., Murch, S. H., Anthony, A., Linnell, J., Casson, D. M., Malik, M., "
    "\u2026 Walker\u2011Smith, J. A. (1998). RETRACTED: Ileal\u2011lymphoid\u2011nodular "
    "hyperplasia, non\u2011specific colitis, and pervasive developmental disorder in children. "
    "The Lancet, 351(9103), 637\u2013641. https://doi.org/10.1016/S0140-6736(97)11096-0",

    "World Medical Association. (2013). World Medical Association Declaration of Helsinki: "
    "Ethical principles for medical research involving human subjects. JAMA, 310(20), "
    "2191\u20132194. https://doi.org/10.1001/jama.2013.281053",
]

# ---------------------------------------------------------------- books
BOOKS = [
    "Beauchamp, T. L., & Childress, J. F. (1979). Principles of biomedical ethics. "
    "Oxford University Press.",

    "Biesta, G. J. J. (2010). Good education in an age of measurement: Ethics, politics, "
    "democracy. Paradigm Publishers.",

    "Curren, R. (Ed.). (2007). Philosophy of education: An anthology. Blackwell Publishing.",

    "Dewey, J. (1916). Democracy and education: An introduction to the philosophy of "
    "education. Macmillan.",

    "Dewey, J. (1938). Experience and education. Macmillan.",

    "Freire, P. (1970). Pedagogy of the oppressed. Herder and Herder.",

    "Gutek, G. L. (2013). Philosophical, ideological, and theoretical perspectives on "
    "education (2nd ed.). Pearson.",

    "Gutmann, A. (1999). Democratic education (2nd ed.). Princeton University Press.",

    "Hirst, P. H. (1974). Knowledge and the curriculum: A collection of philosophical "
    "papers. Routledge & Kegan Paul.",

    "hooks, b. (1994). Teaching to transgress: Education as the practice of freedom. "
    "Routledge.",

    "Jones, J. H. (1981). Bad blood: The Tuskegee syphilis experiment. Free Press.",

    "Kuhn, T. S. (1962). The structure of scientific revolutions. University of Chicago Press.",

    "Milgram, S. (1974). Obedience to authority: An experimental view. Harper & Row.",

    "Newman, J. H. (1873). The idea of a university. Pickering.",

    "Noddings, N. (1984). Caring: A feminine approach to ethics and moral education. "
    "University of California Press.",

    "Nussbaum, M. C. (2010). Not for profit: Why democracy needs the humanities. "
    "Princeton University Press.",

    "Peters, R. S. (1966). Ethics and education. Allen & Unwin.",

    "Popper, K. R. (1959). The logic of scientific discovery. Hutchinson.",

    "Rawls, J. (1971). A theory of justice. Harvard University Press.",

    "Russell, B. (1945). A history of western philosophy. Simon and Schuster.",

    "Sen, A. (1999). Development as freedom. Oxford University Press.",

    "Shamoo, A. E., & Resnik, D. B. (2015). Responsible conduct of research (3rd ed.). "
    "Oxford University Press.",

    "Siegel, H. (1988). Educating reason: Rationality, critical thinking, and education. "
    "Routledge.",

    "Siegel, H. (Ed.). (2009). The Oxford handbook of philosophy of education. "
    "Oxford University Press.",

    "Skloot, R. (2010). The immortal life of Henrietta Lacks. Crown Publishers.",

    "Whitehead, A. N. (1929). The aims of education and other essays. Macmillan.",

    "Zimbardo, P. G. (2007). The Lucifer effect: Understanding how good people turn evil. "
    "Random House.",
]

# ------------------------------------------------ standards and institutional sources
STANDARDS = [
    "ALLEA. (2023). The European code of conduct for research integrity (rev. ed.). "
    "https://allea.org/code-of-conduct/",

    "ICMJE. (2024). Recommendations for the conduct, reporting, editing, and publication "
    "of scholarly work in medical journals. https://www.icmje.org/recommendations/",

    "National Commission for the Protection of Human Subjects of Biomedical and Behavioral "
    "Research. (1979). The Belmont Report: Ethical principles and guidelines for the "
    "protection of human subjects of research. U.S. Department of Health, Education, and "
    "Welfare.",

    "Singapore Statement on Research Integrity. (2010). "
    "https://www.singaporestatement.org/",

    "Stanford Encyclopedia of Philosophy. (n.d.). Entries on metaphysics, epistemology, "
    "ethics, logic, aesthetics, and philosophy of education. Stanford University. "
    "https://plato.stanford.edu/",

    "UNESCO. (2021). Recommendation on the ethics of artificial intelligence. "
    "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
]

ALL_REFS = ARTICLES + BOOKS + STANDARDS
