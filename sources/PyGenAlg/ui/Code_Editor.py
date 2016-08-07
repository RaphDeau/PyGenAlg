# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1 -*-

from PyQt4 import QtGui
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

class Code_Editor(QsciScintilla):
    """
    Display a Qscintilla code editor
    """
    def __init__(self, top=None):
        """
        Initialize the editor
        """
        super(Code_Editor, self).__init__(top)

        ## define the font to use
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setFixedPitch(True)
        # the font metrics here will help
        # building the margin width later
        fm = QtGui.QFontMetrics(font)

        ## set the default font of the editor
        ## and take the same font for line numbers
        self.setFont(font)
        self.setMarginsFont(font)
        ## Line numbers
        self.setMarginLineNumbers(1, True)

        ## Folding visual : we will use boxes
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ## Editing line color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#CDA869"))

        ## Margins colors
        # line numbers margin
        self.setMarginsBackgroundColor(QtGui.QColor("#333333"))
        self.setMarginsForegroundColor(QtGui.QColor("#CCCCCC"))

        # folding margin colors (foreground,background)
        self.setFoldMarginColors(QtGui.QColor("#99CC66"), QtGui.QColor("#333300"))

        ## Choose a lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
