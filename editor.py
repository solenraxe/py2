import libraries.solui as ui
import libraries.interpreter as inter

LINE_HEIGHT = 24
TEXT_X = 75
TEXT_Y = 60
LINE_NUM_X = 50
VISIBLE_LINES = 12

class EditorVariable():
    def __init__(self):
        self.text = ""
        self.lNum = 0
        self.delete = 0
        self.moveDir = 0
        self.editInd = 0
        self.prev = []
        self.kPressed = {}
        self.frameCnt = 0
        self.scroll = 0

edVars = EditorVariable()

def openFile(txt):
    edVars.text = txt
    edVars.lNum = txt.count("\n")
    edVars.editInd = len(txt)

def updateScrollBar():
    scrollBar.hidden = edVars.lNum <= VISIBLE_LINES
    if edVars.lNum > VISIBLE_LINES:
        scrollBar.rect.y = 70+300*edVars.scroll/edVars.lNum
        scrollBar.rect.height = 300*VISIBLE_LINES/edVars.lNum

def addLine():
    edVars.text = edVars.text[:edVars.editInd] + '\n' + edVars.text[edVars.editInd:]
    edVars.lNum += 1
    edVars.editInd += 1
    if len(edVars.text[:edVars.editInd].split('\n')) - edVars.scroll - 1 > VISIBLE_LINES:
        edVars.scroll += 1
    updateScrollBar()

def appendHere(s):
    edVars.text = edVars.text[:edVars.editInd] + s + edVars.text[edVars.editInd:]
    edVars.editInd += len(s)

def delete(n):
    edVars.text = edVars.text[:edVars.editInd-n] + edVars.text[edVars.editInd:]
    edVars.editInd = max(0, edVars.editInd-n)
    edVars.lNum = edVars.text.count("\n")
    updateScrollBar()

def deleteAndMove():
    if edVars.delete > 0: edVars.delete += 1
    if edVars.delete > 30 and edVars.frameCnt%6 == 0: 
        repeat = round(edVars.delete/20)
        delete(repeat)
    if edVars.frameCnt % 8 == 0 and edVars.moveDir != 0:
        edVars.editInd = max(0, min(len(edVars.text), edVars.editInd + edVars.moveDir))
        print(edVars.editInd)

def run(txt):
    lines = txt.split('\n')
    for i, line in enumerate(lines):
        inter.runL(line)

mainWindow = ui.Element((20, 50, ui.WIDTH - 40, ui.HEIGHT - 70), hollow=2, radius=5)
consoleWindow = ui.Element((40, ui.HEIGHT - 210, ui.WIDTH - 80, 170), hollow=2, radius=5)
txtElem = ui.Text((TEXT_X, TEXT_Y), edVars.text, center=False)
consoleTxt = ui.Text((50, ui.HEIGHT-200), "", center=False)
scrollBar = ui.Element((750, 0, 5, 0), radius=5, hidden=True)

ui.globalElements.append(mainWindow)
ui.globalElements.append(consoleWindow)
ui.globalElements.append(txtElem)
ui.globalElements.append(consoleTxt)
ui.globalElements.append(scrollBar)

ui.globalElements.append(ui.Button((20, 10, 100, 30), "Save (F2)", lambda: save()))
ui.globalElements.append(ui.Button((130, 10, 100, 30), "Load (F8)", lambda: loadFile()))
ui.globalElements.append(ui.Button((240, 10, 100, 30), "Clear (F3)", lambda: clear()))
ui.globalElements.append(ui.Button((350, 10, 100, 30), "Run (F9)", lambda: run(edVars.text)))
ui.globalElements.append(ui.Button((460, 10, 150, 30), "Fullscreen (F11)", lambda: ui.toggleFullscreen()))

def main():
    edVars.frameCnt += 1

    for ev in ui.events:
        if ev.type == ui.KEYDOWN:
            edVars.kPressed[ev.key] = True
            if ev.key == ui.K_BACKSPACE:
                delete(1)
                edVars.delete = 1
            elif ev.key == ui.K_RETURN:
                addLine()
            elif ev.key == ui.K_TAB:
                appendHere("- ")
            elif ev.key == ui.K_RIGHT or ev.key == ui.K_LEFT:
                edVars.moveDir = (ev.key == ui.K_RIGHT and 1) or -1
            elif ev.unicode and (not ui.K_LCTRL in edVars.kPressed):
                appendHere(ev.unicode)
        elif ev.type == ui.KEYUP:
            edVars.kPressed.pop(ev.key)
            if ev.key == ui.K_BACKSPACE:
                edVars.delete = 0
            elif ev.key == ui.K_LEFT or ev.key == ui.K_RIGHT:
                edVars.moveDir = 0
        elif ev.type == ui.MOUSEWHEEL:
            edVars.scroll -= ev.y
            edVars.scroll = max(min(edVars.scroll, edVars.lNum-VISIBLE_LINES), 0)
            updateScrollBar()

    deleteAndMove()

    displayedTxt = edVars.text
    cursorChar = (edVars.frameCnt % 60 < 35 and "|") or " "
    displayedTxt = displayedTxt[:edVars.editInd] + cursorChar + displayedTxt[edVars.editInd:]

    bound = min(edVars.scroll+VISIBLE_LINES, edVars.lNum)
    lines = displayedTxt.split('\n')[edVars.scroll:bound+1]

    txtElem.text = '\n'.join(lines)

    consoleTxt.text = inter.getCons()

    for i in range(len(lines)):
        y = TEXT_Y + (i) * LINE_HEIGHT
        numTxt = ui.comicSans.render(str(i+edVars.scroll+1) + ".", True, (255, 255, 255))
        ui.screen.blit(numTxt, (LINE_NUM_X, y))

openFile("")

ui.createTab("Main", lambda: main(), [])
ui.changeTab("Main")
ui.launch()