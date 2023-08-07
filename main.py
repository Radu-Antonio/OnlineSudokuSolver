from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


class Browser:
    def __init__(self):
        options = Options()
        service = Service("C://chromedriver.exe")
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, service=service)
        self.driver.get("http://ro.sudokuonline.eu/")
        self.driver.maximize_window()
        ActionChains(self.driver).scroll_by_amount(0, 220).perform()
        self.cellsToSkip = None

    def getSudokuBoard(self):
        toSkip = set()
        board = []
        for i in range(9):
            lst = []
            for j in range(9):
                square = self.driver.find_element(By.ID, f'p{i*9+j+1}')
                value = square.get_attribute("value")
                if value:
                    lst.append(int(value))
                    toSkip.add((i, j))
                else:
                    lst.append(0)
            board.append(lst)

        self.cellsToSkip = toSkip
        return board, toSkip

    def executeSolution(self, solution):
        for i in range(9):
            for j in range(9):
                if (i, j) in self.cellsToSkip:
                    continue
                cell = self.driver.find_element(By.ID, f'p{i*9+j+1}')
                cell.send_keys(solution[i][j])
        cell.send_keys(Keys.ENTER)
        self.driver.switch_to.alert.accept()
        ActionChains(self.driver).scroll_by_amount(0, 220).perform()


class SudokuSolver:
    def __init__(self, data):
        self.board, self.toSkip = data

    def getSudokuBoard(self):
        return self.board

    def solveSudoku(self):
        self.dfs(0, 0)

    def dfs(self, x, y):
        if x == 9:
            return True

        if (x, y) in self.toSkip:
            if self.dfs(*self.getNextState(x, y)):
                return True
            return

        for n in range(1, 10):
            if self.isValidState(x, y, n):
                self.board[x][y] = n
                if self.dfs(*self.getNextState(x, y)):
                    return True
                self.board[x][y] = 0

    def getNextState(self, row, col):
        if col == 8:
            return row+1, 0
        return row, col+1

    def isValidState(self, row, col, value):
        if value in self.board[row]:
            return False

        if value in [self.board[i][col] for i in range(9)]:
            return False

        x, y = row - row % 3, col - col % 3
        for i in range(x, x + 3):
            for j in range(y, y + 3):
                if self.board[i][j] == value:
                    return False
        return True


if __name__ == "__main__":
    browser = Browser()
    solver = SudokuSolver(browser.getSudokuBoard())
    solver.solveSudoku()
    browser.executeSolution(solver.getSudokuBoard())
