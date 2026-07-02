# -*- coding: utf-8 -*-
"""Rotas públicas: página inicial e formulários de recolha."""
import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Anfitriao, Hospede

public_bp = Blueprint("public", __name__)

EXT_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp"}


def _bool(campo):
    return request.form.get(campo) in ("on", "true", "1", "sim")


def _int(campo, default=0):
    try:
        return max(int(request.form.get(campo, default) or default), 0)
    except (TypeError, ValueError):
        return default


def _data(campo):
    valor = request.form.get(campo)
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


def _guardar_foto(ficheiro):
    if not ficheiro or not ficheiro.filename:
        return None
    ext = os.path.splitext(secure_filename(ficheiro.filename))[1].lower()
    if ext not in EXT_PERMITIDAS:
        return None
    nome = f"{uuid.uuid4().hex}{ext}"
    ficheiro.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nome))
    return nome


@public_bp.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------------------------- #
# Formulário 1 – Disponibilidade para Hospedagem (Anfitrião)
# --------------------------------------------------------------------- #
@public_bp.route("/anfitriao", methods=["GET", "POST"])
def form_anfitriao():
    if request.method == "POST":
        a = Anfitriao(
            nome=request.form.get("nome", "").strip(), # type: ignore
            fotografia=_guardar_foto(request.files.get("fotografia")), # type: ignore
            sexo=request.form.get("sexo", ""), # type: ignore
            telefone=request.form.get("telefone", "").strip(), # type: ignore
            whatsapp=request.form.get("whatsapp", "").strip(), # type: ignore
            comunidade=request.form.get("comunidade", "").strip(), # type: ignore
            bairro=request.form.get("bairro", "").strip(), # type: ignore
            rua=request.form.get("rua", "").strip(), # type: ignore
            ponto_referencia=request.form.get("ponto_referencia", "").strip(), # type: ignore
            gps=request.form.get("gps", "").strip(), # type: ignore
            classificacao=request.form.get("classificacao", "Irmão"), # type: ignore
            escalao=request.form.get("escalao") or None, # type: ignore
            capacidade=_int("capacidade", 1) or 1, # type: ignore
            quartos=_int("quartos"), # type: ignore
            camas=_int("camas"), # type: ignore
            recebe_homens=_bool("recebe_homens"), # type: ignore
            recebe_mulheres=_bool("recebe_mulheres"), # type: ignore
            recebe_familias=_bool("recebe_familias"), # type: ignore
            recebe_casais=_bool("recebe_casais"), # type: ignore
            recebe_criancas=_bool("recebe_criancas"), # type: ignore
            recebe_idosos=_bool("recebe_idosos"), # type: ignore
            tem_energia=_bool("tem_energia"), # type: ignore
            tem_agua=_bool("tem_agua"), # type: ignore
            tem_internet=_bool("tem_internet"), # type: ignore
            tem_wc_privado=_bool("tem_wc_privado"), # type: ignore
            tem_wc_partilhado=_bool("tem_wc_partilhado"), # type: ignore
            tem_ac=_bool("tem_ac"), # type: ignore
            tem_ventoinha=_bool("tem_ventoinha"), # type: ignore
            tem_acessibilidade=_bool("tem_acessibilidade"), # type: ignore
            tem_viatura=_bool("tem_viatura"), # type: ignore
            tipo_viatura=request.form.get("tipo_viatura", "").strip(), # type: ignore
            lugares_viatura=_int("lugares_viatura"), # type: ignore
            transporta_hospedes=_bool("transporta_hospedes"), # type: ignore
            observacoes=request.form.get("observacoes", "").strip(), # type: ignore
        )
        if a.classificacao != "Servo":
            a.escalao = None
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("public.sucesso", tipo="anfitriao"))

    return render_template("form_anfitriao.html")


# --------------------------------------------------------------------- #
# Formulário 2 – Registo de Hóspedes
# --------------------------------------------------------------------- #
@public_bp.route("/hospede", methods=["GET", "POST"])
def form_hospede():
    if request.method == "POST":
        tipo_grupo = request.form.get("tipo_grupo", "Sozinho")
        if tipo_grupo == "Sozinho":
            total = 1
        elif tipo_grupo == "Casal":
            total = 2
        else:
            total = max(_int("total_pessoas", 1), 1)

        h = Hospede(
            nome=request.form.get("nome", "").strip(), # type: ignore
            sexo=request.form.get("sexo", ""), # type: ignore
            telefone=request.form.get("telefone", "").strip(), # type: ignore
            comunidade_origem=request.form.get("comunidade_origem", "").strip(), # type: ignore
            cidade=request.form.get("cidade", "").strip(), # type: ignore
            provincia=request.form.get("provincia", "").strip(), # type: ignore
            classificacao=request.form.get("classificacao", "Irmão"), # type: ignore
            escalao=request.form.get("escalao") or None, # type: ignore
            tipo_grupo=tipo_grupo, # type: ignore
            total_pessoas=total, # type: ignore
            n_homens=_int("n_homens"), # type: ignore
            n_mulheres=_int("n_mulheres"), # type: ignore
            n_criancas=_int("n_criancas"), # type: ignore
            n_idosos=_int("n_idosos"), # type: ignore
            data_chegada=_data("data_chegada"), # type: ignore
            hora_prevista=request.form.get("hora_prevista", "").strip(), # type: ignore
            data_saida=_data("data_saida"), # type: ignore
            necessita_transporte=_bool("necessita_transporte"), # type: ignore
            observacoes=request.form.get("observacoes", "").strip(), # type: ignore
        )
        if h.classificacao != "Servo":
            h.escalao = None
        db.session.add(h)
        db.session.commit()
        return redirect(url_for("public.sucesso", tipo="hospede"))

    return render_template("form_hospede.html")


@public_bp.route("/sucesso/<tipo>")
def sucesso(tipo):
    return render_template("sucesso.html", tipo=tipo)