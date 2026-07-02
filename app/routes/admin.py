# -*- coding: utf-8 -*-
"""Dashboard simples."""
from flask import Blueprint, render_template
from app.models import Anfitriao, Hospede

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@admin_bp.route("/dashboard")
def dashboard():
    familias = Anfitriao.query.all()
    hospedes = Hospede.query.all()

    kpis = {
        "total_familias": len(familias),
        "total_hospedes": len(hospedes),
        "total_pessoas": sum(h.total_pessoas for h in hospedes),
        "total_vagas": sum(f.capacidade for f in familias),
        "total_servos": sum(1 for f in familias if f.classificacao == "Servo")
                      + sum(1 for h in hospedes if h.classificacao == "Servo"),
        "total_irmaos": sum(1 for f in familias if f.classificacao == "Irmão")
                      + sum(1 for h in hospedes if h.classificacao == "Irmão"),
        "total_viaturas": sum(1 for f in familias if f.tem_viatura),
    }

    ultimos_anfitrioes = Anfitriao.query.order_by(Anfitriao.criado_em.desc()).limit(10).all()
    ultimos_hospedes = Hospede.query.order_by(Hospede.criado_em.desc()).limit(10).all()

    return render_template(
        "dashboard.html",
        kpis=kpis,
        ultimos_anfitrioes=ultimos_anfitrioes,
        ultimos_hospedes=ultimos_hospedes,
    )