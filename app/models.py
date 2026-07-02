# -*- coding: utf-8 -*-
"""Modelos de dados do sistema de hospedagem."""
from datetime import datetime
from app import db


class Anfitriao(db.Model):
    __tablename__ = "anfitrioes"

    id = db.Column(db.Integer, primary_key=True)

    # Dados pessoais
    nome = db.Column(db.String(160), nullable=False)
    fotografia = db.Column(db.String(255))
    sexo = db.Column(db.String(12), nullable=False)          # Masculino / Feminino
    telefone = db.Column(db.String(30), nullable=False)
    whatsapp = db.Column(db.String(30))
    comunidade = db.Column(db.String(120), nullable=False)
    bairro = db.Column(db.String(120), nullable=False)
    rua = db.Column(db.String(160))
    ponto_referencia = db.Column(db.String(200))
    gps = db.Column(db.String(60))                            # "lat,lng" (opcional)

    # Classificação
    classificacao = db.Column(db.String(12), nullable=False)  # Servo / Irmão
    escalao = db.Column(db.String(30))                        # Diácono, Evangelista, ...

    # Disponibilidade
    capacidade = db.Column(db.Integer, nullable=False, default=1)
    quartos = db.Column(db.Integer, default=0)
    camas = db.Column(db.Integer, default=0)
    recebe_homens = db.Column(db.Boolean, default=False)
    recebe_mulheres = db.Column(db.Boolean, default=False)
    recebe_familias = db.Column(db.Boolean, default=False)
    recebe_casais = db.Column(db.Boolean, default=False)
    recebe_criancas = db.Column(db.Boolean, default=False)
    recebe_idosos = db.Column(db.Boolean, default=False)

    # Infra-estrutura
    tem_energia = db.Column(db.Boolean, default=False)
    tem_agua = db.Column(db.Boolean, default=False)
    tem_internet = db.Column(db.Boolean, default=False)
    tem_wc_privado = db.Column(db.Boolean, default=False)
    tem_wc_partilhado = db.Column(db.Boolean, default=False)
    tem_ac = db.Column(db.Boolean, default=False)
    tem_ventoinha = db.Column(db.Boolean, default=False)
    tem_acessibilidade = db.Column(db.Boolean, default=False)

    # Transporte
    tem_viatura = db.Column(db.Boolean, default=False)
    tipo_viatura = db.Column(db.String(60))
    lugares_viatura = db.Column(db.Integer, default=0)
    transporta_hospedes = db.Column(db.Boolean, default=False)

    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "comunidade": self.comunidade,
            "bairro": self.bairro,
            "classificacao": self.classificacao,
            "escalao": self.escalao,
            "capacidade": self.capacidade,
            "tem_viatura": self.tem_viatura,
        }


class Hospede(db.Model):
    __tablename__ = "hospedes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(160), nullable=False)
    sexo = db.Column(db.String(12), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    comunidade_origem = db.Column(db.String(120), nullable=False)
    cidade = db.Column(db.String(120))
    provincia = db.Column(db.String(120))

    classificacao = db.Column(db.String(12), nullable=False)  # Servo / Irmão
    escalao = db.Column(db.String(30))

    tipo_grupo = db.Column(db.String(12), nullable=False, default="Sozinho")
    total_pessoas = db.Column(db.Integer, nullable=False, default=1)
    n_homens = db.Column(db.Integer, default=0)
    n_mulheres = db.Column(db.Integer, default=0)
    n_criancas = db.Column(db.Integer, default=0)
    n_idosos = db.Column(db.Integer, default=0)

    data_chegada = db.Column(db.Date)
    hora_prevista = db.Column(db.String(10))
    data_saida = db.Column(db.Date)
    necessita_transporte = db.Column(db.Boolean, default=False)

    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)