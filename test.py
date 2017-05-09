from blessed import Terminal

from greenscreen.style import colors, capabilities

terminal = Terminal()

phrase = colors.red('This is a long line of text.  It is pretty great',
                  capabilities.bold(' I hope that the wrapping function works well'),
                  colors.on_green(' This text will definitely be pretty ugly'))

print(phrase.escape(terminal))

print('-' * 80)

wrapped = phrase.wrap(20)
for line in wrapped:
    print(line.escape(terminal))

print('-' * 80)

line = colors.black(colors.on_cyan('Here is another line of text'))

print('{}|'.format(line.escape(terminal)))
print('-' * 80)

justified = line.justify(80)
print('{}|'.format(justified.escape(terminal)))
print('-' * 80)

justified_clean = line.justify(80, expand=False)
print('{}|'.format(justified_clean.escape(terminal)))

