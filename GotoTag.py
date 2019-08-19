import sublime
import sublime_plugin

def getKey(id):
    return ''.join(["gtmark_", str(id)])

def indexIcon(index):
    return "Packages/gototag/icon/number_{0}.png".format(index)

def totalCount():
    return 15

class GotoTagCommand(sublime_plugin.TextCommand):

  def run(self, edit, func = '', tagId = 0):
    if func == 'goto':
        self.goto(tagId)
    elif func == 'tag':
        self.tag()
    elif func == 'clear':
        self.clearAll()

  def tag(self):
    count = totalCount()
    sels = self.view.sel()
    currentLine = None
    if sels and len(sels) >= 1:
        currentLine = self.view.line(sels[0])
    else:
        return
    emptyKey = ''
    emptyIndex = 0
    for i in range(count):
        key = getKey(i)
        regions = self.view.get_regions(key)
        if emptyKey == '' and len(regions) == 0:
            emptyKey = key
            emptyIndex = i
        if regions and len(regions) >= 1:
            if currentLine.contains(regions[0]) or regions[0].contains(currentLine):
                self.view.erase_regions(key)
                return
    if emptyKey:
        self.view.add_regions(emptyKey, [currentLine], "mark", indexIcon(emptyIndex+1), sublime.HIDDEN | sublime.PERSISTENT)

  def goto(self, tagId):
    key = getKey(tagId)
    regions = self.view.get_regions(key)
    if regions and len(regions) >= 0:
        self.view.show_at_center(regions[0])

  def clearAll(self):
    count = totalCount()
    for i in range(count):
            self.view.erase_regions(getKey(i))
