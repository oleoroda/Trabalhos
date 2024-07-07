import os

class Pessoa:
    def __init__(self, nome, idade, sexo):
        self.__nome = nome
        self.__idade = idade
        self.__sexo = sexo

    @property
    def nome(self):
        return self.__nome

    @property
    def idade(self):
        return self.__idade
    
    @property
    def sexo(self):
        return self.__sexo

class Paciente(Pessoa):
    def __init__(self, cpf, nome, idade, sexo):
        super().__init__(nome, idade, sexo)
        self.__cpf = cpf
        self.__historico = []

    @property
    def cpf(self):
        return self.__cpf

    def adicionar_historico(self, consulta):
        self.__historico.append(consulta)

    def remover_historico(self, consulta):
        if consulta in self.__historico:
            self.__historico.remove(consulta)

    def get_historico(self):
        return self.__historico

class Medico(Pessoa):
    def __init__(self, nome, idade, sexo, especialidade, crm):
        super().__init__(nome, idade, sexo)
        self.__especialidade = especialidade
        self.__crm = crm

    @property
    def especialidade(self):
        return self.__especialidade

    @property
    def crm(self):
        return self.__crm
    
    def __str__(self):
        return f"{self.nome} ({self.especialidade})"

class Consulta:
    def __init__(self, paciente, medico, data, horario, motivo):
        self.__paciente = paciente
        self.__medico = medico
        self.__data = data
        self.__horario = horario
        self.__motivo = motivo

    @property
    def paciente(self):
        return self.__paciente

    @property
    def medico(self):
        return self.__medico

    @property
    def data(self):
        return self.__data

    @property
    def horario(self):
        return self.__horario

    @property
    def motivo(self):
        return self.__motivo

    def __str__(self):
        return f"{self.data} {self.horario} - {self.motivo} com {self.medico.nome} ({self.medico.especialidade})"

class Verificador:
    @staticmethod
    def verificador_cpf(cpf):
        nove_digitos = cpf[:9]
        contador_regressivo_1 = 10
        resultado_digito_1 = 0

        try:
            for digito in nove_digitos:
                resultado_digito_1 += int(digito) * contador_regressivo_1
                contador_regressivo_1 -= 1

            digito_1 = (resultado_digito_1 * 10) % 11
            digito_1 = str(digito_1 if digito_1 <= 9 else 0)
            contador_regressivo_2 = 11
            resultado_digito_2 = 0

            for digito_2 in nove_digitos + str(digito_1):
                resultado_digito_2 += int(digito_2) * contador_regressivo_2
                contador_regressivo_2 -= 1

            digito_2 = (resultado_digito_2 * 10) % 11
            digito_2 = str(digito_2 if digito_2 <= 9 else 0)

            cpf_verdadeiro = nove_digitos + digito_1 + digito_2
            return cpf_verdadeiro == cpf
        
        except ValueError:
            return False

class Clinica:
    def __init__(self):
        self.__pacientes = []
        self.__medicos = [
            Medico('Dr. Carlos', 45, 'M', 'Ortopedista', '1234'),
            Medico('Dr. Mariano', 50, 'M', 'Pediatra', '5678'),
            Medico('Dra. Letícia', 40, 'F', 'Otorrinolaringologista', '9101'),
            Medico('Dra. Patrícia', 35, 'F', 'Neurologista', '1121')
        ]
        self.__consultas = []

    @property
    def pacientes(self):
        return self.__pacientes
    
    @property
    def medicos(self):
        return self.__medicos

    @property
    def consultas(self):
        return self.__consultas

    def cadastrar_paciente(self, paciente):
        self.__pacientes.append(paciente)

    def listar_medicos(self):
        for i, medico in enumerate(self.__medicos, 1):
            print(f"{i}) {medico.nome} ({medico.especialidade})")

    def agendar_consulta(self, paciente, medico, data, horario, motivo):
        consulta = Consulta(paciente, medico, data, horario, motivo)
        self.__consultas.append(consulta)
        paciente.adicionar_historico(consulta)

    def listar_consultas(self):
        if self.__consultas:
            for i, consulta in enumerate(self.__consultas, 1):
                print(f"{i}) {consulta}")
        else:
            print("Nenhuma consulta cadastrada.")

    def listar_consultas_paciente(self, paciente):
        historico = [consulta for consulta in self.__consultas if consulta.paciente == paciente]

        if historico:
            for i, consulta in enumerate(historico, 1):
                print(f"{i}) {consulta}")
        else:
            print("Nenhuma consulta encontrada para este paciente.")

    def remover_consulta(self, paciente, consulta):
        if consulta in self.__consultas:
            self.__consultas.remove(consulta)
            paciente.remover_historico(consulta)
            os.system('cls')

            print("Consulta removida com sucesso!")

        else:
            print("Consulta não encontrada.")

class SistemaClinica:
    def __init__(self):
        self.clinica = Clinica()
        self.menu_principal()

    def menu_principal(self):
        while True:
            login = input('Login: [Medico/Paciente] ').strip().upper()

            if login == "PACIENTE":
                self.menu_paciente()

            elif login == "MEDICO":
                self.menu_medico()

            else:
                os.system('cls')
                print("Opção inválida. Tente novamente.")

    def menu_paciente(self):
        cpf = input('Insira seu CPF: ')

        if Verificador.verificador_cpf(cpf):
            paciente = next((p for p in self.clinica.pacientes if p.cpf == cpf), None)

            if not paciente:
                nome = input("Insira seu nome: ")
                idade = input("Insira sua idade: ")
                sexo = input("Insira seu sexo: ")
                paciente = Paciente(cpf, nome, idade, sexo)
                self.clinica.cadastrar_paciente(paciente)

            while True:
                print('--------------------------------------------------')
                resposta = input(
                    '1 - Agendar consulta\n'
                    '2 - Ver consultas\n'
                    '3 - Remover consulta\n'
                    '4 - Sair\n'
                ).strip()

                if resposta == "1":
                    os.system('cls')

                    self.agendar_consulta(paciente)

                elif resposta == "2":
                    os.system('cls')
                    self.clinica.listar_consultas_paciente(paciente)

                elif resposta == "3":
                    os.system('cls')
                    self.remover_consulta(paciente)

                elif resposta == "4":
                    os.system('cls')
                    break

                else:
                    os.system('cls')
                    print("Opção inválida. Tente novamente.")

        else:
            os.system('cls')
            print("O CPF digitado não está correto. Por gentileza, refaça o login e insira um CPF válido")

    def agendar_consulta(self, paciente):
        self.clinica.listar_medicos()

        while True:
            try:
                medico_index = int(input("Escolha o médico pelo número: ")) - 1
                if 0 <= medico_index < len(self.clinica.medicos):
                    break

                else:
                    print("Número inválido. Tente novamente.")

            except ValueError:
                print("Entrada inválida. Digite um número.")

        medico = self.clinica.medicos[medico_index]
        data = input("Data da consulta (dd/mm/yyyy): ")
        horario = input("Horário da consulta (hh:mm): ")
        motivo = input("Motivo da consulta: ")
        self.clinica.agendar_consulta(paciente, medico, data, horario, motivo)
        
        os.system('cls')
        print("Consulta agendada com sucesso!")

    def remover_consulta(self, paciente):
        self.clinica.listar_consultas_paciente(paciente)

        while True:
            try:
                consulta_index = int(input("Escolha a consulta pelo número: ")) - 1
                if 0 <= consulta_index < len(self.clinica.consultas):
                    consulta = self.clinica.consultas[consulta_index]
                    self.clinica.remover_consulta(paciente, consulta)
                    break

                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def menu_medico(self):
        while True:
            print('--------------------------------------------------')
            resposta = input(
                '1 - Ver consultas\n'
                '2 - Remover consulta\n'
                '3 - Sair\n'
            ).strip()

            if resposta == "1":
                os.system('cls')
                self.clinica.listar_consultas()

            elif resposta == "2":
                os.system('cls')
                self.remover_consulta_medico()

            elif resposta == "3":
                os.system('cls')
                break
            
            else:
                os.system('cls')
                print("Opção inválida. Tente novamente.")

    def remover_consulta_medico(self):
        self.clinica.listar_consultas()
        while True:
            try:
                consulta_index = int(input("Escolha a consulta pelo número: ")) - 1
                if 0 <= consulta_index < len(self.clinica.consultas):
                    consulta = self.clinica.consultas[consulta_index]
                    paciente = consulta.paciente
                    self.clinica.remover_consulta(paciente, consulta)
                    break

                else:
                    print("Número inválido. Tente novamente.")

            except ValueError:
                print("Entrada inválida. Digite um número.")

if __name__ == "__main__":
    SistemaClinica()
