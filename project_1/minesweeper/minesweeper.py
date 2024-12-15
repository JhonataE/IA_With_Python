import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Declaracao logica sobre um jogo de Minesweeper.
    Uma sentenca consiste em um conjunto de celulas do tabuleiro
    e uma contagem do numero dessas celulas que sao minas.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Retorna o conjunto de todas as celulas em self.cells que sao conhecidas como minas.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Retorna o conjunto de todas as celulas em self.cells que sao conhecidas como seguras.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Atualiza a representacao interna ao saber que
        uma celula e uma mina.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Atualiza a representacao interna ao saber que
        uma celula e segura.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Jogador de Minesweeper.
    """

    def __init__(self, height=8, width=8):
        # Define a altura e a largura iniciais
        self.height = height
        self.width = width

        # Mantem registro das celulas clicadas
        self.moves_made = set()

        # Mantem registro das celulas conhecidas como seguras ou minas
        self.mines = set()
        self.safes = set()

        # Lista de sentencas sobre o jogo conhecidas como verdadeiras
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marca uma celula como mina e atualiza todas as sentencas
        para tambem marcar essa celula como mina.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marca uma celula como segura e atualiza todas as sentencas
        para tambem marcar essa celula como segura.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Atualiza a base de conhecimento da IA com informacoes sobre uma celula segura.
        """
        # Marca a celula como um movimento feito
        self.moves_made.add(cell)

        # Marca a celula como segura
        self.mark_safe(cell)

        # Determina as celulas vizinhas
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell or not (0 <= i < self.height and 0 <= j < self.width):
                    continue
                if (i, j) not in self.safes and (i, j) not in self.mines:
                    neighbors.add((i, j))

        # Adiciona uma nova sentenca a base de conhecimento
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        # Atualiza a base de conhecimento com novas inferencias
        self.update_knowledge()

    def update_knowledge(self):
        """
        Faz inferencias e atualiza a base de conhecimento.
        """
        for sentence in self.knowledge[:]:
            # Identifica minas e celulas seguras conhecidas
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()

            # Marca celulas identificadas como minas ou seguras
            for mine in known_mines:
                self.mark_mine(mine)
            for safe in known_safes:
                self.mark_safe(safe)

        # Remove sentencas vazias
        self.knowledge = [s for s in self.knowledge if s.cells]

        # Infere novas sentencas a partir de subconjuntos
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                    inferred_cells = sentence2.cells - sentence1.cells
                    inferred_count = sentence2.count - sentence1.count
                    inferred_sentence = Sentence(inferred_cells, inferred_count)
                    if inferred_sentence not in self.knowledge:
                        self.knowledge.append(inferred_sentence)

    def make_safe_move(self):
        """
        Retorna uma celula segura para escolher no tabuleiro do Minesweeper.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Retorna um movimento aleatorio para fazer no tabuleiro do Minesweeper.
        """
        choices = [
            (i, j)
            for i in range(self.height)
                for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        return random.choice(choices) if choices else None
