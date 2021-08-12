CAMINHO_DB = "db.sqlite3"


from datetime import date, datetime

from peewee import (
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    fn,
)


class Base(Model):
    class Meta:
        print(f"INICIANDO BASE {CAMINHO_DB}")
        database = SqliteDatabase(CAMINHO_DB)


class Mix_data(Base):
    data_insercao = DateTimeField(verbose_name="Data de Registro")
    data_modificacao = DateTimeField(verbose_name="Data de Modificação")

    class Meta:
        abstract = True


class website_tb_Paciente(Mix_data):
    sexo_choice = (("M", "Masculino"), ("F", "Feminino"), ("X", "Não binário"))
    tp_parentesco = (
        ("H", "Nenhum"),
        ("T", "Tio(a)"),
        ("S", "Sobrinho(a)"),
        ("A", "Amigo(a)"),
        ("P", "Primo(a)"),
        ("I", "Irmão/Irmã"),
        ("J", "Cônjuge"),
        ("F", "Filho(a)"),
        ("C", "Cuidador(ra)"),
        ("O", "Outros"),
        ("N", "Neto(a)"),
    )
    nome = CharField(null=False, max_length=200, verbose_name="nome")
    sobrenome = CharField(null=True, max_length=200, verbose_name="sobrenome")
    email = CharField(null=False, max_length=200, default=None)
    data_nascimento = DateField(null=True, verbose_name="data nascimento")
    sexo = CharField(
        default=sexo_choice[0][0],
        max_length=1,
        choices=sexo_choice,
        verbose_name="Sexo",
    )
    cpf = CharField(max_length=14, null=True, verbose_name="cpf do paciente")
    prontuario = IntegerField(
        verbose_name="número do prontuário",
        unique=True,
    )
    whatsapp = CharField(
        null=True,
        max_length=15,
        verbose_name="número do whatsapp",
        unique=True,
    )
    whatsapp_h = CharField(
        null=True,
        max_length=30,
        unique=True,
    )

    parentesco = CharField(
        default=tp_parentesco[0][0],
        max_length=1,
        choices=tp_parentesco,
        verbose_name="Grau parentesco",
    )
    nome_parente = CharField(
        max_length=200,
        verbose_name="Nome do parente",
        null=True,
        default="",
    )

    class Meta:
        unique_together = (("prontuario", "whatsapp"),)
        verbose_name = "Paciente"

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.id})"


class website_tb_Protocolo_Tratamento(Mix_data):
    nome = CharField(null=False, max_length=200, verbose_name="nome")
    intervalo_repeticao_tratamento = IntegerField(
        null=True, verbose_name="intervalo repeticao"
    )

    class Meta:
        verbose_name = "Protocolos Tratamento"

    def __str__(self):
        return f"{self.id} {self.nome} {self.intervalo_repeticao_tratamento}"


class website_tb_Receitas_Medica(Mix_data):
    data_inicio_tratamento = DateField(verbose_name="Data inicio tratamento")
    data_fim_tratamento = DateField(verbose_name="Data fim tratamento")
    fk_id_paciente = ForeignKeyField(website_tb_Paciente, verbose_name="paciente")
    fk_id_tratamento = ForeignKeyField(
        website_tb_Protocolo_Tratamento, verbose_name="tratamento"
    )
    status = CharField(default=True, verbose_name="status da receita")

    class Meta:
        verbose_name = "Receitas Medica"

    def __str__(self):
        return f"{self.id} {self.fk_id_paciente} {self.fk_id_medico}"


class website_tb_Rotina(Mix_data):
    nome_rotina = CharField(verbose_name="nome da rotina", null=False, max_length=200)
    apikey = TextField(verbose_name="apikey da blip")
    workspace_id = TextField(verbose_name="workspace da blip")

    class Meta:
        verbose_name = "Rotinas disparo"

    def __str__(self):
        return f"{self.nome_rotina}"


class website_tb_Rotina_Protocolo_Tratamento(Mix_data):
    fk_id_rotina = ForeignKeyField(website_tb_Rotina)
    fk_id_protocolo_tratamento = ForeignKeyField(website_tb_Protocolo_Tratamento)
    dias_apos_intervalo_tratamento = IntegerField(
        verbose_name="dias apos intervalo tratamento"
    )

    class Meta:
        verbose_name = "Rotina Protocolo Tratamento"

    def __str__(self):
        return f"{self.fk_id_rotina} {self.fk_id_protocolo_tratamento} {self.dias_apos_intervalo_tratamento}"


print("TESTE DE CONEXAO")
for i in website_tb_Paciente.select():
    print(i.nome, i.sobrenome)

print("Pegar Receitas Medicas no período ")

hoje = datetime.now().strftime("%Y-%m-%d")
print(hoje)

query = (website_tb_Receitas_Medica.select().where(('2021-08-10' >= website_tb_Receitas_Medica.data_inicio_tratamento) & ('2021-08-10' <= website_tb_Receitas_Medica.data_fim_tratamento)))

for i in query: print(i.id, i.data_inicio_tratamento, i.data_fim_tratamento)