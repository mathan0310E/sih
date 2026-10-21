#!/usr/bin/env python3
"""Compare the built front matter against the reference record book.

Reads the reference ``NM LAB MANUAL CS.pdf`` and the built manual, then reports
each cover / certificate / index element as a fraction of its own page height.
The reference is Letter (792pt) and the manual is A4 (841.89pt); expressing both
as fractions makes them directly comparable, which is how the gap values in
spacing.json are tuned.

Usage:  python3 compare_layout.py [--tune]
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

NS = "{http://www.w3.org/1999/xhtml}"
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref", "NM LAB MANUAL CS.pdf")
BUILT = os.path.join(HERE, "output", "NM_LAB_MANUAL_GenAI.pdf")


def lines_of(pdf, page_no):
    """Return [(y_fraction, text)] for one page, using the real page height."""
    xml = subprocess.run(["pdftotext", "-bbox", "-f", str(page_no),
                          "-l", str(page_no), pdf, "-"],
                         capture_output=True, text=True).stdout
    root = ET.fromstring(xml)
    pg = next(root.iter(NS + "page"))
    height = float(pg.get("height"))
    buckets = defaultdict(list)
    for w in pg.iter(NS + "word"):
        buckets[round(float(w.get("yMin")) / 4)].append(w)
    out = []
    for k in sorted(buckets):
        ws = sorted(buckets[k], key=lambda w: float(w.get("xMin")))
        y = min(float(w.get("yMin")) for w in ws)
        out.append((y / height, " ".join(w.text for w in ws)))
    return out, height


def find(lines, needle):
    """First line whose text contains needle, case-insensitively."""
    for frac, text in lines:
        if needle.lower() in text.lower():
            return frac
    return None


ELEMENTS = {
    "college": (1, "SKP ENGINEERING"),
    "address": (1, "Tiruvannamalai"),
    "dept_head": (1, "DEPARTMENT OF"),
    "programme": (1, "CSE (CYBER SECURITY)"),
    "course": (1, "SB8015"),
    "regulation": (1, "REGULATION"),
    "name_field": (1, "Name :"),
    "register_field": (1, "Register Number"),
    "dept_field": (1, "Department :"),
    "year_field": (1, "Year / Semester"),
    "subject_field": (1, "Subject"),
}

COVER_KEYS = ["college", "address", "dept_head", "regulation", "name_field",
              "register_field", "dept_field", "year_field", "subject_field"]
CERT_KEYS = ["c_college", "c_address", "c_heading", "c_name", "c_register",
             "c_statement", "c_sig1", "c_submission", "c_sig2"]


# element -> (page, reference search text)
SEQUENCE = [
    # (spacing param it follows, cover key, cert key)
    (None, "college", "c_college"),
    ("after_college", "address", "c_address"),
    ("after_address", "dept_head", "c_heading"),
    ("after_dept_head", None, "c_name"),
    ("after_dept_name", None, None),   # unused on the certificate
    ("after_programme", None, None),
    ("after_course", None, None),
    ("after_regulation", None, None),
    ("after_last_field", None, None),
]


def gaps(pdf, spec, keys):
    """Return the gaps between consecutive present elements, in points of the
    page's own height."""
    vals = collect(pdf, spec)
    present = [(k, vals[k]) for k in keys if vals.get(k) is not None]
    out = []
    for i in range(1, len(present)):
        (k0, v0), (k1, v1) = present[i - 1], present[i]
        out.append((f"{k0}->{k1}", (v1 - v0) * 841.89))
    return out


# element key -> the spacing parameter whose value controls the gap *above* it
COVER_PARAM = {
    "address": "after_college",
    "dept_head": "after_address",
    "programme": "after_dept_name",
    "course": "after_programme",
    "regulation": "after_course",
    "name_field": "after_regulation",
    "register_field": "after_last_field",
    "dept_field": "field_gap",
    "year_field": "field_gap",
    "subject_field": "field_gap",
}
CERT_PARAM = {
    "c_address": "after_college",
    "c_heading": "after_address",
    "c_name": "after_heading",
    "c_register": "field_gap",
    "c_statement": "after_fields",
    "c_sig1": "after_statement",
    "c_submission": "after_sig1",
    "c_sig2": "after_submission",
}

CERT_ELEMENTS = {
    "c_college": (2, "SKP ENGINEERING"),
    "c_address": (2, "Tiruvannamalai"),
    "c_heading": (2, "CERTIFICATE"),
    "c_name": (2, "Name :"),
    "c_register": (2, "Register No"),
    "c_statement": (2, "Certified that"),
    "c_sig1": (2, "Staff-In-Charge"),
    "c_submission": (2, "Submission for"),
    "c_sig2": (2, "Internal Examiner"),
}


def collect(pdf, spec):
    out = {}
    cache = {}
    for key, (page, needle) in spec.items():
        if page not in cache:
            cache[page] = lines_of(pdf, page)[0]
        out[key] = find(cache[page], needle)
    return out


def report():
    if not os.path.exists(REF) or not os.path.exists(BUILT):
        print("need both the reference and the built PDF")
        return
    for label, spec, keys, param in (("COVER", ELEMENTS, COVER_KEYS, COVER_PARAM),
                                     ("CERTIFICATE", CERT_ELEMENTS, CERT_KEYS,
                                      CERT_PARAM)):
        rg = dict(gaps(REF, spec, keys))
        bg = dict(gaps(BUILT, spec, keys))
        print(label)
        print(f"  {'gap':<28}{'ref(pt)':>9}{'built':>9}{'delta':>8}  param")
        for gname in rg:
            if gname not in bg:
                continue
            d = bg[gname] - rg[gname]
            bkey = gname.split("->")[1]
            print(f"  {gname:<28}{rg[gname]:>9.1f}{bg[gname]:>9.1f}"
                  f"{d:>+8.1f}  {param.get(bkey,'')}")


if __name__ == "__main__":
    report()
