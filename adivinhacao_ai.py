import json
import random
import os
from datetime import datetime
from colorama import init, Fore, Style

init()  # ANSI colors no Windows

class AdivinhacaoAI:
    def __init__(self):
        self.leaderboard = self._carregar_leaderboard()
        self.stats = {}
        self.jogador = ""
        self.tentativas = 0
        self.numero_secreto = 0
        
    def _carregar_leaderboard(self):
        if os.path.exists('leaderboard.json'):
            with open('leaderboard.json', 'r') as f:
                return json.load(f)
        return []
    
    def _salvar_leaderboard(self):
        with open('leaderboard.json', 'w') as f:
            json.dump(self.leaderboard, f, indent=2)
    
    def novo_jogo(self, nome):
        self.jogador = nome
        self.tentativas = 0
        self.numero_secreto = random.randint(1, 100)
        self.stats[nome] = {'jogos': 0, 'vitorias': 0, 'media_tentativas': 0}
        print(f"{Fore.GREEN}🎮 Bem-vindo {nome}!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Pensei em um número de 1 a 100!{Style.RESET_ALL}")
    
    def jogar(self, palpite):
        self.tentativas += 1
        
        if palpite < self.numero_secreto:
            return f"{Fore.RED}📈 Mais alto!{Style.RESET_ALL}"
        elif palpite > self.numero_secreto:
            return f"{Fore.BLUE}📉 Mais baixo!{Style.RESET_ALL}"
        else:
            self._vitoria()
            return f"{Fore.GREEN}🎉 PARABÉNS! Você acertou em {self.tentativas} tentativas!{Style.RESET_ALL}"
    
    def _vitoria(self):
        stats = self.stats[self.jogador]
        stats['jogos'] += 1
        stats['vitorias'] += 1
        stats['media_tentativas'] = (stats['media_tentativas'] * (stats['jogos']-1) + self.tentativas) / stats['jogos']
        
        recorde = {
            'jogador': self.jogador,
            'tentativas': self.tentativas,
            'data': datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.leaderboard.append(recorde)
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x['tentativas'])[:10]
        self._salvar_leaderboard()
    
    def mostrar_leaderboard(self):
        print(f"\n{Fore.CYAN}🏆 TOP 10 JOGADORES{Style.RESET_ALL}")
        for i, recorde in enumerate(self.leaderboard, 1):
            emoji = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else "⭐"
            print(f"{emoji} {i}. {recorde['jogador']} - {recorde['tentativas']} tentativas ({recorde['data']})")
    
    def mostrar_stats(self):
        if self.jogador in self.stats:
            stats = self.stats[self.jogador]
            taxa_acerto = (stats['vitorias']/stats['jogos'])*100
            print(f"\n{Fore.MAGENTA}📊 Suas Estatísticas{Style.RESET_ALL}")
            print(f"Jogos: {stats['jogos']} | Vitórias: {stats['vitorias']} ({taxa_acerto:.1f}%)")
            print(f"Média tentativas: {stats['media_tentativas']:.1f}")

# MULTIPLAYER 1v1
def modo_duelo(jogador1, jogador2):
    jogo1 = AdivinhacaoAI()
    jogo2 = AdivinhacaoAI()
    
    jogo1.novo_jogo(jogador1)
    jogo2.novo_jogo(jogador2)
    
    while True:
        p1 = int(input(f"{Fore.GREEN}{jogador1}, seu palpite: {Style.RESET_ALL}"))
        print(jogo1.jogar(p1))
        
        if p1 == jogo1.numero_secreto:
            print(f"{Fore.GREEN}{jogador1} VENCEU!{Style.RESET_ALL}")
            break
            
        p2 = int(input(f"{Fore.RED}{jogador2}, seu palpite: {Style.RESET_ALL}"))
        print(jogo2.jogar(p2))
        
        if p2 == jogo2.numero_secreto:
            print(f"{Fore.RED}{jogador2} VENCEU!{Style.RESET_ALL}")
            break

# MAIN INTERATIVA
def main():
    jogo = AdivinhacaoAI()
    
    while True:
        print("\n" + "="*50)
        print("🎮 JOGO DE ADIVINHAÇÃO COM IA")
        print("1. Novo Jogo | 2. Leaderboard | 3. Minhas Stats | 4. Duelo 1v1 | 5. Sair")
        op = input("Escolha: ")
        
        if op == "1":
            nome = input("Seu nome: ")
            jogo.novo_jogo(nome)
            while True:
                try:
                    palpite = int(input("Seu palpite (1-100): "))
                    resultado = jogo.jogar(palpite)
                    print(resultado)
                    if palpite == jogo.numero_secreto:
                        input("Pressione Enter para continuar...")
                        break
                except:
                    print("Digite um número válido!")
                    
        elif op == "2":
            jogo.mostrar_leaderboard()
            
        elif op == "3":
            nome = input("Seu nome: ")
            jogo.mostrar_stats()
            
        elif op == "4":
            p1 = input("Jogador 1: ")
            p2 = input("Jogador 2: ")
            modo_duelo(p1, p2)
            
        elif op == "5":
            break

if __name__ == "__main__":
    main()
