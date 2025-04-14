# annex/services/docx_generator.py

import os
import io

from pkg_resources import resource_filename
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Cm

# Returns the absolute path to Annexe6a.docx in annex/templates/.
# Raises FileNotFoundError if it doesn’t exist.
def get_template_path():
    tpl_path = resource_filename('annex', 'templates/Annexe6a.docx')
    if not os.path.exists(tpl_path):
        raise FileNotFoundError(f"Template not found at {tpl_path!r}")
    return tpl_path

# Flattens the Annex6a instance into a dict for docxtpl.
def build_context(annex):
    ctx = annex.__dict__.copy()
    ctx.pop('_state', None)
    return ctx

# Renders the Annex6a instance into a .docx and returns an in‑memory BytesIO.
# May raise FileNotFoundError or any docxtpl/python‑docx error.
def render_to_buffer(annex) -> io.BytesIO:
    tpl_path = get_template_path()
    doc = DocxTemplate(tpl_path)

    ctx = build_context(annex)

    # If there’s an image, replace the key with an InlineImage
    if annex.image_field:
        ctx['image_field'] = InlineImage(
            doc,
            annex.image_field.path,
            Cm(6.5),
            Cm(4.5)
        )

    buf = io.BytesIO()
    doc.render(ctx)
    doc.save(buf)
    buf.seek(0)
    return buf

# Top‑level service: returns either an HttpResponse with the .docx
# or a DRF Response with an error message.
def generate_annex6a_docx_response(annex):
    try:
        buf = render_to_buffer(annex)
        resp = HttpResponse(
            buf.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )
        resp["Content-Disposition"] = (
            f'attachment; filename="Annex6a_{annex.id}.docx"'
        )
        return resp

    except FileNotFoundError as e:
        return Response(
            {"detail" : "Template Not Found"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {"detail" : "Failed to generate DOCX"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
