from django.core.exceptions import ValidationError
import re


def valida_cpf(cpf : str):

    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos ou se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF incorreto: digitos iguais")

    if len(cpf) != 11:
        raise ValidationError("CPF incorreto: quantidade de digitos incorreta")

    # Converte para lista de inteiros
    numeros = [int(d) for d in cpf]

    def calcular_digito(posicao):
        soma = sum(numeros[i] * (posicao - i) for i in range(posicao - 1))
        return (soma * 10) % 11 % 10

    if not (calcular_digito(10) == numeros[9] and calcular_digito(11) == numeros[10]):
        raise ValidationError("CPF incorreto: padrão incorreto ou erro de digitação")