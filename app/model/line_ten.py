class Field:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __set_name__(self, owner, nome):
        self.nome = nome

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.raw_data[self.initial: self.final]


class Base:
    def __init__(self, data):
        self.raw_data = data

    def __repr__(self):
        fields = []
        for name, obj in self.__class__.__dict__.items():
            if isinstance(obj, Field):
                fields.append((name, str(getattr(self, name)).strip()))
        return "\n".join(f"{field}:{content}" for field, content in fields)

    def __dict__(self):
        fields = {}
        for name, obj in self.__class__.__dict__.items():
            if isinstance(obj, Field):
                fields[name] = str(getattr(self, name)).strip()

        return fields


class InvoiceLineTen(Base):
    nome_cliente = Field(22, 72)
    cpf_cnpj = Field(730, 744)
    conta = Field(744, 755)
    cep = Field(350, 358)
    cidade = Field(288, 348)
    estado = Field(348, 350)
    endereco = Field(72, 172)
    numero = Field(172, 178)
    complemento = Field(178, 208)
